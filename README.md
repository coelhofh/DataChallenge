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

## Data Model
Only 2 tables were created for this challenge.<br>
I would create a fact-dimension model but does not seems necessary. Making a fact-dimension is made necessary in case of report use - Power Bi for example - which handles better this type of modeling. In this case fields like region doesn't have any id's to load in a dimension table and there is no guarantee it would be equals in all loads, which can lead to a huge dimension if a sequential identifier is created using the "char" content. 
SQL script in the /venv/SQLScripts/ folder.

**Table tbtrips**
* idtrips - Sequential id
* nmregion - Region name
* vloriginlat - Origin latitude
* vloriginlon - Origin longitude
* vldestinationlat - Destination Latitude
* vldestinationlon - Destination Longitude
* tstrip - Trip timestamp
* nmdatasource - Data source name
* nboriginclustering - Origin clustering number
* nbdestinationclustering - Destination clustering number
* idloadcontrol - Loading identifier (foreign key)

Consideration: idloadcontrol is present here in case of a load error. As the commit's are done in batch if a loading failed and any rows are committed is possible to delete the load manually ou automatically.

**Table tbloadcontrol**
* idloadcontrol - Load sequential id
* nmfile - Sile loaded
* tsloadstart - Start date time (local time)
* tsloadfinish - Finish date time (local time). Null if not finished.
* nmloadstatus - Load status - Processing, Error ou Success
* tsloadupdate - Date time the rows was update, for status on load.
* nbrowsloaded - Number of rows loaded. If Status = "Processing" it gives the partial commits. If Success gives the full rows loaded. Error always gives 0.

With this is possible to get a status of each processing. Evidence of this in de TestEvidence folder.

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

## Mandatory features
* There must be an automated process to ingest and store the data.
  Process is automated as seen on the /venv/TestEvidence/ - Console_output.pdf and Db_load*.jpg files.
  
* Trips with similar origin, destination, and time of day should be grouped together.
  Sql script "groupedTrips.sql" is bringing this information with region clustering.
  
* Develop a way to obtain the weekly average number of trips for an area, defined by a bounding box (given by coordinates) or by a region.
  Sql script "weekAverage.sql" brings this information but not with bounding boxes. The logic would be use the min and max coordinates for each cluster region and get the 4 points of the rectangle and draw the bouding box.

* Develop a way to inform the user about the status of the data ingestion without using a polling solution.
  Table TbLoadControl give the load status as seen on the /venv/TestEvidence/ files - Db_load*.jpg 
  
* The solution should be scalable to 100 million entries. It is encouraged to simplify the data by a data model. Please add proof that the solution is scalable.
  Test make with 1.2M rows took 6 minutes to complete in my personal notebook (/venv/TestEvidence/ files - Db_load_finish.jpg - idloadcontrol - 79). As commits are a load parameters it's scalable to me. TbTrips table could be partitioned for better select performance.

* Use a SQL database
  Postgresql database was used in this solution. Last release postgresql-15.3-3.

## Bonus features
* Sketch up how you would set up the application using any cloud provider
  This solution could run in any cloud provider with a single VM and a database connection if the proper configuration is done (firewall and file access).
  Files could be in a storage account in any provider and a, Data factory for example, trigger can catch a new file and turn on the VM and start the program, turning of the machine after that.

* Include a .sql file with queries to answer these questions:
  **From the two most commonly appearing regions, which is the latest datasource?**
  Sql script "commonregions.sql" is bringing this information with region clustering.

  **What regions has the "cheap_mobile" datasource appeared in?**
  Sql script "cheap_mobile.sql" is bringing this information with region clustering.




