import ROOT
from algo_map import algo_map
import numpy as np
import argparse, sys, os
from array import array

decisionTreeLabel_emu = "l1uGTEmuTree/L1uGTTree"
decisionTreeLabel     = "l1uGTTree/L1uGTTree"

jetInfoLabel_emu      = "l1UpgradeEmuTree/L1UpgradeTree"
jetInfoLabel          = "l1UpgradeTree/L1UpgradeTree"

eventTreeLabel        = "l1EventTree/L1EventTree"

trig_map = np.array(algo_map)

param_LLP1 = [-1.0875,1.3485]
param_LLP2 = [0.0435,0.7395]
              #eta , phi

dEta = 0.01
dPhi = 0.01
dR = np.sqrt(dEta**2 + dPhi**2)

ROOT.gStyle.SetOptStat(0)

# ------------------------------------------------------------------------------
def parseArgs():
    parser = argparse.ArgumentParser(
        add_help=True,
        description=''
    )

    parser.add_argument("-i", "--infilePath", action="store", required=True, help="Input file path")
    parser.add_argument("-n", "--nEvents", action="store", default = -1 ,help="Number of Events to process")
    parser.add_argument("--emu", action="store_true", help="Use emulated events")
    parser.add_argument("--mc", action="store_true", help="Input file is MC")
    parser.add_argument("--print", action="store_true", help="Print LLP trigger info")


    args = parser.parse_args()

    return args
# ------------------------------------------------------------------------------
def GetData(infilepaths, label):
    # Create a TChain to hold the trees from all files
    chain = ROOT.TChain(label) # Access the tree by label

    # Loop over the list of file paths and add each file's tree to the chain
    for infilepath in infilepaths:
        print(f"Adding file: {infilepath}")
        chain.Add(infilepath)  # Add the tree from the current file to the chain

    # Check if the chain has any entries
    if chain.GetEntries() == 0:
        print(f"No entries found in the tree '{label}' across all files.")
        return None  # Return None if no data is found
    else:
        print(f"Found tree with label '{label}'")

    # Return the chain (holding trees from all files)
    return chain  # No need to return the file, as TChain handles it

# ------------------------------------------------------------------------------
def GetLLPTrigIndex():
    trigIndList = np.array([s for s in trig_map if "LLP" in s[1]])

    return trigIndList

# ------------------------------------------------------------------------------
def makeLegend(hList):
    legend = ROOT.TLegend(0.47, 0.80, 0.67, 0.93)
    legend.SetTextSize(0.025)
    #legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    for i,hist in enumerate(hList):
        if(i == len(hList) - 1):
            legend.AddEntry(hist, "Unmatched LLP", "f")
        else:
            legend.AddEntry(hist, f"MC matched LLP {i}", "f")

    return legend

# ------------------------------------------------------------------------------
def cmsLabel(runNum):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextColor(ROOT.kBlack)
    latex.SetTextSize(0.05)
    latex.DrawLatex(0.12, 0.95, "#scale[1]{#bf{CMS}  }")
    latex.DrawLatex(0.20, 0.95, "#scale[0.75]{#it{ Preliminary}  }")
    
    if(runNum == 0):
        text = f"#scale[0.8]{{MC}}"
    else:
        text = f"#scale[0.8]{{Run {runNum}}}"
    
    latex.DrawLatex(0.79, 0.95, text)

    return latex

# ------------------------------------------------------------------------------
def L1Analyzer(infilePath,nEvents,emu,mc,print_all):
   
    parts = infilePath[0].split('_')
    if(mc):
        runNum = 00000
    else:
        runNum = parts[2].replace("run","")



    tree_Event = GetData(infilePath,eventTreeLabel)
    if(emu):
        tree_DTL = GetData(infilePath,decisionTreeLabel_emu)
        tree_JIL = GetData(infilePath,jetInfoLabel_emu)
    else:
        tree_DTL     = GetData(infilePath,decisionTreeLabel)
        tree_JIL     = GetData(infilePath,jetInfoLabel)

    max_lumi_bin = tree_Event.GetMaximum("lumi") + 0.5
    min_lumi_bin = 1 - 0.5 
    nBins = int(max_lumi_bin - min_lumi_bin)
    print(f"Lumisection total: {max_lumi_bin - 0.5}")

    h1 = ROOT.TH1F("h1", "LLP 1", nBins, min_lumi_bin, max_lumi_bin)
    h2 = ROOT.TH1F("h2", "LLP 2", nBins, min_lumi_bin, max_lumi_bin)
    h3 = ROOT.TH1F("h3", "LLP Unknown", nBins, min_lumi_bin, max_lumi_bin)
   
    h1_Et = ROOT.TH1F("h1_Et", ";E_{T};Entries", 1050, 0, 1050)
    h2_Et = ROOT.TH1F("h2_Et", ";E_{T};Entries", 1050, 0, 1050)
    h3_Et = ROOT.TH1F("h3_Et", ";E_{T};Entries", 1050, 0, 1050)

    h_2d_count = ROOT.TH2D("h_2d_count", ";#eta;#phi",33,-1.4,1.4,72,-np.pi,np.pi)
    h_2d_sumET   = ROOT.TH2D("h_2d_sumET", ";#eta;#phi",33,-1.4,1.4,72,-np.pi,np.pi)

    h1.SetFillColor(9)#ROOT.kAzure - 3)#4
    h2.SetFillColor(8)#ROOT.kGreen - 3)#1
    h3.SetFillColor(ROOT.kRed - 3)#7
    
    h1_Et.SetLineColor(9)
    h2_Et.SetLineColor(8)
    h3_Et.SetLineColor(ROOT.kRed - 3)

    trigIndList = GetLLPTrigIndex()
    trigIndices = trigIndList[:, 0]
    trigNames   = trigIndList[:, 1]
    #print(trigIndList)

    if nEvents < 0: 
        nEvents = tree_DTL.GetEntries()

    trigDecList = np.zeros(len(trigNames))

    for i in range(nEvents):
        tree_DTL.GetEntry(i) 
        tree_JIL.GetEntry(i)
        tree_Event.GetEntry(i)

        for k in range(len(trigNames)):
            index = int(trigIndices[k])
            trigDec = tree_DTL.m_algoDecisionInitial[index]
            trigDecList[k] = trigDec

        if (np.any(trigDecList) or mc):
            if(print_all): print(f"------------------------ Event {i} ------------------------")
            
            nJets = tree_JIL.GetLeaf("nJets").GetValue()
            if(print_all): print(f"NumJets = {nJets}")

            for j in range(len(trigNames)):
                if(j==0):
                    if(print_all): print(f"| {trigNames[j]}        | {bool(trigDecList[j])} ")
                else:
                    if(print_all): print(f"| {trigNames[j]} | {bool(trigDecList[j])} ")
            
            LLP = 0
            for k in range(int(nJets)):
                eta   = tree_JIL.jetEta[k]
                phi   = tree_JIL.jetPhi[k]
                et     = tree_JIL.jetEt[k]
                hwqual = tree_JIL.jetHwQual[k] 
                
                if(hwqual == 1):
                    et_LLP = et
                    eta_LLP = eta
                    phi_LLP = phi

                    if((abs(eta-param_LLP1[0])< 0.01) and (abs(phi-param_LLP1[1])< 0.01)):
                        LLP = 1
                    elif((abs(eta-param_LLP2[0])< 0.01) and (abs(phi-param_LLP2[1])< 0.01)):
                        LLP = 2
                    else:
                        LLP = 3
                
                if(print_all): print(f"  Jet {k}: Et = {round(et,5)}, Eta = {round(eta,5)}, Phi = {round(phi,5)}, Qual = {hwqual}")

            if(LLP > 0):
                h_2d_sumET.Fill(eta_LLP,phi_LLP,et_LLP)
                h_2d_count.Fill(eta_LLP,phi_LLP)
                if(not mc):
                    lumisec = tree_Event.GetLeaf("lumi").GetValue()
                    if(print_all): print(f"Lumisection: {lumisec}")
                    if(LLP == 1):
                        h1.Fill(lumisec)
                        h1_Et.Fill(et_LLP)
                    elif(LLP == 2):
                        h2.Fill(lumisec)
                        h2_Et.Fill(et_LLP)
                    elif(LLP == 3):
                        h3.Fill(lumisec)
                        h3_Et.Fill(et_LLP)
                        #print(f"E_T:{et_LLP}; ETA: {eta_LLP}; PHI: {phi_LLP}")

    h_avg = h_2d_sumET.Clone("h_avg")
    h_avg.Divide(h_2d_count)

    for ix in range(1, h_avg.GetNbinsX()+1):
        for iy in range(1, h_avg.GetNbinsY()+1):
            if h_2d_count.GetBinContent(ix, iy) == 0:
                h_avg.SetBinContent(ix, iy, 0)

    if(not mc):
        stack = ROOT.THStack("stack", ";Lumisection;L1T LLP Event Count")
        stack.Add(h1)
        stack.Add(h2)
        stack.Add(h3)
        
        c = ROOT.TCanvas("c", "Canvas", 800, 600)
        c.SetTopMargin( 0.06 )
        c.SetRightMargin( 0.06 )
       
        stack.Draw("HIST")
      
        ROOT.gStyle.SetHistTopMargin(0.02)
        cmsLabel(runNum)

        legend0 = makeLegend([h1,h2,h3])
        legend0.Draw()

        c.SaveAs(f"stack_LLPhits_run{runNum}.png")
        del c


        c1 = ROOT.TCanvas("c1", "Canvas", 800, 600)
        c1.SetTopMargin( 0.06 )
        c1.SetRightMargin( 0.06 )

        h1_Et.Draw("HIST")
        h2_Et.Draw("HIST SAME")
        h3_Et.Draw("HIST SAME")
        ROOT.gStyle.SetHistTopMargin(0.02)
        cmsLabel(runNum)

        legend1 = makeLegend([h1_Et,h2_Et,h3_Et])
        legend1.Draw()
        c1.SaveAs(f"hist_ET_run{runNum}.png")
        del c1

    #invert kBlackBody colors
    ncontours = 255
    ROOT.gStyle.SetPalette(ROOT.kBlackBody)  
    colors = [ROOT.gStyle.GetColorPalette(i) for i in range(ncontours)]
    colors.reverse()
    c_array = array('i', colors) 

    c2 = ROOT.TCanvas("c2", "Canvas", 800, 600)
    c2.SetTopMargin( 0.06 )
    c2.SetRightMargin( 0.12 )

    h_2d_count.SetMarkerSize(0.65)
    ROOT.gStyle.SetPalette(ROOT.kBird)

    h_2d_count.Draw("COLZ TEXT")

    cmsLabel(runNum)
    c2.SaveAs(f"hist_2D_count_run{runNum}.png")
    del c2

    c3 = ROOT.TCanvas("c3", "Canvas", 800, 600)
    c3.SetTopMargin( 0.06 )
    c3.SetRightMargin( 0.14 )#0.06 )

    h_avg.GetZaxis().SetTitle("Mean E_{T}")
    h_avg.GetZaxis().SetTitleOffset(1.32)
    ROOT.gStyle.SetPalette(ncontours, c_array)
    h_avg.Draw("COLZ")

    latex = ROOT.TLatex()
    latex.SetTextAlign(22)  # center text
    latex.SetTextSize(0.013)
    latex.SetTextColor(ROOT.kBlack)

    for ix in range(1, h_avg.GetNbinsX() + 1):
        for iy in range(1, h_avg.GetNbinsY() + 1):
            val = h_avg.GetBinContent(ix, iy)
            if val == 0:
                continue
            x = h_avg.GetXaxis().GetBinCenter(ix)
            y = h_avg.GetYaxis().GetBinCenter(iy)
            latex.DrawLatex(x, y, f"{val:.1f}")  # 1 decimal place

    cmsLabel(runNum)
    c3.SaveAs(f"hist_2D_avgET_run{runNum}.png")
    del c3


# ------------------------------------------------------------------------------
def main():
    #infilePath = ["/eos/user/e/ethazelt/PatternTesting/CMSSW_15_0_4/src/uHTRStudies/PatTestAnalysis/python/L1Ntuple_Data_run390758_1000.root"]
    args = parseArgs()

    infilePath = [args.infilePath]
    nEvents    = int(args.nEvents)
    emu        = args.emu
    mc         = args.mc
    print_all  = args.print

    print("Analyzing L1 emulated data for LLP triggers")
    print(f"Matching jets with dR < {dR}")
    
    L1Analyzer(infilePath,nEvents,emu,mc,print_all)

if __name__ == '__main__':
    main()
