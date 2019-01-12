var scene;
var camera;
var renderer;

var controls;

var PoolSize = 5;

var poolCube;

function init(){
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
    camera.position.z = -10;
    
    scene.background = new THREE.Color( 0x72645b );
    
    var light = new THREE.PointLight( 0xff0000, 1, 100 );
    light.position.set( 5, 5, 5 );
    scene.add( light );

  
    poolCube = new THREE.Mesh( new THREE.BoxGeometry( PoolSize, PoolSize, PoolSize ), new THREE.MeshBasicMaterial({ color: 0x597aff, transparent: true, opacity: 0.5 }));
    scene.add( poolCube );

    var axesHelper = new THREE.AxesHelper( PoolSize+2 );
    axesHelper.position.x = -PoolSize/2;
    axesHelper.position.y = -PoolSize/2;
    axesHelper.position.z = -PoolSize/2;
    scene.add( axesHelper );


    renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );

    controls = new THREE.OrbitControls(camera);
    controls.update();

    initCurrentPoints();
    botInit();

    document.body.appendChild( renderer.domElement );

    animate();
}


function animate() {
    requestAnimationFrame( animate );

    currentPointsTick();

    controls.update();
    renderer.render(scene, camera);
};

init();

setInterval(function(){
    botTick();
}, TIME_BETWEEN_BOT_TICK);

//getCurrentAtCoord(1,1,1).energy = 100;
//getCurrentAtCoord(1,1,1).direction = new THREE.Vector3(-1,-1,-1);
//getCurrentAtCoord(1,1,1).getPointingTo();
