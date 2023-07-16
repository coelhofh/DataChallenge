# insert new row in table TbLoadControl for load status
import psycopg2
from configparser import ConfigParser

def config(filename='config.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def insertControlLog(filename):

    strInsControl = "INSERT INTO tripsdb.tbloadcontrol " \
                    "(nmfile, " \
                    "tsloadstart, " \
                    "tsloadfinish, " \
                    "nmloadstatus, " \
                    "tsloadupdate) " \
                    "VALUES('{}', CURRENT_TIMESTAMP, null, 'Processing', CURRENT_TIMESTAMP) RETURNING idloadcontrol".format(filename)

    try:
        dbConf = config()
        conn = psycopg2.connect(**dbConf)
        cur = conn.cursor()
        cur.execute(strInsControl)
        id = cur.fetchone()[0]
        print("load control table id: {}".format(id))
        conn.commit()
        conn.close
        return id

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# update Control Table based on Success or Failed processing
def updateControlLog(status, idloadcontrol, rows=0):

    strUpdControl = "update tripsdb.tbloadcontrol " \
                    "set tsloadfinish = CURRENT_TIMESTAMP," \
                    "nmloadstatus = '{0}'," \
                    "tsloadupdate = CURRENT_TIMESTAMP," \
                    "nbrowsload = {1} " \
                    "where idloadcontrol = {2} ".format(status, rows, idloadcontrol)

    try:
        dbConf = config()
        conn = psycopg2.connect(**dbConf)
        cur = conn.cursor()
        cur.execute(strUpdControl)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insertTbTrips(values, idloadcontrol):
    strSql = "INSERT INTO tripsdb.tbtrips " \
             "(nmregion, " \
             "vloriginlat, " \
             "vloriginlon, " \
             "vldestinationlat, " \
             "vldestinationlon, " \
             "tstrip, " \
             "nmdatasource, " \
             "nboriginclustering, " \
             "nbdestinationclustering, " \
             "idloadcontrol) " \
             "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,{0})".format(idloadcontrol)

    loadConfig = config("config.ini","loadparam")

    try:
        dbConf = config()
        conn = psycopg2.connect(**dbConf)
        cur = conn.cursor()
        totalRows = len(values)
        rowsCounter = 0

        print("Begining loading - commit size {}".format(loadConfig["commitsize"]))

        while values:
            chunk, values = values[:int(loadConfig["commitsize"])], values[int(loadConfig["commitsize"]):]
            cur.executemany(strSql, chunk)
            conn.commit()
            rowsCounter = rowsCounter + len(chunk)
            print("Partial insert ok. {0} rows inserted. Total until now: {1} ".format(len(chunk), rowsCounter))
            updateControlLog("Processing", idloadcontrol, rowsCounter)
            # time.sleep(10)
        return totalRows

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        updateControlLog("Error", idloadcontrol)
        if conn is not None:
            conn.close()
