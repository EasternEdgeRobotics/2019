class NotificationHandler{
    constructor(){
        this._snackbarIDs = [];
        this.handleNotifications();
    }


    get snackbars(){
        return this._snackbarIDs;
    }

    addSnackBar(elementID){
        if($("#" + elementID).hasClass('snackbar')){
            this._snackbarIDs.push(elementID);
        }
    }

    
    handleNotifications(){
        /*var client = new XMLHttpRequest();
        client.open('get', 'notificationTest');
        client.send();
        client.onprogress = function(){
            console.log(this.responseText);              
        }*/
        var eventSource = new EventSource("notificationTest");
        eventSource.onmessage = function(e){
            console.log(e.data);
        };
    }



}