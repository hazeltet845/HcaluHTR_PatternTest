# Setup Working Environment

    cmsrel CMSSW_15_0_0
    cd $CMSSW_BASE/src
    cmsenv

    git cms-init

    git cms-merge-topic --unsafe hazeltet845:PatTest_15_0_0

    git clone git@github.com:hazeltet845/HcaluHTR_PatternTest.git uHTRStudies/PatTest/

    scram b clean
    scram b -j 8

#Offload RAWSIM QIE11 Data 
The QIE11 data must be offloaded from the input root file in a format that makes pattern generation possible. The `python/HcalDigiToRawPatTest_cfg.py` config file calls `plugins/HcalDigiToRawPatTest.cc` to offload the QIE11 data to `python/output/offload`. The usage is shown below:
 
    usage: cmsRun HcalDigiToRawPatTest_cfg.py [-i PATH/TO/INPUT.root] [-n EVENTS] [-g GLOBAL_TAG] [-e ERA] [-o OUTPUT_TAG]

    arguments:
      -i, --input              Path to input ROOT file
      -n, --num_events         Number of events to process
      -g, --global_tag         Global tag to use
      -e, --era                Era to use
      -o, --output_tag         Name of output file (OUTPUT_TAG.root)

Example:

    cd $CMSSW_BASE/src/uHTRStudies/PatTest/python

    cmsRun HcalDigiToRawPatTest_cfg.py -i /eos/user/e/ethazelt/cmssw/CMSSW_14_2_2/src/VLL_RAWSIM_ex.root -n 3 -g "140X_mcRun3_2024_realistic_v26" -e "Run3_2025" -o "outputFile"

#Generate Patterns
The offloaded output file is utilized by `python/genPattern.py` to generate .txt files for each crate/uHTR combination to `python/output/patterns`. This can be run for a specific crate and uHTR or over all crate/uHTR combinations. The usage is shown below:

    usage: python3 genPattern.py [-o OUTPUT_DIRECTORY_TAG] [-i INPUT_TAG] [-a] [-c CRATE_NUMBER] [-u UHTR_NUMBER]

    arguments:
      -i, --input_tag          Input file tag (TAG.root)
      -o, --output_dir         Output directory name 
      -a, --all                Create pattern for ALL crates and uHTRS
      -c, --crate              Crate number for pattern generation
      -u, --uHTR               uHTR number for pattern generation

Example:

    cd $CMSSW_BASE/src/uHTRStudies/PatTest/python
    
    python3 genPattern.py -o directory_test -i outputFile --all

    python3 genPattern.py -o directory_test -i outputFile -c 21 -u 4
