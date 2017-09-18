// @author: Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)

var vbars = [vbar0, vbar1, vbar2, vbar3, vbar4, vbar5, vbar6, vbar7, vbar8, vbar9, vbar10, vbar11, vbar12];

// var msecPerMinute = 1000 * 60;
// var msecPerHour = msecPerMinute * 60;
// var msecPerDay = msecPerHour * 24;

var start_date = new Date(xr.start);
var end_date = new Date(xr.end);
var max_interval = new Date(xr.max_interval);
var ref_date = new Date(2010,1,1,0,0,0,0);
var line_width = 10;

document.getElementById("demo1").innerHTML = start_date;
document.getElementById("demo2").innerHTML = end_date;

var start = start_date.getTime();
var end = end_date.getTime();
var max = max_interval.getTime();
var ref = ref_date.getTime();
var interval = max - ref;
var int_date = new Date(interval)


var daydif = end_date.getDay() - start_date.getDay()
var monthdif = end_date.getMonth() - start_date.getMonth()
var yeardif = end_date.getFullYear() - start_date.getFullYear()

if (yeardif >1) {
    line_width = 1
}

else if (monthdif > 2) {
    line_width = 7
}
else {
    line_width = 20
}


document.getElementById("demo3").innerHTML = yeardif;



document.getElementById("demo4").innerHTML = monthdif;
document.getElementById("demo5").innerHTML = line_width;

for (i = 0; i < vbars.length; i++) {
    vbars[i].glyph.line_width = line_width
}


