# vrui_mdf
"Vrui modified" for use with HTC Vive and ROS + Gazebo 


### Figur for implementation

![figure_1](https://user-images.githubusercontent.com/24307076/42660737-0c8e63b0-85fa-11e8-95ff-bbf9ec9a4d53.png)

### Demo Video 

https://www.youtube.com/watch?v=fZ7kt_WORCY

### Software:

OS:     Ubuntu 16.04<br />
ROS:    Kinetic<br />
Vrui:   4.5<br />


### Vrui:
releasing time line of vrui: <br />
http://idav.ucdavis.edu/~okreylos/

The newest version 4.5-004 was released on 05/17/2018 :<br />
http://idav.ucdavis.edu/~okreylos/ResDev/Vrui/LinkDownload.html<br />
(this package is based on Ubuntu 16.04, "Build-Ubuntu.sh" should work)

Follow the instruction on the website above to install, may need to use "sudo" to bash the script<br />


### Turtlebot_Gazebo:

Installation tutorial: <br />
http://wiki.ros.org/turtlebot/Tutorials/indigo/Turtlebot%20Installation<br />
(this package is based on Kinetic, not indigo, need to change the counterpart when installing)

### Hector_quadrotor:

	$ source /opt/ros/kinetic/setup.bash
	$ sudo apt install ros-kinetic-joystick-drivers ros-kinetic-teleop-twist-keyboard
	$ mkdir ~/catkin_ws/src
	$ rosinstall ~/catkin_ws/src /opt/ros/kinetic https://raw.githubusercontent.com/AS4SR/hector_quadrotor/kinetic-devel/tutorials.rosinstall
	$ cd ~/catkin_ws
	$ catkin_make
	$ source devel/setup.bash
for more information, go to: https://github.com/AS4SR/hector_quadrotor

### Other packages:

Xbox controller in Ubuntu:<br />
http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick

ROS installation tutorial: <br />
http://wiki.ros.org/kinetic/Installation/Ubuntu<br />
(including methods to search and install indivitual packages)<br />
Use last command in section 1.4 to seach for the correct name of the packages, and install them if needed.

### Displays setting:
	
Vive (usually named as HVR 5" in setting) needs to be set as **secondary display** on the right side of the main moniter<br />
Resolution: 1920*1200 (**16:10**)<br />
Rotation: Normal<br />
Launcher placement: Main monitor<br />
Scale all window contents to match: Main monitor<br />

The first number in the 59th line from the code of "src/imagesub" needs to be the width of the main monitor plus one, so change the resolution of the main monitor or change the number in the code.<br />

	
### Before implementation:

build the tracking node:<br />
(assume the package path is "~/catkin/src/vrui_mdf")


	$cd vrui_mdf/scripts

	$chmod +x cod_edi.py

	$cd ~/catkin_ws
	(Assume the work space is ~/catkin_ws, and the codes start reading from there)

	$rosrun vrui_mdf cod_edi.py

THen you can compile the package with:

	$cd ~/catkin_ws
	
	$catkin_make

model file path in following codes need to be changed according to the local path:<br />
tracking.cpp, controllers.cpp (all the other controllers), standingpoint.cpp, joy_hector.cpp<br />
(I'll fix this ASAP)

### Implementation:
	
	$roslaunch vrui_mdf VR_quadrotor.launch
(using **Vive controllers** to control **quadrotor**)<br />
(system button to switch between methods, right triger to assign the point)<br />

	$roslaunch vrui_mdf VR_quadrotor_outdoor.launch
(using **Vive controllers** to control **quadrotor**, with environment)<br />
(system button to switch between methods, right triger to assign the point)<br />

	$roslaunch vrui_mdf VR_quadrotor_xbox.launch
(using **xbox controller** to control **quadrotor**)<br />
(up&down button to switch between methods, right triger to assign the point)<br />


	$roslaunch vrui_mdf VR_turtlebot.launch
(using **Vive controllers** to control **turtlebot**)<br />
(system button to switch between methods, right triger to assign the point)<br />

	$roslaunch vrui_mdf VR_turtlebot_xbox.launch
(using **xbox controllers** to control **turtlebot**)<br />
(system button to switch between methods, right triger to assign the point)<br />
