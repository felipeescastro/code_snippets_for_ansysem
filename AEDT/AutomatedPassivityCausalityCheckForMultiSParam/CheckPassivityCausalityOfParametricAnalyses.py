SParamFolder = r"D:\Scripts\3DLayout\causal_pass_ck\project\ParametricSetup1"
AnsysEMPath = r"c:\Program Files\AnsysEM\v241\Win64"        # Use "" to use one of the AnsysEM versions installed in your machine

# ================================================================================================

import os
import re
import subprocess
import sys
import logging

logging.basicConfig(filename=os.path.join(SParamFolder,'Passivity and Causality Check.log'),
                    encoding='utf-8',
                    filemode='w',
                    level=logging.DEBUG, format='%(message)s')

def Msg(message):
    if "oDesktop" in globals():
        oDesktop.AddMessage('','',0,message)
        logging.warning(message)
    else:
        print(message)
        logging.warning(message)

if AnsysEMPath == "":
    if "oDesktop" in globals():
        AnsysEMPath = oDesktop.GetExeDir()
    else:
        installedAnsysEM = [envvar for envvar in os.environ if 'ANSYSEM_ROOT' in envvar]
        if installedAnsysEM == []:
            logging.error('No valid version of Ansys EM installed. No checks will be done.')
            sys.exit('ERROR: No valid version of Ansys EM installed. No checks will be done.')
        else:
            AnsysEMPath = os.environ[installedAnsysEM[0]]
Msg('Ansys EM path: '+AnsysEMPath)

if not os.path.exists(SParamFolder):
    logging.error(SParamFolder+' doesn NOT exist! Please check path and try again.')
    sys.exit('ERROR: '+SParamFolder+' doesn NOT exist! Please check path and try again.')
if not os.listdir(SParamFolder):
    logging.error(SParamFolder+' is empty! No checks will be done.')
    sys.exit('ERROR: '+SParamFolder+' is empty! No checks will be done.')

pat_snp = re.compile('\.s\d+p$')
sNpFiles={f:os.path.join(SParamFolder,f) for f in os.listdir(SParamFolder) if re.search(pat_snp, f)}
pat_ts = re.compile('\.ts$')
for f in os.listdir(SParamFolder):
    if re.search(pat_ts, f):
        sNpFiles[f] = os.path.join(SParamFolder,f)
if sNpFiles == {}:
    logging.error(SParamFolder+' has no sNp file! No checks will be done.')
    sys.exit('ERROR: '+SParamFolder+' has no sNp file! No checks will be done.')


for snpf in sNpFiles:
    if os.name == 'nt':
        genequiv_path = os.path.join(AnsysEMPath,"genequiv.exe")
    else:
        genequiv_path = os.path.join(AnsysEMPath,"genequiv")
        
    cmd = [genequiv_path,
           "-checkpassivity",
           "-checkcausality",
           sNpFiles[snpf]
           ]
    Msg('Running checks on '+ snpf + '. This can take a while depending on file size...')
    Msg(' ---- Results for '+ snpf + ' : ----- ')
    output_str=str(subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0])
    output_lst=output_str.split('\\r\\n')
    if len(output_lst)==1:
        output_lst=output_str.splitlines()
    pass_flag = False
    caus_flag = False
    for line in output_lst:
        if "Checking passivity" in line:
            pass_flag = True
        if "Input data" in line and pass_flag:
            Msg(line[17:])
        if "Checking causality" in line:
            caus_flag = True
        if "Maximum causality" in line and caus_flag:
            Msg(line[17:])
        if "Causality check is" in line and caus_flag:
            Msg(line[17:])
          
Msg('All messages saved under "'+os.path.join(SParamFolder,'Passivity and Causality Check.log')+'"')
