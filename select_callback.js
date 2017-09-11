if (isNaN(cb_obj.value)) {

    document.getElementById("id1").innerHTML = " which in else:" + which;
    var xmax = source.data['x'][source.data['x'].length -1] * 1000;
    var xmaxDate = new Date(xmax);
    document.getElementById("id6").innerHTML = "xmax works" + xmaxDate;
    var which = cb_obj.value;
    if (which.indexOf('365') > -1) {
        document.getElementById("id1").innerHTML = "6";
        document.getElementById("id1").innerHTML = "2";
        var xmin = new Date(xmaxDate.getTime());
        document.getElementById("id1").innerHTML = xmin;
        xmin.setFullYear(xmaxDate.getFullYear() -1);
        var xminmilli = xmin.getTime();
        var xmaxmilli = xmaxDate.getTime();

    }
    else if (which.indexOf('30') > -1) {
        document.getElementById("id1").innerHTML = "1";
        document.getElementById("id1").innerHTML = "2";
        var xmin = new Date(xmaxDate.getTime());
        document.getElementById("id1").innerHTML = xmin;
        xmin.setMonth(xmaxDate.getMonth() -1);
        // document.getElementById("id1").innerHTML = maxYear;
        var xminmilli = xmin.getTime();
        var xmaxmilli = xmaxDate.getTime();
    }
}

else {

    var which = Number(cb_obj.value);
    var xmin = new Date(which, 0, 1);
    var xmax = new Date(which + 1, 0, 1);
    var xminmilli = xmin.getTime();
    var xmaxmilli = xmax.getTime();

    document.getElementById("id1").innerHTML = " which:" + which;
    document.getElementById("id4").innerHTML = " xmin_date:" + xmin;
    document.getElementById("id5").innerHTML = " xmax_date:" + xmax;
    document.getElementById("id2").innerHTML = " xmin:" + xminmilli;
    document.getElementById("id3").innerHTML = " xmax:" + xmaxmilli;


}

xr.start = xminmilli;
xr.end = xmaxmilli;