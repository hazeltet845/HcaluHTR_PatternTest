# Setup Working Environment

    cmsrel CMSSW_15_0_0
    cd $CMSSW_BASE/src
    cmsenv

    git cms-addpkg DataFormats/HcalDigi

    git cms-checkdeps -a -A

    git clone git@github.com:hazeltet845/HcaluHTR_PatternTest.git uHTRStudies/PatTest/

    scram b clean
    scram b -j 8

