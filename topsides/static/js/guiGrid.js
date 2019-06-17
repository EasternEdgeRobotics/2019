$(document).ready(function(){
    $('.grid').masonry({
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true
    });
});

var profileHandler = new ProfileHandler();
var controlOptions = new ControlOptions();
var controlHandler = new ControlHandler(controlOptions);
var notificationHandler = new NotificationHandler("notification");
profileHandler.onProfilesLoaded = function(){
    controlHandler.profile = profileHandler.profiles[0];
    // Set up profile changer
    profileHandler.profiles.forEach(function(profile){
    $(".profile-select").append("<option value='" + profile.id + "'>" + profile.name + "</option>")
    });
    $(".profile-select").change(function(){
    controlHandler.profile = profileHandler.getProfileById($(this).val());
    notificationHandler.localNotification("Profile set to " + controlHandler.profile.name, "info");
    });
}

$(document).ready(function() {
    // Set up Notification Handler
    controlHandler.registerNotificationHandler(notificationHandler);
    
    // Handle sliders
    var sliderInputs = $(".slider");
    sliderInputs.on('input', function() {
    var inputAttribute = $( this ).attr('name');
    var inputValue = $( this ).val();
    getNewSliderValues(inputAttribute, inputValue)
    });

    // Handle count down timer
    var timer = $('#startTimer');
    timer.click(function() {
    var fifteenMinutes = 60 * 15,
    display = $('#timerText');
    startCountDown(fifteenMinutes, display);
    });

    // Handle preset slider button
    var preset = $('#presetButton');
    preset.click(function() {
    var inputAttribute = ["surge", "heave", "sway", "yaw", "pitch", "roll"];
    var inputValue = $('#presetValue').val();
    getPresetValue(inputAttribute, inputValue);
    });

    // Handle present button slider enter in input
    $('#presetValue').keypress(function (e) {
    var key = e.which;
    if(key == 13) {
        $('#presetButton').click();
        return false;
    }
    });

    // Handle joystick input
    setInterval(function(){
    var controls = controlHandler.parseControlsIfChanged();
    if(controls == null) return;
    // Scaling each control based on sliders
    $.each(controls, function(control, value){
        if($("#" + control).length){
        controls[control] = value * ($("#" + control).val()/100);
        }
        if($("#pause")[0].checked != true){
        controls[control] *= 0;
        }
    });
    runPythonPOST("sendControlValues", JSON.stringify(controls), function(){});
    }, 30);
});