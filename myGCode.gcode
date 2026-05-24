M17 ; Enable all stepper motors
G90 ; Set to Absolute Positioning
M83 ; Set extruder to relative mode
G1 Z40 F1200
M109 R40 ; Cool down Nozzle before Homing
G28 ; Home all axes
G1 Z20 F1200 ; Lift nozzle to 20mm quickly for safety
G1 X10.5 Y23.5 F4800 ; Move over the Homing Point, if set correctly
G1 X68.00000000000166 Y137.7777777777922 F1200;
G1 Z0 F1200
G1 Z15 F1200
G1 X68.00000000000166 Y102.50000000001444 F1200;
G1 Z0 F1200
G1 Z15 F1200
G1 X68.00000000000166 Y67.22222222223667 F1200;
G1 Z0 F1200
G1 Z15 F1200
G1 X68.00000000000166 Y102.50000000001444 F1200;
G1 Z0 F1200
G1 Z15 F1200
G1 Z40 F1200 ; Lift nozzle safely up to 20mm when done
G1 X0 Y200 F4800 ; Present the bed (pushes bed forward, moves X to 0)
M84 ; Disable stepper motors
