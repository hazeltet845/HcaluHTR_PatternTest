# Setup:

Make sure all materials are on cmsusr machine (patterns,pushPattern.py,etc.)

SSH:

	ssh hcalutca01

Source this:

	source ~hcalsw/bin/env.sh
 
Put uHTRtool.exe location into pushPattern.py. Make sure that uhtrtool is working and look at configurations.

	which uHTRtool.exe
	uHTRtool.exe -o bridge-hbhe -c 20:1

LINK -> FE_RAMS -> SETUP -> 0, 0, 0. Dump current FE_RAMS
   
TRIG -> LUTS. Dump current LUTs

Record read delay and orbit delay 
	read_delay  = 
        orbit_delay = 

IF ORBIT_DELAY DIFFERS ACROSS CRATES: remove spy from pushPattern.py

Uncomment uhtrtool command in pushPattern.py

# Load Test Patterns:

Start Run

Load pattern for 2 events per buffer followed by an empty pattern

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_2EV/VLLS_ele_M750_D1e-16_13p6TeV_0-2_2EV --orbit_delay $ --live --pattern

 	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_2EV/VLLS_ele_M750_D1e-16_13p6TeV_0-2_2EV --live --empty_pattern

--If trigger rate OK in monitoring:

Load pattern for 6 events per buffer followed by an empty pattern

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_6EV/VLLS_ele_M750_D1e-16_13p6TeV_0-6_6EV --orbit_delay $ --live --pattern

 	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_6EV/VLLS_ele_M750_D1e-16_13p6TeV_0-6_6EV --live --empty_pattern

--If trigger rate OK in monitoring:

Load pattern for 12 events per buffer followed by an empty pattern

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_12EV/VLLS_ele_M750_D1e-16_13p6TeV_0-12_12EV --orbit_delay $ --live --pattern

 	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_12EV/VLLS_ele_M750_D1e-16_13p6TeV_0-12_12EV --live --empty_pattern

--If trigger rate OK in monitoring:

Load pattern for 18 events per buffer followed by an empty pattern 

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_18EV/VLLS_ele_M750_D1e-16_13p6TeV_0-18_18EV --orbit_delay $ --live --pattern 

 	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_18EV/VLLS_ele_M750_D1e-16_13p6TeV_0-18_18EV --live --empty_pattern

--If trigger rate OK in monitoring:

Load pattern for 25 events per buffer followed by an empty pattern 

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --orbit_delay $ --live --pattern

 	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --live --empty_pattern

-- If trigger rate OK in monitoring

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --live --reset

End run 

# Load Patterns Back-To-Back

Start Run

Load pattern for 25 events per buffer (120s) followed by an empty pattern (30s)

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --orbit_delay $ --live --pattern --empty_pattern

 	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_25-50_25EV --orbit_delay $ --live --pattern --empty_pattern

  	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_50-75_25EV --orbit_delay $ --live --pattern --empty_pattern

	...

Pay attention to "GOOD" Patterns to use for next section

RESET:

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --live --reset

End run

# Load 1 Pattern 

Start Run 

Load pattern for 25 events per buffer and let run for a while

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --orbit_delay $ --live --pattern 

RESET:

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --live --reset

 End run

 # Reset ALL uHTRs 

	python3 pushPattern.py -i ABSPATH/output/patterns/VLLS_ele_M750_D1e-16_13p6TeV_25EV/VLLS_ele_M750_D1e-16_13p6TeV_0-25_25EV --live --reset

