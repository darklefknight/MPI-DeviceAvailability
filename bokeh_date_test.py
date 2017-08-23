from bokeh.io import show
from bokeh.layouts import row
from datetime import timedelta
from datetime import datetime as dt
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter
import numpy as np

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__ == "__main__":
    start = dt(2017, 1, 1)
    end = dt(2017, 6, 1)

    dates = [x for x in daterange(start, end)]
    data = [x for x in range(len(dates))]
    index = [x for x in range(len(dates))]

    data = np.asarray(data)
    index = np.asarray(index)

    p1 = figure(title='test1',x_axis_type='datetime')
    p1.line(dates,data)
    # p1.xaxis.formatter = DatetimeTickFormatter(
    #     hours=["%d %B %Y"],
    #     days=["%d %B %Y"],
    #     months=["%d %B %Y"],
    #     years=["%d %B %Y"],
    # )

    # plot = row(p1)

    show(p1, browser='firefox')
