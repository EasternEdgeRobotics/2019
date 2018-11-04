
var axis = {"x":0, "y": 0, "z": 0, "thumbstick": 0};



/** getNewJoystickValues
 * 
 *  gets the values from the first joystick plugged in.
 * 
 *  Returns: 
 *      - false: if there are no joysticks plugged in or the values from the joystick haven't changed
 * 
 *      - axis: json containing all the joystick values
 *          -structure: {x: double, y: double, z:double, thumbstick: double} 
 */
function getNewJoystickValues(){
    var gamepads = navigator.getGamepads();
    var newAxis = {"x":0, "y": 0, "z": 0, "thumbstick": 0};
    if(gamepads.length > 0){
        var gamepad = gamepads[0];
        newAxis.x = gamepad.axes[0];
        newAxis.y = gamepad.axes[1];
        newAxis.z = gamepad.axes[2];
        newAxis.thumbstick = gamepad.axes[3];
    }else{
        console.log("nogamepad");
        return false;
    }

    if(JSON.stringify(newAxis) != JSON.stringify(axis)){
        axis = newAxis
        return axis;
    }

    console.log("Old Values Detected");
    return false;
}