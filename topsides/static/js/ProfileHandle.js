class ProfileHandle{
    constructor(data){
        this._profiles = data;
    }

    get profiles(){
        return this._profiles;
    }
    
    getProfileById(id){
        for(let i = 0; i < this._profiles.length ; i++){
            if(this._profiles[i]['id'] == id){
                return this._profiles[i];
            }
        }
    }

    getNextId(){
        let highest = 0;
        for(let i = 0; i < this._profiles.length ; i++){
            if(this._profiles[i]['id'] >= highest){
                highest = this._profiles[i]['id'] + 1;
            }
        }
        return highest;
    }

    
    saveProfile(profile){
        runPythonPOST("saveProfile", JSON.stringify(profile), function(){

        });
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