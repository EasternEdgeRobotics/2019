class ProfileHandler{

    //Constructor, runs GET for profiles and stores information (asynchronously)
    constructor(){
        var profileHandler = this;
        var xhr = runPythonGET("getProfiles", null, function(data){
            profileHandler._filesize = xhr.getResponseHeader("Content-Length")*3; //filesize (*3 adjusts for whitespace)
            profileHandler._profiles = data;
            if(profileHandler._onProfileLoad != null){
                profileHandler._onProfileLoad(data);
            }
        });
    }

    //getter for profiles, therefore you can use profilehandler.profiles to get the profiles
    get profiles(){
        return this._profiles;
    }

    get fileSize(){
        return this._filesize;
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
     *      returns the integer of the next available unique id when saving new profiles
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
     *  sends ID to server for profile to delete from server
     * 
     * @param {int} id - id value for the profile
     */
    deleteProfile(id){
        runPythonPOST("deleteProfile", JSON.stringify({"profileId": id}), function(){

        });
    }

    /** profilesLoaded
     * 
     *  @description
     *      setter for a function that will run when the handler finishes loading profiles from the server
     *      if the profiles are already loaded, the function will run
     */
    set onProfilesLoaded(func){
        this._onProfileLoad = func;
        if(this._profiles != null)
            this._onProfileLoad();
    }

}