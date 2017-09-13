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
from bokeh.models import Range1d, DatetimeTickFormatter, ColumnDataSource, CustomJS, Legend
from bokeh.models.widgets import Select, Button
from bokeh.layouts import gridplot, column, widgetbox, column, row, layout
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.events import ButtonClick, Tap
from netCDF4 import Dataset
import matplotlib.dates as mdate
from datetime import timedelta
from datetime import datetime as dt
from functools import lru_cache
import os

# ==============Set up data================
# NC_FILE = '/scratch/local1/m300517/DeviceAvailability/Availability.nc'  # Path to the netcdf4 file
NC_FILE = 'C:/Users/darkl/PycharmProjects/MPI-DeviceAvailability/Availability.nc'
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

last_date = np.asarray(mdate.num2epoch(mdate.date2num(dates[:])))
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
              RamanLidar=RamanLidar,
              Weather=WxSensor,
              Radiation=Radiation,
              Disdro=Disdro))

last_date_source = ColumnDataSource(
    data=dict(
        # x = str(mdate.num2epoch(mdate.date2num(dates[-4:])))
        x=last_date
    )
)

# ================Set up plot=======================
years = end_date.year - start_date.year + 1  # Defines the complete timerange
menu1 = ["last 365 days", "last 30 days", "Complete Timerange"] + ["%i" % (i + start_date.year) for i in range(
    years)]  # Creates the entries for the select-dropdown-menu

select = Select(title="Select Timerange", value=("Complete Timerange"),
                options=menu1)  # create the select-dropdown-menu
select.width = 200

xmax = dates[-1]
xmin = BCO_START_DATE

# toolbox = "xbox_select,xbox_zoom"
toolbox = "xbox_zoom"  # just for v1.1
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
        years=["%Y"],
    )  # defines how the date is displayed at different zoom-in stages

    vbars = p.vbar(x="x", width=1, line_width=20, top=dev_name, line_color='blue',  # colors[dev_name],
                   fill_color='blue'
                   , line_alpha=0.95,
                   fill_alpha=0.95, source=source)

                # circles = p.square(x="x", y=dev_name, source=source, size=20, color='blue', selection_color="orange", alpha=0.9,
                # selection_alpha=0.9)

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

legend = Legend(
    items=[
        (dev_name, []),
    ],
    location=(20, -8),
    label_text_font_size="10pt",
    label_text_font_style="bold",
    label_width=80,
    label_text_align="left",
    margin=5,
    background_fill_color="black",
    background_fill_alpha=0.1

)  # p.add_layout(legend, "left")

Buttons = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12] = [Button(
    label=dev_name,
    button_type="success",
    width=200,
    height=75,
    callback=(
        CustomJS(args=dict(source=source),
                 code=open("legend_callback.js").read())
    )
) for dev_name in Devices_names]

del p_list[8]  # TODO: add the right path for RamanLidar! This just excludes wrong Ramanlidar data from being plotted.
del Buttons[8]

grid1 = gridplot([[b, x] for b, x in zip(Buttons, p_list)]
                 )  # builds a grid from all plots and the select-menu

grid = column(select, grid1)

# change window to selection:
callback_select = CustomJS(args=dict(xr=p1.x_range, source=last_date_source), code=open("select_callback.js").read())
select.js_on_change('value', callback_select)

curdoc().add_root(grid)
curdoc().title = "Device Availability"
# show(grid) # can be used for debugging, but the select menu will not work then

# export to JS:
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

with open("AvailabilityPlotDiv.html", "w") as f:
    f.write(div)
    f.close()
