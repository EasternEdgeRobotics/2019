/** getNewSliderValues
 *
 *  gets the values from the 6 degrees of power gui sliders
 */
function getNewSliderValues(degreevalue) {
  var val = document.getElementById(degreevalue).value

  runPythonPOST("guislider", JSON.stringify({ slider: degreevalue, value: val }), function(){
      console.log("new slider value has been sent to server");
  });
}
