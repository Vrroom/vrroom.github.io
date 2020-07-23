//create 4 overlapping circles in CMYK
var a = new Path.Circle(new Point(100, 100), 90);
a.fillColor = "cyan";
var b = new Path.Circle(new Point(110, 110), 90);
b.fillColor = "yellow";
var c = new Path.Circle(new Point(120, 120), 90);
c.fillColor = "magenta";
var d = new Path.Circle(new Point(130, 130), 90);
d.fillColor = "black";

//using the insertBelow function, we reverse their order.
b.insertBelow(a);
c.insertBelow(b);
d.insertBelow(c);