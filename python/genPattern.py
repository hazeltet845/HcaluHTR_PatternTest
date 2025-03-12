import uproot
import pandas as pd
import numpy as np
import argparse, sys, os

def parseArgs():
    parser = argparse.ArgumentParser(
        add_help=True,
        description=''
    )

    parser.add_argument("-o", "--output_dir", action="store", default="./", help="Output directory path")
    parser.add_argument("-a", "--all",        action="store_true", help="Create pattern for ALL crates and uHTRS")
    parser.add_argument("-c", "--crate",      action="store", help="Crate number for pattern generation")
    parser.add_argument("-u", "--uHTR",       action="store", help="uHTR number for pattern generation")

    args = parser.parse_args()

    return args

def getCrate(value):
    out = value & 0xFF
    return out

def getSlot(value):
    out = (value & 0xF00) >> 8
    return out

def getFiber(value):
    out = (value & 0xFF0000) >> 16
    return out

def getFibChan(value):
    out = (value & 0xFF000000) >> 24
    return out

def getTDC(value):
    mask_HE = 0x3F
    mask_HB = 0x3
    out = (value >> 8) & mask_HB
    return out

def getADC(value):
    mask_ADC = 0xFF
    out = value & mask_ADC
    return out

def createTDCWord(tdc_l):
    tdc_word = tdc_l[0]
    for k in range(1,len(tdc_l)):
        tmp = tdc_l[k] << (2*k)
        tdc_word = tmp | tdc_word
    
    return tdc_word

def fillMissingChnls(df):
    adc_l = list(df['ADC'])
    tdc_l = list(df['TDC'])
    fibchan_l = list(df["FibChan"])
    
    fill_adc = [0] * 8
    fill_tdc = [3] * 8
    
    for i, chan in enumerate(fibchan_l):
        fill_adc[chan] = adc_l[i]
        fill_tdc[chan] = tdc_l[i]
        
    return pd.Series([fill_adc,fill_tdc])

def patternWrite(df,outfile,crate,uHTR,max_BX):
    
    num_fib = 24
    for fib in range(num_fib):

        outfile.write('# Fiber %d\n' % fib)
        filt = df.query(f"Crate == {crate} and Slot == {uHTR} and Fiber == {fib}")
        
        if not filt.empty:
            group = (filt.groupby("bunchCrossing", group_keys=False)
                   .apply(fillMissingChnls)
                   .reset_index(drop=True))

            group.columns = ["ADC", "TDC"]
            group['TDC'] = group['TDC'].apply(createTDCWord)
        else:
            group = pd.DataFrame()
            group['bunchCrossing'] = np.arange(1,max_BX+1)
            group['ADC'] = [np.zeros(8,dtype=int)] * max_BX
            group['TDC'] = np.ones(max_BX,dtype=int)*0xffff

        for index, row in group.iterrows():

            bc0 = 1 if index==0 else 0
            ce = 0
            capID = index%4 #doesnt matter
            res = 0

            byte0 = 0xbc #K28.5
            byte1 = res<<4 | capID<<2 | ce<<1 | bc0

            ADC = row['ADC']
            TDC = row['TDC']
            

            outfile.write("1%02x%02x\n"%(byte1, byte0))
            outfile.write("0%02x%02x\n"%(ADC[1],ADC[0]))
            outfile.write("0%02x%02x\n"%( ADC[3],ADC[2] ))
            outfile.write("0%02x%02x\n"%( ADC[5],ADC[4] ))
            outfile.write("0%02x%02x\n"%( ADC[7],ADC[6] ))
            outfile.write("0%04x\n"%(TDC))

def main():
    args = parseArgs()

    output_dir  = args.output_dir
    all_uHTR    = args.all
    crate       = args.crate
    uHTR        = args.uHTR

    tree = uproot.open("test.root")['hcalRawData/UHTRTree']

    df = tree.arrays(library="pd")
    df['Crate'] = df['uhtrIndex'].apply(getCrate)
    df['Slot'] = df['uhtrIndex'].apply(getSlot)
    df['Fiber'] = df['uhtrIndex'].apply(getFiber)
    df['FibChan'] = df['uhtrIndex'].apply(getFibChan)
    df['TDC'] = df['uhtrData'].apply(getTDC)
    df['ADC'] = df['uhtrData'].apply(getADC)

    df = df.drop('uhtrIndex',axis=1)
    df = df.drop('uhtrData', axis=1)
    
    max_BX = df['bunchCrossing'].max()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if(all_uHTR):
        print("Generating patterns for all uHTRs")
        uHTR_df = df[['Crate', 'Slot']].drop_duplicates()
        for index,row in uHTR_df.iterrows():
            crate = row['Crate']
            uHTR  = row['Slot']

            patternfpath = f"{output_dir}/pattern_c{crate}_u{uHTR}.txt"
            with open(patternfpath, 'w') as outfile:
                print(f"Writing pattern to {patternfpath}")
                patternWrite(df,outfile,crate,uHTR,max_BX)

    else:
        patternfpath = f"{output_dir}/pattern_c{crate}_u{uHTR}.txt"
        with open(patternfpath, 'w') as outfile:
            print(f"Writing pattern to {patternfpath}")
            patternWrite(df,outfile,crate,uHTR,max_BX)
    


if __name__ == "__main__":
    main()
