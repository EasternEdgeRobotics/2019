class ControlHandler{
    constructor(){
        this._gamepads = [{profile:null,gamepad_index:null},{profile:null,gamepad_index:null},{profile:null,gamepad_index:null},{profile:null,gamepad_index:null}];
        this._profile = null;

        window.addEventListener("gamepadconnected", this.gamepadConnected(e));
        window.addEventListener("gamepaddisconnected", this.gamepadDisconnected(e));
        
    }

    //adds gamepad to _gamepads and gives it a blank profile when plugged in
    gamepadConnected(gamepad){
        this._gamepads[gamepad['index']]["gamepad"] = gamepad.index;
        this._gamepads[gamepad['index']]["profile"] = null;
    }

    //removes gamepad from _gamepads and gives it a blank profile when unplugged
    gamepadDisconnected(gamepad){
        this._gamepads[gamepad['index']]["gamepad"] = null;
        this._gamepads[gamepad['index']]["profile"] = null; 
    }

    //getter for _gamepads
    get gamepads(){
        return this._gamepads;
    }

    /** parseControls()
     * 
     *  @description - Parses and maps gamepad values to the respected controls from the current profile. All valid controls are located in controls.json
     * 
     *  @returns
     *      JSON - the values for controls to send to server
     *      null - if there is an error or no current profile
     * 
     * 
     */
    parseControls(){
        if(this._profile != null){
            let i = 0;
            var returnControls = [null,null,null,null];
            this._gamepads.forEach(function(obj){
                if(obj.profile != null){
                    returnControls[i] = {};
                    let tempGamepad = navigator.getGamepads()[i];
                    $.each(tempGamepad.axes, function(axes_index, axes_value){
                        returnControls[obj.profile.axes[axes_index]] = axes_value;
                    });

                    $.each(tempGamepad.buttons, function(button_index, button_value){
                        returnControls[obj.profile.buttons[button_index]] = button_value;
                    });
                }
                i++;
            });
            return returnControls;
        }
        return null;
    }

    /** isValidProfile
     * 
     *  @param
     *      p - profile JSON
     * 
     *  @returns
     *      true - if all required gamepads are plugged in for profile
     *      false - not all required gamepads are plugged in
     * 
     */
    isValidProfile(p){
        let tempGamepads = navigator.getGamepads();
        p.gamepads.forEach(function(gamepad){
            tempGamepads.forEach(function(tempGamepad){
                if(gamepad.id == tempGamepad.id){
                    tempGamepads.splice(tempGamepad.index, tempGamepad.index+1);
                    break;
                }
            });
        });
    }


    //setter for profile, only sets if it is a valid profile
    set profile(p){
        if(this.isValidProfile(p)){
            this._profile = p;
        }
    }

    //getter for profile
    get profile(){
        return this._profile;
    }
}