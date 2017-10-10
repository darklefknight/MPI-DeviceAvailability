// Script to make the dropdown menu in DeviceAvailability.html work.
// Depending on the users choice, a range for the x_axis will be set.
//
// @author: Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)

var vbars = [vbar0,vbar1,vbar2,vbar3,vbar4,vbar5,vbar6,vbar7,vbar8,vbar9,vbar10,vbar11,vbar12,vbar13];
var selected_line_width = 1;

if (isNaN(cb_obj.value)) {  //checks if the selected Value is an integer. e.g 2017

    var xmax = source.data['x'][source.data['x'].length -1] * 1000; //reads in the last value of the last_date_source object
    var xmaxDate = new Date(xmax);
    var which = cb_obj.value; //stores the selected value to the variable "which"

    //if "365" in the selected value:
    if (which.indexOf('365') > -1) {

        var xmin = new Date(xmaxDate.getTime());
        xmin.setFullYear(xmaxDate.getFullYear() -1);
        var xminmilli = xmin.getTime();
        var xmaxmilli = xmaxDate.getTime();
        selected_line_width = 7


    }
    // if "30" in the selected value:
    else if (which.indexOf('30') > -1) {

        var xmin = new Date(xmaxDate.getTime());
        xmin.setMonth(xmaxDate.getMonth() -1);
        var xminmilli = xmin.getTime();
        var xmaxmilli = xmaxDate.getTime();
        selected_line_width = 30

    }
    //if "complete" in the selected value:
    else if (which.indexOf('Complete') > -1) {

        var xmin = source.data['x'][0] * 1000;
        var xminDate = new Date(xmin);
        var xminmilli = xminDate.getTime();
        var xmaxmilli = xmaxDate.getTime();
        selected_line_width = 1
    }
}

//if the value is an integer (meaning a year):
else {

    var which = Number(cb_obj.value); //read the selected value as an integer
    var xmin = new Date(which, 0, 1); //make a date where the selected number is the year. Set Month and day to January 1st
    var xmax = new Date(which + 1, 0, 1); //make a date where the selected number is the year. Set Month and day to December 31st
    var xminmilli = xmin.getTime();
    var xmaxmilli = xmax.getTime();
    selected_line_width = 7

}

for (i=0; i < vbars.length; i++) {
    vbars[i].glyph.line_width = selected_line_width
}

xr.start = xminmilli;   //set p1.x_range.start
xr.end = xmaxmilli;     //set p1.x_range.end