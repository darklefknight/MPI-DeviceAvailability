var vbars = [vbar0, vbar1, vbar2, vbar3, vbar4, vbar5, vbar6, vbar7, vbar8, vbar9, vbar10, vbar11, vbar12];

var msecPerMinute = 1000 * 60;
var msecPerHour = msecPerMinute * 60;
var msecPerDay = msecPerHour * 24;

var start_date = new Date(xr.start);
var end_date = new Date(xr.end);
var max_interval = new Date(xr.max_interval);
var ref_date = new Date(2010,1,1,0,0,0,0);
var line_width = 10;

document.getElementById("demo1").innerHTML = max_interval;

var start = start_date.getTime();
var end = end_date.getTime();
var max = max_interval.getTime();
var ref = ref_date.getTime();
var interval = max - ref;
var int_date = new Date(interval)


document.getElementById("demo2").innerHTML = ref;
var delta = end - start;
var days = Math.floor(delta / msecPerDay );
delta = delta - (days * msecPerDay );
document.getElementById("demo3").innerHTML = delta;

line_width = max/delta;

document.getElementById("demo4").innerHTML = line_width;

for (i = 0; i < vbars.length; i++) {
    vbars[i].glyph.line_width = line_width
}


