# DataChallenge

## First considerations
First I would like to say that the challenge was inspiring. Creating something from requirements and having the chance to create a solution freely, using creativity and experience is very good.

## Execution logic

The execution logic is as follows:
- List all files in the /venv/LoadFiles/ directory. All files in that directory will be processed sequentially in any order. Each file generates a different load batch identifier in TbLoadControl table.
- For each file in the directory will be done:
  - Reading the file and separating the data into different fields: file sequential id, region, origin latitude, origin longitude, destination latitude, destination longitude, time, datasource
  - The reading result will be passed through a data clustering logic to define the origin and destination regions of each trip.
  - With the clustering result the records will be inserted in the "Trips" table in batches of configurable size (more details bellow)

## Code
### main.py
Here you will only find the calling order for the logic explained above.

### config.ini
Parameters for database connection and size of commits according to the expected volumetry. This file must not be exposed to the end user.

### dbfunc.py
In this program we have all the functions of inserting and updating the database.

**def config(filename='config.ini', section='postgresql')**<BR>
Capture connection configuration and database commits.<BR>

**def insertControlLog(filename)**<BR>
* Input:<BR>
filename: name of the file being processed<BR><BR>
* Output:<BR>
id: control table identifier<BR><BR>

Insertion of the control record to monitor loads. It must receive the name of the file for insertion and will return the id of the load for later use in the inserts of the 'Trips' table.<BR><BR>

**def updateControlLog(status, idloadcontrol, rows=0)**<BR>
* Input:<BR>
status: processing status (Processing, Error or Success)<BR>
idloadcontrol: load control identifier provided by the above function<BR>
rows: number of rows loaded in case of a Success.<BR>
* Output:<BR>
None<BR><BR>

Update the control table based on input parameters.<BR>
Example: (status = Succes, idloadcontrol = 70, rows = 100200) would update the '70' id as a success, loading 100200 rows in the Trips table.<BR><BR>

**def insertTbTrips(values, idloadcontrol)**
* Input:<BR>
values: array with all values that must be inserted in the Trips table. Values must be in the same order as the Trips table field, except the autoincrement field and idloadcontrol.<BR>
idloadcontrol: load control identifier provided in the load start by function insertControlLog.<BR><BR>

* Output:<BR>
totalRows: total of rows loaded for the current file / idloadcontrol.<BR>

All rows are loaded with batches of 'n' rows - 'n' defined by config file commitsize variable.

### loadfile.py
**def inFile(filename):**
* Input:<BR>
filename: name of the file being processed<BR><BR>
* Output:<BR>
finalArr: array with all fields separated, specially the "Points" of Origin and Destination for use in de clustering function.<BR><BR>

It looks easier to load the csv with pandas dataframe but as the file doesn't have a key field I used this function to treat the data and also create a sequential key field for each rows. It is necessary to associate the regions after the clusterization.

### clustering.py
**def plotElbowCurve(XOri, XDes):**
* Input:<BR>
XOri: array of coordinates (latitude and longitude) of trip origins<BR>
XDes: array of coordinates (latitude and longitude) of trip destination <BR><BR>
* Output:<BR>
None <BR><BR>

This function plots the Elbow curve for the Origin and Destination data. It's not used in normal operation but it tells the number of clusters "needed" for clustering. In the given data number 3 was given, as saw in the Tests Evidences (files Elbow_Curve_Destination and Elbow_Curve_Origin)

**def RegionCluster(fileRows):**
* Input:<BR>
fileRows: array of the data given by the inFile(filename) function.<BR>
* Output:<BR>
dfFinal.iloc[: , 1:].values.tolist(): original input data plus the regions of origin and destination given the clustering algorithm. <BR><BR>

This function get the input data and calculate the region clustering for both Origin and Destination. This values will be used in the insert and for the reports.




