var gamepads = navigator.getGamepads();

for(let i = 0 ; i < gamepads.length; i++){
    if(gamepads[i] != null){
        console.log(gamepads[i]);
    }
}