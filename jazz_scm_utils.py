import subprocess
import shlex
import ConfigParser

from yihutils import rectifyList as rectifyList

def load(scmExe, strSandBox, strRepoWS):
	"scm load workspace to local sandbox"
	
	print "entering load function"
	runCmd = []
	##scm=r"C:\RTC-Client-Win-4.0.5\jazz\scmtools\eclipse\scm.exe"
	argList0 = "load --all -r jazz7 --force -d"
	runCmd.append(scmExe.decode('string_escape'))
	runCmd.extend(shlex.split(argList0))
	runCmd.append(strSandBox)
	runCmd.append(strRepoWS)
	print runCmd

	runCmd = rectifyList(runCmd)
	print "\nafter rectification:\n", runCmd

	p = subprocess.Popen(runCmd)
	p.wait()
	return

def unload(scmExe, strSandBox, strRepoWS):
	"scm unload local sandbox"
	print "entering unload function"
	runCmd = []
	##scm=r"C:\RTC-Client-Win-4.0.5\jazz\scmtools\eclipse\scm.exe"
	argList0 = "unload --overwrite-uncommitted -r jazz7 -d"
	
	runCmd.append(scmExe.decode('string_escape'))
	runCmd.extend(shlex.split(argList0))
	runCmd.append(strSandBox)
	runCmd.append("-w")

	# Need to make sure enclosed by double quote
	print "strRepoWS: " + strRepoWS
	print strRepoWS.startswith("\"")
	if strRepoWS.startswith("\"") == False:
		strRepoWS = '"' + strRepoWS + '"'
	print "strRepoWS[2]: " + strRepoWS

	runCmd.append(strRepoWS)
	print runCmd

	runCmd = rectifyList(runCmd)
	print "\nafter rectification:\n", runCmd
	p = subprocess.Popen(runCmd)
	p.wait()
	return
