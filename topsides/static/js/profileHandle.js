var profiles;


$(document).ready(function(){
    profiles = getProfiles();
    console.log(profiles);
});

function getProfiles(){
    var response = $.ajax({
        type: "GET",
        url: "http://localhost:5000/getProfiles",
        dataType: "json",
        async: false
    }).responseText;

    return JSON.parse(response);
}


/**
 *
 * @param {int} id - id value for the profile
 *
 */
function editProfile(id){

}


/**
 *
 * @param {int} id - id value for the profile
 */
function deleteProfile(id){
    $.ajax({
        type: "GET",
        url: "http://localhost:5000/deleteProfile?profileID=" + id,
        dataType: "json",
        success: function(data){
            returnFunction(data);
        }
    });
}
