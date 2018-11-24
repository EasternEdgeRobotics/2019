class ControlOptions{
    constructor(){
        var controlOption = this;
        runPythonGET("getControlOptions", null, function(data){
            controlOption._axes = data["axes"];
            controlOption._buttons = data["button"]
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

    //returns string to generate <select> options (USED ON PROFILEEDIT PAGE)
    getAxesOptionsString(){
        let returnString = "";
        $.each(this._axes, function(i, obj){
            returnString += "<option value='" + obj + "'>" + obj + "</option>"
        });
        return returnString;
    }

    //returns string to generate <select> options (USED ON PROFILEEDIT PAGE)
    getButtonOptionsString(){
        let returnString = "";
        $.each(this._buttons, function(i, obj){
            returnString += "<option value='" + obj + "'>" + obj + "</option>"
        });
        return returnString;
    }
}