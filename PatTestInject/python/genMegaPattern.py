import numpy as np
import argparse, sys, os

event_binedges = np.arange(0,918,18)#np.arange(0,3025,25)

input_tag  = "VLLS_ele_M750_D1e-16_13p6TeV"
input_file = f"/eos/user/e/ethazelt/MC_files/VLL_gen/{input_tag}_GENSIMDIGIRAW_HLT.root" 

for k in range(1,event_binedges.shape[0]):
    binedge_0 = event_binedges[k-1]
    binedge_1 = event_binedges[k]

    command = f"cmsRun HcalDigiToRawPatTest_cfg.py -i {input_file} -s {binedge_0} -n 18 -g '140X_mcRun3_2024_realistic_v26' -e 'Run3_2025' -o '{input_tag}_offload_{binedge_0}-{binedge_1}_18EV'"
    
    os.system(command)
    print(f"Offload complete for {binedge_0}-{binedge_1}")

    command = f"python3 genPattern.py -o {input_tag}_{binedge_0}-{binedge_1}_18EV -i {input_tag}_offload_{binedge_0}-{binedge_1}_18EV -f 7 --all"

    os.system(command)
    print(f"Patterns complete for {binedge_0}-{binedge_1}")

