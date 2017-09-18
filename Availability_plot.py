#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 11:04:45 2017
tested and working with bokeh-version 0.12.6

Usage: 1. Run DeviceAvailability.py to get the Availability.nc file.
       2. Run this code without parameters.
       3. Open the DeviceAvailability.html in your browser

Dependencies:
    - Availability.nc
    - button_callback.js
    - box_zoom.js
    - select_callback.js

This script creates an interactive Browser-application with bokeh to display the device availability on the
Barbados (BCO) site. It therefore needs the netCDF4 file created by the DeviceAvailability.py to work.

@author: Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)
"""

# ============Importing ================
import numpy as np
from bokeh.io import curdoc, show
from bokeh.models import Range1d, DatetimeTickFormatter, ColumnDataSource, CustomJS, Legend
from bokeh.models.widgets import Select, Button
from bokeh.layouts import gridplot, column, widgetbox, column, row, layout
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.events import ButtonClick, Tap, LODStart
from netCDF4 import Dataset
import matplotlib.dates as mdate
from datetime import timedelta
from datetime import datetime as dt
from functools import lru_cache
import os

# ==============Set up data================
NC_FILE = 'Availability.nc'
BCO_START_DATE = dt(2010, 1, 1)

# ===========read from netcdf==========================
nc = Dataset(NC_FILE, mode="r")
numtime = nc.variables['numtime'][:].copy()

# bring time-variable in right format for plotting:
time = []
for time_obj in numtime:
    # print(time_obj)
    time.append(mdate.num2date(time_obj))

start_date = BCO_START_DATE
end_date = dt.today()

dates = np.asarray(time)
for i in range(len(dates)):
    dates[i] = dt.replace(dates[i], tzinfo=None)

# read all other variables from netcdf-file:
height = 1.5 # height of the plotted vbars
Allsky = nc.variables['Allsky'][:].copy().astype(float) * height
Ceilometer = nc.variables['Ceilometer'][:].copy().astype(float) * height
HATPRO = nc.variables['HATPRO'][:].copy().astype(float) * height
KIT = nc.variables['KIT'][:].copy().astype(float) * height
KATRIN = nc.variables['KATRIN'][:].copy().astype(float) * height
MBR2 = nc.variables['MBR2'][:].copy().astype(float) * height
MRR = nc.variables['MRR'][:].copy().astype(float) * height
WindLidar = nc.variables['WindLidar'][:].copy().astype(float) * height
# RamanLidar = nc.variables['RamanLidar'][:].copy().astype(float)*height
WxSensor = nc.variables['WxSensor'][:].copy().astype(float) * height
Radiation = nc.variables['Radiation'][:].copy().astype(float) * height
Disdro = nc.variables['Disdro'][:].copy().astype(float) * height
EARLI = nc.variables['EARLI'][:].copy().astype(float) * height
LICHT = nc.variables['LICHT'][:].copy().astype(float) * height

# creating lists for easy acces within loops:
Devices = [Allsky, WxSensor, Radiation, Disdro, HATPRO, KIT, KATRIN, MBR2, MRR, Ceilometer, WindLidar, EARLI, LICHT]
Devices_names = ['Allsky', 'Weather', 'Radiation', 'Disdro', 'HATPRO', 'KIT', 'KATRIN', 'MBR2', 'MRR', 'Ceilometer',
                 'WindLidar', 'EARLI', 'LICHT']

nc.close()

# ============= Prepare data for plotting==================

colors = dict(
    Allsky='#FEB57E',
    Weather='#FD8F3A',
    Radiation='#CE5A02',
    Disdro='#9F4D0F',
    HATPRO='#653510',
    KIT='#7896E8',
    KATRIN='#396EFE',
    MBR2='#013EE4',
    MRR='#143AA3',
    Ceilometer='#B5E195',
    WindLidar='#82CD4C',
    # RamanLidar='#508A27',
    EARLI='#28500C',
    LICHT='#152907')

# creating a general data-source:
source = ColumnDataSource(
    data=dict(x=dates,
              Allsky=Allsky,
              Ceilometer=Ceilometer,
              HATPRO=HATPRO,
              KIT=KIT,
              KATRIN=KATRIN,
              MBR2=MBR2,
              MRR=MRR,
              WindLidar=WindLidar,
              # RamanLidar=RamanLidar,
              Weather=WxSensor,
              Radiation=Radiation,
              Disdro=Disdro,
              EARLI=EARLI,
              LICHT=LICHT))

# creating a data-source for the select-dropdown list:
last_date = np.asarray(mdate.num2epoch(mdate.date2num(dates[:])))
last_date_source = ColumnDataSource(data=dict(x=last_date))

# ================Set up plot=======================
years = end_date.year - start_date.year + 1  # Defines the complete timerange

xmax = dates[-1]
xmin = BCO_START_DATE

toolbox = "xbox_zoom,undo"  # which
p1 = figure(title=Devices_names[0], tools=toolbox, x_range=Range1d(start=xmin, end=xmax), y_range=(0.5, 1.5),
            responsive=True, x_axis_type='datetime')  # set up the first plot

p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13 = [
    figure(title=Devices_names[i + 1], tools=toolbox, x_range=p1.x_range, y_range=p1.y_range, responsive=True,
           x_axis_type='datetime')
    for i in range(len(Devices) - 1)]  # set up all other plots, sharing the x and y-axis with p1

p_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13]

p1.x_range.min_interval = timedelta(days=14)  # maximal allowed zoom-in
p1.x_range.max_interval = timedelta(days=len(dates))  # maximal allowed zoom-out

vbar_list = []
for p, device, dev_name in zip(p_list, Devices, Devices_names):  # Creating all the plots
    p.name = dev_name
    p.toolbar_location = "right"
    p.min_border_top = 20
    # p.min_border_bottom=50

    p.yaxis.axis_label_text_color = None
    p.yaxis.visible = True
    p.yaxis.axis_line_color = None
    p.yaxis.major_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_label_text_color = None
    p.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %b %y"],
        days=["%d %b %y"],
        months=["%b %y"],
        years=["%Y"])  # defines how the date is displayed at different zoom-in stages

    vbars = p.vbar(x="x", top=dev_name,
                   width=1, line_width=1,
                   line_color=colors[dev_name],
                   fill_color=colors[dev_name],
                   line_alpha=0.95,
                   fill_alpha=0.95,
                   source=source)
    vbar_list.append(vbars)

    p.xaxis.major_label_text_color = 'black'

    p.xaxis.visible = True
    p.xgrid.grid_line_color = 'black'
    p.xgrid.grid_line_alpha = 0.5
    p.ygrid.grid_line_color = 'black'
    p.ygrid.bounds = (0.955, 0.957)
    p.outline_line_color = None
    p.xaxis.axis_line_color = None

    p.xaxis.major_tick_line_color = 'black'
    p.xaxis.minor_tick_line_color = 'black'
    p.xaxis.major_tick_in = 30
    p.xaxis.major_tick_line_width = 2

    p.plot_width = 1300
    p.plot_height = 70
    p.sizing_mode = "scale_width"

    p.title.visible = False

# ============== Adding widgets: ===============================================================

menu1 = ["last 365 days", "last 30 days", "Complete Timerange"] + ["%i" % (i + start_date.year) for i in range(
    years)]  # Creates the entries for the select-dropdown-menu
select = Select(title="Select Timerange", value=("Complete Timerange"),options=menu1)  # create the select-dropdown-menu
select.width = 200

Buttons = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13] = [Button(
    name=dev_name,
    label=dev_name,
    button_type="success",
    width=150,
    height=0,
    callback=(
        CustomJS(code=open("button_callback.js").read()))) for dev_name in Devices_names]

grid1 = gridplot([[b, x] for b, x in zip(Buttons, p_list)])  # builds a grid from all plots and the select-menu

grid = column(select, grid1)

# change window to selection:
callback_select = CustomJS(args=dict(xr=p1.x_range, source=last_date_source,
                                     vbar0=vbar_list[0],
                                     vbar1=vbar_list[1],
                                     vbar2=vbar_list[2],
                                     vbar3=vbar_list[3],
                                     vbar4=vbar_list[4],
                                     vbar5=vbar_list[5],
                                     vbar6=vbar_list[6],
                                     vbar7=vbar_list[7],
                                     vbar8=vbar_list[8],
                                     vbar9=vbar_list[9],
                                     vbar10=vbar_list[10],
                                     vbar11=vbar_list[11],
                                     vbar12=vbar_list[12],
                                     ), code=open("select_callback.js").read())

select.js_on_change('value', callback_select)

# change vbar-width after zooming: #TODO: this part is not working yet due to the bokeh 0.12.6 version. maybe in a later version try to put this back in again
# p1.x_range.js_on_change('start',
#                         CustomJS(args=dict(xr=p1.x_range,
#                                      vbar0=vbar_list[0],
#                                      vbar1=vbar_list[1],
#                                      vbar2=vbar_list[2],
#                                      vbar3=vbar_list[3],
#                                      vbar4=vbar_list[4],
#                                      vbar5=vbar_list[5],
#                                      vbar6=vbar_list[6],
#                                      vbar7=vbar_list[7],
#                                      vbar8=vbar_list[8],
#                                      vbar9=vbar_list[9],
#                                      vbar10=vbar_list[10],
#                                      vbar11=vbar_list[11],
#                                      vbar12=vbar_list[12],),
#                  code=open("box_zoom.js").read()))

curdoc().add_root(grid)
curdoc().title = "Device Availability"
# show(grid) # can be used for debugging, but the select menu will not work then

# ================ Export to JS:=================================================

script, div = components(grid)
script = script[35:]  # removes the <script> tag at the beginning
script = script[:-9]  # removes the </script> tag at the end

# Replace the elementid in the script:
start_index = script.index("elementid") + 12

end_index = start_index
for c in script[start_index:]:
    if (c == ','):
        break
    else:
        end_index += 1
end_index -= 1
replace_me = script[start_index:end_index]
script = script.replace(replace_me, 'AvailabilityPlotElementID')
print(replace_me)

# write everything out as .js file:
with open("AvailabilitPlot.js", "w") as f:
    f.write("/*This code is generated by a python Script.")
    f.write("\nScript name: " + os.path.basename(__file__))
    f.write("\nLast modification: " + dt.today().strftime("%x"))
    f.write("\nAuthor: Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de) */\n")
    f.write(script)
    f.close()
