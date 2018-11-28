/**
 *  Gets the values from the dev input textbox for the server.
 *
 *  @param {string} inputValue - string value from textarea
 */
function getDevInput(inputValue) {
  runPythonPOST("devinput", JSON.stringify(inputValue), function(){
      console.log("new dev input has been sent to server");
  });
}
