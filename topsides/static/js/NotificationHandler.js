class NotificationHandler{
    constructor(){
        this._snackbarIDs = [];
    }


    get snackbars(){
        return this._snackbarIDs;
    }


    /** addSnackbar
     * 
     * @description - Registers a snackbar with the notifications. Keeps track of all ids of the snackbars. Ids must be aded before running start.
     * 
     * @param {string} elementID 
     */
    addSnackbar(elementID){
        if($("#" + elementID).hasClass("snackbar")){
            this._snackbarIDs.push(elementID);
        }
    }

    /** start
     * 
     * @description - Begins the HTTP Streaming to recieve notifications from the server
     *              - Snackbars must be added before running start
     * 
     */
    start(){
        var _snackbarIDs = this._snackbarIDs;
        
        //Creating EventSource to read stream from server
        var eventSource = new EventSource("notificationTest");
        eventSource.onmessage = function(e){ //when stream recieves message
            $.each(_snackbarIDs, function(i, id){//open registered snackbars with message
                //TODO - add message type logic
                openSnackbar(id, e.data);
            });
        };
    }



}