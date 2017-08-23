#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 11:04:45 2017

@author: m300517
"""

import numpy as np
from bokeh.io import curdoc, show
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, Range1d, DatetimeTickFormatter
from bokeh.models.widgets import Slider, TextInput, Dropdown, Select
from bokeh.layouts import gridplot, layout, column
from bokeh.plotting import figure
from netCDF4 import Dataset
import matplotlib.dates as mdate
from datetime import date, timedelta
from datetime import datetime as dt

#BCO_START_DATE = date(2010, 1, 1)
BCO_START_DATE = dt(2010,1,1)

#
# Set up data

NC_FILE = "C:/Users/darkl/Dropbox/MPI/Availability/Availability.nc"

nc = Dataset(NC_FILE, mode="r")

# numtime = nc.variables['numtime'][:].copy()
# time = []
# for time_obj in numtime:
#    time.append(mdate.num2date(time_obj))

ASCA = nc.variables['ASCA'][:].copy().astype(float)
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

Devices = [ASCA, Ceilometer, HATPRO, KIT, KATRIN, MBR2, MRR, WindLidar, RamanLidar, WxSensor, Radiation, Disdro]
Devices_names = ['ASCA', 'Ceilometer', 'HATPRO', 'KIT', 'KATRIN', 'MBR2', 'MRR', 'WindLidar', 'RamanLidar', 'WxSensor',
                 'Radiation', 'Disdro']

nc.close()

# %%
# Prepare data for plotting

#for i, s in enumerate(Devices):
#    Devices[i][Devices[i] == 0] = np.nan

colors = dict(
    ASCA='olive',
    Ceilometer='blue',
    HATPRO='red',
    KIT='green',
    KATRIN='yellow',
    MBR2='orange',
    MRR='lime',
    WindLidar='magenta',
    RamanLidar='sienna',
    WxSensor='olive',
    Radiation='crimson',
    Disdro='red'
)


#
# subset = data.ix['2010-10-06']
# x, y = subset.index.to_series(), subset['glucose']


# %%
# Make Dates (just temporary solution):
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = BCO_START_DATE
end_date = dt(2017, 8, 9)

def daterange2(start_date,days):
    for n in range(int(days)):
        yield start_date + timedelta(n)

dates = [x for x in daterange2(BCO_START_DATE,len(ASCA))]
dates = np.asarray(dates)



# %%
# Set up plot
years = end_date.year - start_date.year + 1
menu1 = ["last 365 days", "last 30 days", "Complete Timerange"] + ["%i" % (i + start_date.year) for i in range(years)]

select = Select(title="Select Timerange", value=("last 365 days"), options=menu1)
select.width = 200

xmax = dates[-1]
xmin = xmax - timedelta(365)
tool_box = "xbox_zoom,xpan,xwheel_zoom,undo,redo,reset,save"
p1 = figure(title=Devices_names[0], title_location='left', tools=tool_box, x_range=(xmin, xmax), y_range=(1, 2),
            responsive=True,x_axis_type='datetime')
p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 = [
    figure(title=Devices_names[i + 1], title_location='left', tools=tool_box, x_range=p1.x_range, y_range=p1.y_range)
    for i in range(len(Devices) - 1)]
p_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
#              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

p1.x_range.min_interval = 30
p1.x_range.max_interval = len(ASCA)

p1.line(dates,[0 for x in range(len(ASCA))])


for p, device, dev_name in zip(p_list, Devices, Devices_names):
    #    p.cross([x for x in daterange(start_date,end_date)],device,size=40, line_cap='butt', line_alpha=0.6, line_color=colors[dev_name], fill_color=colors[dev_name])
    p.name = dev_name
    p.yaxis.axis_label = dev_name
    p.yaxis.visible = False
    p.yaxis.axis_line_color = None
    p.yaxis.major_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_label_text_color = None
    p.vbar(dates[device == 1], 0.5, 3, line_color=colors[dev_name], fill_color=colors[dev_name], line_alpha=0.8,
           fill_alpha=0.8)
    #p.vbar(dates, 0.5, 3, line_color=colors[dev_name], fill_color=colors[dev_name], line_alpha=0.8,
     #      fill_alpha=0.8)
    p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
    p.xaxis.visible = True
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.outline_line_color = None
    p.xaxis.axis_line_color = None
    #    p.xaxis.se

    p.xaxis.major_tick_line_color = 'black'  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = 'black'  # turn off x-axis minor ticks

    p.plot_width = 1300
    p.plot_height = 100
    p.sizing_mode = "scale_width"

# plot_obj = column(p_list,responsive=True)

grid = gridplot([
    [x] for x in [select] + p_list]
)


# %%
# change window to selection:
def update_range(attrname, old, new):
    try:
        which = int(select.value) - BCO_START_DATE.year
        xmin = dt(1,1,which)
        xmax = dt(1,1,which+1)
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




# %%

select.on_change('value', update_range)
curdoc().add_root(grid)
curdoc().title = "Device Availability"
#show(grid)

