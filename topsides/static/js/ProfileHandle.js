class ProfileHandle{
    construcor(){
        this.profiles = getProfiles();
    }

    get profiles(){
        return this.profiles;
    }

    getProfiles(){
        runPythonGET("getProfiles", null, function(data){
            profiles = data;
        });
    }

    getProfileById(id){
        for(let i = 0; i < profiles.length ; i++){
            if(profiles[i]['id'] == id){
                return profiles[i];
            }
        }
    }


    
    saveProfile(profile){

    }

    /** deleteProfile
     * 
     *  sneds ID to server for profile to delete from server
     * 
     * @param {int} id - id value for the profile
     */
    deleteProfile(id){
        runPythonPOST("deleteProfile", JSON.stringify({"profileId": id}), function(){

        });
    }
}