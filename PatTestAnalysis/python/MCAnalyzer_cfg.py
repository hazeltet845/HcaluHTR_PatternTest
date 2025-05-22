import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
import os

event_num  = 200

process = cms.Process("CheckTrig", eras.Run3_2025)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(event_num)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring("file:/eos/user/e/ethazelt/MC_files/VLL_gen/VLLS_ele_M750_D1e-16_13p6TeV_GENSIMDIGIRAW_HLT.root")
)

process.CheckTrig = cms.EDAnalyzer("MCAnalyzer")
process.p = cms.Path(process.CheckTrig)
