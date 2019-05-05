/**gamepadConnected
 * 
 *  event called when a gamepad is connected
 *  maps the gamepad to a gamepad in the profile if required
 * 
 * 
 */
function gamepadConnected(gamepad, controlhandler){
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
    constructor(options){
        //{profile_index:null,gamepad_index:null}
        
        //[profileIndex...]
        this._gamepads = [null,null,null,null];
        this._profile = null;
        this._previous = null;

        this._notificationHandler = null;

        this._CONTROLOPTIONS = options;

        this._toggledControls = {};
        this._previousToggledButtons = [{},{},{},{}];

        //this._holdControls = {};
        //this._previousHoldControls = [{},{},{},{}];

        $(document).ready(function(){
            $('body').append("<div id='popupAssignGamepads' style='display:none'><div class='black-overlay'></div><p class='panel' id='assignGamepadsText'></p></div>");
        });

        var self = this;
        window.addEventListener("gamepadconnected", function(e){gamepadConnected(e.gamepad, self);});
        window.addEventListener("gamepaddisconnected", function(e){gamepadDisconnected(e.gamepad, self);});
        
    }


    //getter for _gamepads
    get gamepads(){
        return this._gamepads;
    }


    registerNotificationHandler(handler){
        this._notificationHandler = handler;
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
    _parseControls(){
        var gamepads = navigator.getGamepads();
        var parsedControls = {}; //empty preset

        //gets instances to use in nested functions
        var _profile = this._profile;
        var _gamepads = this._gamepads;
        var _previousToggledButtons = this._previousToggledButtons;
        //var _previousHoldControls = this._previousHoldControls;
        var _toggledControls = this._toggledControls;
        //var _holdControls = this._holdControls;
        var _controloptions = this._CONTROLOPTIONS;


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
                            if(mapped_control != "" && mapped_control != null){//if the button is mapped to something aka not empty string
                                var value = gamepad.buttons[button_index].value;
                                if(_controloptions.toggleButtons.includes(mapped_control)){
                                    if(_previousToggledButtons[gamepad_index][mapped_control] != undefined){
                                        if(value == 1){
                                            if(_previousToggledButtons[gamepad_index][mapped_control] != value){
                                                _toggledControls[mapped_control] = Math.abs(_toggledControls[mapped_control] - 1);
                                            }
                                        }
                                        _previousToggledButtons[gamepad_index][mapped_control] = value;
                                    }else{
                                        _previousToggledButtons[gamepad_index][mapped_control] = 0;
                                        _toggledControls[mapped_control] = 0;
                                    }
                                    parsedControls[mapped_control] = _toggledControls[mapped_control];
                                }/*else if(_controloptions.isHoldControl(mapped_control) == true){
                                    if(value == 1){
                                        parsedControls[_controloptions.holdButtons[mapped_control].hold] = 1;
                                        parsedControls[_controloptions.holdButtons[mapped_control].release] = 0;
                                    }else{
                                        parsedControls[_controloptions.holdButtons[mapped_control].release] = 1;
                                        parsedControls[_controloptions.holdButtons[mapped_control].hold] = 0;
                                    }
                                }*/
                                
                                else{
                                    parsedControls[mapped_control] = value; //set the control option mapped to the value of the gamepad
                                }
                            }
                        });
                    }
                }
            });
        }

        this._toggledControls = _toggledControls;
        this._previousToggledButtons = _previousToggledButtons;
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
        let parsed = this._parseControls();

        if(parsed == null){
            return null;
        }
        if(JSON.stringify(parsed) != this._previous){
            this._previous = JSON.stringify(parsed);
            console.log(parsed);
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
                                done = true;
                            }
                            
                        }
                    }
                }
            });
        });
        this._gamepads = _gamepads;
    }

    //getter for profile
    get profile(){
        return this._profile;
    }




    /**setGamepads
     * 
     * @description assigns each gamepad a profile index step by step. AKA pilot can choose which physical
     *              gamepad is mapped to which mapped gamepad from the profile builder.
     * 
     *              Each profile gamepad is done sequentially but still asynchronously. Basically It begins an interval of the 
     *              function assignGamepadStep each time a gamepad is assigned
     * 
     * 
     */
    setGamepads(){
        console.log("GAMEPAD MAPPING BEGIN");

        if(this.profile != null && this.isValidProfile(this.profile)){ //if profile is set and is valid (proper gamepads are connected)
            this._gamepads = [null, null, null, null];

            var profile = this._profile;
            var controlHandlerInstance = this;
            
            //sets the user friendly popup visiable
            document.getElementById("popupAssignGamepads").style['display'] = "block";
            
            //starting first instance of assignGamepadStep
            setTimeout(function(){assignGamepadStep(controlHandlerInstance, 0)}, 50);
            
        }else{
            if(this._notificationHandler != null)
            this._notificationHandler.localNotification("Required gamepads aren't connected for this profile!", "warning");
        }
    }

    finishedAssignGamepads(){
        if(this._notificationHandler != null)
            this._notificationHandler.localNotification("Gamepads successfully assigned for profile: " + this._profile.name, "success");
    }


}

var activeIntervals = [];
var currentIntervalID = null;

function assignGamepadStep(controlHandler, profile_gamepadIndex){
    //set the user friendly popup to indicate which gamepad is being set
    $("#assignGamepadsText").html("Press Button on a valid Gamepad to Assign it as <b>" + controlHandler.profile.gamepads[profile_gamepadIndex].friendly_name + "</b>.");

    profile_gamepadIndex = profile_gamepadIndex;
    profile_gamepad = controlHandler.profile.gamepads[profile_gamepadIndex];
    var movedGamepadIndex = null;
    let gamepads = navigator.getGamepads();

    $.each(gamepads, function(gamepadIndex, gamepad){
        if(gamepad != null){
            if(controlHandler._gamepads[gamepadIndex] == null && gamepad.id == profile_gamepad.name){
                $.each(gamepad.buttons, function(i, input){
                    if(Math.abs(input.value) > 0.8){
                        movedGamepadIndex = gamepadIndex;
                    } 
                });
            }
        }
    });

    //If gamepad button was hit aka selected
    if(movedGamepadIndex != null){
        controlHandler._gamepads[movedGamepadIndex] = profile_gamepadIndex;
        console.log("MAPPED GAMEPAD AT INDEX " + movedGamepadIndex);
        console.log(controlHandler._gamepads);
        if(profile_gamepadIndex < controlHandler.profile.gamepads.length - 1){//if there are more gamepads to be assigned, start new interval with next gamepad
            clearInterval();
            setTimeout(function(){assignGamepadStep(controlHandler, profile_gamepadIndex+1)}, 50);
        }else{
            //if finished
            $("#popupAssignGamepads").css('display', "none");
            controlHandler.finishedAssignGamepads();
        }
    }else{
        setTimeout(function(){assignGamepadStep(controlHandler, profile_gamepadIndex)}, 50);
    }
}

/*
function clearIntervals(){
    //stop all threading for assigning gamepads
    for(var i = 0; i < activeIntervals.length ; i++){
        clearInterval(activeIntervals[i]);
    }
    activeIntervals = [];

}*/