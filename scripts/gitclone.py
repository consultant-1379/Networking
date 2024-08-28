#!/usr/bin/python



__author__  = 'eeoiosu'
__version__ = 1.0
__date__    = '2018-12-04'



### Imports ###
import sys
import os
import re
import shutil
import logging
import logging.handlers
import time
import datetime



### Defaults ###
ALSO_LOG_TO_SCREEN      = True
PID_FILE                = "/tmp/" + os.path.basename(re.sub(r'.py$', '.pid', sys.argv[0]))
REPO_DIR                = "/opt/git/Networking"
ANSIBLE_DIR             = "/etc/ansible"
CURR_DATE_TIME          = datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')



### Logging ###
# Log Levels: [CRITICAL, ERROR, WARNING, INFO, DEBUG, UNSET]
LOGGING_LEVEL           = logging.DEBUG
LOG_FILENAME            = re.sub(r'.py$', '.log', sys.argv[0])
logger                  = logging.getLogger('RepositoryCloneLogger:' + str(os.getpid()))
formatter               = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s]:\t%(message)s')
handler                 = logging.handlers.RotatingFileHandler(LOG_FILENAME,maxBytes=200000,backupCount=5) # Keep 2Mb broken into 5 files
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(LOGGING_LEVEL)
if(ALSO_LOG_TO_SCREEN):
    stdout_logger = logging.StreamHandler(sys.stdout)
    stdout_logger.setLevel(LOGGING_LEVEL)
    stdout_logger.setFormatter(formatter)
    logger.addHandler(stdout_logger)



### Start ###
def start():
    logger.info("===========================================================================")
    logger.info("Starting Git Clone Script")
    logger.debug("DEBUG is ON")



### Check If Already Running ###
def checkIfAlreadyRunning():
    if(os.path.isfile(PID_FILE)):
        logger.debug("Pid file found: " + PID_FILE)
        if(os.system("pgrep -F " + PID_FILE) == 0):
            logger.debug("###########################################################################");
            logger.debug("##                 Script is already running. Must EXIT.                 ##");
            logger.debug("###########################################################################");
            exit()
        else:
            logger.debug("Script is not already running.")
            PIDFILE = open(PID_FILE, "w")
            PIDFILE.write(str(os.getpid()));
            PIDFILE.close()
    else:
        logger.debug("No pid file found.")
        PIDFILE = open(PID_FILE, "w")
        PIDFILE.write(str(os.getpid()));
        PIDFILE.close()



### Check if Repo already Exists ###
def checkForExistingRepo():
    logger.debug("Checking if Networking Repository already exists.")
    if(os.path.isdir(REPO_DIR)):
        logger.debug("Networking Repository exists. Deleting older Version.")
        shutil.rmtree(REPO_DIR)
        if(os.path.isdir(REPO_DIR)):
            logger.debug("###########################################################################");
            logger.debug("##       Networking Repository has not been deleted.Must EXIT.           ##");
            logger.debug("###########################################################################");
            exit()
        else:
            logger.debug("Networking Repository has been successfully removed.")
    else:
        logger.debug("Networking Repository does not currently exist.")



### Clone Repository from Gerrit ###
def cloneRepo():
    os.chdir("/opt/git")
    logger.debug("Starting Clone of latest Networking Repository.")
    os.system("ssh-agent bash -c 'ssh-add /home/emamulv/.ssh/id_rsa_root; git clone ssh://emamulv@gerrit.ericsson.se:29418/TestServices_Automation/Networking'")
    if(os.path.isdir(REPO_DIR)):
        logger.debug("Networking Repository has been successfully cloned.")
    else:
        logger.debug("###########################################################################");
        logger.debug("##   Networking Repository was unable to be been cloned.Must EXIT.       ##");
        logger.debug("###########################################################################");
        exit()



### Move Ansible Dir From Repo ###
def sortUsers():
    logger.debug("Preparing sort user specific files & information from Reop.")
    if(os.path.isdir(REPO_DIR + "/ansible")):
        logger.debug("Ansible directory present in Networking Repo, Continue.")
        if(os.path.isdir(REPO_DIR + "/ansible/ansible-user")):
            logger.debug("ansible-user directory exists, try move user files to specific destinations")
            for uname in os.listdir(REPO_DIR + "/ansible/ansible-user"):
                logger.debug("We have files for user: " + uname + ", will now check if user has account on this server.")
                if(os.path.isdir("/home/" + uname)):
                    if(os.path.isdir("/home/" + uname + "/ansible/")):
                        for file_name in os.listdir("/home/" + uname + "/ansible/"):
                            if(os.path.isdir("/home/" + uname + "/ansible/" + file_name)):
                                shutil.rmtree("/home/" + uname + "/ansible/" + file_name)
                            else:
                                os.remove("/home/" + uname + "/ansible/" + file_name)
                    logger.debug("Local account found for user: " + uname + ", will now move all the specific Repo content for this user.")
                    os.system("cp -a " + REPO_DIR + "/ansible/ansible-user/" + uname + "/. /home/" + uname + "/ansible")
                    os.system("chown -R " + uname + ":" + uname + " /home/" + uname + "/ansible/")
                else:
                    logger.debug("No local account found for user: " + uname + ", no further actions for this user.")
        else:
            logger.debug("ansible-user directory does not exist in the Repo, nothing to do for users")
    else:
        logger.debug("Ansible dir not present in Networking Repo, exiting script, Please Troubleshoot issue.")
        exit()



### Move Ansible Dir From Repo ###
def copyRepo():
    logger.debug("Preparing to move the ansible directory in the Networking Repo to the local /etc/ansible")
    if(os.path.isdir(REPO_DIR + "/ansible")):
        logger.debug("Ansible directory present in Networking Repo, Will now remove local ansible dir.")
        if(os.path.isdir(ANSIBLE_DIR)):
            #~# Remove the contents of Dir
            shutil.rmtree(ANSIBLE_DIR)
        if(not os.path.isdir(ANSIBLE_DIR)):
            #~# Check to ensure it is removed
            logger.debug("local ansible dir has been successfully removed")
        else:
            logger.debug("local ansible dir was not removed. Exiting script")
            exit()
        logger.debug("Moving Ansible dir from Networking Repo to /etc/ansible")
        shutil.move(REPO_DIR + "/ansible", "/etc/")
    else:
        logger.debug("Ansible dir not present in Networking Repo, exiting script, Please Troubleshoot issue.")
        exit()
    #~# Now check if move was successful
    if(os.path.isdir(ANSIBLE_DIR)):
        logger.debug("Ansible dir has been successfully moved from repo to local '/etc/ansible'.")
        ## Make Scripts in /etc/ansible/scripts executable ##
        for fname in os.listdir(ANSIBLE_DIR + "/scripts"):
            logger.debug("Making " + ANSIBLE_DIR + "/scripts/" + fname + " an executable script.")
            os.system("chmod +x " + ANSIBLE_DIR + "/scripts/" + fname)
    else:
        logger.debug("Ansible files have not been moved, Please Troubleshoot issue.")



### Move Ansible Dir From Repo ###
def cleanup():
    logger.debug("Cleaning up & delete Remaining Networking Repository.")
    shutil.rmtree(REPO_DIR)
    if(os.path.isdir(REPO_DIR)):
        logger.debug("#######################################################################");
        logger.debug("##       Networking Repository has not been deleted.Must EXIT.       ##");
        logger.debug("#######################################################################");
        exit()
    else:
        logger.debug("Networking Repository has been successfully removed.")


### Finish ###
def finish():
    logger.info("Finished Git Clone Script.")
    wrt = open("/etc/motd", "w")
    wrt.write('' + "\n")
    wrt.write('#################################################################' + "\n")
    wrt.write('## Ansible Directory last updated on : '+ CURR_DATE_TIME +'    ##' + "\n")
    wrt.write('## Do not modify any files in the "/etc/ansible" Directory,    ##' + "\n")
    wrt.write('## This Directory is overwritten by a Repository every hour.   ##' + "\n")
    wrt.write('#################################################################' + "\n")
    wrt.write('' + "\n")
    wrt.close()



### Procedure ###
start()
checkIfAlreadyRunning()
checkForExistingRepo()
cloneRepo()
sortUsers()
copyRepo()
cleanup()
finish()