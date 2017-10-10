// Script for the buttons in DeviceAvailability.html to work.
// Each button sends the user to a different url.
//
// created 18.09.2017
// @author: Tobias Machnitzki (tobias.machnitzki@mpimet.mpg.de)
var button = cb_obj.label;
var page="";

if (button == "Allsky") {page="http://bcoweb.mpimet.mpg.de/camera/allsky/allsky.jpg"}
if (button == "Weather") {page="http://bcoweb.mpimet.mpg.de/quicklooks/weather/wxt_yesterday.png"}
if (button == "Radiation") {page="http://bcoweb.mpimet.mpg.de/quicklooks/radiation/radql.png"}
if (button == "Disdro") {page="http://bcoweb.mpimet.mpg.de/quicklooks/disdrometer/odm_yesterday.png"}
if (button == "HATPRO") {page=""}
if (button == "KIT") {page="NOT RUNNING"}
if (button == "KATRIN") {page="NOT RUNNING"}
if (button == "MBR2") {page="http://bcoweb.mpimet.mpg.de/quicklooks/mbr2ql/MBR2_QL.png"}
if (button == "MRR") {page="http://bcoweb.mpimet.mpg.de/quicklooks/mrr-bco/mrr_yesterday.png"}
if (button == "Ceilometer") {page="http://bcoweb.mpimet.mpg.de/quicklooks/ceilometer/ceilo_ql.png"}
if (button == "WindLidar") {page="http://bcoweb.mpimet.mpg.de/quicklooks/windlidar/wl_yesterday.png"}
if (button == "EARLI") {page="http://barbados.mpimet.mpg.de/lidarql/YESTERDAY.pdf"}
if (button == "LICHT") {page="http://lidar.mpimet.mpg.de/lidarql/"}
if (button == "BCOHAT") {page=""}

if (page==""){
    document.getElementById("buttonInfo").innerHTML = "There is no quicklook for the " + cb_obj.label + " yet.";
    alert("There is no quicklook for the " + cb_obj.label + " yet.")
}
else if (page == "NOT RUNNING") {
    document.getElementById("buttonInfo").innerHTML = "The " + cb_obj.label + " is not running at the moment.";
    alert("The " + cb_obj.label + " is not running at the moment.")
}
else {
    var win = window.open(page);
    if (win) {
        //Browser has allowed it to be opened
        win.focus();
    } else {
        //Browser has blocked it
        alert('Please allow popups for this website');
    }
}

