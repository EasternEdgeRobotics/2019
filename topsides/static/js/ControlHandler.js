//adds gamepad to _gamepads and gives it a blank profile when plugged in
function gamepadConnected(gamepad, controlhandler){
    console.log(navigator.getGamepads());
    var doLink = false;

    if(controlhandler._profile != null){
        $.each(controlhandler._profile.gamepads, function(profile_gamepad_index, profile_gamepad){
            if(profile_gamepad.name == gamepad.id){
                doLink = true;
                $.each(controlhandler._gamepads, function(i, registered_profile_gamepad_index){
                    if(registered_profile_gamepad_index == profile_gamepad_index){
                        doLink = false;
                    }
                });
                if(doLink){
                    controlhandler._gamepads[gamepad.index] = profile_gamepad_index;
                    console.log("GAMEPAD AT INDEX " + gamepad.index + " CONNECTED AND LINKED TO PROFILE GAMEPAD " + profile_gamepad_index);
                }
            }
        });
    }
    /*if(controlhandler._profile != null){
        let done = false;
        $.each(controlhandler._profile.gamepads, function(profile_index, profile_gamepad){
            $.each(controlhandler._gamepads, function(gampead_index, registered_gamepad){ //loop through each registerd gamepad
                if(!done){
                    if(registered_gamepad.profile_index == profile_index){//if this profile index is already registered
                        return;
                    }
                    if(profile_gamepad.name == gamepad.id){//if profiles wanted gamepad is gamepad
                        controlhandler._gamepads.push({profile_index: profile_index, gamepad_index: gamepad.index});
                        
                        console.log("ADDED GAMEPAD AT INDEX " + gamepad.index + " AND LINKED IT TO PROFILE GAMEPAD " + profile_index);
                        done =true;
                    }    
                }
            });
        });
    }else{
        controlhandler._gamepads.push({profile_index: null, gamepad_index: gamepad.index});
        console.log("ADDED NEW JOYSTICK WITH NO PROFILE LINK");
    }*/



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
        var parsedControls = {};

        var _profile = this._profile;
        var _gamepads = this._gamepads;


        if(_profile != null){
            $.each(_gamepads, function(gamepad_index, profile_gamepad_index){
                if(profile_gamepad_index != null || profile_gamepad_index != undefined){
                    let gamepad = gamepads[gamepad_index];
                    if(gamepad != null){
                        $.each(_profile.gamepads[profile_gamepad_index].axes, function(axes_index, mapped_control){
                            if(mapped_control != ""){
                                parsedControls[mapped_control] = gamepad.axes[axes_index];
                            }
                        });

                        $.each(_profile.gamepads[profile_gamepad_index].buttons, function(button_index, mapped_control){
                            if(mapped_control != ""){
                                parsedControls[mapped_control] = gamepad.buttons[button_index].value;
                            }
                        });
                    }
                }
            });
        }

        return parsedControls;

        /*
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
        return null;*/
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
        $.each(p.gamepads, function(i, gamepad){
            if(desiredCounts[gamepad.name] == undefined || desiredCounts[gamepad.name] == null){
                desiredCounts[gamepad.name] = 1;
                return;
            }
            desiredCounts[gamepad.name]++;
        })

        var connectedCounts = {};
        let gamepads = navigator.getGamepads();
        console.log(gamepads)
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
        $.each(desiredCounts, function(i,amount){
            console.log("fdsf" + connectedCounts[i]);
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


        var gamepads = navigator.getGamepads();
        $.each(p.gamepads, function(profile_gamepad_index, profile_gamepad){
            $.each(gamepads, function(gamepad_index, gamepad){
                if(gamepad!=null){
                    if(profile_gamepad.name == gamepad.id){
                        if(_gamepads[gamepad_index] == null){
                            _gamepads[gamepad_index] = profile_gamepad_index;
                            //DONE
                            console.log("GAMEPAD AT INDEX " + gamepad_index + " DETECTED AND ASSIGNED TO PROFILE INDEX " + profile_gamepad_index);
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