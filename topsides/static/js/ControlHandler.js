/**gamepadConnected
 * 
 *  event called when a gamepad is connected
 *  maps the gamepad to a gamepad in the profile if required
 * 
 * 
 */
function gamepadConnected(gamepad, controlhandler){
    console.log(navigator.getGamepads());
    var doLink = false;
    alreadyRegistered = false;

    if(controlhandler._profile != null){
        $.each(controlhandler._profile.gamepads, function(profile_gamepad_index, profile_gamepad){
            if(profile_gamepad.name == gamepad.id){
                doLink = true;
                $.each(controlhandler._gamepads, function(i, registered_profile_gamepad_index){
                    if(registered_profile_gamepad_index == profile_gamepad_index){
                        doLink = false;
                    }
                });
                if(doLink && !alreadyRegistered){
                    alreadyRegistered = true;
                    controlhandler._gamepads[gamepad.index] = profile_gamepad_index;
                    console.log("GAMEPAD AT INDEX " + gamepad.index + " CONNECTED AND LINKED TO PROFILE GAMEPAD " + profile_gamepad_index);
                }
            }
        });
    }

}

//removes gamepad from _gamepads and gives it a blank profile when unplugged
function gamepadDisconnected(gamepad, controlhandler){
    controlhandler._gamepads[gamepad.index] = null;
}


class ControlHandler{
    constructor(){
        //{profile_index:null,gamepad_index:null}
        
        //[profileIndex...]
        this._gamepads = [null,null,null,null];
        this._profile = null;
        this._previous = null;

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
        var gamepads = navigator.getGamepads();
        var parsedControls = {}; //empty preset

        //gets instances to use in nested functions
        var _profile = this._profile;
        var _gamepads = this._gamepads;


        if(_profile != null){//if there is a function
            $.each(_gamepads, function(gamepad_index, profile_gamepad_index){//loop through each mapped profile gamepads
                if(profile_gamepad_index != null || profile_gamepad_index != undefined){//if it exists
                    let gamepad = gamepads[gamepad_index]; //gets the gamepad linked to that profile_index
                    if(gamepad != null){ //if the gamepad exists
                        $.each(_profile.gamepads[profile_gamepad_index].axes, function(axes_index, mapped_control){ //loop through each axes controls of the profile
                            if(mapped_control != ""){ //if the axes is mapped to something aka not empty string
                                parsedControls[mapped_control] = gamepad.axes[axes_index]; //set the control option mapped to the value of the gamepad
                            }
                        });

                        $.each(_profile.gamepads[profile_gamepad_index].buttons, function(button_index, mapped_control){ //loop through each button controls of the profile
                            if(mapped_control != ""){//if the button is mapped to something aka not empty string
                                parsedControls[mapped_control] = gamepad.buttons[button_index].value; //set the control option mapped to the value of the gamepad
                            }
                        });
                    }
                }
            });
        }

        return parsedControls;
    }

    /** parseControls()
     * 
     *  @description - Parses and maps gamepad values to the respected controls from the current profile. All valid controls are located in controls.json
     *               - Will return values if they are different than the last read, otherwise returns null
     * 
     *  @returns
     *      JSON - the values for controls to send to server
     *      null - if there is an error or no current profile
     * 
     * 
     */
    parseControlsIfChanged(){
        let parsed = this.parseControls();

        if(parsed == null){
            return null;
        }
        if(JSON.stringify(parsed) != this._previous){
            console.log("fdsfds");
            this._previous = JSON.stringify(parsed);
            return parsed;
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
     *  @deprecated
     * 
     */
    isValidProfile(p){
        var desiredCounts = {};

        //counts how many of each controller is required by the profile
        $.each(p.gamepads, function(i, gamepad){
            if(desiredCounts[gamepad.name] == undefined || desiredCounts[gamepad.name] == null){
                desiredCounts[gamepad.name] = 1;
                return;
            }
            desiredCounts[gamepad.name]++;
        })

        var connectedCounts = {};
        let gamepads = navigator.getGamepads();
        //counts the amount of each type of joystick connected
;        $.each(gamepads, function(i, gamepad){
            if(gamepad !=null){
                if(connectedCounts[gamepad.id] == undefined || connectedCounts[gamepad.id] == null){
                    connectedCounts[gamepad.id] = 1;
                    return;
                }
                connectedCounts[gamepad.id]++;
            }
        });

        var isGood = true;
        //compares the desired counts and actual counts
        $.each(desiredCounts, function(i,amount){
            if(amount != connectedCounts[i]){
                isGood = false;
            }
        });

        return isGood;
    }


    //setter for profile, only sets if it is a valid profile
    set profile(p){
        this._profile = p;
        this._gamepads = [null,null,null,null];
        var _gamepads = this._gamepads;
        console.log("PROFILE SET");

        //Auto setting the gamepads
        var gamepads = navigator.getGamepads();
        //loop through each required gamepad in the profile
        $.each(p.gamepads, function(profile_gamepad_index, profile_gamepad){
            let done =false
            //loop through each connected gamepad
            $.each(gamepads, function(gamepad_index, gamepad){
                if(!done){//used to stop double mapping
                    //if there is a gamepad connected
                    if(gamepad!=null){
                        if(profile_gamepad.name == gamepad.id){ //if the id of the connected gamepad is equal to the required id
                            if(_gamepads[gamepad_index] == null){//if the gamepad isn't already mapped
                                _gamepads[gamepad_index] = profile_gamepad_index;
                                //Set map the gamepad to the profile gamepad
                                console.log("GAMEPAD AT INDEX " + gamepad_index + " DETECTED AND ASSIGNED TO PROFILE INDEX " + profile_gamepad_index);
                                done = true;
                            }
                            
                        }
                    }
                }
            });
        });
    }

    //getter for profile
    get profile(){
        return this._profile;
    }
}