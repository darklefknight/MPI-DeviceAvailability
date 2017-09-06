#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 11:04:45 2017

Usage: in a terminal type:                                "bokeh serve Availability_plot,py"
       or if you want your browser to display the plot:   "bokeh serve --show Availability_plot.py"

This script creates an interactive Browser-application with bokeh to display the device availability on the
Barbados (BCO) site. It therefore needs the netCDF4 file created by the DeviceAvailability.py to work.

@author: Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)
"""

# ============Importing ================
import numpy as np
from bokeh.io import curdoc, show
from bokeh.models import Range1d, DatetimeTickFormatter, ColumnDataSource
from bokeh.models.widgets import Select, Button
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from netCDF4 import Dataset
import matplotlib.dates as mdate
from datetime import timedelta
from datetime import datetime as dt
from functools import lru_cache

# ==============Set up data================
NC_FILE = '/scratch/local1/m300517/DeviceAvailability/Availability.nc'  # Path to the netcdf4 file
BCO_START_DATE = dt(2010, 1, 1)

nc = Dataset(NC_FILE, mode="r")

numtime = nc.variables['numtime'][:].copy()
time = []
for time_obj in numtime:
    time.append(mdate.num2date(time_obj))

# ===========read from netcdf==========================
Allsky = nc.variables['Allsky'][:].copy().astype(float)
Ceilometer = nc.variables['Ceilometer'][:].copy().astype(float)
HATPRO = nc.variables['HATPRO'][:].copy().astype(float)
KIT = nc.variables['KIT'][:].copy().astype(float)
KATRIN = nc.variables['KATRIN'][:].copy().astype(float)
MBR2 = nc.variables['MBR2'][:].copy().astype(float)
MRR = nc.variables['MRR'][:].copy().astype(float)
WindLidar = nc.variables['WindLidar'][:].copy().astype(float)
RamanLidar = nc.variables['RamanLidar'][:].copy().astype(float)
WxSensor = nc.variables['WxSensor'][:].copy().astype(float)
Radiation = nc.variables['Radiation'][:].copy().astype(float)
Disdro = nc.variables['Disdro'][:].copy().astype(float)

Devices = [Allsky, Ceilometer, HATPRO, KIT, KATRIN, MBR2, MRR, WindLidar, RamanLidar, WxSensor, Radiation, Disdro]
Devices_names = ['Allsky', 'Ceilometer', 'HATPRO', 'KIT', 'KATRIN', 'MBR2', 'MRR', 'WindLidar', 'RamanLidar', 'Weather',
                 'Radiation', 'Disdro']

nc.close()


# ============= Prepare data for plotting==================

colors = dict(
    Allsky='olive',
    Ceilometer='blue',
    HATPRO='red',
    KIT='green',
    KATRIN='yellow',
    MBR2='orange',
    MRR='lime',
    WindLidar='magenta',
    RamanLidar='sienna',
    Weather='olive',
    Radiation='crimson',
    Disdro='red'
)

start_date = BCO_START_DATE
end_date = dt.today()

dates = np.asarray(time)
for i in range(len(dates)):
    dates[i] = dt.replace(dates[i], tzinfo=None)




source = ColumnDataSource(
    data=dict(x = dates,
              Allsky=Allsky,
              Ceilometer=Ceilometer,
              HATPRO=HATPRO,
              KIT=KIT,
              KATRIN=KATRIN,
              MBR2=MBR2,
              MRR=MRR,
              WindLidar=WindLidar,
              RamanLidar=RamanLidar,
              Weather=WxSensor,
              Radiation=Radiation,
              Disdro=Disdro))

# ================Set up plot=======================
years = end_date.year - start_date.year + 1  # Defines the complete timerange
menu1 = ["last 365 days", "last 30 days", "Complete Timerange"] + ["%i" % (i + start_date.year) for i in range(
    years)]  # Creates the entries for the select-dropdown-menu

select = Select(title="Select Timerange", value=("Complete Timerange"),
                options=menu1)  # create the select-dropdown-menu
select.width = 200

xmax = dates[-1]
xmin = BCO_START_DATE

toolbox = "xbox_select,xbox_zoom"
p1 = figure(title=Devices_names[0], tools=toolbox, x_range=Range1d(start=xmin, end=xmax), y_range=(0.5, 1.5),
            responsive=True, x_axis_type='datetime')  # set up the first plot

p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 = [
    figure(title=Devices_names[i + 1], tools=toolbox, x_range=p1.x_range, y_range=p1.y_range, responsive=True,
           x_axis_type='datetime')
    for i in range(len(Devices) - 1)]  # set up all other plots, sharing the x and y-axis with p1

p_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]

p1.x_range.min_interval = timedelta(days=7)  # maximal allowed zoom-in
p1.x_range.max_interval = timedelta(days=len(dates))  # maximal allowed zoom-out

for p, device, dev_name in zip(p_list, Devices, Devices_names):  # Creating all the plots
    p.name = dev_name
    p.toolbar_location = "right"

    p.yaxis.axis_label = dev_name
    p.yaxis.visible = True
    p.yaxis.axis_line_color = None
    p.yaxis.major_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_label_text_color = None
    p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %b %y"],
        days=["%d %b %y"],
        months=["%b %y"],
        years=["%Y"],
    )  # defines how the date is displayed at different zoom-in stages

    # vbars = p.vbar(dev_name, width=1, line_width=20, top=3, line_color='blue',  # colors[dev_name],
    #                fill_color='blue'  # colors[dev_name]
    #                , line_alpha=0.95,
    #                fill_alpha=0.95, source=source)

    circles = p.square(x="x",y=dev_name,source=source, size=20, color='blue', selection_color="orange", alpha=0.9,selection_alpha=0.9)

    p.xaxis.visible = True
    p.xgrid.grid_line_color = 'black'
    p.xgrid.grid_line_alpha = 1
    p.ygrid.grid_line_color = None
    p.outline_line_color = None
    p.xaxis.axis_line_color = None

    p.xaxis.major_tick_line_color = 'black'
    p.xaxis.minor_tick_line_color = 'black'
    p.xaxis.major_tick_in = 100

    p.plot_width = 1300
    p.plot_height = 75
    p.sizing_mode = "scale_width"

    p.title_location = 'left'
    p.title.visible = False

del p_list[8]  # TODO: add the right path for RamanLidar! This just excludes wrong Ramanlidar data from being plotted.

grid = gridplot([
    [x] for x in [select] + p_list]
)  # builds a grid from all plots and the select-menu


# change window to selection:
def update_range(attrname, old, new):
    '''
    Set up the x-range depending on the chosen entry from
    the select menu.
    '''
    try:
        which = int(select.value)
        xmin = dt(which, 1, 1)
        xmax = dt(which + 1, 1, 1)
        print(type(which), which)
    except:
        xmax = dates[-1]
        if 'last 365' in select.value:
            xmin = xmax - timedelta(365)
        elif 'last 30' in select.value:
            xmin = xmax - timedelta(30)
        elif 'Complete Timerange' in select.value:
            xmin = BCO_START_DATE
        else:
            xmin = 0

    p1.x_range.start = xmin
    p1.x_range.end = xmax


select.on_change('value', update_range)
curdoc().add_root(grid)
curdoc().title = "Device Availability"
# show(grid) # can be used for debugging, but the select menu will not work then
