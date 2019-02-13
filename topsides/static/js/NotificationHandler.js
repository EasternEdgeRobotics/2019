class NotificationHandler{
    
    constructor(snackbarID){
        this.snackbar = snackbarID;
        this.open = false;
        this.timeout = null;

        $("#"+snackbarID).toggleClass("hidden", true);

        if(typeof io != "undefined"){
            var nf = this;
            var socket = io.connect("/notification/stream");
            socket.on("notification", function(data){
                nf.localNotification(data.message, data.type);
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

    localNotification(msg, type){
        if(this.open && type != "danger" && type != "warning")
            return

        if(this.timeout != null)
            clearTimeout(this.timeout);
        
        this.setSnackbarMessage(msg);
        this.setSnackbarType(type);
        $("#" + this.snackbar).toggleClass("hidden", false);
        this.open = true;


        var nf = this;
        if(type == "danger"){
            var btn = $("<button class='btn btn-link'>Dismiss</button>").on("click", function(){
                nf.dismissNotification();
            });
            $("#"+this.snackbar).append(btn);
        }else{
            this.timeout = setTimeout(function(){
                nf.dismissNotification();
                nf.timeout = null;
            }, 3000);
        }

        
    }

    globalNotification(msg, type){
        runPythonPOST("notification/send", JSON.stringify({message: msg, type: type}), function(){});
    }

    dismissNotification(){
        $("#"+this.snackbar).toggleClass("hidden", true);
        this.open = false;
    }
}