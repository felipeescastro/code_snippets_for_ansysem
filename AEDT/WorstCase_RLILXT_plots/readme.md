This code will calculate the worst Insertion Losses (IL), Return Losses (RL) and Cross-talk (XT) and plot them on AEDT. 

Pre-requisites:
- This script needs pyAEDT v0.15.0 or newer

Inputs:
- input_file: str
  * Can be a full path to a solved 3D Layout project, a full path to a S-parameters (sNp or ts files) or an empty string ('') to use interactively on an opened and solved 3D layout design
- driver_preffix: str, optional
  * For example, a port on the driver is named "U1_DQ0", so one could use driver_preffix="U1"
- receiver_preffix: str, optional
  * For example, a port on the receiver is named "U7_DQ0", so one could use receiver_preffix="U7"

Steps to run the script:

1. Modify inputs (lines 1-3) on a text editor and save the file
2. Run it into AEDT via menu Automation > Run PyAEDT Script
