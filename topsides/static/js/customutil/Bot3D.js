function $Bot3D(){

    //Initializing THREE.js
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x555555);
    var camera = new THREE.PerspectiveCamera( 10, window.innerWidth / window.innerHeight, 0.1, 60 );

    //var texture = new THREE.CanvasTexture(canvas);

    var renderer = new THREE.WebGLRenderer({alpha: true});
    renderer.setClearColor( 0xC5C5C3 );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize(window.innerWidth, window.innerHeight);

    var botMesh;
    var point = new THREE.Group();
    scene.add(point);

    var loader = new THREE.GLTFLoader();
    loader.load("/static/models/model.min.gltf", function(geo){
        geo.scene.scale.set(0.5,0.5,0.5);
        geo.scene.position.x = 0;
        geo.scene.position.y = 0;
        geo.scene.position.z = 0;
        
        botMesh = geo.scene;
        botMesh.position.y = -0.0625;
        point.add(botMesh);
    });



    camera.position.z = 3;

    var directionalLight = new THREE.DirectionalLight( 0xffffff, 0.5 );
    directionalLight.position.set(0,0,5);
    scene.add( directionalLight );

    function animate() {
        //controls.update();
        requestAnimationFrame( animate );
        renderer.render( scene, camera );
    }
    animate();


    function initSocket(){
        var socket = io.connect("/bot/telemetry");

        socket.on("data", function(data){
            point.rotation.set(data.gyroscope.x/(2*Math.PI),data.gyroscope.y/(2*Math.PI),data.gyroscope.z/(2*Math.PI));
        });
    }
    initSocket();

    



    this.appendTo = function(identify){
        var dom = $(renderer.domElement);
        dom.css("width", "100%").css("height", "100%");
        $(identify).append(dom);
    }

    return this;
}