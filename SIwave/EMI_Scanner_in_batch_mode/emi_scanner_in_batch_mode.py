# inputFile = r"D:\prep\Galileo_G87173_204.brd"
# EMIRulesFile = r"D:/prep/emi_rules.xml"
# EMITagsFile = r"D:/prep/emi_tags.tgs"        

# ================================================================================================
# Inputs needed:
#     - ECAD file (brd, odb++, edb, etc) or siwave file (siw)
#     - EMI rules file (xml)
#     - EMI tags file (tgs)

# Steps:
#     1- Check input, if ECAD:
#         Run anstranslator and siwave_ng to save siw
#        Elsif siw:
#         Move forward
#        Else error!
#     2- Create exec file on the fly with rules and tags files
#     3- Run EMI scanner with siwave_ng and save output in string
#     4- Check if analysis succeded and open browser with html report
# ================================================================================================

import os
import re
import subprocess
import sys
import shutil
import datetime

inputFile = sys.argv[1]
EMIRulesFile = sys.argv[2]
EMITagsFile = sys.argv[3]

ECAD_dict = {
    '.brd'  :   'extracta',
    '.mcm'  :   'extracta',
    '.sip'  :   'extracta',
    '.tgz'  :   'odb',
    '.zip'  :   'odb'
    }

def Msg(message,msglvl=0):
    if "oDesktop" in globals():
        oDesktop.AddMessage('','',msglvl,message)
    elif 'oDoc' in globals():
        if msglvl == 0:
            oDoc.ScrAddInfo(message)
            oDoc.ScrLogMessage('INFO: '+message)
        elif msglvl == 1:
            oDoc.ScrAddWarning(message)
            oDoc.ScrLogMessage('WARNING: '+message)
        elif msglvl == 2:
            oDoc.ScrAddError(message)
            oDoc.ScrLogMessage('ERROR: '+message)
        else:
            oDoc.ScrLogMessage(message)
    else:
        print(message)
        
def ECAD2Siw(ECADType):
    tmpEdb = inputFile.replace(ECADType,'.aedb')
    cmd = [anstranslator_path,
           inputFile,
           tmpEdb,
           "-i="+ECAD_dict[ECADType],
           "-o=edb"
           ]
    Msg('Converting ECAD to EDB...')
    output_str=str(subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0])
    Msg('Done.')
    tmpExec = inputFile.replace(ECADType,'.exec')
    print("SaveSiw "+inputFile.replace(ECADType,'.siw'), file=open(tmpExec, 'w'))
    cmd_siw = [siwave_ng_path,
               tmpEdb,
               tmpExec,
        	   "-formatOutput",
        	   "-useSubdir"
               ]
    Msg('Converting ECAD to SIwave...')
    output_str_siw=str(subprocess.Popen(cmd_siw,stdout=subprocess.PIPE).communicate()[0])
    os.remove(tmpExec)
    shutil.rmtree(tmpEdb)
    Msg('Done.')
    return (True, inputFile.replace(ECADType,'.siw'))
    
    
if "oDesktop" in globals():
    AnsysEMPath = oDesktop.GetExeDir()
else:
    installedAnsysEM = [envvar for envvar in os.environ if 'ANSYSEM_ROOT' in envvar]
    if installedAnsysEM == []:
        sys.exit('ERROR: No valid version of Ansys EM installed. No checks will be done.')
    else:
        AnsysEMPath = os.environ[installedAnsysEM[3]]
Msg('Ansys EM path: '+AnsysEMPath)
Msg('Input File: '+inputFile)
Msg('EMI Rules File: '+EMIRulesFile)
Msg('EMI Tags File: '+EMITagsFile)


if os.name == 'nt':
    anstranslator_path = os.path.join(AnsysEMPath,"anstranslator.exe")
    siwave_ng_path = os.path.join(AnsysEMPath,"siwave_ng.exe")
else:
    anstranslator_path = os.path.join(AnsysEMPath,"anstranslator")
    siwave_ng_path = os.path.join(AnsysEMPath,"siwave_ng")

goodInput = False
_, inputExt = os.path.splitext(inputFile)
if inputExt == '.siw':
    goodInput = True
    inputSIW = inputFile
else:
    goodInput, inputSIW = ECAD2Siw(inputExt)

tmpExec = inputFile.replace(inputExt,'.exec')
with open(tmpExec,'w') as fo:
    fo.write('ExecEmiScanSim\n')
    fo.write('SetEmiScanSimName EMI_Scanner_'+datetime.datetime.now().strftime('%y%m%d_%H%M%S')+'\n')
    fo.write('EmiScanTagsFile "{}"\n'.format(EMITagsFile))
    fo.write('EmiScanRulesFile "{}"\n'.format(EMIRulesFile))
cmd = [siwave_ng_path,
	   inputSIW,
	   tmpExec,
	   "-formatOutput",
	   "-useSubdir",
	   ]
Msg('Running EMI Scanner...')
output_str=str(subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0])

if "Ansys EMI Scanner COMPLETE" in output_str:
	pat = re.compile('For HTML output, see ===>(.*?)\s+For ASCII output')
	html_path = re.findall(pat,output_str)[0]
	html_path = html_path.replace(' \\r\\n','').replace('\\\\index','index')
	subprocess.call('start '+html_path,shell=True)
	Msg('HTML report opened on your internet browser')
