class NotificationHandler{
    constructor(){
        this._snackbarIDs = "";
    }


    get snackbars(){
        return this._snackbarID;
    }


    /** setSnackbar
     * 
     * @description - Registers the snackbar with the notifications.  Id must be added before running start.
     * 
     * @param {string} elementID 
     */
    setSnackbar(elementID){
        if($("#" + elementID).hasClass("notification")){
            this._snackbarID = elementID;
        }
    }

    /**sendNotification
     * 
     * @description Displays a notification of a type with a message
     * 
     * @param {string} message 
     * @param {string} type
     * 
     */
    sendNotification(message, type){
        var id = this._snackbarID;
        $("#"+id).attr("class", "snackbar");
        $("#"+id).toggleClass(type, true);
        if(type != "danger"){
            //force the have to manually close
            openSnackbar(id, message);
        }else{
            openSnackbar(id, message, 0, true);
        }
    }

    /** start
     * 
     * @description - Begins the HTTP Streaming to receive notifications from the server
     *              - Snackbars must be added before running start
     * 
     */
    start(){
        var id = this._snackbarID;
        
        //Creating EventSource to read stream from server
        var eventSource = new EventSource("notificationTest");
        eventSource.onmessage = function(e){ //when stream receives message
            let data = JSON.parse(e.data); //parse data to JSON
            $("#"+id).attr("class", "snackbar");
            $("#"+id).toggleClass(data.type, true);
            if(data.type != "danger"){
                //force the have to manually close
                openSnackbar(id, data.message);
            }else{
                openSnackbar(id, data.message, 0, true);
            }
        };
    }
}