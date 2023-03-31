from GENIutils import getConfigInfo, buildDictonary, orchestrateRemoteCommands
import sys
import re
from datetime import datetime

def get_failure_time(output):
    token = output.split("\n")
    last = ""
    for n in token:
        if re.search(r'eth\d+:\sLink',n):
            last = n

    token = last.split(" ")
    failure_time = token[0] +" "+ token[1]
    failure_timestamp = int(datetime.timestamp(datetime.strptime(failure_time,"%Y-%m-%d %H:%M:%S.%f")) * 1000)
    return failure_timestamp

def main():
    # Grabbing configuration info from GENI config file
    rspec = getConfigInfo("Local Utilities", "RSPEC")
    GENIDict = buildDictonary(rspec)
	
    if(len(sys.argv) != 4):
        print("invalid number of args")
        sys.exit(0)
	
	# Take in the arguments
    nodeName = sys.argv[1]
    intf = sys.argv[2]
    updown = sys.argv[3]
	
	# Build the command
    cmd = f'sudo ifconfig {intf} {updown}'
    bashCmd = "sudo bash ifupdown.sh"
	
	# Send the command over and run it on the remote node
    orchestrateRemoteCommands(nodeName, GENIDict, cmd)

    # Grab the timing information
    output = orchestrateRemoteCommands(nodeName, GENIDict, "sudo tail -n {0} /var/log/syslog".format(200),True)
    
    failure_timestamp = get_failure_time(output.decode())
    print(f"Failure timestamp: {failure_timestamp}")

    orchestrateRemoteCommands(nodeName, GENIDict, bashCmd)
    print("remote ifupdown.sh run")

if __name__ == "__main__":
    main() # run main