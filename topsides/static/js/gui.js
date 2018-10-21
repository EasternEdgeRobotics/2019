/** getNewSliderValues
 *
 *  gets the values from the 6 degrees of power gui sliders
 */
function getNewSliderValues(inputArtribute, inputValue) {
  runPythonPOST("guislider", JSON.stringify({ slider: inputArtribute, value: inputValue }), function(){
      console.log("new slider value has been sent to server");
  });
}
