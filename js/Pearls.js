
// helper function to get a random point inside the project canvas
// (i.e. the view on the right)
function randomPosition()
{
    return project.view.size * Point.random();
}

// helper function to get a radom number in the range _min to _max
function random(_min = 0, _max = 1)
{
    return _min + Math.random() * (_max - _min);
}

// create a path that represents the string we put the pearls on
var string = new Path();
string.strokeColor = "black";
string.strokeWidth = 2.0;

// add 20 random positions
for(var i = 0; i < 20; ++i)
{
    string.add(randomPosition())
}
// smooth the path so we get a nicely rounded curve
string.smooth();

// the following code iterates over the path in a certain interval to create the pearls
// =====================================================================================
// variable holding the current offset on the path
var offset = 0;
// the distance between the pearls
var sampleDist = 30;
// we iterate until te current offset is longer than the path.
while(offset < string.length)
{
    //save the current offset and make sure it never overshoots beyond the path length
    var currentOffset = Math.min(string.length, offset);
    //create the current pearl at the sample position   
    var pearl = new Path.Circle(string.getPointAt(offset), random(5, 10));
    //color it with a random color
    pearl.fillColor = Color.random();

    //advance the offset by the sample distance to advance to the next position on the path.
    //(or exit the loop if it goes beyond the length of the path)
    offset += sampleDist;
}
