var axis = {"x":0, "y": 0, "z": 0, "thumbstick": 0, "trigger": 0};
/**
 *
 *  Gets the values from the first joystick plugged in.
 *
 *  @return
 *    false if there are no joysticks plugged in or the values from the joystick haven't changed
 *    or json containing all the joystick values in format [slider: string, direction: int]
 */
function getNewJoystickValues(){
    var gamepads = navigator.getGamepads();
    var newAxis = {"x":0, "y": 0, "z": 0, "thumbstick": 0, "trigger": 0};
    if(gamepads.length > 0) {
        var gamepad = gamepads[0];
        newAxis.x = gamepad.axes[0];
        newAxis.y = gamepad.axes[1];
        newAxis.z = gamepad.axes[2];
        newAxis.thumbstick = gamepad.axes[3];
        triggerTemp = gamepad.buttons[0];
        newAxis.trigger = triggerTemp['value'];
    }else {
        console.log("nogamepad");
        return false;
    }

    if(JSON.stringify(newAxis) != JSON.stringify(axis)) {
        axis = newAxis

        // Add before testing

        // Forwards (Surge=1)
        if(axis['y'] <= -0.8 && axis['thumbstick'] == -1 && axis['trigger'] == 0) {
          return { 'slider': 'Surge', 'direction': 1 };
        }
        // Backwards (Surge=-1)
        if(axis['y'] >= 0.8 && axis['thumbstick'] == -1 && axis['trigger'] == 0) {
          return { 'slider': 'Surge', 'direction': -1 };
        }
        // Upwards (Heave=1)
        if(axis['y'] >= 0.8 && axis['thumbstick'] == 1 && axis['trigger'] == 0) {
          return { 'slider': 'Heave', 'direction': 1 };
        }
        // Downwards (Heave=-1)
        if(axis['y'] <= -0.8 && axis['thumbstick'] == 1 && axis['trigger'] == 0) {
          return { 'slider': 'Heave', 'direction': -1 };
        }
        // Pitch up (Pitch=1)
        if(axis['y'] >= 0.8 && axis['trigger'] == 1) {
          return { 'slider': 'Pitch', 'direction': 1 };
        }
        // Pitch down (Pitch=-1)
        if(axis['y'] <= -0.8 && axis['trigger'] == 1) {
          return { 'slider': 'Pitch', 'direction': -1 };
        }
        // Right (Sway=1)
        if (axis['x'] >= 0.8) {
          return { 'slider': 'Sway', 'direction': 1 };
        }
        // Left (Sway=-1)
        if (axis['x'] <= -0.8) {
          return { 'slider': 'Sway', 'direction': -1 };
        }
        // Yaw right (Yaw=1)
        if (axis['z'] >= 0.8) {
          return { 'slider': 'Yaw', 'direction': 1 };
        }
        // Yaw Left (Yaw=-1)
        if (axis['z'] <= -0.8) {
          return { 'slider': 'Yaw', 'direction': -1 };
        }
        // Deadzone
        if (axis['x'] <= 0.1 && axis['x'] >= -0.1 && axis['y'] <= 0.1 && axis['y'] >= -0.1) {
          return false;
          // Stop all sliders (All=0) return { 'slider': 'All', 'direction': 0 };
        }
        // If no cases are met
        return false;
    }

    console.log("old values detected");
    return false;
}
