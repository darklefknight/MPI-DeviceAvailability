document.getElementById("devInfo").innerHTML = "Done!";

var TXTFile = "C:/Users/darkl/PycharmProjects/MPI-DeviceAvailability/ASCA_example.txt";

var openFile = function (event) {
    var input = event.target;

    var reader = new FileReader();
    reader.onload = function () {
        var text = reader.result;
        var node = document.getElementById('divInfo');
        node.innerText = text;
        console.log(reader.result.substring(0, 200));
    };
    reader.readAsText(input.files[0]);
};

document.getElementById("devInfo").innerHTML = openFile(TXTFile);