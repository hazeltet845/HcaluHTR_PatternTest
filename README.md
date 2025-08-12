# Setup Working Environment

    cmsrel CMSSW_15_0_0
    cd CMSSW_15_0_0/src
    cmsenv

    git cms-init

    git cms-merge-topic --unsafe hazeltet845:PatTest_15_0_0
    git clone --depth 1 https://github.com/cms-l1-dpg/L1MenuTools.git  # Needed for analysis only

    git clone git@github.com:hazeltet845/HcaluHTR_PatternTest.git uHTRStudies/

    scram b clean
    scram b -j 8

# PatTestInject
See README in `PatTestInject/`

# PatTestAnalysis
See README in `PatTestAnalysis/`
