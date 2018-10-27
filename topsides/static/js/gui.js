/** getNewSliderValues
*
*  gets the values from the 6 degrees of power gui sliders for the server and
*  front end display.
*/
function getNewSliderValues(inputAttribute, inputValue) {
 runPythonPOST("guislider", JSON.stringify({ slider: inputAttribute, value: inputValue }), function() {
     $("#output" + inputAttribute).html(inputValue);
     console.log("new slider value has been sent to server");
 });
}

/** getPresetValue
 *
 *  gets the values from the preset button for the server and front end display.
 */
function getPresetValue(inputAttribute, inputValue) {
  for(i = 0; i < inputAttribute.length; i++) {
    inputAttr = inputAttribute[i];
    $("#" + inputAttr).val(inputValue);
    $("#output" + inputAttr).html(inputValue);
    runPythonPOST("guislider", JSON.stringify({ slider: inputAttr, value: inputValue }), function() {
    });
  }
  console.log("preset button pressed and new slider values has been sent to server");
}

/** startCountDown
*
*  starts the coutdown timer.
*/
function startCountDown(duration, display) {
  var timer = duration, minutes, seconds;
  setInterval(function () {
      minutes = parseInt(timer / 60, 10);
      seconds = parseInt(timer % 60, 10);

      minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      display.text(minutes + ":" + seconds);

      if (--timer < 0) {
          timer = duration;
      }
  }, 1000);
}
