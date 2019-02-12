class NotificationHandler{
    
    constructor(snackbarID){
        this.snackbar = snackbarID;
        this.open = false;

        $("#"+snackbarID).toggleClass("hidden", true);

        if(typeof io != "undefined"){
            var nf = this;
            var socket = io.connect("/notification/stream");
            socket.on("notification", function(data){
                if(!nf.open){
                    console.log("yo");
                    $("#" + nf.snackbar).toggleClass("hidden", false);
                    nf.setSnackbarType(data.type);
                    nf.setSnackbarMessage(data.msg);
                    nf.open = true;
                    setTimeout(function(){
                        $("#" + nf.snackbar).toggleClass("hidden", true);
                        nf.open = false;
                    }, 3000);
                }
            });
        }else{
            console.warn("Notification Handler: SocketIO not included on page. Notifications will not be recieved.");
        }
    }

    setSnackbarType(type){
        $("#" + this.snackbar).attr("type", type);
    }

    setSnackbarMessage(msg){
        $("#" + this.snackbar).html(msg);
    }



}