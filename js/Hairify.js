
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

// create a temporary path that we want to create "hairs" on
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
// the distance between the hairs. Change this to generate more or less hairs on the path.
var sampleDist = 10;
// we iterate until te current offset is longer than the path.
while(offset < path.length)
{
    //save the current offset and make sure it never overshoots beyond the path length
    var currentOffset = Math.min(path.length, offset);
    //get the curve location at the current offset
    var location = path.getLocationAt(currentOffset);

    //create the current hair    
    var hair = new Path();
    hair.strokeColor = Color.random();
    //add the start position of the hair, which is just the current position on the path
    hair.add(location.point);
    //add the end point of the hair. The normal is a vector that perpendicularily 
    //points away from the current position on the path. We choose a random hair length between 10 and 20.
    hair.add(location.point + location.normal * random(10, 20));
    
    //advance the offset by the sample distance to advance to the next position on the path.
    //(or exit the loop if it goes beyond the length of the path)
    offset += sampleDist;
}

// remove the temporary path that we created the hairs on
path.remove();
