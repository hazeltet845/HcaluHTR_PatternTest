# Pattern Testing Analysis
## Generate L1T Ntuples
In order to analyze the pattern testing data, an L1T Ntuple must be generated from data and MC. This step runs the L1T step and outputs a root file with the L1T seed decisions per event. To generate the L1T Ntuples, first change the `--filein` tag in `runL1Emul_MC.sh` and `runL1Emul_Data.sh` to the correct input MC or data file. Then, 

    source runL1Emul_MC.sh
    cmsRun mc.py

    #OR

    source runL1Emul_Data.sh
    cmsRun data.py

## Parse L1T menu
The L1Ntuples do not contain the trigger menu information, so the trigger seeds in the L1Ntuples do not have names. To match the L1T names to the seeds, the correct menu must be downloaded and copied over from [https://github.com/cms-l1-dpg/L1MenuRun3/tree/master](https://github.com/cms-l1-dpg/L1MenuRun3/tree/master). For the pattern test in April of 2025, the correct menu for both data and MC is `L1Menu_Collisions2024_v1_3_0.csv`. To parse the menu for the analysis,

    cp ../../../L1MenuTools/uGT_decision_counts/parse_algo_map.py ./
    python3 parse_algo_map.py L1MENU.csv
    
This generates a file named `algo_map.py` with a list matching L1T seeds to names. This file is reference in the the main analysis file, `L1emuAnalyzer.py`, so make sure the correct L1 menu is loaded in `algo_map.py` before running the analysis on MC or data. 

## L1emuAnalyzer.py

This file accesses the L1 trigger and jet information from the L1Ntuples. This file also generates a number of plots to understand the trigger information. This file is specific for the 2025 pattern test and its corresponding MC. Modifications MUST be made before analyzing future pattern testing data from different MC. The usage is shown below:

    python3 L1emuAnalyzer.py [-i PATH/TO/INPUT_NTUPLE.root] [-n EVENTS] [--emu] [--mc] [--print]

    arguments:
      -i, --infilePath         Path to input Ntuple ROOT file
      -n, --nEvents            Number of events to process
      --emu                    Use emulated events
      --mc                     Input file is MC Ntuple
      --print                  Print LLP trigger and jet info

Disclaimer: the `--emu` argument uses the emulated trigger information from the L1Ntuple. This is NOT what you want to use for data. The emulated data in the L1Ntuple has emulated the HCALdigis from QIE11 data, which is NOT what we want to use.

Examples:

    #MC
    python3 L1emuAnalyzer.py -i L1Ntuple_MC_100.root --mc --print -n 6

    #Data from 25-event pattern test
    python3 L1emuAnalyzer.py -i L1Ntuple_Data_run390757_all.root

# Old
## MCAnalyzer.cc & MCAnalyzer_cfg.py
These files were used to print out out trigger information from the MC. These are old and do not generate any plots. The code is stil here because it could be useful to have in the future.  
    

  

