from GENIutils import getConfigInfo, buildDictonary, printDictonaryContent

def main():
    # Grabbing configuration info from GENI config file
    rspec = getConfigInfo("Local Utilities", "RSPEC")
    GENIDict = buildDictonary(rspec)

    printDictonaryContent(GENIDict)

if __name__ == "__main__":
    main() # run main