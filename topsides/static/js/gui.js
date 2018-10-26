/** getNewSliderValues
 *
 *  gets the values from the 6 degrees of power gui sliders for the server and
 *  front end display.
 */
 function getNewSliderValues(inputAttribute, inputValue) {
   runPythonPOST("guislider", JSON.stringify({ slider: inputAttribute, value: inputValue }), function(){
       $("#output" + inputAttribute).html(inputValue);
       console.log("new slider value has been sent to server");
   });
 }
