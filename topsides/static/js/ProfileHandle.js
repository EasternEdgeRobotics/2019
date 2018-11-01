class ProfileHandle{
    constructor(data){
        this._profiles = data;
        console.log(data);
    }

    static get profiles(){
        return this._profiles;
    }

    getProfiles(){
        
    }
    
    getProfileById(id){
        for(let i = 0; i < this._profiles.length ; i++){
            if(this._profiles[i]['id'] == id){
                return this._profiles[i];
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