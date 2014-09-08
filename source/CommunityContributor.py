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

logFileName ='.\\logs\\ParcelUpdate.log'
##configFilePath =  '.\\configs\\UpdateCommunityParcels.ini'
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
    LocalParcels = config.get('LOCAL_DATA', 'localaddresses')
    createCurrent = config.get('LOCAL_DATA', 'createcurrent')
    reportCurrentURL = config.get('FS_INFO', 'featureserviceurl')
    deleteSQL = config.get('FS_INFO', 'deletesql')
    localaddresses = config.get('LOCAL_DATA', 'localaddresses')
    communityaddresseslocalcopy = config.get('LOCAL_DATA', 'communityaddresseslocalcopy')
    localfips = config.get('LOCAL_DATA', 'localfips')
    SiteAddressID = config.get('FIELD_MAPPER', 'siteaddressid')
    AddressPointID =  config.get('FIELD_MAPPER', 'addresspointid')
    AddressNumberPrefix = config.get('FIELD_MAPPER', 'addressnumberprefix')
    AddressNumberSuffix = config.get('FIELD_MAPPER', 'addressnumbersuffix')
    FullAddressNumber = config.get('FIELD_MAPPER', 'fulladdressnumber')
    AddressRange = config.get('FIELD_MAPPER', 'addressrange')
    AddressUnitType = config.get('FIELD_MAPPER', 'addressunittype')
    AddressUnitNumber = config.get('FIELD_MAPPER', 'addressunitnumber')
    AlternateAddressUnitType = config.get('FIELD_MAPPER', 'alternateaddressunittype')
    AlternateAddressUnitNumber = config.get('FIELD_MAPPER', 'alternateaddressunitnumber')
    FullRoadName = config.get('FIELD_MAPPER', 'fullroadname')
    FullAddress = config.get('FIELD_MAPPER', 'fulladdress')
    PlaceName = config.get('FIELD_MAPPER', 'placename')
    MunicipalityName = config.get('FIELD_MAPPER', 'municipalityname')
    EmergencyServiceNumber = config.get('FIELD_MAPPER', 'emergencyservicenumber')
    PublicSafetyAnsweringPoint = config.get('FIELD_MAPPER', 'publicsafetyansweringpoint')
    MSAGCommunity = config.get('FIELD_MAPPER', 'msagcommunity')
    USNGCoordinate = config.get('FIELD_MAPPER', 'usngcoordinate')
    Description = config.get('FIELD_MAPPER', 'description')
    Location = config.get('FIELD_MAPPER', 'siteaddressid')
    CaptureMethod = config.get('FIELD_MAPPER', 'capturemethod')
    Status = config.get('FIELD_MAPPER', 'status')

    print "Loading Configuration File"
    arcpy.AddMessage("Loading Configuration File")


    if arcpy.Exists(localaddresses) == False:
        print "Please specify a input address feature class (localaddresses=) in the configuration file, exiting"
        arcpy.AddMessage("Please specify a input parcel layer in the configuration file, exiting")
        sys.exit()


    if communityaddresseslocalcopy == "":
        print "Please specify a input community address layer (communityaddresslocalcopy=) in the configuration file, exiting"
        arcpy.AddMessage("Please specify a input community address layer in the configuration file, exiting")
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


    # Update Current service if used - see the services helper in the arcrest folder


    if createCurrent == "True":
        fs.url = reportCurrentURL


    # Delete existing dataset that matches the community parcel schema
        arcpy.management.TruncateTable(communityaddresseslocalcopy)
        print "Cleaning up local address data"


    # Append new parcels into the community parcels schema, field map your data into the community schema.  Add local data field names after the "#" in the list.
    # For example, for STATEAREA "STATEAREA" true true false 50 Text 0 0 ,First,#,LocalParcels,TotalAcres,-1,-1;  The local Parcels field name from STATEDAREA (community parcels schema) is TotalAcres.


        common_vars = "true true false 250 Text 0 0, First, #"

        if SiteAddressID == "":
            new_field = """SITEADDID 'Site Address ID' true true false 20 Text 0 0, First, #"""

        else:
            new_field = """SITEADDID 'Site Address ID' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, SiteAddressID)
        field_map = "{}".format(new_field)


        if AddressPointID =="":
            new_field = """ADDPTKEY 'Address Point ID' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """ADDPTKEY 'Address Point ID' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, AddressPointID)

        field_map = "{}; {}".format(field_map, new_field)


        if AddressNumberPrefix =="":
            new_field = """PREADDRNUM 'Address Number Prefix' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """PREADDRNUM 'Address Number Prefix' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, AddressNumberPrefix)

        field_map = "{}; {}".format(field_map, new_field)


        if AddressNumberSuffix =="":
            new_field = """ADDRNUMSUF  'Address Number Suffix' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """ADDRNUMSUF  'Address Number Suffix' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, AddressNumberSuffix)

        field_map = "{}; {}".format(field_map, new_field)


        if FullAddressNumber =="":
            new_field = """ADDRNUM  'Full Address Number' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """ADDRNUM  'Full Address Number' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, FullAddressNumber)

        field_map = "{}; {}".format(field_map, new_field)


        if AddressRange =="":
            new_field = """ADDRRANGE 'Address Range' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """ADDRRANGE 'Address Range' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, AddressRange)

        field_map = "{}; {}".format(field_map, new_field)

        if AddressUnitType =="":
            new_field = """UNITTYPE 'Address Unit Type' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """UNITTYPE 'Address Unit Type' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, AddressUnitType)

        field_map = "{}; {}".format(field_map, new_field)


        if AddressUnitNumber =="":
            new_field = """UNITID 'Address Unit Number' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """UNITID 'Address Unit Number' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, AddressUnitNumber)

        field_map = "{}; {}".format(field_map, new_field)


        if AlternateAddressUnitType =="":
            new_field = """ALTUNITTYPE 'Alternate Address Unit Type' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """ALTUNITTYPE 'Alternate Address Unit Type' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, AlternateAddressUnitType)

        field_map = "{}; {}".format(field_map, new_field)


        if AlternateAddressUnitNumber =="":
            new_field = """ALTUNITID 'Alternate Address Unit Number' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """ALTUNITID 'Alternate Address Unit Number' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, AlternateAddressUnitNumber)

        field_map = "{}; {}".format(field_map, new_field)


        if FullRoadName =="":
            new_field = """FULLNAME 'Full Road Name' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """FULLNAME 'Full Road Name' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, FullRoadName)

        field_map = "{}; {}".format(field_map, new_field)


        if FullAddress =="":
            new_field = """FULLADDR 'Full Address' true true false 250 Text 0 0, First, #"""

        else:
            new_field = """FULLADDR 'Full Address' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, FullAddress)

        field_map = "{}; {}".format(field_map, new_field)


        if PlaceName =="":
            new_field = """PLACENAME 'Place Name' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """PLACENAME 'Place Name' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, PlaceName)

        field_map = "{}; {}".format(field_map, new_field)

        if MunicipalityName =="":
            new_field = """MUNICIPALITY  'Municipality Name' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """MUNICIPALITY  'Municipality Name' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, MunicipalityName)

        field_map = "{}; {}".format(field_map, new_field)


        if EmergencyServiceNumber =="":
            new_field = """ESN 'Emergency Service Number' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """ESN 'Emergency Service Number' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, EmergencyServiceNumber)

        field_map = "{}; {}".format(field_map, new_field)


        if PublicSafetyAnsweringPoint =="":
            new_field = """PSAP 'Public Safety Answering Point' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """PSAP 'Public Safety Answering Point' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, PublicSafetyAnsweringPoint)

        field_map = "{}; {}".format(field_map, new_field)


        if MSAGCommunity =="":
            new_field = """MSAG 'MSAG Community' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """MSAG 'MSAG Community' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, MSAGCommunity)

        field_map = "{}; {}".format(field_map, new_field)


        if USNGCoordinate =="":
            new_field = """USNGCOORD 'USNG Coordinate' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """USNGCOORD 'USNG Coordinate' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, USNGCoordinate)

        field_map = "{}; {}".format(field_map, new_field)


        if Description =="":
            new_field = """ADDRCLASS 'Description' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """ADDRCLASS 'Description' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, Description)

        field_map = "{}; {}".format(field_map, new_field)


        if Location =="":
            new_field = """POINTTYPE 'Location' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """POINTTYPE 'Location' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, Location)

        field_map = "{}; {}".format(field_map, new_field)

        if  CaptureMethod =="":
            new_field = """CAPTUREMETH 'Capture Method' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """CAPTUREMETH 'Capture Method' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, CaptureMethod)

        field_map = "{}; {}".format(field_map, new_field)


        if Status =="":
            new_field = """STATUS 'Status' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """STATUS 'Status' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, Status)

        field_map = "{}; {}".format(field_map, new_field)


        if localfips =="":
            new_field = """localfips 'Local FIPS code' true true false 50 Text 0 0, First, #"""

        else:
            new_field = """localfips 'Local FIPS code' {}, {}, {}, -1, -1""".format(common_vars, localaddresses, localfips)

        field_map = "{}; {}".format(field_map, new_field)


        arcpy.Append_management(localaddresses, communityaddresseslocalcopy, "NO_TEST", field_map)

        print "Mapping Local Address data to Community Address Schema"
        print "Community Address Update to ArcGIS Online Started, please be patient"
        arcpy.AddMessage("Mapping Local Address data to Community Address Schema")
        arcpy.AddMessage("Community Address Update to ArcGIS Online Started, please be patient")


        # Calculate the Last Update field
        arcpy.CalculateField_management(communityaddresseslocalcopy, "LASTUPDATE", "time.strftime(\"%m/%d/%Y\")", "PYTHON", "")
        print "Calculating Last Update"
        arcpy.AddMessage("Calculating Last Update")

        #Calculate Last Editor Field
        calc0 = '"{0}"'.format(localfips)
        arcpy.CalculateField_management(communityaddresseslocalcopy, "LASTEDITOR", calc0)
        print "Calculating Last Editor"
        arcpy.AddMessage("Calculating Last Editor")


        # Calculate the LOCALFIPS to the County/City Name
        calc = '"{0}"'.format(localfips)
        arcpy.CalculateField_management(communityaddresseslocalcopy, "localfips", calc, "VB", "")
        print "Set FIPS Code information"
        arcpy.AddMessage("Calculating 'FIPS' Code Information")

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
        arcpy.AddMessage("Community Address upload started, please be patient.  For future consideration, please run tool during non-peak internet usage")
        fs.addFeatures(communityaddresseslocalcopy)


if __name__ == '__main__':
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    main(*argv)


