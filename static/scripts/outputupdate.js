/**
 * Created by mathias on 7/06/2017.
 */

function outputUpdate(vol) {
	var home = document.getElementById("home");
	document.querySelector('#volume').value = vol;
	home.style["-webkit-filter"] = "brightness(" + vol +"%)";


}