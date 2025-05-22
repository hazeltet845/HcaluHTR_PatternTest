#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"

using namespace std;

class MCAnalyzer : public edm::one::EDAnalyzer<>{
public:
  explicit MCAnalyzer(const edm::ParameterSet&);
  ~MCAnalyzer() override;

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<trigger::TriggerFilterObjectWithRefs> tokTrigFilter_;
};

MCAnalyzer::MCAnalyzer(const edm::ParameterSet& iConfig)
    : tokTrigFilter_(consumes<trigger::TriggerFilterObjectWithRefs>(
			    edm::InputTag("hltL1sVoHTT200SingleLLPJet60", "", "HLT"))){
}

MCAnalyzer::~MCAnalyzer() {}

int ietaFromEta(float eta) {
    int ieta = int(fabs(eta) / 0.087) + 1;
    return (eta > 0) ? ieta : -ieta;
}


void MCAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  edm::Handle<trigger::TriggerFilterObjectWithRefs> trigFilter;
  iEvent.getByToken(tokTrigFilter_,trigFilter);

  if (trigFilter.isValid()) {
    if (trigFilter->l1tjetSize() != 0) {
      cout<< "Event " << iEvent.id().event()<< " passed LLP filter w/ l1tjetSize == " << trigFilter->l1tjetSize()  << endl;
      vector<l1t::JetRef> jetRefVector;
      trigFilter->getObjects(trigger::TriggerL1Jet, jetRefVector);
      const size_t sizeJetRefVector = jetRefVector.size();
      for (size_t i = 0; i != sizeJetRefVector; i++) {
        l1t::JetRef obj = l1t::JetRef(jetRefVector[i]);
        cout << "\tL1Jet     " << "\t" << "pt = " << obj->pt() << "\t" << "eta =  " << obj->eta() << "\t"
                               << "phi =  " << obj->phi() << endl;  //<< "\t" << "BX = " << obj->bx();
        cout << "ieta == " << ietaFromEta(obj->eta()) << endl;
      }
    }
  }

}

DEFINE_FWK_MODULE(MCAnalyzer);
