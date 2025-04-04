import os
import sys
import time
#from collections import defaultdict
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(
        add_help=True,
        description=''
    )

    parser.add_argument("-i", "--input_dir", action="store",required=True,default="./", help="input directory path")
    parser.add_argument("-c", "--crate",     action="store", help="Crate number for pattern generation")
    parser.add_argument("-u", "--uHTR",      action="store", help="uHTR number for pattern generation")
    parser.add_argument("--local",           action="store_true", help="Run on cmssw2 teststand")
    parser.add_argument("--live",            action="store_true", help="Run at P5")
   
    parser.add_argument("--uhtrtool",        action="store",type=str, default="/opt/xdaq/bin/uHTRtool.exe")
    parser.add_argument("--ip",              action="store",type=str, default="192.168.1.12")

    parser.add_argument("--read_delay",      action="store",type=int,   default=144)
    parser.add_argument("--orbit_delay",     action="store",type=int,   default=8)


    args = parser.parse_args()

    return args

def makeCommandList(cmdfpath, pattern_dir_path, spyfpath, read_delay, orbit_delay, crate, slot):
    with open(cmdfpath, "w") as of:
        def writeSequence(sequence):
            seq = sequence.strip().split(",")
            for cmd in seq:
                of.write(cmd+"\n")

        seq = "clock, setup, 3, quit"
        writeSequence(seq)
        seq = "link, fe_rams, zero, quit, quit"
        writeSequence(seq)
        seq = "link, fe_rams, setup, 1, 1, 0, load, {}/pattern_c{}_u{}.txt, -1, quit, quit".format(pattern_dir_path,crate,slot)
        #seq = "link, fe_rams, setup, 1, 1, 0, load, /root/tdcUMnCode/hcal/hcalUHTR/scripts/uHTRtest/patterns/pattern_test.txt, -1, quit, quit"
       
        writeSequence(seq)
        seq = "link, init, 99, {}, -1, 1, quit".format(read_delay)
        writeSequence(seq)
        seq = "trig, debug, Y, quit"
        writeSequence(seq)
        # seq = "trig, fir, 1, -1, quit"
        # writeSequence(seq)

        seq = "trig, soft, linkreset, quit"
        writeSequence(seq)

        if False:
            seq = "link, fe_rams, dump, {}.dump, quit, quit".format(patternfpath)
            writeSequence(seq)
            seq = "trig, luts, 2, 0, {}/c{}_s{}/LUT0.dump, -1, quit".format(pattern_dir_path,crate,slot)
            writeSequence(seq)
            seq = "trig, luts, 2, 1, {}/c{}_s{}/LUT1.dump, -1, quit".format(pattern_dir_path,crate,slot)
            writeSequence(seq)
            seq = "trig, luts, 2, 2, {}/c{}_s{}/LUT2.dump, -1, quit".format(pattern_dir_path,crate,slot)
            writeSequence(seq)
            seq = "trig, luts, 2, 3, {}/c{}_s{}/LUT3.dump, -1, quit".format(pattern_dir_path,crate,slot)
            writeSequence(seq)

        # Upload LLP-modified 1:1 LUT group0
        seq = "trig, luts, 4, 0, {}, -1, quit".format("/root/tdcUMnCode/hcal/hcalUHTR/scripts/uHTRtest/HcaluHTR_PatternTest/python/LUT0.txt")
        writeSequence(seq)

        # Set 1:1 LUT group1
        seq = "trig, luts, 3, 1, -1, -1, quit"
        writeSequence(seq)
        
        num_tls = 12

        for tl in range(num_tls):
            fpath = spyfpath + f"TL{tl}.txt"
            seq = "trig, spy, {}, {}, {}, quit".format(orbit_delay, tl, fpath)
            writeSequence(seq)

        seq = "quit"
        writeSequence(seq)

        of.close()



if __name__ == "__main__":
    args = parseArgs()

    input_dir   = args.input_dir #path to patterns
    local       = args.local
    live        = args.live
    crate       = args.crate
    uHTR        = args.uHTR
    read_delay  = args.read_delay
    orbit_delay = args.orbit_delay
    local_ip    = args.ip
    uhtrtool    = args.uhtrtool

    cmdfpath    = f"{input_dir}/uHTR_commands_c{crate}_u{uHTR}.txt"
    outputfpath = f"{input_dir}/uHTR_commands_c{crate}_u{uHTR}_out.txt"
    spyfpath    = f"{input_dir}/spy/spy_c{crate}_u{uHTR}"

    makeCommandList(cmdfpath, input_dir, spyfpath, read_delay, orbit_delay, crate, uHTR)

    if live:
        print("live")
    elif local:
        print("Pushing pattern to uHTR locally")
        os.system("{} {} -s {} > {}".format(uhtrtool,local_ip,cmdfpath,outputfpath))

