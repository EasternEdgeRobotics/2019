/**runPythonGET
*
*    @params
*        scriptName:
*            -the name of the function to run. Declared in the @app.route in python file
*
*        data:
*            - data to send to the python script. JSON Format only. (Non JSON will crash the program)
*
*        returnFunction:
*            -function to run when ajax call is done. Function must take in variable for JSON data
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



/** runPythonPOST
*
*    @params
*        scriptName:
*            -the name of the function to run. Declared in the @app.route in python file
*
*        data:
*            - data to send to the python script. JSON Format only. (Non JSON will crash the program)
*
*        returnFunction:
*            -function to run when ajax call is done. Function must take in variable for JSON data
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


//TODO --------------------------------------------------------------------------------------


/** HandleSliderValues
 *
 *  Empty function for handling slider values.
 *  joystick values will be handled on the server side (Python)
 *
 */
function HandleSliderValues(){

}




 /** GetAllValues
  *
  *  Cleaner function to run a GET command to server and return all nessessary values in a single server call
  *  instead of all seperate.
  *
  */
 function GetAllValues(){

 }
