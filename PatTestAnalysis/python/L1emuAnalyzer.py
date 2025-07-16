import ROOT
from algo_map import algo_map
import numpy as np
import argparse, sys, os

decisionTreeLabel_emu = "l1uGTEmuTree/L1uGTTree"
decisionTreeLabel     = "l1uGTTree/L1uGTTree"

jetInfoLabel_emu      = "l1UpgradeEmuTree/L1UpgradeTree"
jetInfoLabel          = "l1UpgradeTree/L1UpgradeTree"

trig_map = np.array(algo_map)

# ------------------------------------------------------------------------------
def parseArgs():
    parser = argparse.ArgumentParser(
        add_help=True,
        description=''
    )

    parser.add_argument("-i", "--infilePath", action="store", required=True, help="Input file path")
    parser.add_argument("-n", "--nEvents", action="store", default = -1 ,help="Number of Events to process")
    parser.add_argument("--emu", action="store_true", help="Number of Events to process")

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
def L1Analyzer(infilePath, nEvents,emu):
    
    if(emu):
        tree_DTL = GetData(infilePath,decisionTreeLabel_emu)
        tree_JIL = GetData(infilePath,jetInfoLabel_emu)
    else:
        tree_DTL     = GetData(infilePath,decisionTreeLabel)
        tree_JIL     = GetData(infilePath,jetInfoLabel)

    trigIndList = GetLLPTrigIndex()
    trigIndices = trigIndList[:, 0]
    trigNames   = trigIndList[:, 1]
    print(trigIndList)

    if nEvents < 0: 
        nEvents = tree_DTL.GetEntries()

    trigDecList = np.zeros(len(trigNames))
    for i in range(nEvents):
        tree_DTL.GetEntry(i) 
        tree_JIL.GetEntry(i)

        for k in range(len(trigNames)):
            index = int(trigIndices[k])
            trigDec = tree_DTL.m_algoDecisionInitial[index]
            trigDecList[k] = trigDec

       
        if np.any(trigDecList):
            print(f"------------------------ Event {i} ------------------------")
            
            nJets = tree_JIL.GetLeaf("nJets").GetValue()
            print(f"NumJets = {nJets}")

            for j in range(len(trigNames)):
                if(j==0):
                    print(f"| {trigNames[j]}        | {bool(trigDecList[j])} ")
                else:
                    print(f"| {trigNames[j]} | {bool(trigDecList[j])} ")

            for k in range(int(nJets)):
                eta   = tree_JIL.jetEta[k]
                phi   = tree_JIL.jetPhi[k]
                et     = tree_JIL.jetEt[k]
                hwqual = tree_JIL.jetHwQual[k] 

                print(f"  Jet {k}: Et = {round(et,1)}, Eta = {round(eta,2)}, Phi = {round(phi,2)}, Qual = {hwqual}")
# ------------------------------------------------------------------------------
def main():
    #infilePath = ["/eos/user/e/ethazelt/PatternTesting/CMSSW_15_0_4/src/uHTRStudies/PatTestAnalysis/python/L1Ntuple_Data_run390758_1000.root"]
    args = parseArgs()

    infilePath = [args.infilePath]
    nEvents    = int(args.nEvents)
    emu        = args.emu

    print("Analyzing L1 emulated data for LLP triggers")
    
    L1Analyzer(infilePath,nEvents,emu)

if __name__ == '__main__':
    main()
