# Setup Working Environment

    cmsrel CMSSW_15_0_0
    cd $CMSSW_BASE/src
    cmsenv

    git cms-init

    git cms-merge-topic --unsafe hazeltet845:PatTest_15_0_0

    git clone git@github.com:hazeltet845/HcaluHTR_PatternTest.git uHTRStudies/PatTest/

    scram b clean
    scram b -j 8

# Offload RAWSIM QIE11 Data 
The QIE11 data must be offloaded from the input root file in a format that makes pattern generation possible. The input root file must contain a tree of QIE11 data frames. The `python/HcalDigiToRawPatTest_cfg.py` config file calls `plugins/HcalDigiToRawPatTest.cc` to offload the QIE11 data to `python/output/offload`. The usage is shown below:
 
    usage: cmsRun HcalDigiToRawPatTest_cfg.py [-i PATH/TO/INPUT.root] [-n EVENTS] [-s NUM_SKIP_EVENTS] [-g GLOBAL_TAG] [-e ERA] [-o OUTPUT_TAG]

    arguments:
      -i, --input              Path to input ROOT file
      -n, --num_events         Number of events to process
      -s, --skip_num           Number of events to skip
      -g, --global_tag         Global tag to use
      -e, --era                Era to use
      -o, --output_tag         Name of output file (OUTPUT_TAG.root)

#### Example:

    cd $CMSSW_BASE/src/uHTRStudies/PatTest/python

    cmsRun HcalDigiToRawPatTest_cfg.py -i /eos/user/e/ethazelt/cmssw/CMSSW_14_2_2/src/VLL_RAWSIM_ex.root -n 3 -g "140X_mcRun3_2024_realistic_v26" -e "Run3_2025" -o "outputFile"

# Generate Patterns
The offloaded output file is utilized by `python/genPattern.py` to generate .txt files for each crate/uHTR combination to `python/output/patterns`. This can be run for a specific crate and uHTR or over all crate/uHTR combinations. The usage is shown below:

    usage: python3 genPattern.py [-o OUTPUT_DIRECTORY_TAG] [-i INPUT_TAG] [-a] [-c CRATE_NUMBER] [-u UHTR_NUMBER] [-f NUM_EVENTS_FILL]

    arguments:
      -i, --input_tag          Input file tag (TAG.root)
      -o, --output_dir         Output directory name 
      -a, --all                Create pattern for ALL crates and uHTRS
      -c, --crate              Crate number for pattern generation
      -u, --uHTR               uHTR number for pattern generation
      -f, --fill_events        Number of events (10 BXs each) to fill with empty patterns in between MC events

#### Example:

    cd $CMSSW_BASE/src/uHTRStudies/PatTest/python
    
    python3 genPattern.py -o directory_test -i outputFile --all

    python3 genPattern.py -o directory_test -i outputFile -c 21 -u 4

# Inject Patterns to uHTR
The patterns can be fed into a local teststand or fed live to the uHTRS in HB at P5. The patterns are injected via `python/pushPattern.py`. The file generates a list of commands to feed into the selected uHTRs for configuration and injection. For injections at P5, reset commands are generated to ensure that the uHTRs are in a configuration for collision data taking following the pattern testing. The usage of `python/pushPattern.py` is shown below:

    usage: python3 pushPattern.py [-i PATTERN_PATH] [-c CRATE] [-u UHTR_SLOT] [--local] [--live] [--uhtrtool UHTRTOOL_PATH] [--ip UHTR_IP] [--read_delay READ_DELAY] [--orbit_delay --ORBIT_DELAY] [--pattern] [--empty_pattern] [--reset]

    arguments:
      -i, --input_dir          Input directory absolute path
      -c, --crate              Crate number for pattern generation
      -u, --uHTR               uHTR number for pattern generation
      --local                  Run on cmssw2 teststand
      --live                   Run at P5
      --uhtrtool               uHTRtool abosolute path
      --ip                     IP address of uHTR
      --read_delay             Read Delay value
      --orbit_delay            Orbit Delay value
      --pattern                Insert pattern live
      --empty_pattern          Insert empty pattern live
      --reset                  Reset uHTRs live

#### Example: Live

Insert pattern only:

    cd $CMSSW_BASE/src/uHTRStudies/PatTest/python

    python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --live --pattern --orbit_delay 8  --uhtrtool "/opt/xdaq/bin/uHTRtool.exe"

Insert empty pattern:

    python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --live --empty_pattern --orbit_delay 8  --uhtrtool "/opt/xdaq/bin/uHTRtool.exe"

Reset uHTRs:

    python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --live --reset --orbit_delay 8  --uhtrtool "/opt/xdaq/bin/uHTRtool.exe"


#### Example: Local

    cd $CMSSW_BASE/src/uHTRStudies/PatTest/python

    python3 pushPattern.py -i "/root/tdcUMnCode/hcal/hcalUHTR/scripts/uHTRtest/HcaluHTR_PatternTest/python/output/patterns/directory_test" -c 21 -u 4 --local --read_delay 14 --orbit_delay 8 --ip "192.168.X.X" --uhtrtool "/home/daqowner/daq.15.4.0/bin/uHTRtool.exe"
    
