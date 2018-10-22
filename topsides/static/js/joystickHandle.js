//Variable to hold joysticks connected to client
var connectedJoysticks = null


/** refreshJoysticks()
 * 
 *  @description refreshes the data of the connected joysticks
 *  @augments connectedJoysticks
 * 
 */
function refreshJoysticks(){
    connectedJoysticks = navigator.getGamepads();
    console.log(connectedJoysticks);
}


refreshJoysticks();
