Please follow the steps below to run this code:
1- Create and export meaningful EMI Scanner Rules (*.xml) and Tags (*.tgs) files from an existing SIwave project
2- In the terminal, enter the following command:
    python emi_scanner_in_batch_mode.py <SIwave or ECAD file> <EMI rules file with path> <EMI tags file with path>

Current supported ECAD files:
- Cadence (brd, mcm, sip)
- ODB++ (tgz or zip)
