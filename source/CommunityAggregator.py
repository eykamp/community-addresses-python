"""
    @author:
    @contact:
    @company: Esri
    @version: 1.0.0
    @description:
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014

"""
import arcpy
import sys, os, datetime
import ConfigParser
from os.path import dirname, join, exists, splitext, isfile

from arcpy import env
from arcrest.agol import layer

logFileName ='.\\logs\\AddressUpdate.log'
##configFilePath =  '.\\configs\\UpdateCommunityAddresses.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def main(config_file, *args):

    # Set overwrite output option to True
    arcpy.env.overwriteOutput = True

    if isfile(config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)

    else:
        print "INI file not found."
        sys.exit()

# Config File

    username = config.get( 'AGOL', 'user')
    password = config.get('AGOL', 'pass')
    localaddresses = config.get('LOCAL_DATA', 'localaddresses')
    CommunityAddressLocalCopy = config.get('LOCAL_DATA', 'communityaddresseslocalcopy')
    createCurrent = config.get('LOCAL_DATA', 'createcurrent')
    reportCurrentURL = config.get('FS_INFO', 'featureserviceurl')
    deleteSQL = config.get('FS_INFO', 'deletesql')
    countycityname = config.get ('LOCAL_DATA','localfips')


    print "Loading Configuration File"
    arcpy.AddMessage("Loading Configuration File")



    if CommunityAddressLocalCopy == "":
        print "Please specify a input community parcel layer (CommunityParcelsLocalCopy=) in the configuration file, exiting"
        arcpy.AddMessage("Please specify a input parcel layer in the configuration file, exiting")
        sys.exit()


    if username == "":
        print "Please specify a ArcGIS Online Username (username =)in the configuration file, exiting"
        arcpy.AddMessage(username)
        sys.exit()


    if password == "":
        print "Please specify a ArcGIS Online password (password =)in the configuration file, exiting"
        arcpy.AddMessage(password)
        sys.exit()


    if deleteSQL == "":
        print "Please specify a SQL query (DELETESQL= LOCALFIPS ='jurisdiction') in the configuration file, exiting"
        arcpy.AddMessage("Please specify a SQL query (DELETESQL= LOCALFIPS ='jurisdiction') in the configuration file, exiting")
        sys.exit()


    fs = layer.FeatureLayer(url=reportCurrentURL,username=username,password=password)
    if fs == None:
        print "Cannot find or connect to service, make sure service is accessible"
        arcpy.AddMessage("Cannot find or connect to service, make sure service is accessible")
        sys.exit()


    # Update Current service if used - see the ArcREST folder in the application directory

    arcpy.management.TruncateTable(localaddresses)
    print "Cleaning up local parcel data"
    arcpy.AddMessage("Cleaning up local parcels")

    if createCurrent == "True":
        fs.url = reportCurrentURL

        arcpy.Append_management(CommunityAddressLocalCopy, localaddresses, "TEST")
        print "Mapping Local Parcel data to Community Address Schema"
        arcpy.AddMessage("Mapping Local Parcel data to Community Address Schema")


        print "Truncating Addresses from Feature Service"
        arcpy.AddMessage("Truncating Addresses from Feature Service")
        print "Community Address update started, please be patient"
        arcpy.AddMessage("Community Address update started, please be patient")

        try:
                value1 = fs.query(where=deleteSQL, returnIDsOnly=True)
                myids=value1 ['objectIds']


                minId = min(myids)
                i = 0
                maxId = max(myids)


                print minId
                print maxId
                chunkSize = 500


                while (i <= len(myids)):
                    #print myids[i:i+1000]
                    oids = ",".join(str(e) for e in myids[i:i+chunkSize])
                    print oids
                    if oids == '':
                        continue
                    else:
                        fs.deleteFeatures(objectIds=oids)
                    i+=chunkSize
                    print i
                    print "Completed: {0:.0f}%".format( i/ float(len(myids))*100)
                    arcpy.AddMessage("Deleted: {0:.0f}%".format ( i/ float(len(myids))*100))


        except:
            pass


        print "Community Address upload Started"
        arcpy.AddMessage("Community Address upload started, please be patient. For future consideration, please run tool during non-peak internet usage")

        fs.addFeatures(localaddresses)


if __name__ == '__main__':
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    main(*argv)
