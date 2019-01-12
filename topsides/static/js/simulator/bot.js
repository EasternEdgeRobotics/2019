var botCube;

const BOT_WIDTH = 0.550;//m
const BOT_LENGTH = 0.530;//m
const BOT_HEIGHT = 0.300;//m

const BOT_WEIGHT = 14.0; //kg

const MAX_THRUST = 34.65; //N

const TIME_BETWEEN_BOT_TICK = 50; //ms

var VelX = 0; // m/s
var VelY = 0; // m/s
var VelZ = 0; // m/s

var RotateX = 0;
var RotateY = 0;
var Rotatez = 0;


/*
var AccX = 0;
var AccY = 0;
var AccZ = 0;
*/

//z - fore/aft
//x - port/star
//thrust - -1 to 1
var thrusters = {
    "fore-star-vert": {
        x: 0,
        y: 1,
        z: 1,
        direction: new THREE.Vector3(0,1,0).normalize(),
        thrust: 0
    },
    "fore-port-vert": {
        x: 1,
        y: 1,
        z: 1,
        direction: new THREE.Vector3(0,1,0).normalize(),
        thrust: 0
    },
    "aft-star-vert": {
        x: 0,
        y: 1,
        z: 0,
        direction: new THREE.Vector3(0,1,0).normalize(),
        thrust: 0
    },
    "aft-port-vert": {
        x: 1,
        y: 1,
        z: 0,
        direction: new THREE.Vector3(0,1,0).normalize(),
        thrust: 0
    },

};


function botInit(){
    botCube = new THREE.Mesh(new THREE.BoxGeometry(BOT_WIDTH,BOT_HEIGHT,BOT_LENGTH), new THREE.MeshBasicMaterial({color: 0xffffff}));
    scene.add(botCube);
}


function botTick(){
    var AccY = 0;
    $.each(thrusters, function(name, values){
        if(name.includes("vert")){
            AccY += values.thrust/BOT_WEIGHT;
        }
    });
    
    VelX += AccY;

    botCube.y += VelX * TIME_BETWEEN_BOT_TICK;
}