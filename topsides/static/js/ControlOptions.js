class ControlOptions{
    constructor(data){
        this._axes = data["axes"];
        this._buttons = data["button"];
    }

    get axes(){
        return this._axes;
    }

    getAxesOptionsString(){
        let returnString = "";
        $.each(this._axes, function(i, obj){
            returnString += "<option value='" + obj + "'>" + obj + "</option>"
        });
        return returnString;
    }

    getButtonOptionsString(){
        let returnString = "";
        $.each(this._buttons, function(i, obj){
            returnString += "<option value='" + obj + "'>" + obj + "</option>"
        });
        return returnString;
    }
}