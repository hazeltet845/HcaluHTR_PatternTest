#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "EventFilter/HcalRawToDigi/interface/HcalUHTRData.h"
#include "DataFormats/HcalDigi/interface/HcalQIESample.h"

#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/HcalDigi/interface/QIE11DataFrame.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"

#include "CondFormats/HcalObjects/interface/HcalElectronicsMap.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"

#include "EventFilter/HcalRawToDigi/plugins/PackerHelp.h"

#include <fstream>
#include <iostream>
#include <memory>
#include <vector>

#include <sstream>
#include <string>

using namespace std;

class HcalDigiToRawPatTest : public edm::one::EDAnalyzer<>{
public:
  explicit HcalDigiToRawPatTest(const edm::ParameterSet&);
  ~HcalDigiToRawPatTest() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;
 
  const int _verbosity; 
  const vector<int> tdc1_;
  const vector<int> tdc2_;
  static constexpr int tdcmax_ = 49;

  TTree* tree;

  uint32_t uhtrIndex;
  uint32_t bunchCrossing;
  uint16_t uhtrData; 

  const edm::EDGetTokenT<HcalDataFrameContainer<QIE11DataFrame>> tok_QIE11DigiCollection_;
  const edm::ESGetToken<HcalElectronicsMap, HcalElectronicsMapRcd> tok_electronicsMap_;
};

HcalDigiToRawPatTest::HcalDigiToRawPatTest(const edm::ParameterSet& iConfig)
	: _verbosity(iConfig.getUntrackedParameter<int>("Verbosity", 0)),
	  tdc1_(iConfig.getParameter<vector<int>>("tdc1")),
          tdc2_(iConfig.getParameter<vector<int>>("tdc2")),
	  tok_QIE11DigiCollection_(consumes<HcalDataFrameContainer<QIE11DataFrame>>(iConfig.getParameter<edm::InputTag>("QIE11"))),
	  tok_electronicsMap_(esConsumes<HcalElectronicsMap, 
			  HcalElectronicsMapRcd>(edm::ESInputTag("", iConfig.getParameter<std::string>("ElectronicsMap")))){
    for (size_t i = 0; i < tdc1_.size(); i++) {
      if (!(tdc1_.at(i) >= 0 && tdc1_.at(i) <= tdc2_.at(i) && tdc2_.at(i) <= tdcmax_))
        edm::LogWarning("HcalDigiToRawPatTest")
             << " incorrect TDC ranges " << i << "-th element: " << tdc1_.at(i) << ", " << tdc2_.at(i) << ", " << tdcmax_;
    }
    
    edm::Service<TFileService> fileService;
    tree = fileService->make<TTree>("UHTRTree", "Store uhtr data");

    // Define branches
    tree->Branch("uhtrIndex", &uhtrIndex, "uhtrIndex/I");
    tree->Branch("bunchCrossing", &bunchCrossing, "bunchCrossing/I");
    tree->Branch("uhtrData", &uhtrData);

}

HcalDigiToRawPatTest::~HcalDigiToRawPatTest() {}

void HcalDigiToRawPatTest::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  using namespace edm;
 
  unsigned int eventNumber = iEvent.id().event();

  std::cout << eventNumber << std::endl;

  edm::ESHandle<HcalElectronicsMap> item = iSetup.getHandle(tok_electronicsMap_);
  const HcalElectronicsMap* readoutMap = item.product();

  edm::Handle<QIE11DigiCollection> qie11DigiCollection;
  iEvent.getByToken(tok_QIE11DigiCollection_, qie11DigiCollection);


  // - - - - - - - - - - - - - - - - - - - - - - - - - - -
  // QIE11 precision data
  // - - - - - - - - - - - - - - - - - - - - - - - - - - -
  UHTRpacker uhtrs;
  // loop over each digi and allocate memory for each
  if (qie11DigiCollection.isValid()) {
    const QIE11DigiCollection& qie11dc = *(qie11DigiCollection);
    for (unsigned int j = 0; j < qie11dc.size(); j++) {
      QIE11DataFrame qiedf = static_cast<QIE11DataFrame>(qie11dc[j]);
      HcalDetId detid = qiedf.detid();
      HcalElectronicsId eid(readoutMap->lookup(detid));
      int crateId = eid.crateId();
      int slotId = eid.slot();
      int fiber = eid.fiberIndex();
      int fiberChan = eid.fiberChanId();
      int uhtrIndex_ = ((fiberChan & 0xFF) << 24) | ((fiber & 0xFF) << 16)  | ((slotId & 0xF) << 8) | (crateId & 0xFF);
     // int presamples = qiedf.presamples();
     //
      //   convert to hb qie data if hb
      if (HcalDetId(detid.rawId()).subdet() == HcalSubdetector::HcalBarrel){// || HcalDetId(detid.rawId()).subdet() == HcalSubdetector::HcalEndcap){
	qiedf = convertHB(qiedf, tdc1_, tdc2_, tdcmax_);
	uhtrs.addChannel(uhtrIndex_, qiedf, readoutMap, _verbosity);

      }

    }
  }

  // -----------------------------------------------------
  // loop over each uHTR and format data
  // -----------------------------------------------------


  //cout << "****** uHTR Loop ******" << endl;

  /*uint64_t min_crate = 20;
  uint64_t max_crate = 37;
  uint64_t min_slot = 1;
  uint64_t max_slot = 12;*/

  std::ofstream file;

  for (UHTRpacker::UHTRMap::iterator uhtr = uhtrs.uhtrs.begin(); uhtr != uhtrs.uhtrs.end(); ++uhtr) {
  //  uint64_t crateId = (uhtr->first) & 0xFF;
  //  uint64_t slotId = (uhtr->first & 0xF00) >> 8;
    //uint64_t fiber = (uhtr->first & 0xFF0000) >> 16;
    //uint64_t fiberChan = (uhtr->first & 0xFF000000) >> 24;

    //uhtrs.finalizeHeadTail(&(uhtr->second), _verbosity);

    uhtrIndex = uhtr->first;
      
    //Skipping header word
    for (size_t i = 1; i < uhtr->second.size(); ++i) {
      uint16_t word = uhtr->second[i];
      bunchCrossing = i + ((eventNumber-1) * 10);
      uhtrData = word;
      tree->Fill();
    }

  }  // end loop over uhtr containers

}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void HcalDigiToRawPatTest::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  
  edm::ParameterSetDescription desc;
  desc.addUntracked<int>("Verbosity", 0);
  desc.add<vector<int>>("tdc1", {12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                                 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                                 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12});
  desc.add<vector<int>>("tdc2", {14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
                                 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
                                 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14});
  desc.add<std::string>("ElectronicsMap", "");
  desc.add<edm::InputTag>("QIE11", edm::InputTag("simHcalDigis", "HBHEQIE11DigiCollection"));
  descriptions.add("hcalDigiToRawPatTest", desc);
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HcalDigiToRawPatTest);
