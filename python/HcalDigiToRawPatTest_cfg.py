import FWCore.ParameterSet.Config as cms
import os
from Configuration.StandardSequences.Eras import eras
import argparse

# Argument Parsing
parser = argparse.ArgumentParser(description="Run HcalDigiToRawPatTest with arguments")

parser.add_argument("-i", "--input", required=True, help="Path to input ROOT file")
parser.add_argument("-n", "--num_events", type=int, required=True, help="Number of events to process")
parser.add_argument("-g", "--global_tag", required=True, help="Global Tag")
parser.add_argument("-e", "--era", required=True, help="Era")
parser.add_argument("-o", "--output_tag", required = False,default="offload_out",help="Name of output file")
args = parser.parse_args()

era = getattr(eras, args.era) #eras.Run3_2025
event_num = args.num_events #3
input_file = f"file:{args.input}" #file:/eos/user/e/ethazelt/cmssw/CMSSW_14_2_2/src/VLL_RAWSIM_ex.root
global_tag = args.global_tag #140X_mcRun3_2024_realistic_v26
output_file = f"output/offload/{args.output_tag}.root"

try: 
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Error:{args.input} does not exist")
except FileNotFoundError as e:
    print(e)

if not os.path.exists("output/offload"):
    os.makedirs("output/offload")

print(f"Output file path: {output_file}")

#Process
process = cms.Process("HcalDigiToRawPatTest", era)

process.load("Configuration.StandardSequences.Services_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag,global_tag, "")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(event_num)  
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(input_file)
)

process.hcalRawData = cms.EDAnalyzer("HcalDigiToRawPatTest",
    Verbosity = cms.untracked.int32(1),  # Enable debug output
    ElectronicsMap = cms.string(""),
    
    QIE11 = cms.InputTag("simHcalUnsuppressedDigis", "HBHEQIE11DigiCollection"),

    tdc1 = cms.vint32([12] * 64),
    tdc2 = cms.vint32([14] * 64)
    
)

process.TFileService = cms.Service("TFileService",
                                   closeFileFast=cms.untracked.bool(True),
                                   fileName=cms.string(output_file))

process.p = cms.Path(process.hcalRawData)

process.MessageLogger.cerr.FwkReport.reportEvery = 1
