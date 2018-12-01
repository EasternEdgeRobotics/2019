class NotificationHandler{
    constructor(){
        this._snackbarIDs = "";
    }


    get snackbars(){
        return this._snackbarID;
    }


    /** addSnackbar
     * 
     * @description - Registers a snackbar with the notifications. Keeps track of all ids of the snackbars. Ids must be aded before running start.
     * 
     * @param {string} elementID 
     */
    setSnackbar(elementID){
        if($("#" + elementID).hasClass("notification")){
            this._snackbarID = elementID;
        }
    }

    /** start
     * 
     * @description - Begins the HTTP Streaming to recieve notifications from the server
     *              - Snackbars must be added before running start
     * 
     */
    start(){
        var id = this._snackbarID;
        
        //Creating EventSource to read stream from server
        var eventSource = new EventSource("notificationTest");
        eventSource.onmessage = function(e){ //when stream recieves message
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