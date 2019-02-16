/*var eventSource = new EventSource("simulator/getCommand");
eventSource.onmessage = function(e){ //when stream receives message
    console.log(e.data)
};*/


setInterval(function(){
    runPythonGET("simulator/getCommand", null, function(msg){
        msg.forEach(function(fullString){
            let params = fullString.split(" ");
            let func = params[0].slice(0, -3);
            params.shift();
            RaspiScripts[func](params);
        });
    });
}, 50);