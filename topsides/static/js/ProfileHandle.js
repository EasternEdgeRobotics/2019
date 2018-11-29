class ProfileHandle{

    //Constructor, runs GET for profiles and stores information (asyncronously)
    constructor(){
        var profileHandler = this;
        runPythonGET("getProfiles", null, function(data){
            profileHandler._profiles = data;
        });
    }

    //getter for profiles, therefore you can use profilehandler.profiles to get the profiles
    get profiles(){
        return this._profiles;
    }


    /** getProfileByID
     * 
     *  @description
     *      returns the JSON of the profile with that specific ID.
     * 
     *  @param {int} id: The ID of the profile to return
     * 
     * `@returns
     *      -JSON: profile json
     * 
     */
    getProfileById(id){
        for(let i = 0; i < this._profiles.length ; i++){
            if(this._profiles[i]['id'] == id){
                return this._profiles[i];
            }
        }
    }

    /** getNextId
     * 
     *  @description
     *      returns the integer of the next avaliable unique id when saving new profiles
     * 
     *  @returns
     *      next unique id
     * 
     */
    getNextId(){
        let highest = 0;
        for(let i = 0; i < this._profiles.length ; i++){
            if(this._profiles[i]['id'] >= highest){
                highest = this._profiles[i]['id'] + 1;
            }
        }
        return highest;
    }

    /** saveProfile
     * 
     *  @description
     *      Runs python post to save the new or edited profile to the JSON
     * 
     *  @param {JSON} profile - Profile JSON to save. Can be new or an edited version of an existing profile
     * 
     */
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