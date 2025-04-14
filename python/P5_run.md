# Setup:

## 1
Make sure all materials are on cmsusr machine (patterns,pushPattern.py,etc.)

## 2 
	ssh hcalutca01

## 3 
Source this:
	source ~hcalsw/bin/env.sh

## 4 
Put uHTRtool.exe location into pushPattern.py. Make sure that uhtrtool is working and look at configurations.

	which uHTRtool.exe
	uHTRtool.exe -o bridge-hbhe -c 20:1

LINK -> FE_RAMS -> SETUP -> 0, 0, 0. Dump current FE_RAMS
   
TRIG -> LUTS. Dump current LUTs

Record read delay and orbit delay 
	read_delay  = 
        orbit_delay = 

IF ORBIT_DELAY DIFFERS ACROSS CRATES: remove spy from pushPattern.py

## 5
Uncomment uhtrtool command in pushPattern.py

# Load Patterns:

# 1

Start Run

# 2 
Load pattern for 2 events per buffer (120s)

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_2EV/VLLS_ele_M750_D1e-16_13p6TeV_0-2_2EV --orbit_delay $ --live --pattern --empty_pattern 

--If trigger rate OK in monitoring:

Load pattern for 6 events per buffer (120s) followed by an empty pattern (30s)

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_6EV/VLLS_ele_M750_D1e-16_13p6TeV_0-6_6EV --orbit_delay $ --live --pattern --empty_pattern

--If trigger rate OK in monitoring:

Load pattern for 12 events per buffer (120s) followed by an empty pattern (30s)

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_12EV/VLLS_ele_M750_D1e-16_13p6TeV_0-12_12EV --orbit_delay $ --live --pattern --empty_pattern

--If trigger rate OK in monitoring:

Load pattern for 12 events per buffer (120s) followed by an empty pattern (30s)
