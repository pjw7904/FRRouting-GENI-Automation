'''
Author: Peter Willis (pjw7904@rit.edu)
Last Updated: 10/04/2022
Desc: Upload a bash script and run it in a GNU Screen in the background.
'''
from GENIutils import getConfigInfo, buildDictonary, uploadToGENINode, orchestrateRemoteCommands
import ntpath

def executeScript(GENIDict=None):

    if(not GENIDict):
        GENIDict = buildDictonary(rspec)

    scriptLocation = getConfigInfo("Local Utilities", "scriptLocation")
    scriptType = getConfigInfo("Local Utilities", "scriptType")

    scriptName = ntpath.basename(scriptLocation)
    scriptDestination = getConfigInfo("GENI Credentials", "remoteCodeDirectory")

    # Config command to start a GNU screen and run through the script (MAKE SURE FILE IS LF NOT CRLF) 
    startCommand = "screen -dmS {scriptName} bash -c 'sudo {scriptType} {scriptName}; exec bash'".format(scriptName=scriptName, scriptType=scriptType)

    print("\n+---------Number of Nodes: {0}--------+".format(len(GENIDict)))
    for node in GENIDict:
        print(node)

        uploadToGENINode(node, GENIDict, scriptLocation, scriptDestination)
        print("\tScript uploaded")
        orchestrateRemoteCommands(node, GENIDict, startCommand, waitForResult=False)
        print("\tScript started")

if __name__ == "__main__":
    # Grabbing configuration info from GENI config file
    rspec = getConfigInfo("Local Utilities", "RSPEC")
    GENIDict = buildDictonary(rspec)
    executeScript(GENIDict=GENIDict)