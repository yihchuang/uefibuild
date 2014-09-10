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
    p = subprocess.Popen(runCmd)
    p.wait()
    returnCode = p.returncode
    logging.debug("Popen.returncode: " + str(returnCode))
    if returnCode == 0 :
        logging.info("load function completed successfully.")
    else:
        raise ValueError("load function failed to complete.")    
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
    logging.debug("strRepoWS: " + strRepoWS)
    #print strRepoWS.startswith("\"")
    if strRepoWS.startswith("\"") == False:
        strRepoWS = '"' + strRepoWS + '"'
        logging.debug("strRepoWS[2]: " + strRepoWS)

    runCmd.append(strRepoWS)
    print runCmd

    runCmd = rectifyList(runCmd)
    logging.debug("\nafter rectification runCmd:")
    logging.debug(runCmd)
    p = subprocess.Popen(runCmd)
    p.wait()
    returnCode = p.returncode
    logging.debug("Popen.returncode: " + str(returnCode))

    if returnCode == 0 :
        logging.info("unload function completed successfully.")
    else:
        raise ValueError("unload function failed to complete.")    
    logging.info("<-- exits unload function")
    return
