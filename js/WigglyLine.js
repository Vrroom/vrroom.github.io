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

// create the base path that we want to wigglify
var path = new Path();
// add 20 random positions
for(var i = 0; i < 20; ++i)
{
    path.add(randomPosition())
}
// smooth the path so we get a nicely rounded curve
path.smooth();

// the following code iterates over the path in a certain interval to create the "hairs"
// =====================================================================================
// variable holding the current offset on the path
var offset = 0;
// the distance between the positions samples. lowering this will make the line more jittery.
var sampleDist = 50;
// create the path object for the wiggly line and color the stroke red
var wigglyPath = new Path();
wigglyPath.strokeColor = "red"
// we iterate until te current offset is longer than the path.
while(offset < path.length)
{
    //save the current offset and make sure it never overshoots beyond the path length
    var currentOffset = Math.min(path.length, offset);
    //get the curve location at the current offset
    var location = path.getLocationAt(currentOffset);
    //generate a position that is close to the path (-6 to 6 pixels apart) based on the originals
    //paths position and normal (normal is a vector perpendicular to the path)   
    wigglyPath.add(location.point + location.normal * random(-6, 6));
    //advance the offset by the sample distance to advance to the next position on the path.
    //(or exit the loop if it goes beyond the length of the path)
    offset += sampleDist;
}
wigglyPath.smooth();