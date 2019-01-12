
/*

    ____                   _    _____           _       __      
   / __ \____ __________  (_)  / ___/__________(_)___  / /______
  / /_/ / __ `/ ___/ __ \/ /   \__ \/ ___/ ___/ / __ \/ __/ ___/
 / _, _/ /_/ (__  ) /_/ / /   ___/ / /__/ /  / / /_/ / /_(__  ) 
/_/ |_|\__,_/____/ .___/_/   /____/\___/_/  /_/ .___/\__/____/  
                /_/                          /_/               
                
                
*/


function fControl(params){
    tChan = params[0];
    tSpeed = params[1];
    PORTS = ["aft-star-vert", "fore-port-vert", "fore-star-vert", "fore-star-horz", "fore-port-horz", "aft-port-vert", "aft-port-horz", "aft-star-horz"];
    thrusters[PORTS[tChan]] = tSpeed;
}