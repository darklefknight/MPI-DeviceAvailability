#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:04:23 2017

@author: m300517
"""

from datetime import date, timedelta

import numpy as np
import os 
import matplotlib.pyplot as plt
import glob
from netCDF4 import Dataset
import sys

BCO_START_DATE = date(2010,1,1)
#BCO_START_DATE = date(2016,1,1) # for testing
NC_NAME = 'Availability.nc'
NC_PATH = ''

Devices = []
days = 0

#%%

class Device:
    """
    Creating a Class for all devices for easy acces of the attributes:
        name
        availability
        launch date
        termination date
    """
    
    def __init__(self,varname,name, filepath):
        self.__name=name
        self.__filepath = filepath
        self.__varname = varname
        self.__availability = []                
        Devices.append(self)
        
    def _AvailabilityAppend(self, availability=None):
        self.__availability.append(availability)
            
    def name(self):
        return self.__name
    
    def avail(self):
        return self.__availability
    
    def filepath(self):
        return self.__filepath
    
    def varname(self):
        return self.__varname
            
#%%    
#Define Paths:
MBR2_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/16_Cloud_radar_MBR2/"
WindLidar_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/15_Wind_lidar/Proc/"
ASCA_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/1_Allskyimager/data/"
Ceilometer_path = "/data/mpi/mpiaes/obs/ACPC/Ceilometer/Level_1/"
HATPRO_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/4_Microwave_radiometer_HATPRO/"
KATRIN_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/5_Cloud_radar_KATRIN/data/"
KIT_path = "/data/mpi/mpiaes/obs/ACPC/KIT-WORA/Data/"
MRR_path1 = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/7_Rain_radar_MRR/DeeblesPoint_201004-201501/"
MRR_path2 = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/7_Rain_radar_MRR/DeeblesPoint_201502-today/"
WxSensor_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/12_Weathersensors/"
Radiation_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/14_Radiation/"
Disdro_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/17_Disdrometer/"
RamanLidar_path = "/data/mpi/mpiaes/obs/ACPC/RamanLidar-LICHT/HiRes/preProcessed/"

#%%
#Set up Classes for each Device
ASCA = Device('ASCA','AllskyImager',ASCA_path)    
Ceilometer = Device('Ceilometer','Ceilometer',Ceilometer_path)
HATPRO = Device('HATPRO','Microwave Radiometer HATPRO',HATPRO_path)
KIT = Device('KIT','Cloud Radar KIT',KIT_path)
KATRIN = Device('KATRIN','Cloud Radar KATRIN',KATRIN_path)
MBR2 = Device('MBR2','Cloud Radar MBR2',MBR2_path)        
MRR = Device('MRR','Micro Rain Radar MRR',MRR_path2)
WindLidar = Device('WindLidar','Wind Lidar', WindLidar_path)
RamanLidar = Device('RamanLidar','Raman Lidar', RamanLidar_path)
#Radio_airport
#Radio_BCO
WxSensor = Device('WxSensor','Weather Sensors',WxSensor_path)
Radiation = Device('Radiation','Radiation Sensors', Radiation_path)
Disdro = Device('Disdro','Disdrometer',Disdro_path)

#%%


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
#%%
#Check if full scan is necessary
NC_FILE = NC_PATH + NC_NAME
if not os.path.isfile(NC_FILE):
    print('No previous Data found. Scanning whole timerange.')
    start_date = BCO_START_DATE
    end_date = date.today()+timedelta(days=1) # "+ timedelta(days=1)" is for today actually being included in the loop
else:
    nc_file = Dataset(NC_FILE, mode="r")
    nc_date_str= str(nc_file.variables['strftime'][-1])
    nc_year = int(nc_date_str[:4])
    nc_month = int(nc_date_str[4:6])
    nc_day = int(nc_date_str[6:8])
    start_date = date(nc_year,nc_month,nc_day) + timedelta(days=1)
    end_date = date.today()+timedelta(days=1) # "+ timedelta(days=1)" is for today actually being included in the loop
    nc_file.close()
    if start_date >= end_date:
        print('The File is already up to date. Delete the file first to start a complete new scan.')
        sys.exit()
    print('Found netCDF-File %s - Just appending missing data.' %(NC_FILE))
    
#end_date = date(2017,1,1) #for testing
# end_date = date(2010,2,1) #for testing

#%%
dates = []

for single_date in daterange(start_date, end_date):
    days +=1
#    print(single_date.strftime("%Y-%m-%d"))
    date_str = single_date.strftime("%Y%m%d")
    day_str  = single_date.strftime("%d")
    month_str  = single_date.strftime("%m")
    year_str  = single_date.strftime("%Y")
    dates.append(single_date)
    
    #Check for Allsky-imager:
    ASCA_file= glob.glob(ASCA_path + "cc" + year_str[2:4] + month_str + "/" + day_str + "/*" + year_str[2:4] + month_str + day_str + ".tgz")
    if len(ASCA_file) >= 1:
        ASCA._AvailabilityAppend(1)
    else:
        ASCA._AvailabilityAppend(0)        

    #Check for Ceilometer:
    Ceilo_file= glob.glob(Ceilometer_path + "*" +year_str + month_str + ".nc.bz2")
    if len(Ceilo_file) >= 1:
        Ceilometer._AvailabilityAppend(1)
    else:
        Ceilometer._AvailabilityAppend(0)  
        
    #Check for HATPRO:
    HATPRO_path_date = HATPRO_path + year_str[2:4] + month_str + "/" + year_str[2:4] + month_str + day_str
    if os.path.isdir(HATPRO_path_date):
        HATPRO._AvailabilityAppend(1)   
    else:
        HATPRO._AvailabilityAppend(0)  
        
    #Check for KATRIN:
    KATRIN_file= glob.glob(KATRIN_path + date_str + "/" + date_str + "_*.*")
    if len(KATRIN_file) >= 1:
        KATRIN._AvailabilityAppend(1)  
    else:
        KATRIN._AvailabilityAppend(0)  
        
    #Check for KIT:
    KIT_file= glob.glob(KIT_path + date_str[2:] + "/" + year_str[:2] + "_*")
    if len(KIT_file) >= 1:
        KIT._AvailabilityAppend(1)     
    else:
        KIT._AvailabilityAppend(0)  

    #Check for MBR2:
    if os.path.isdir(MBR2_path + date_str):
        MBR2._AvailabilityAppend(1)
    else:
        MBR2._AvailabilityAppend(0)  
        
    #Check for MRR:
    MRR_file1= glob.glob(MRR_path1 + year_str + month_str + "/" + month_str + day_str + ".*" )
    MRR_file2= glob.glob(MRR_path2 + year_str + month_str + "/" + month_str + day_str + ".*" )    
    if len(MRR_file1) >= 1:
        MRR._AvailabilityAppend(1)     
    elif len(MRR_file2) >= 1:
        MRR._AvailabilityAppend(1) 
    else:
        MRR._AvailabilityAppend(0)  
        
    #Check for Windlidar:
    WindLidar_path_date = WindLidar_path + year_str + "/" + year_str + month_str + "/" + year_str + month_str + day_str
    if os.path.isdir(WindLidar_path_date):
        WindLidar._AvailabilityAppend(1)
    else:
        WindLidar._AvailabilityAppend(0)  
        
    #Check for Weather Sensors:
    WxSensor_file= glob.glob(WxSensor_path + date_str[:-2] + "/*" + date_str + ".wxt")
    if len(WxSensor_file) >= 1:
        WxSensor._AvailabilityAppend(1)  
    else:
        WxSensor._AvailabilityAppend(0)  
        
    #Check for Radiation Sensors:
    Radiation_file= glob.glob(Radiation_path + date_str[:-2] + "/" + date_str + ".*")
    if len(Radiation_file) >= 1:
        Radiation._AvailabilityAppend(1)  
    else:
        Radiation._AvailabilityAppend(0)  
        
    #Check for Disdrometer:
    Disdro_file= glob.glob(Disdro_path + "*" + date_str + ".nc")
    if len(Disdro_file) >= 1:
        Disdro._AvailabilityAppend(1)   
    else:
        Disdro._AvailabilityAppend(0)  
    
    #Check for Raman Lidar:
    Raman_file= glob.glob(RamanLidar_path + "app" + year_str[2:4] + month_str + "/" + "app" + date_str[2:] + ".nc")
    if len(Raman_file) >= 1:
        RamanLidar._AvailabilityAppend(1)    
    else:
        RamanLidar._AvailabilityAppend(0)  

#%%

def create_netCDF(nc_name,path_name='',dates=dates):
    from netCDF4 import Dataset
    import time    
    import os
    import datetime
    import matplotlib.dates as mdate
    
    MISSING_VALUE = 999
    
    nc = Dataset(path_name+nc_name,mode='w',format='NETCDF4')

    numtime = []    
    time_fill = []
    strftime = []
    for date_obj in dates:
        time_fill.append((date_obj-datetime.datetime(1970,1,1).date()).total_seconds())
        strftime.append((date_obj.strftime("%Y%m%d")))
        numtime.append(mdate.date2num(date_obj))

    numtime = np.asarray(numtime,dtype="f8")
    time_fill = np.asarray(time_fill, dtype="f8")
    strftime = np.asarray(strftime,dtype="S8")

        
    
    #Create global attributes
    nc.location		= "The Barbados Cloud Observatory, Deebles Point, Barbados"
    nc.converted_by	= "Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)"
    nc.institution	= "Max Planck Institute for Meteorology, Hamburg"
    nc.created_with	= os.path.basename(__file__)+" with its last modification on "+ time.ctime(os.path.getmtime(os.path.realpath(__file__)))
    nc.creation_date	= time.asctime()
    nc.version		="1.0.0"
    
    #Create dimensions
    time_dim 	  = nc.createDimension('time', None)
    
    #Create variable
    time_var 					          = nc.createVariable('time','f8',('time',))
    time_var.units                   = "Seconds since 1970-1-1 0:00:00 UTC"
    time_var.CoordinateAxisType      = "Time"
    time_var.calendar 			      = "Standard"
    
    strftime_var                     = nc.createVariable('strftime','S8',('time',))
    strftime_var.units               = "YYYYMMDD"
    strftime_var.CoordinateAxisType  = "Time"    
    
    numtime_var                      = nc.createVariable('numtime','f8',('time',))
    numtime_var.units                = "Days since 0001-01-01 00:00:00 UTC, plus one" 
    numtime_var.description          = "This is Pythons matplotlib standard. Use matplotlib.dates.num2date() to get a datetime-object."    
    numtime_var.CoordinateAxisType   = "Time"    
    time_var.calendar 			     = "Gregorian"

    time_var[:]     = time_fill[:]
    strftime_var[:] = strftime[:]
    numtime_var[:]  = numtime[:]
     
    #Close netCDF-file
    nc.close()  
#%%     
    
def appendToNetCDF(nc_name,path_name,Devices,dates=dates):
    from netCDF4 import Dataset
    import time    
    import os
    import datetime
    import matplotlib.dates as mdate
    
    MISSING_VALUE = 999
    
    nc = Dataset(path_name+nc_name,mode='a',format='NETCDF4')

    numtime = []    
    time_fill = []
    strftime = []
    for date_obj in dates:
        time_fill.append((date_obj-datetime.datetime(1970,1,1).date()).total_seconds())
        strftime.append((date_obj.strftime("%Y%m%d")))
        numtime.append(mdate.date2num(date_obj))

    numtime = np.asarray(numtime,dtype="f8")
    time_fill = np.asarray(time_fill, dtype="f8")
    strftime = np.asarray(strftime,dtype="S8")
    
    nc_length_old = len(nc.variables['time']) 
    nc_length_new = len(dates) + nc_length_old
    print(nc_length_old,nc_length_new)
    for i,j in zip(range(nc_length_old,nc_length_new),range(len(time_fill))):
        nc.variables['time'][i]     = time_fill[j]
        nc.variables['strftime'][i] = strftime[j]
        # print(i,j,nc.variables['strftime'][i])
        nc.variables['numtime'][i] = numtime[j]
        for Device in Devices:
            nc.variables[Device.varname()][i] = Device.avail()[j]
     
    #Close netCDF-file
    nc.close()  

#%%
def WriteAttrToNetCDF(nc_name,path_name,Device):
    from netCDF4 import Dataset
    
    MISSING_VALUE = 999
    nc = Dataset(path_name+nc_name,mode='a',format='NETCDF4')
    
    dev_var                = nc.createVariable(Device.varname(),'u1',('time',))
    dev_var.long_name      = Device.name()
    dev_var.description    = "shows the Availability of the " + Device.name()
    
    dev_var[:] = Device.avail()[:]
    nc.close()
    
#%%
def AppendAttrToNetCDF(nc_name,path_name,Device):
    from netCDF4 import Dataset
    
    nc = Dataset(path_name+nc_name,mode='a',format='NETCDF4')
    
    nc_length_old = len(nc.variables[Device.varname()])
    nc_length_new = len(Device.avail()) + nc_length_old
    for i,j in zip(range(nc_length_old,nc_length_new),range(len(Device.avail()))):
        nc.variables[Device.varname()][i] = Device.avail()[j]
    
    nc.close()
    
#%%
if not os.path.isfile(NC_FILE):  #Create netCDF-file if none exists
    create_netCDF(NC_NAME,NC_PATH)        
    for Sensor in Devices:
        WriteAttrToNetCDF(NC_NAME,NC_PATH,Sensor)
    
else:               #if a netCDF-file already exists append the data
    appendToNetCDF(NC_NAME,NC_PATH,Devices)




        
