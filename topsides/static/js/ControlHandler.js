//adds gamepad to _gamepads and gives it a blank profile when plugged in
function gamepadConnected(gamepad, controlhandler){
    console.log(gamepad);
    controlhandler._gamepads[gamepad.index]["gamepad"] = gamepad.index;
    controlhandler._gamepads[gamepad.index]["gamepad_index"] = gamepad.index;
}

//removes gamepad from _gamepads and gives it a blank profile when unplugged
function gamepadDisconnected(gamepad, controlhandler){
    controlhandler._gamepads[gamepad['index']]["gamepad"] = null;
    controlhandler._gamepads[gamepad['index']]["profile"] = null; 
}


class ControlHandler{
    constructor(){
        this._gamepads = [{profile:null,gamepad_index:null},{profile:null,gamepad_index:null},{profile:null,gamepad_index:null},{profile:null,gamepad_index:null}];
        this._profile = null;

        var self = this;
        window.addEventListener("gamepadconnected", function(e){gamepadConnected(e.gamepad, self);});
        window.addEventListener("gamepaddisconnected", function(e){gamepadDisconnected(e.gamepad, self);});
        
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
        var _profile = this._profile;
        var _gamepads = this._gamepads;
        if(this._profile != null){
            var returnControls = {}; //blank array to hold parsed controls
            $.each(_gamepads, function(i, obj){
                if(obj != null && obj != undefined){
                    let tempGamepad = navigator.getGamepads()[obj['gamepad_index']];
                    if(tempGamepad != null){
                        $.each(tempGamepad.axes, function(axes_index, axes_value){
                            if(_profile.gamepads[i].axes[axes_index] != "")
                            returnControls[_profile.gamepads[i].axes[axes_index]] = axes_value;
                        });

                        $.each(tempGamepad.buttons, function(button_index, button_value){
                            if(_profile.gamepads[i].buttons[button_index] != "")
                            returnControls[_profile.gamepads[i].buttons[button_index]] = button_value.value;
                        });
                    }
                }
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
        let usedGamepadIndexs = [];
        let points = 0;
        p.gamepads.forEach(function(gamepad){
            if(gamepad != null){
                for(let i = 0 ; i < tempGamepads.length ; i++){
                    let tempGamepad = tempGamepads[i];
                    if(tempGamepad != null && !usedGamepadIndexs.includes(i)){
                        if(gamepad.name == tempGamepad.id){
                            usedGamepadIndexs.push(i);
                            points++;
                            break;
                        }
                    }
                }
            }else{
                points++;
            }
        });
        if(points >= p.gamepads.length){
            return true;
        }
        return false;
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