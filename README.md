# Setup Working Environment

    cmsrel CMSSW_15_0_0
    cd $CMSSW_BASE/src
    cmsenv

    git cms-init

    git cms-merge-topic --unsafe hazeltet845:PatTest_15_0_0

    git clone git@github.com:hazeltet845/HcaluHTR_PatternTest.git uHTRStudies/PatTest/

    scram b clean
    scram b -j 8

