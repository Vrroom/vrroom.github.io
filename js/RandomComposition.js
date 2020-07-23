
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

// create a 100 randomly colored paths
for(var i=0; i<100; ++i)
{   
    //variable declaration to reference the path we create below
    var path;
    //~50% of the time we create a circle, the other times a star
    if(random() >= 0.5)
    {
        path = new Path.Circle(randomPosition(), random(10, 100))
    }
    else
    {
        var radius1 = random(10, 100)
        var radius2 = radius1 * random(1.1, 2.0)
        path = new Path.Star(randomPosition(), Math.ceil(random(3, 8)), radius1, radius2);
    }
    //assign a random fill color to the path object
    path.fillColor = Color.random();
}