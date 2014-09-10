import subprocess
import shlex
import logging

from yihutils import rectifyList as rectifyList

def load(scmExe, strSandBox, strRepoWS):
    "scm load workspace to local sandbox"

    logging.info("--> enters load function")
    runCmd = []
    argList0 = "load --all -r jazz7 --force -d"
    runCmd.append(scmExe)
    runCmd.extend(shlex.split(argList0))
    runCmd.append(strSandBox)
    runCmd.append(strRepoWS)
    logging.debug("runCmd:")
    logging.debug(runCmd)

    runCmd = rectifyList(runCmd)
    logging.debug("\nafter rectification: runCmd:")
    logging.debug(runCmd)
    p = subprocess.Popen(runCmd, shell=True)
    p.wait()
    #stdout = open("stdout.txt","wb")
    #stderr = open("stderr.txt","wb")
    #returnCode = subprocess.call(runCmd, stdout=stdout, stderr=stderr, , shell=True)
    #logging.info("returnCode: " + returnCode)
    logging.info("<-- exits load function")
    return

def unload(scmExe, strSandBox, strRepoWS):
    "scm unload local sandbox"
    logging.info("--> enters unload function")
    print "entering unload function"
    runCmd = []
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
    logging.debug("\nafter rectification:\n", runCmd)
    p = subprocess.Popen(runCmd)
    p.wait()
    logging.info("<-- exits unload function")
    return
