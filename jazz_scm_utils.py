import subprocess, shlex, logging

from yihutils import rectifyList as rectifyList

def scmLoad(scmExe, SandBox, strRepoWS):
    "scm load workspace to local sandbox"

    logging.info("--> enters scmLoad function")
    runCmd = []
    argList0 = "load --all -r jazz7 --force -d"
    runCmd.append(scmExe)
    runCmd.extend(shlex.split(argList0))
    runCmd.append(SandBox)
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
        logging.info("scmLoad function completed successfully.")
    else:
        raise ValueError("scmLoad function failed to complete.")    
    logging.info("<-- exits scmLoad function")
    return

def scmUnload(scmExe, SandBox, strRepoWS):
    "scm unload local sandbox"
    logging.info("--> enters scmUnload function")
    print "entering scmUnload function"
    runCmd = []
    argList0 = "unload --overwrite-uncommitted -r jazz7 -d"

    runCmd.append(scmExe)
    runCmd.extend(shlex.split(argList0))
    runCmd.append(SandBox)
    runCmd.append("-w")

    logging.debug("strRepoWS: " + strRepoWS)
    # Need to make sure enclosed by double quote
    #print strRepoWS.startswith("\"")
    #if strRepoWS.startswith("\"") == False:
    #    strRepoWS = '"' + strRepoWS + '"'
    #    logging.debug("strRepoWS[2]: " + strRepoWS)

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
        logging.info("scmUnload function completed successfully.")
    else:
        raise ValueError("scmUnload function failed to complete.")    
    logging.info("<-- exits scmUnload function")
    return
