function $Bot3D(){

    //Initializing THREE.js
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(0x555555);
    var camera = new THREE.PerspectiveCamera( 10, window.innerWidth / window.innerHeight, 0.1, 1000 );

    //var texture = new THREE.CanvasTexture(canvas);

    var renderer = new THREE.WebGLRenderer({alpha: true});
    renderer.setClearColor(0xffffff, 0);
    renderer.setSize( window.innerWidth, window.innerHeight );

    var botMesh;

    var loader = new THREE.STLLoader();
    loader.load("/static/models/Calypso.stl", function(geo){
        var material = new THREE.MeshPhongMaterial({color: 0x0011ff, specular: 0x111111, shininess: 200});
        botMesh = new THREE.Mesh(geo, material);
        botMesh.position.set(0,0,0);
        botMesh.scale.set(0.1,0.1,0.1);
        botMesh.receiveShadow = true;
        botMesh.castShadow = true;

        scene.add(botMesh);
    });



    camera.position.z = 500;

    var directionalLight = new THREE.DirectionalLight( 0xffffff, 0.5 );
    directionalLight.position.set(0,100,300);
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
            botMesh.rotation.set(data.accelerometer.x/(2*Math.PI),data.accelerometer.y/(2*Math.PI),data.accelerometer.y/(2*Math.PI));
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