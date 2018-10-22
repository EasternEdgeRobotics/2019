
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
        url: "http://localhost:5000/" + scriptName,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: data,
        success: function(data){
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
        url: "http://localhost:5000/" + scriptName,
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





 


 /*


    _____          _                    __  __           _       _           
  / ____|        | |                  |  \/  |         | |     | |          
 | |    _   _ ___| |_ ___  _ __ ___   | \  / | ___   __| |_   _| | ___  ___ 
 | |   | | | / __| __/ _ \| '_ ` _ \  | |\/| |/ _ \ / _` | | | | |/ _ \/ __|
 | |___| |_| \__ \ || (_) | | | | | | | |  | | (_) | (_| | |_| | |  __/\__ \
  \_____\__,_|___/\__\___/|_| |_| |_| |_|  |_|\___/ \__,_|\__,_|_|\___||___/
                                                                           
 


 */
$(document).ready(function(){

    /**
     *  @name  Modal
     *  @author Troake 
     * 
     *  @description Modals are popup panels that overlay content. These can be used as a user-frendly
     *               input menu. Like a login popup.
     * 
     *  HOW TO USE:
     *      1. Create a div with the [modal] class and any ID of your choice
     *      2. Create a div inside of the previous div with the class [modal-content]
     *      3. Create an element to use as a trigger to open the modal (ex: button)
     *          - give that element the [modal-trigger] class
     *          - set the atrribute [modal-id] of that element to the id of the div in step 1.
     *  
     */
    $(".modal-content").prepend("<span class='modal-close'>&times</span>"); //adds X to close modal
    $(".modal-trigger").click(function(){ //click event for modal triggers
        var modalID = $(this).attr("modal-id");
        $("#"+modalID).toggleClass("visible", true);
    });
    $(".modal, .modal-close").click(function(){ //click event to close modals (whenblack overlay is clicked.
        $(this).toggleClass("visible", false);
        $(this).parents(".modal").toggleClass("visible", false);
    });

    $(".modal *").click(function(e){ //event to cancel previous event if child inside modal (aka content) is clicked.
        e.stopPropagation();
    });
});




