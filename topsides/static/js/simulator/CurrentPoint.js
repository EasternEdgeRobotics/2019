const MAX_ARROW_LENGTH = 0.6;
const ZERO_ENERGY = 0.01;

const CurrentDistance = 0.5;

class CurrentPoint{
	constructor(x, y, z){
		this._x = x;
		this._y = y;
		this._z = z;
		this._energy = ZERO_ENERGY;
		this._direction = new THREE.Vector3(1,0,0);
		this._arrow = new THREE.ArrowHelper(this._direction, new THREE.Vector3(x,y,z), this._energy, 0xffffff);
		
		this.time = 0;
		
		scene.add(this._arrow);
	}
	
	get x() {
		return this._x;
	}
	
	get y() {
		return this._y;
	}
	
	get z() {
		return this._z;
	}
	
	get energy() {
		return this._energy;
	}
	
	set energy(i){
		i > 100 ? i = 100 : null;
		i < 0 ? i = 0 : null;
		this._energy = i/100;
	}
	
	set direction(d){
		this._direction = d.normalize();
	}

	get direction(){
		return this._direction;
	}
	
	tick(){
		if(this._arrow.visible){
			this.time++;
			
			//this._direction.x = Math.cos(this.time*0.005);
			//this._direction.y = Math.sin(this.time*0.005);
			this._arrow.setLength(this.energy*MAX_ARROW_LENGTH);
			this._arrow.setDirection(this._direction);
		}

		if(this._energy > ZERO_ENERGY){
			this._arrow.visible = true;
		}else{
			this._arrow.visible = false;
		}
	}

	getPointingTo(){
		return getNearbyCurrents(this._x + this._direction.x, this._y + this._direction.y, this._z + this._direction.z);
	}
}


/*

STATIC STUFF

*/
CurrentPoints = [];

function createCurrent(x,y,z){
	CurrentPoints.push(new CurrentPoint(x,y,z));
}

function getCurrentAtCoord(x,y,z){
	console.log("x: " + x*(PoolSize/CurrentDistance));
	console.log("y: " + y*(PoolSize/CurrentDistance));
	console.log("z: " + z*(PoolSize/CurrentDistance));
	return CurrentPoints[x*(PoolSize/CurrentDistance) * (PoolSize/CurrentDistance+1)*(PoolSize/CurrentDistance+1) + y*(PoolSize/CurrentDistance)*(PoolSize/CurrentDistance+1) + z*(PoolSize/CurrentDistance)];
}

function getNearbyCurrents(x,y,z){
	var points = [];

	let xDif = x % CurrentDistance;
	let yDif = y % CurrentDistance;
	let zDif = z % CurrentDistance;
	for(let x1 =  x - xDif ; x1 <= x + (x - xDif) ; x1 += CurrentDistance){
		for(let y1 =  y - yDif ; y1 <= y + (y - yDif) ; y1 += CurrentDistance){
			for(let z1 =  z - zDif ; z1 <= z + (z - zDif) ; z1 += CurrentDistance){
				console.log("yeah");
				let percentLoc = ThreeCoordToPercent(x1, y1, z1);
				current = getCurrentAtCoord(percentLoc.x, percentLoc.y, percentLoc.z);
				if(current != null){
					current._arrow.setColor(new THREE.Color(0xff0000));
					current.energy = 100;
					points.push(current);
				}
			}
		}	
	}

	return points;
}

function initCurrentPoints(){
	for(let x  = -PoolSize/2; x <= PoolSize/2; x += CurrentDistance){
		for(let y  = -PoolSize/2; y <= PoolSize/2; y+= CurrentDistance){
			for(let z  = -PoolSize/2; z <= PoolSize/2; z+= CurrentDistance){
				createCurrent(x,y,z);
			}
		}
	}
}

function currentPointsTick(){
	CurrentPoints.forEach(function(current) {
		current.tick();
	});
}

function ThreeCoordToPercent(x, y, z){
	return {x: (x+PoolSize/2)/PoolSize, y:(y+PoolSize/2)/PoolSize, z:(z+PoolSize/2)/PoolSize};
}