var profiles = null;

var profileToEdit = null;


$(document).ready(function(){
    getProfiles();
});


function getProfiles(){
    runPythonGET("getProfiles", null, function(data){
        profiles = data;
        console.log(profiles);
    });
}


/**
 * 
 * @param {int} id - id value for the profile
 *  
 */
function editProfile(id){
    setProfileEiitPanel(id);
    openProfileEditPanel();
}


function setProfileEiitPanel(id){
    profileToEdit = getProfileById(id);

}

function clearProfile(){

}


function openProfileEditPanel(){
    $("#panelEditProfile").toggleClass("hidden", false);
}

function closeProfileEditPanel(){
    $("#panelEditProfile").toggleClass("hidden", true);
}

function getProfileById(id){
    for(let i = 0; i < profiles.length ; i++){
        if(profiles[i]['id'] == id){
            return profiles[i];
        }
    }
}

/** deleteProfile
 * 
 *  sneds ID to server for profile to delete from server
 * 
 * @param {int} id - id value for the profile
 */
function deleteProfile(id){
    runPythonPOST("deleteProfile", JSON.stringify({"profileId": id}), function(){

    });
}