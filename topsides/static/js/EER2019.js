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


/**
 *  @name Snackbar
 *  @author Troake
 * 
 *  @description - Bar at the bottom of a page to appear when wanted for an amount of time
 * 
 * HOW TO USE:
 *      1. Create a div with the [.snackbar] class and any ID of your choice
 * 
 * NOTE:
 *      - For the system notifications, set the id of the snackbar to notification.
 *          This will automatically link it to the incoming notifications
 */
$(document).ready(function(){
    $(".snackbar").html("<div class='snack'></div>");
});


/**openSnackbar
 * 
 *  opens a snackbar of an id with a message for an amount of time (ms)
 */
function openSnackbar(id, message, time=3000, requireExit = false){
    $('.snackbar').toggleClass('visible', false);
    $.each($('.snackbar'), function (i, obj) {
        if($(obj).attr('id') == id){
            $(obj).toggleClass('visible', true);
            $(obj).find(".snack").html("<p>" + message + "</p>");
            if(!requireExit){
                setTimeout(function(){$(obj).toggleClass('visible', false)}, time);
            }else{
                $(obj).find(".snack").append("<span onclick='closeSnackbar(" + '"' + id + '"' + ")'>&times</span>");
            }
        }
    });
}

function closeSnackbar(id){
    $.each($('.snackbar'), function (i, obj) {
        if($(obj).attr('id') == id){
            $(obj).toggleClass('visible', false);
        }
    });
}


/**
 *  @name Snackbar
 *  @author Keif/Troake
 * 
 *  @description - Bar at the bottom of any page to appear when wanted for an amount of time
 * 
 * HOW TO USE:
 *      1. Create a div with the [.snackbar] class and any ID of your choice
 * 
 * NOTE:
 *      - For the system notifications, set the id of the snackbar to notification.
 *          This will automatically link it to the incoming notifications
 */
$(document).ready(function() {
        var note = new NotificationHandler();
        note.setSnackbar('notification');
        note.start();
    }
);