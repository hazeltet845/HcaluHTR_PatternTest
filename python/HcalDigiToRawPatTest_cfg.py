import FWCore.ParameterSet.Config as cms
import os
from Configuration.StandardSequences.Eras import eras

process = cms.Process("HcalDigiToRawPatTest", eras.Run3_2025)

process.load("Configuration.StandardSequences.Services_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag,"140X_mcRun3_2024_realistic_v26", "")

event_num = 3

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(event_num)  
)

input_file = 'file:/eos/user/e/ethazelt/cmssw/CMSSW_14_2_2/src/VLL_RAWSIM_ex.root'


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
                                   fileName=cms.string('test.root'))

process.p = cms.Path(process.hcalRawData)

process.MessageLogger.cerr.FwkReport.reportEvery = 1
