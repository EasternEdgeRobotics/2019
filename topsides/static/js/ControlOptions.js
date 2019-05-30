class ControlOptions{
    constructor(){
        this._axes = null;
        var controlOption = this;
        this._loadFunction = function(){};
        runPythonGET("getControlOptions", null, function(data){
            controlOption._axes = data["axes"];
            controlOption._buttons = data["button"];
            controlOption._holdButtons = data["buttonHold"];
            controlOption._toggleButtons = data["buttonToggle"];
            controlOption._loadFunction();
        });
    }

    //getter for axes control options ex:sway,heave
    get axes(){
        return this._axes;
    }

    //getter for button control options ex:electromagnet, pitchup
    get buttons(){
        return this._buttons;
    }

    get toggleButtons(){
        return this._toggleButtons;
    }

    get holdButtons(){
        return this._holdButtons;
    }

    set onOptionsLoaded(f){
        if(f instanceof Function){
            this._loadFunction = f;
            if(this._axes != null){
                this._loadFunction();
            }
        }
    }
    

    //returns string to generate <select> options (USED ON PROFILEEDIT PAGE)
    getAxesOptionsString(){
        let returnString = "";
        returnString += "<option value = '' disabled></option><option value=''>No Control</option><option value = '' disabled></option><option value='' style='font-weight: bold;color:rgb(1,1,1);' disabled>Axes Controls</option>";
        $.each(this._axes, function(i, obj){
            returnString += "<option value='" + i + "'>" + i + "</option>"
        });
        return returnString;
    }

    //returns string to generate <select> options (USED ON PROFILEEDIT PAGE)
    getButtonOptionsString(){
        let returnString = "";

        //REGULAR BUTTONS
        returnString += "<option value = '' disabled></option><option value = ''>No Control</option><option value = '' disabled></option><option value='' style='font-weight: bold;color:rgb(1,1,1);' disabled>Press Controls</option>";
        $.each(this._buttons, function(i, obj){
            returnString += "<option value='" + i + "'>" + i + "</option>"
        });

        //HOLD BUTTONS
        returnString += "<option value = '' disabled></option><option value='' style='font-weight: bold;color:rgb(1,1,1);' disabled>Hold Controls</option>";

        $.each(this._holdButtons, function(i, obj){
            returnString += "<option value='" + i + "'>" + i + "</option>";
        });

        //TOGGLE BUTTONS
        returnString += "<option value = '' disabled></option><option value='' style='font-weight: bold;color:rgb(1,1,1);' disabled>Toggle Controls</option>";

        $.each(this._toggleButtons, function(i, obj){
            returnString += "<option value='" + i +"'>" + i + "</option>";
        });

        return returnString;
    }

    get(name){
        if(name in this._axes){
            return this._axes[name];
        }else if(name in this._buttons){
            return this._buttons[name];
        }else if(name in this._toggleButtons){
            return this._toggleButtons[name];
        }
        return false
    }

    /*isHoldControl(name){
        var returnVal = false;
        $.each(this._holdButtons, function(control, _){
            if(control == name){
                returnVal = true;
            }
        });
        return returnVal;
    }*/
}