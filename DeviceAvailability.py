#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:04:23 2017

Usage: Just run it. No arguments required.
       If the netCDF file with NC_NAME does not exists in NC_PATH, the script will search all data from BCO_START_DATE
       unti today and create a netCDF4 file with the results.
       If the file NC_NAME does already exists in NC_PATH, then the script will look if there are time steps to be
       appended to the file.

@author: Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)
"""
# ================Import==================
from datetime import date, timedelta
import numpy as np
import os
import glob
from netCDF4 import Dataset
import sys
import asyncio

# ===========Settings====================
BCO_START_DATE = date(2010, 1, 1)
# BCO_START_DATE = date(2017,1,1) #for testing
NC_NAME = 'Availability.nc'
NC_PATH = ""

Devices = []
days = 0

# Define Paths:
MBR2_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/16_Cloud_radar_MBR2/"
WindLidar_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/15_Wind_lidar/Proc/"
Allsky_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/1_Allskyimager/data/"
Ceilometer_path = "/data/mpi/mpiaes/obs/ACPC/Ceilometer/"
HATPRO_path = "/data/mpi/mpiaes/obs/ACPC/HATPRO/level0/"
KATRIN_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/5_Cloud_radar_KATRIN/data/"
KIT_path = "/data/mpi/mpiaes/obs/ACPC/KIT-WORA/Data/"
MRR_path1 = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/7_Rain_radar_MRR/DeeblesPoint_201004-201501/"
MRR_path2 = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/7_Rain_radar_MRR/DeeblesPoint_201502-today/"
WxSensor_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/12_Weathersensors/"
Radiation_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/14_Radiation/"
Disdro_path = "/pool/OBS/BARBADOS_CLOUD_OBSERVATORY/Level_0/17_Disdrometer/"
RamanLidar_path = "/data/mpi/mpiaes/obs/ACPC/RamanLidar-LICHT/HiRes/preProcessed/"  # TODO: Add the right Path


# ============Creating the "Device" Class==============
class Device:
    """
    Creating a Class for all devices for easy acces of the attributes:
        -name
        -varname (variable name which is used in the script)
        -avail (availability)
        -filepath
    """

    def __init__(self, varname, name, filepath):
        self.__name = name
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


# ========Set up Classes for each Device===================
Allsky = Device('Allsky', 'AllskyImager', Allsky_path)
Ceilometer = Device('Ceilometer', 'Ceilometer', Ceilometer_path)
HATPRO = Device('HATPRO', 'Microwave Radiometer HATPRO', HATPRO_path)
KIT = Device('KIT', 'Cloud Radar KIT', KIT_path)
KATRIN = Device('KATRIN', 'Cloud Radar KATRIN', KATRIN_path)
MBR2 = Device('MBR2', 'Cloud Radar MBR2', MBR2_path)
MRR = Device('MRR', 'Micro Rain Radar MRR', MRR_path2)
WindLidar = Device('WindLidar', 'Wind Lidar', WindLidar_path)
RamanLidar = Device('RamanLidar', 'Raman Lidar', RamanLidar_path)
WxSensor = Device('WxSensor', 'Weather Sensors', WxSensor_path)
Radiation = Device('Radiation', 'Radiation Sensors', Radiation_path)
Disdro = Device('Disdro', 'Disdrometer', Disdro_path)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


dates = []


async def get_availability(start_date, end_date):
    """
    :param start_date: datetime-obj
    :param end_date: datetime-obj

    Appending a 1 to the device availability of each class, if data was found on the actual date
    and a 0 if no data was found for the actual date.
    """
    days = 0
    for single_date in daterange(start_date, end_date):
        days += 1
        #    print(single_date.strftime("%Y-%m-%d"))
        date_str = single_date.strftime("%Y%m%d")
        day_str = single_date.strftime("%d")
        month_str = single_date.strftime("%m")
        year_str = single_date.strftime("%Y")
        dates.append(single_date)

        # Check for Allsky-imager:
        Allsky_file = glob.glob(Allsky_path + "cc" + year_str[2:4] + month_str + "/" + day_str + "/*" + year_str[
                                                                                                    2:4] + month_str + day_str + ".tgz")
        if len(Allsky_file) >= 1:
            Allsky._AvailabilityAppend(1)
        else:
            Allsky._AvailabilityAppend(0)

            # Check for Ceilometer:
        broken = False
        for folder in glob.glob(Ceilometer_path+"CH*"):
            Ceilo_file = glob.glob(folder+ "/" + year_str + "/" + month_str + "/" + "CH*" + day_str + ".dat")
            if len(Ceilo_file) >= 1:
                Ceilometer._AvailabilityAppend(1)
                broken = True
                break
        if not broken:
            Ceilometer._AvailabilityAppend(0)

            # Check for HATPRO:
        HATPRO_path_date = HATPRO_path + year_str[2:4] + month_str + "/" + date_str[2:]
        if os.path.isdir(HATPRO_path_date):
            HATPRO._AvailabilityAppend(1)
        else:
            HATPRO._AvailabilityAppend(0)

            # Check for KATRIN:
        KATRIN_file = glob.glob(KATRIN_path + date_str + "/" + date_str + "_*.*")
        if len(KATRIN_file) >= 1:
            KATRIN._AvailabilityAppend(1)
        else:
            KATRIN._AvailabilityAppend(0)

            # Check for KIT:
        KIT_file = KIT_path + date_str[2:]
        if os.path.isdir(KIT_file):
            # if len(KIT_file) >= 1:
            KIT._AvailabilityAppend(1)
        else:
            KIT._AvailabilityAppend(0)

            # Check for MBR2:
        if os.path.isdir(MBR2_path + date_str):
            MBR2._AvailabilityAppend(1)
        else:
            MBR2._AvailabilityAppend(0)

            # Check for MRR:
        MRR_file1 = glob.glob(MRR_path1 + year_str + month_str + "/" + month_str + day_str + ".*")
        MRR_file2 = glob.glob(MRR_path2 + year_str + month_str + "/" + month_str + day_str + ".*")
        if len(MRR_file1) >= 1:
            MRR._AvailabilityAppend(1)
        elif len(MRR_file2) >= 1:
            MRR._AvailabilityAppend(1)
        else:
            MRR._AvailabilityAppend(0)

            # Check for Windlidar:
        WindLidar_path_date = WindLidar_path + year_str + "/" + year_str + month_str + "/" + year_str + month_str + day_str
        if os.path.isdir(WindLidar_path_date):
            WindLidar._AvailabilityAppend(1)
        else:
            WindLidar._AvailabilityAppend(0)

            # Check for Weather Sensors:
        WxSensor_file = glob.glob(WxSensor_path + date_str[:-2] + "/*" + date_str + ".wxt")
        if len(WxSensor_file) >= 1:
            WxSensor._AvailabilityAppend(1)
        else:
            WxSensor._AvailabilityAppend(0)

            # Check for Radiation Sensors:
        Radiation_file = glob.glob(Radiation_path + date_str[:-2] + "/" + date_str + ".*")
        if len(Radiation_file) >= 1:
            Radiation._AvailabilityAppend(1)
        else:
            Radiation._AvailabilityAppend(0)

            # Check for Disdrometer:
        Disdro_file = glob.glob(Disdro_path + "*" + date_str + ".nc")
        if len(Disdro_file) >= 1:
            Disdro._AvailabilityAppend(1)
        else:
            Disdro._AvailabilityAppend(0)

            # Check for Raman Lidar:
        Raman_file = glob.glob(RamanLidar_path + "app" + year_str[2:4] + month_str + "/" + "app" + date_str[2:] + ".nc")
        if len(Raman_file) >= 1:
            RamanLidar._AvailabilityAppend(1)
        else:
            RamanLidar._AvailabilityAppend(0)


# =========Check if full scan is necessary=====================
NC_FILE = NC_PATH + NC_NAME
if not os.path.isfile(NC_FILE):
    print('No previous Data found. Scanning whole timerange.')
    start_date = BCO_START_DATE
    end_date = date.today() + timedelta(
        days=1)  # "+ timedelta(days=1)" is for today actually being included in the loop
else:
    nc_file = Dataset(NC_FILE, mode="r")
    nc_date_str = str(nc_file.variables['strftime'][-1])
    nc_year = int(nc_date_str[:4])
    nc_month = int(nc_date_str[4:6])
    nc_day = int(nc_date_str[6:8])
    start_date = date(nc_year, nc_month, nc_day) + timedelta(days=1)
    end_date = date.today() + timedelta(
        days=1)  # "+ timedelta(days=1)" is for today actually being included in the loop
    nc_file.close()
    if start_date >= end_date:
        print('The File is already up to date. Delete the file first to start a complete new scan.')
        sys.exit(0)
    print('Found netCDF-File %s - Just appending missing data.' % (NC_FILE))

# end_date = date(2012,1,1)

loop = asyncio.get_event_loop()  # for more information on this visit: https://docs.python.org/3/library/asyncio.html
ids = loop.run_until_complete(get_availability(start_date, end_date))  # much faster then just iterating over the
loop.close()


def create_netCDF(nc_name, path_name='', dates=dates):
    """

    :param nc_name: Name of the netCDF4 file
    :param path_name: Where the netCDF4 file will be written
    :param dates: datetime-obj

    This function creates a netCDF4 file.
    It just defines the structure and fills in the time values, not the actual values
    for the availability of each instrument.
    """
    from netCDF4 import Dataset
    import time
    import os
    import datetime
    import matplotlib.dates as mdate

    MISSING_VALUE = 999

    nc = Dataset(path_name + nc_name, mode='w', format='NETCDF4')

    numtime = []
    time_fill = []
    strftime = []
    for date_obj in dates:
        time_fill.append((date_obj - datetime.datetime(1970, 1, 1).date()).total_seconds())
        strftime.append((date_obj.strftime("%Y%m%d")))
        numtime.append(mdate.date2num(date_obj))

    numtime = np.asarray(numtime, dtype="f8")
    time_fill = np.asarray(time_fill, dtype="f8")
    strftime = np.asarray(strftime, dtype="S8")

    # Create global attributes
    nc.location = "The Barbados Cloud Observatory, Deebles Point, Barbados"
    nc.converted_by = "Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)"
    nc.institution = "Max Planck Institute for Meteorology, Hamburg"
    nc.created_with = os.path.basename(__file__) + " with its last modification on " + time.ctime(
        os.path.getmtime(os.path.realpath(__file__)))
    nc.creation_date = time.asctime()
    nc.version = "1.0.0"

    # Create dimensions
    time_dim = nc.createDimension('time', None)

    # Create variable
    time_var = nc.createVariable('time', 'f8', ('time',))
    time_var.units = "Seconds since 1970-1-1 0:00:00 UTC"
    time_var.CoordinateAxisType = "Time"
    time_var.calendar = "Standard"

    strftime_var = nc.createVariable('strftime', 'S8', ('time',))
    strftime_var.units = "YYYYMMDD"
    strftime_var.CoordinateAxisType = "Time"

    numtime_var = nc.createVariable('numtime', 'f8', ('time',))
    numtime_var.units = "Days since 0001-01-01 00:00:00 UTC, plus one"
    numtime_var.description = "This is Pythons matplotlib standard. Use matplotlib.dates.num2date() to get a datetime-object."
    numtime_var.CoordinateAxisType = "Time"
    time_var.calendar = "Gregorian"

    # Fill varaibles with values
    time_var[:] = time_fill[:]
    strftime_var[:] = strftime[:]
    numtime_var[:] = numtime[:]

    nc.close()


def appendToNetCDF(nc_name, path_name, Devices, dates=dates):
    """

    :param nc_name: Name of the netCDF4 file
    :param path_name: Path where the file will be written to
    :param Devices: List containing elements of the Device-class
    :param dates: datetime-obj

    This function appends data to an already existing netCDF4 file.
    It will append the time-variables as well as the data-variables.
    """
    from netCDF4 import Dataset
    import datetime
    import matplotlib.dates as mdate

    MISSING_VALUE = 999

    nc = Dataset(path_name + nc_name, mode='a', format='NETCDF4')

    numtime = []
    time_fill = []
    strftime = []
    for date_obj in dates:
        time_fill.append((date_obj - datetime.datetime(1970, 1, 1).date()).total_seconds())
        strftime.append((date_obj.strftime("%Y%m%d")))
        numtime.append(mdate.date2num(date_obj))

    numtime = np.asarray(numtime, dtype="f8")  # forcing the time-variables into these data-formats solves some issues
    time_fill = np.asarray(time_fill, dtype="f8")  # when reading them later.
    strftime = np.asarray(strftime, dtype="S8")

    nc_length_old = len(nc.variables['time'])
    nc_length_new = len(dates) + nc_length_old
    # print(nc_length_old,nc_length_new)
    for i, j in zip(range(nc_length_old, nc_length_new), range(len(time_fill))):
        nc.variables['time'][i] = time_fill[j]
        nc.variables['strftime'][i] = strftime[j]
        # print(i,j,nc.variables['strftime'][i])
        nc.variables['numtime'][i] = numtime[j]
        for Device in Devices:
            nc.variables[Device.varname()][i] = Device.avail()[j]

    nc.close()


def WriteAttrToNetCDF(nc_name, path_name, Device):
    """

    :param nc_name: Name of the netCDF4 file
    :param path_name: Path where the file will be written to
    :param Device: Device-class object

    This function writes the Data of the availability of one Instrument to the netCDF4 file.
    """
    from netCDF4 import Dataset

    MISSING_VALUE = 999
    nc = Dataset(path_name + nc_name, mode='a', format='NETCDF4')

    dev_var = nc.createVariable(Device.varname(), 'u1', ('time',))
    dev_var.long_name = Device.name()
    dev_var.description = "shows the Availability of the " + Device.name()

    dev_var[:] = Device.avail()[:]
    nc.close()


if not os.path.isfile(NC_FILE):  # Create netCDF-file if none exists
    create_netCDF(NC_NAME, NC_PATH)
    for Sensor in Devices:
        WriteAttrToNetCDF(NC_NAME, NC_PATH, Sensor)

else:  # if a netCDF-file already exists append the data
    appendToNetCDF(NC_NAME, NC_PATH, Devices)
