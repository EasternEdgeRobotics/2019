EESchema Schematic File Version 4
LIBS:Dual CamCon-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 7355 7515 0    79   ~ 16
Dual CamCon
$Comp
L EER:SFW15R-1STE1LF J4
U 1 1 5BB9481F
P 3750 4800
F 0 "J4" H 4100 2950 69  0000 C CNN
F 1 "Camera FPC Connector" H 3950 3050 50  0000 C CNN
F 2 "EER:CON15_1X15_DRB_SFW" H 3750 4800 50  0001 C CNN
F 3 "" H 3750 4800 50  0001 C CNN
	1    3750 4800
	1    0    0    -1  
$EndComp
$Comp
L EER:SFW15R-1STE1LF J3
U 1 1 5BB9489E
P 3750 2650
F 0 "J3" H 4050 800 69  0000 C CNN
F 1 "Camera FPC Connector" H 3950 900 50  0000 C CNN
F 2 "EER:CON15_1X15_DRB_SFW" H 3750 2650 50  0001 C CNN
F 3 "609-1905-1-ND" H 3750 2650 50  0001 C CNN
	1    3750 2650
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J2
U 1 1 5BB951EE
P 3600 1950
F 0 "J2" H 3600 1600 50  0000 C CNN
F 1 "Servo Input" H 3600 1700 50  0000 C CNN
F 2 "EER:MOLEX_0705530001" H 3600 1950 50  0001 C CNN
F 3 "WM4900-ND" H 3600 1950 50  0001 C CNN
	1    3600 1950
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 5BB9523E
P 3600 1450
F 0 "J1" H 3600 1100 50  0000 C CNN
F 1 "Servo Input" H 3600 1200 50  0000 C CNN
F 2 "EER:MOLEX_0705530001" H 3600 1450 50  0001 C CNN
F 3 "WM4900-ND" H 3600 1450 50  0001 C CNN
	1    3600 1450
	-1   0    0    1   
$EndComp
$Comp
L EER:10029449-001RLF P1
U 1 1 5BB96ECC
P 5550 3500
F 0 "P1" H 5829 3546 50  0000 L CNN
F 1 "HDMI Connector" H 5829 3455 50  0000 L CNN
F 2 "EER:FCI_10029449-001RLF" H 5950 3400 50  0001 L BNN
F 3 "609-4614-1-ND" H 5950 3700 50  0001 L BNN
	1    5550 3500
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_02x20_Odd_Even J5
U 1 1 5BB97387
P 7400 4250
F 0 "J5" H 7450 5300 50  0000 C CNN
F 1 "Raspberry Pi GPIO" H 7400 3050 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x20_Pitch2.54mm" H 7400 4250 50  0001 C CNN
F 3 "~" H 7400 4250 50  0001 C CNN
	1    7400 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	7700 3450 7800 3450
Wire Wire Line
	7800 3450 7800 3350
Wire Wire Line
	7800 3350 7700 3350
$Comp
L power:+5V #PWR0101
U 1 1 5BB97977
P 7800 3150
F 0 "#PWR0101" H 7800 3000 50  0001 C CNN
F 1 "+5V" H 7815 3323 50  0000 C CNN
F 2 "" H 7800 3150 50  0001 C CNN
F 3 "" H 7800 3150 50  0001 C CNN
	1    7800 3150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5BB97B33
P 7800 5450
F 0 "#PWR0102" H 7800 5200 50  0001 C CNN
F 1 "GND" H 7805 5277 50  0000 C CNN
F 2 "" H 7800 5450 50  0001 C CNN
F 3 "" H 7800 5450 50  0001 C CNN
	1    7800 5450
	1    0    0    -1  
$EndComp
Wire Wire Line
	7700 3950 7800 3950
Wire Wire Line
	7800 3950 7800 3550
Wire Wire Line
	7800 3550 7700 3550
Wire Wire Line
	7700 4250 7800 4250
Wire Wire Line
	7800 4250 7800 3950
Connection ~ 7800 3950
Wire Wire Line
	7700 4750 7800 4750
Wire Wire Line
	7800 4750 7800 4250
Connection ~ 7800 4250
Wire Wire Line
	7700 4950 7800 4950
Wire Wire Line
	7800 4950 7800 4750
Connection ~ 7800 4750
Wire Wire Line
	7800 4950 7800 5350
Connection ~ 7800 4950
Wire Wire Line
	7200 3750 7100 3750
Wire Wire Line
	7100 3750 7100 4550
Wire Wire Line
	7100 5350 7800 5350
Connection ~ 7800 5350
Wire Wire Line
	7800 5450 7800 5350
Wire Wire Line
	7200 5250 7100 5250
Connection ~ 7100 5250
Wire Wire Line
	7100 5250 7100 5350
Wire Wire Line
	7200 4550 7100 4550
Connection ~ 7100 4550
Wire Wire Line
	7100 4550 7100 5250
Wire Wire Line
	7800 3350 7800 3150
Connection ~ 7800 3350
$Comp
L EER:10029449-001RLF P2
U 1 1 5BB96F4D
P 5550 5650
F 0 "P2" H 5829 5696 50  0000 L CNN
F 1 "HDMI Connector" H 5829 5605 50  0000 L CNN
F 2 "EER:FCI_10029449-001RLF" H 5950 5550 50  0001 L BNN
F 3 "609-4614-1-ND" H 5950 5850 50  0001 L BNN
	1    5550 5650
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5BBA4A5B
P 3950 2200
F 0 "#PWR0103" H 3950 1950 50  0001 C CNN
F 1 "GND" H 4100 2100 50  0000 C CNN
F 2 "" H 3950 2200 50  0001 C CNN
F 3 "" H 3950 2200 50  0001 C CNN
	1    3950 2200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5BBA4AC1
P 3950 1650
F 0 "#PWR0104" H 3950 1400 50  0001 C CNN
F 1 "GND" H 4100 1550 50  0000 C CNN
F 2 "" H 3950 1650 50  0001 C CNN
F 3 "" H 3950 1650 50  0001 C CNN
	1    3950 1650
	1    0    0    -1  
$EndComp
Wire Wire Line
	3800 1450 3950 1450
Wire Wire Line
	3800 1950 3950 1950
Text Label 4600 1850 0    50   ~ 0
Servo2
Text Label 4600 1350 0    50   ~ 0
Servo1
$Comp
L power:GND #PWR0105
U 1 1 5BBA877A
P 3250 6600
F 0 "#PWR0105" H 3250 6350 50  0001 C CNN
F 1 "GND" H 3400 6500 50  0000 C CNN
F 2 "" H 3250 6600 50  0001 C CNN
F 3 "" H 3250 6600 50  0001 C CNN
	1    3250 6600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 2650 3250 2950
Wire Wire Line
	3750 4150 3250 4150
Connection ~ 3250 4150
Wire Wire Line
	3250 4150 3250 4250
Wire Wire Line
	3750 4250 3250 4250
Connection ~ 3250 4250
Wire Wire Line
	3250 4250 3250 4800
Wire Wire Line
	3750 6400 3250 6400
Connection ~ 3250 6400
Wire Wire Line
	3250 6400 3250 6600
Wire Wire Line
	3750 6300 3250 6300
Connection ~ 3250 6300
Wire Wire Line
	3250 6300 3250 6400
Wire Wire Line
	3750 2950 3250 2950
Connection ~ 3250 2950
Wire Wire Line
	3250 2950 3250 3250
Wire Wire Line
	3750 3250 3250 3250
Connection ~ 3250 3250
Wire Wire Line
	3250 3250 3250 3550
Wire Wire Line
	3750 3550 3250 3550
Connection ~ 3250 3550
Wire Wire Line
	3250 3550 3250 4150
Wire Wire Line
	3750 2650 3250 2650
Wire Wire Line
	3750 4800 3250 4800
Connection ~ 3250 4800
Wire Wire Line
	3250 4800 3250 5100
Wire Wire Line
	3750 5100 3250 5100
Connection ~ 3250 5100
Wire Wire Line
	3250 5100 3250 5400
Wire Wire Line
	3750 5400 3250 5400
Connection ~ 3250 5400
Wire Wire Line
	3250 5400 3250 5700
Wire Wire Line
	3750 5700 3250 5700
Connection ~ 3250 5700
Wire Wire Line
	3250 5700 3250 6300
Text Label 3350 2750 0    50   ~ 0
CAM1_D0-
Text Label 3350 2850 0    50   ~ 0
CAM1_D0+
Text Label 3350 3050 0    50   ~ 0
CAM1_D1-
Text Label 3350 3150 0    50   ~ 0
CAM1_D1+
Text Label 3350 3350 0    50   ~ 0
CAM1_C-
Text Label 3350 3450 0    50   ~ 0
CAM1_C+
Text Label 3350 3650 0    50   ~ 0
CAM1_GPIO
Text Label 3350 3750 0    50   ~ 0
CAM1_CLK
Text Label 3350 3850 0    50   ~ 0
CAM1_SCL
Text Label 3350 3950 0    50   ~ 0
CAM1_SDA
Text Label 3350 4050 0    50   ~ 0
CAM1_3V3
Wire Wire Line
	3350 2750 3750 2750
Wire Wire Line
	3350 2850 3750 2850
Wire Wire Line
	3350 3150 3750 3150
Wire Wire Line
	3350 3050 3750 3050
Wire Wire Line
	3350 3350 3750 3350
Wire Wire Line
	3350 3450 3750 3450
Wire Wire Line
	3350 3650 3750 3650
Wire Wire Line
	3350 3750 3750 3750
Wire Wire Line
	3350 3850 3750 3850
Wire Wire Line
	3350 3950 3750 3950
Wire Wire Line
	3350 4050 3750 4050
Text Label 3350 4900 0    50   ~ 0
CAM2_D0-
Text Label 3350 5000 0    50   ~ 0
CAM2_D0+
Text Label 3350 5200 0    50   ~ 0
CAM2_D1-
Text Label 3350 5300 0    50   ~ 0
CAM2_D1+
Text Label 3350 5500 0    50   ~ 0
CAM2_C-
Text Label 3350 5600 0    50   ~ 0
CAM2_C+
Text Label 3350 5800 0    50   ~ 0
CAM2_GPIO
Text Label 3350 5900 0    50   ~ 0
CAM2_CLK
Text Label 3350 6000 0    50   ~ 0
CAM2_SCL
Text Label 3350 6100 0    50   ~ 0
CAM2_SDA
Text Label 3350 6200 0    50   ~ 0
CAM2_3V3
Wire Wire Line
	3350 4900 3750 4900
Wire Wire Line
	3350 5000 3750 5000
Wire Wire Line
	3350 5200 3750 5200
Wire Wire Line
	3350 5300 3750 5300
Wire Wire Line
	3350 5500 3750 5500
Wire Wire Line
	3350 5600 3750 5600
Wire Wire Line
	3350 5800 3750 5800
Wire Wire Line
	3350 5900 3750 5900
Wire Wire Line
	3350 6000 3750 6000
Wire Wire Line
	3350 6100 3750 6100
Wire Wire Line
	3350 6200 3750 6200
Wire Wire Line
	6000 2700 6000 2600
Connection ~ 6000 2600
Wire Wire Line
	6000 2600 6000 2500
$Comp
L power:+5V #PWR0106
U 1 1 5BC13C19
P 6000 2500
F 0 "#PWR0106" H 6000 2350 50  0001 C CNN
F 1 "+5V" H 6015 2673 50  0000 C CNN
F 2 "" H 6000 2500 50  0001 C CNN
F 3 "" H 6000 2500 50  0001 C CNN
	1    6000 2500
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0107
U 1 1 5BC13C32
P 6000 4650
F 0 "#PWR0107" H 6000 4500 50  0001 C CNN
F 1 "+5V" H 6015 4823 50  0000 C CNN
F 2 "" H 6000 4650 50  0001 C CNN
F 3 "" H 6000 4650 50  0001 C CNN
	1    6000 4650
	1    0    0    -1  
$EndComp
Connection ~ 6350 5550
Wire Wire Line
	6350 5550 6350 5850
Connection ~ 6350 5850
Wire Wire Line
	6350 5850 6350 6150
Connection ~ 6350 6150
Wire Wire Line
	6350 6150 6350 6450
Connection ~ 6350 6450
Wire Wire Line
	6350 6450 6350 6600
Wire Wire Line
	6350 4300 6350 4000
Wire Wire Line
	6350 4000 6350 3700
Connection ~ 6350 4000
Wire Wire Line
	6350 3700 6350 3400
Connection ~ 6350 3700
Connection ~ 6350 3400
$Comp
L power:GND #PWR0108
U 1 1 5BC2BB85
P 6350 6600
F 0 "#PWR0108" H 6350 6350 50  0001 C CNN
F 1 "GND" H 6500 6500 50  0000 C CNN
F 2 "" H 6350 6600 50  0001 C CNN
F 3 "" H 6350 6600 50  0001 C CNN
	1    6350 6600
	1    0    0    -1  
$EndComp
Connection ~ 6350 4300
Wire Wire Line
	5850 2600 6000 2600
Wire Wire Line
	5850 2700 6000 2700
Text Label 5850 4400 0    50   ~ 0
CAM1_D0-
Text Label 5850 4200 0    50   ~ 0
CAM1_D0+
Wire Wire Line
	5850 4000 6350 4000
Wire Wire Line
	5850 4300 6350 4300
Wire Wire Line
	5850 4400 6250 4400
Wire Wire Line
	5850 4200 6250 4200
Wire Wire Line
	5850 4100 6250 4100
Wire Wire Line
	5850 3900 6250 3900
Wire Wire Line
	5850 3800 6250 3800
Wire Wire Line
	5850 3700 6350 3700
Wire Wire Line
	5850 3600 6250 3600
Wire Wire Line
	5850 3500 6250 3500
Text Label 5850 4100 0    50   ~ 0
CAM1_D1-
Text Label 5850 3900 0    50   ~ 0
CAM1_D1+
Text Label 5850 3800 0    50   ~ 0
CAM1_C-
Text Label 5850 3600 0    50   ~ 0
CAM1_C+
Text Label 5850 3500 0    50   ~ 0
CAM1_GPIO
Text Label 5850 3300 0    50   ~ 0
CAM1_CLK
Text Label 5850 3200 0    50   ~ 0
CAM1_SCL
Text Label 5850 3100 0    50   ~ 0
CAM1_SDA
Text Label 5850 3000 0    50   ~ 0
CAM1_3V3
Wire Wire Line
	5850 2800 6350 2800
Wire Wire Line
	6350 2800 6350 3400
Wire Wire Line
	5850 3400 6350 3400
Wire Wire Line
	5850 3300 6250 3300
Wire Wire Line
	5850 3200 6250 3200
Wire Wire Line
	5850 3100 6250 3100
Wire Wire Line
	5850 3000 6250 3000
Wire Wire Line
	5850 2900 6250 2900
Wire Wire Line
	6350 4300 6350 4950
Wire Wire Line
	5850 4950 6350 4950
Connection ~ 6350 4950
Wire Wire Line
	6350 4950 6350 5550
Wire Wire Line
	5850 5550 6350 5550
Wire Wire Line
	5850 5850 6350 5850
Wire Wire Line
	5850 6150 6350 6150
Wire Wire Line
	5850 6450 6350 6450
Wire Wire Line
	6000 4650 6000 4750
Wire Wire Line
	5850 4750 6000 4750
Connection ~ 6000 4750
Wire Wire Line
	6000 4750 6000 4850
Wire Wire Line
	6000 4850 5850 4850
Wire Wire Line
	5850 5050 6250 5050
Wire Wire Line
	5850 5150 6250 5150
Wire Wire Line
	5850 5250 6250 5250
Wire Wire Line
	5850 5350 6250 5350
Wire Wire Line
	5850 5450 6250 5450
Wire Wire Line
	5850 5650 6250 5650
Wire Wire Line
	5850 5750 6250 5750
Wire Wire Line
	5850 5950 6250 5950
Wire Wire Line
	5850 6050 6250 6050
Wire Wire Line
	5850 6250 6250 6250
Wire Wire Line
	5850 6350 6250 6350
Wire Wire Line
	5850 6550 6250 6550
Text Label 5850 6550 0    50   ~ 0
CAM2_D0-
Text Label 5850 6350 0    50   ~ 0
CAM2_D0+
Text Label 5850 6250 0    50   ~ 0
CAM2_D1-
Text Label 5850 6050 0    50   ~ 0
CAM2_D1+
Text Label 5850 5950 0    50   ~ 0
CAM2_C-
Text Label 5850 5750 0    50   ~ 0
CAM2_C+
Text Label 5850 5650 0    50   ~ 0
CAM2_GPIO
Text Label 5850 5450 0    50   ~ 0
CAM2_CLK
Text Label 5850 5350 0    50   ~ 0
CAM2_SCL
Text Label 5850 5250 0    50   ~ 0
CAM2_SDA
Text Label 5850 5150 0    50   ~ 0
CAM2_3V3
Text Label 5850 5050 0    50   ~ 0
Servo2
Text Label 5850 2900 0    50   ~ 0
Servo1
NoConn ~ 7200 3350
NoConn ~ 7200 3450
NoConn ~ 7200 3550
NoConn ~ 7200 3650
NoConn ~ 7700 3650
NoConn ~ 7700 3750
NoConn ~ 7700 3850
NoConn ~ 7700 4050
NoConn ~ 7700 4150
NoConn ~ 7700 4350
NoConn ~ 7700 4450
NoConn ~ 7700 4550
NoConn ~ 7700 4650
NoConn ~ 7700 4850
NoConn ~ 7700 5050
NoConn ~ 7700 5150
NoConn ~ 7700 5250
NoConn ~ 7200 5150
NoConn ~ 7200 5050
NoConn ~ 7200 4950
NoConn ~ 7200 4850
NoConn ~ 7200 4750
NoConn ~ 7200 4650
NoConn ~ 7200 4450
NoConn ~ 7200 4350
NoConn ~ 7200 4250
NoConn ~ 7200 4150
NoConn ~ 7200 4050
NoConn ~ 7200 3950
NoConn ~ 7200 3850
Wire Wire Line
	3800 1850 4250 1850
Wire Wire Line
	3800 1350 4250 1350
$Comp
L Device:C C2
U 1 1 5BDBBB9B
P 4250 2000
F 0 "C2" H 4365 2046 50  0000 L CNN
F 1 "C" H 4365 1955 50  0000 L CNN
F 2 "EER:C_0805_HandSoldering" H 4288 1850 50  0001 C CNN
F 3 "~" H 4250 2000 50  0001 C CNN
	1    4250 2000
	1    0    0    -1  
$EndComp
Connection ~ 4250 1850
Wire Wire Line
	4250 1850 4550 1850
$Comp
L Device:C C4
U 1 1 5BDBBC17
P 4550 2000
F 0 "C4" H 4665 2046 50  0000 L CNN
F 1 "C" H 4665 1955 50  0000 L CNN
F 2 "EER:C_0805_HandSoldering" H 4588 1850 50  0001 C CNN
F 3 "~" H 4550 2000 50  0001 C CNN
	1    4550 2000
	1    0    0    -1  
$EndComp
Connection ~ 4550 1850
Wire Wire Line
	4550 1850 4850 1850
$Comp
L Device:C C1
U 1 1 5BDBBC45
P 4250 1500
F 0 "C1" H 4365 1546 50  0000 L CNN
F 1 "C" H 4365 1455 50  0000 L CNN
F 2 "EER:C_0805_HandSoldering" H 4288 1350 50  0001 C CNN
F 3 "~" H 4250 1500 50  0001 C CNN
	1    4250 1500
	1    0    0    -1  
$EndComp
Connection ~ 4250 1350
Wire Wire Line
	4250 1350 4550 1350
$Comp
L Device:C C3
U 1 1 5BDBBC77
P 4550 1500
F 0 "C3" H 4665 1546 50  0000 L CNN
F 1 "C" H 4665 1455 50  0000 L CNN
F 2 "EER:C_0805_HandSoldering" H 4588 1350 50  0001 C CNN
F 3 "~" H 4550 1500 50  0001 C CNN
	1    4550 1500
	1    0    0    -1  
$EndComp
Connection ~ 4550 1350
Wire Wire Line
	4550 1350 4850 1350
Wire Wire Line
	3950 1650 4250 1650
Wire Wire Line
	4250 1650 4550 1650
Connection ~ 4250 1650
Wire Wire Line
	3950 1450 3950 1650
Connection ~ 3950 1650
Wire Wire Line
	3950 1950 3950 2200
Wire Wire Line
	4250 2150 4250 2200
Wire Wire Line
	4550 2150 4550 2200
Wire Wire Line
	4550 2200 4250 2200
Connection ~ 4250 2200
Connection ~ 3950 2200
Wire Wire Line
	3950 2200 4250 2200
Text Notes 4950 1550 0    50   ~ 0
Filtering caps incase the servo signal is jittery\n
Text Notes 6150 2650 0    50   ~ 0
Powering the servos with the Pis +5V
Text Notes 6600 6200 0    50   ~ 0
Trying to match sensitive signals\nwith shielded twisted pairs
Text Notes 8200 4500 0    50   ~ 0
If need be, we can solder to \nthe top Pi's GPIOs as a last ditch fix for something\n
Text Notes 7400 6950 0    197  Italic 39
Eastern Edge Robotics
Text Notes 10400 7520 0    79   ~ 16
Mark Belbin\n
Text Notes 8130 7635 0    39   Italic 8
Oct. 2018
$EndSCHEMATC
