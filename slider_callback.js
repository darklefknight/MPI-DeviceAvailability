// Script for the slider in DeviceAvailability.html to work.
//
// created 10.10.2017
// @author: Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)

var vbars = [vbar0,vbar1,vbar2,vbar3,vbar4,vbar5,vbar6,vbar7,vbar8,vbar9,vbar10,vbar11,vbar12,vbar13];
var width = cb_obj.value;

for (i = 0; i < vbars.length; i++) {
    vbars[i].glyph.line_width = width
}