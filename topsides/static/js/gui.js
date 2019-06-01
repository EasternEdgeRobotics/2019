/**
*  Gets the values from the 6 degrees of power gui sliders for the server and
*  front end display.
*
*   @param {string} inputAttribute
*    name of the slider axis
*
*   @param {int} inputValue
*    value of the slider
*/
function getNewSliderValues(inputAttribute, inputValue) {
 runPythonPOST("guislider", JSON.stringify({ slider: inputAttribute, value: inputValue }), function() {
     $("#output" + inputAttribute).html(inputValue);
     console.log("new slider value has been sent to server");
 });
}

/**
 *  Gets the values from the preset button for the server and front end display.
 *
 *  @param {string} inputAttribute
 *   name of the slider axis
 *
 *  @param {int} inputValue
 *   value from the text box
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

/**
*  Starts the countdown timer.
*
*  @param {int} duration
*   time to run
*
*  @param {string} display
*   id from gui.html to display to
*/
function startCountDown(duration, display) {
    var timer = duration, minutes, seconds;
    trigger = setInterval(function () {
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

/**
 *  Stops the countdown timer.
 *
 *  @param {string} display
 *   id from gui.html to display to
 */
function stopCountDown(display) {
    display.text("00:00");
    clearInterval(trigger);
}

/**
 *  Sets slider values according to quick set button.
 *
 *  @param {int} buttonPressed
 *   number of button pressed
 */
function quickSetButtons(buttonPressed) {
    var inputAttribute = ["surge", "heave", "sway", "yaw", "pitch", "roll"];
    var inputValue;
    switch (buttonPressed) {
        case 0:
            // Trash Rack
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 1:
            // Fish
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 2:
            // Cannon
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 3:
            // Pebbles
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 4:
            // Tire
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 5:
            // Micro ROV
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 6:
            // Benthic Species
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 7:
            // Line Following
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 8:
            // PH
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 9:
            // Reef Ball
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
        case 10:
            // Cannon Shells
            inputValue = [0, 0, 0, 0, 0, 0];
            break;
      }
    getQuickSetValue(inputAttribute, inputValue);
}

/**
 *  Gets the values from the quick set buttons for the server and front end display.
 *
 *  @param {string} inputAttribute
 *   name of the slider axis
 *
 *  @param {int} inputValue
 *   value to set each slider
 */
function getQuickSetValue(inputAttribute, inputValue) {
    for(i = 0; i < inputAttribute.length; i++) {
        inputAttr = inputAttribute[i];
        $("#" + inputAttr).val(inputValue[i]);
        $("#output" + inputAttr).html(inputValue[i]);
        runPythonPOST("guislider", JSON.stringify({ slider: inputAttr, value: inputValue[i] }), function() {
        });
    }
    console.log("quick set button pressed and new slider values has been sent to server");
}
