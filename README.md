# FRRouting-GENI-Automation
A collection of scripts to help in the installation, configuration, and testing of routing protocols included in FRRouting on the GENI testbed. This assumes that the image installed on the GENI nodes is Ubuntu/Debian-based. 

## Directories
1. local_scripts = scripts that are run on your local machine and reach out to the remote GENI nodes via SSH (Paramiko library).

2. remote_scripts = scripts that are uploaded and run on the remote node directly. No SSH connection is required once the script has been uploaded (with a script from local_scripts). GNU Screen or another command is used to push the script to the background.