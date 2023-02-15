'''
Author: Peter Willis (pjw7904@rit.edu)
Last Updated: 10/04/2022
Desc: Running 
'''

from GENIutils import getConfigInfo, buildDictonary, orchestrateRemoteCommands
import sys

def main():
    # Grabbing configuration info from GENI config file
    rspec = getConfigInfo("Local Utilities", "RSPEC")
    GENIDict = buildDictonary(rspec)

    notDone = True
    allCmds = []

    resultOutput = False
    if(len(sys.argv) > 1):
        resultOutput = True

    print("Enter the word done to finish")
    while notDone:
        cmd = input("Enter a valid bash command: ")
        if cmd != "done":
            allCmds.append(cmd)
        else:
            notDone = False

    allCmds = allCmds.pop() if len(allCmds) == 1 else allCmds

    print("\n+---------Number of Nodes: {0}--------+".format(len(GENIDict)))
    for node in GENIDict:
        print(node)
        result = orchestrateRemoteCommands(node, GENIDict, allCmds, getOutput=resultOutput)
        if(resultOutput):
            print(result)

if __name__ == "__main__":
    main() # run main