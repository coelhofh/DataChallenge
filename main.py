# This is a sample Python script.
import os
import dbfunc
import loadfile
import clustering

# main function
def main():
    loadDir = "venv/LoadFiles/"
    lstFiles = os.listdir(loadDir)

    for file in lstFiles:
        print("\n*************************\nStart file ingestion: {}\n*************************\n".format(loadDir + file))
        idloadcontrol = dbfunc.insertControlLog(loadDir + file)
        arrTrips = clustering.RegionCluster(loadfile.inFile(loadDir + file))
        nbRows = dbfunc.insertTbTrips(arrTrips, idloadcontrol)
        dbfunc.updateControlLog("Success", idloadcontrol, nbRows)
        print("\n*************************\nFile {} successfully loaded!\n*************************\n".format(file))

    print("*************************\n ALL FILES LOADED SUCCESSFULLY.\n*************************")

if __name__ == "__main__":
    main()



