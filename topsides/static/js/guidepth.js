// initializers!
var depth = 0.0;
var rovPosition = 0;
var lockDepth = 0.0;

// set up the positioning dot!
var dot = document.getElementById("dot");
var dotDot = dot.getContext("2d");
dotDot.beginPath();
dotDot.arc(10,10,10, 0, 2*Math.PI);
dotDot.fillStyle = "red";
dotDot.fill();
dotDot.stroke();

document.getElementById("depthDisplay").innerHTML = depth + " m";

// bring dot closer to bottom by 10 cm
function increment()
{
	depth = (depth * 10 + 0.1 * 10) / 10;
	rovPosition = rovPosition + 11;
	if (depth > 3.0)
	{
		depth = (depth * 10 - 0.1 * 10) / 10;
		rovPosition = rovPosition - 11;
	}
	dotDot.fillStyle = "red";
	dotDot.fill();
	dotDot.stroke();
	document.getElementById("depthDisplay").innerHTML = depth + " m";
	document.getElementById("dot").style.top = rovPosition + "px";
}

// bring dot closer to surface by 10 cm
function decrement()
{
	depth = (depth * 10 - 0.1 * 10) / 10;
	rovPosition = rovPosition - 11;
	if (depth < 0)
	{
		depth = (depth * 10 + 0.1 * 10) / 10;
		rovPosition = rovPosition + 11;
	}
	dotDot.fillStyle = "red";
	dotDot.fill();
	dotDot.stroke();
	document.getElementById("depthDisplay").innerHTML = depth + " m";
	document.getElementById("dot").style.top = rovPosition + "px";
}

// set rov's course to location of red dot
function lockdepth()
{
	lockDepth = depth;
	dotDot.fillStyle = "#b50052";
	dotDot.fill();
	dotDot.stroke();
}

//set position to surface
function surface()
{
	depth = 0;
	rovPosition = 0;
	
	dotDot.fillStyle = "red";
	dotDot.fill();
	dotDot.stroke();
	
	document.getElementById("depthDisplay").innerHTML = depth + " m";
	document.getElementById("dot").style.top = rovPosition + "px";
}

// set position to bottom of pool
function bottom()
{
	depth = 3;
	rovPosition = 334;
	
	dotDot.fillStyle = "red";
	dotDot.fill();
	dotDot.stroke();
	
	document.getElementById("depthDisplay").innerHTML = depth + " m";
	document.getElementById("dot").style.top = rovPosition + "px";
}

// tell rov to stop following the dot
function unlock()
{
	dotDot.fillStyle = "red";
	dotDot.fill();
	dotDot.stroke();
}