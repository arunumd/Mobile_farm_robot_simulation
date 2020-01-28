# A Python based simple navigation algorithm for a mobile robotic rover in a hydrophonic lab

The Rover  in this project is a fictional point robot that is charecterized as a mobile agent which can move between target locations based on path
waypoints. The paths and target locations are predefined in a `.json` file available in the `maps` directory in this project. The robot can handle
various tasks ranging from
- going to a charging station for recharging the batteries; and
- going to a commanded row location in a cropland (a.k.a field in this project);

The user can also ask the robot to plant a specific crop in a specific row of a field through the commandline. The robot goes to every target
location by the shortest path using a euclidean distance based heuristic. The robot's navigation is characterized as one step for every second.

## About the Author

Arun Kumar Devarajulu is a Robotics graduate from University of Maryland, College Park. He has a wide range of interests in Robotics and Computer Vision,
ranging from development of path planning algorithms, robotic simulation, deep learning, software development using agile practices, etc.

## License

This project is release under the MIT License
                                                   
