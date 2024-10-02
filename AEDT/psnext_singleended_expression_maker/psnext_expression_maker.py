agressors_ports = [3,5,7,9]     # Examples: ['Port2','Port3'], ['1','2']
victim_port = 1

# ======================================================================
power_exp = "(pow(10, -dB(S({},{}))/10))"
final_exp = "-10*log10("
for ag_port in agressors_ports:
	final_exp += power_exp.format(ag_port,victim_port) + '+'
final_exp = final_exp[:-1] + ')'

oDesktop.AddMessage('','',0,'Please RMB click on this message and then click on "Copy messages to clipboard"')
oDesktop.AddMessage('','',0,final_exp)


