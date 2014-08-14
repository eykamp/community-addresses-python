"""
    @author:
    @contact:
    @company: Esri
    @version: 1.0.0
    @description:
    @requirements: Python 2.7.x, ArcGIS 10.2.1
    @copyright: Esri, 2014
"""

from os.path import dirname, join, realpath
import arcpy
import ConfigParser

#C:\EsriApplications\Community Parcels\CommunityParcels\source\configs\test.ini

def write_config(names, vals, config, section):

    config.add_section(section)

    i = 0
    while i < len(names):
        if vals[i] == "#" or vals[i] == "":
            vals[i] = ''
        config.set(section, names[i], vals[i])
        i += 1

def main(config_file,                       ##0

         localaddresses = "",               ##1
         communityaddresseslocalcopy ="",   ##2
         CreateCurrent = True,              ##3
         localfips ="",                     ##4

         SiteAddressID = "",                ##5-x
         AddressPointID =  "",              ##6-x
         AddressNumberPrefix = "",          ##7-x
         AddressNumberSuffix = "",          ##8-x
         FullAddressNumber = "",            ##9-x
         AddressRange = "",                 ##10-x
         AddressUnitType = "",              ##11-x
         AddressUnitNumber = "",            ##12-x
         AlternateAddressUnitType = "",     ##13-x
         AlternateAddressUnitNumber = "",   ##14-x
         FullRoadName = "",                 ##15-x
         FullAddress = "",                  ##16-x
         PlaceName = "",                    ##17-x
         MunicipalityName = "",             ##18-x
         EmergencyServiceNumber = "",       ##19-x
         PublicSafetyAnsweringPoint = "",   ##20-x
         MSAGCommunity = "",                ##21-x
         USNGCoordinate = "",               ##22-x
         Description = "",                  ##23-x
         Location = "",                     ##24-x
         CaptureMethod = "",                ##25-x
         Status = "",                       ##26-x
         LocalFIPS = "",                    ##27-x

         *args):

    config = ConfigParser.RawConfigParser()
    arcpy.AddMessage('Configuration file created')

    # Add general parameters
    section = 'LOCAL_DATA'
    p_names = ['LOCALADDRESSES','COMMUNITYADDRESSESLOCALCOPY','CreateCurrent','localfips']
    p_vals  = [ localaddresses,  communityaddresseslocalcopy,   CreateCurrent , localfips ]

    arcpy.AddMessage('Writing general parameters...')
    write_config(p_names, p_vals, config, section)


    #Add general publication parameters
    section = 'FIELD_MAPPER'
    p_names = ['SiteAddressID','AddressPointID','AddressNumberPrefix','AddressNumberSuffix','FullAddressNumber', 'AddressRange', 'AddressUnitType', 'AddressUnitNumber', 'AlternateAddressUnitType', 'AlternateAddressUnitNumber', 'FullRoadName', 'FullAddress', 'PlaceName', 'MunicipalityName', 'EmergencyServiceNumber', 'PublicSafetyAnsweringPoint', 'MSAGCommunity', 'USNGCoordinate', 'Description', 'Location', 'CaptureMethod','Status', 'LocalFIPS' ]
    p_vals  = [ SiteAddressID , AddressPointID , AddressNumberPrefix , AddressNumberSuffix , FullAddressNumber ,  AddressRange ,  AddressUnitType ,  AddressUnitNumber ,  AlternateAddressUnitType ,  AlternateAddressUnitNumber ,  FullRoadName ,  FullAddress ,  PlaceName ,  MunicipalityName ,  EmergencyServiceNumber ,  PublicSafetyAnsweringPoint ,  MSAGCommunity ,  USNGCoordinate ,  Description ,  Location ,  CaptureMethod,  Status ,  LocalFIPS  ]

    arcpy.AddMessage('Writing general publication configuration parameters...')
    write_config(p_names, p_vals, config, section)


    # Save configuration to file
    cfgpath = dirname(realpath(__file__))
    cfgfile = join(cfgpath, "{}.ini".format(config_file))

    with open(cfgfile, "w") as cfg:
        arcpy.AddMessage('Saving configuration "{}"...'.format(cfgfile))
        config.write(cfg)

    arcpy.AddMessage('Done.')

if __name__ == '__main__':
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    main(*argv)
