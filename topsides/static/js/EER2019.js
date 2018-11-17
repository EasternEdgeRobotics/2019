/**
*
*    @param {string} scriptName
*     the name of the function to run. Declared in the @app.route in python file
*
*    @param {json} data
*     data to send to the python script. JSON Format only. (Non JSON will crash the program)
*
*    @param {function} returnFunction
*     function to run when ajax call is done. Function must take in variable for JSON data
*
*/
function runPythonGET(scriptName, data, returnFunction){
    //TODO: Add code to ensure data is JSON
    $.ajax({
        type: "GET",
        url: "http://localhost:80/" + scriptName,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: data,
        success: function(data){
            console.log("fds");
            returnFunction(data);
        }
    });
}



/**
*
*    @param {string} scriptName
*     the name of the function to run. Declared in the @app.route in python file
*
*    @param {json} data
*     data to send to the python script. JSON Format only. (Non JSON will crash the program)
*
*    @param {function} returnFunction
*     function to run when ajax call is done. Function must take in variable for JSON data
*
*/
function runPythonPOST(scriptName, data, returnFunction){
    //TODO: Add code to ensure data is JSON
    $.ajax({
        type: "POST",
        url: "http://localhost:80/" + scriptName,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: data,
        success: function(data){
            returnFunction(data);
        }
    });
}
