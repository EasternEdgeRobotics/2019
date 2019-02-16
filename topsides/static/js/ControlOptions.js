class ControlOptions{
    constructor(){
        this._axes = null;
        var controlOption = this;
        this._loadFunction = function(){};
        runPythonGET("getControlOptions", null, function(data){
            controlOption._axes = data["axes"];
            controlOption._buttons = data["button"];
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
            returnString += "<option value='" + obj + "'>" + obj + "</option>"
        });
        return returnString;
    }

    //returns string to generate <select> options (USED ON PROFILEEDIT PAGE)
    getButtonOptionsString(){
        let returnString = "";
        returnString += "<option value = '' disabled></option><option value = ''>No Control</option><option value = '' disabled></option><option value='' style='font-weight: bold;color:rgb(1,1,1);' disabled>Press Controls</option>";
        $.each(this._buttons, function(i, obj){
            returnString += "<option value='" + obj + "'>" + obj + "</option>"
        });

        returnString += "<option value = '' disabled></option><option value='' style='font-weight: bold;color:rgb(1,1,1);' disabled>Toggle Controls</option>";

        $.each(this._toggleButtons, function(i, obj){
            returnString += "<option value='" + obj +"'>" + obj + "</option>";
        });
        return returnString;
    }
}