

#Load csv file to array for further using
#Not reading directly to pandas dataframe because we need a sequence number to track each line of the csv file
def inFile(filename):
    finalArr = []
    f = open(filename, "r")
    f.readline() ## dispose first line - header
    for idSeqFile,line in enumerate(f):
        arrLine = line.split(',')
        region = arrLine[0]
        oriCordLati = arrLine[1].replace("(","").replace(")","").split(" ")[1]
        oriCordLong = arrLine[1].replace("(","").replace(")","").split(" ")[2]
        desCordLati = arrLine[2].replace("(","").replace(")","").split(" ")[1]
        desCordLong = arrLine[2].replace("(","").replace(")","").split(" ")[2]
        dtTime = arrLine[3]
        dataSource = arrLine[4].replace("\n", "")
        finalArr.append([idSeqFile, region,oriCordLati, oriCordLong, desCordLati, desCordLong, dtTime, dataSource])

    print("File {0} read. {1} total rows.".format(filename, len(finalArr)))
    return finalArr
