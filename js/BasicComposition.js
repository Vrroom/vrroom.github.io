//simple composition

//create a start at the coordinate 100, 100. The Star should have 6 "spikes". 
//Inner radius of 50 and outer spike radius 100.
var star = new Path.Star(new Point(100, 100), 6, 50, 100);
star.fillColor = "yellow";

//create a rectangle
var rect = new Path.Rectangle(new Point(210, 10), new Point(390, 190));
// stroke it in blue with a stroke width of 10 and round corner joins
rect.strokeColor = "blue";
rect.strokeWidth = 10;
rect.strokeJoin = "round";

// create a red circle with a radius of 90
var circle = new Path.Circle(new Point(100, 300), 90);
circle.fillColor = "red";

// create a N-Gon centered at position 300, 300 with 10 sides and a radius of 90
var poly = new Path.RegularPolygon(new Point(300, 300), 10, 90);
poly.fillColor = "green";