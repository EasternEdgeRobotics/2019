

/*var eventSource = new EventSource("simulator/getCommand");
eventSource.onmessage = function(e){ //when stream recieves message
    console.log(e.data)
};*/


setInterval(function(){
    runPythonGET("simulator/getCommand", null, function(msg){
        console.log(msg);
        msg.forEach(function(fullString){
            let params = fullString.split(" ");
            parmas[0](params.shift());
        });
    });
}, 50);