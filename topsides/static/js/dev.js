/** getDevInput
 *
 *  gets the values from the dev input textbox for the server
 */
function getDevInput(inputValue) {
  runPythonPOST("devinput", JSON.stringify(inputValue), function(){
      console.log("new dev input has been sent to server");
  });
}
