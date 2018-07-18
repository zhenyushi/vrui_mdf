/*

Vrui_mdf/imagesub - Node to subscribe images from the camera modle in Gazebo
It will subscribe the images for both the left eye and right eye, and stitch 
the images together, having the left eye image on the left side and the right 
eye image on the right side. 

Potentially, this node can also subscribe for the button states from the controllers
and switch display mode or display different iamge on the Vive headset, like the 
first person view of the turtlebot.

*/

#include <stdlib.h>
#include <ros/ros.h>
#include "std_msgs/String.h"

#include <rosgraph_msgs/Clock.h>

#include "vrui_mdf.h"
#include <vrui_mdf/Vive.h>

// define callback function in a class so that data running inside the class can be used globally



class Listener_ctrlMethod
{
public:

	std::string control_method;

	void chatterCallback(const std_msgs::String::ConstPtr& msg)
	{
	   control_method = msg->data.c_str();
	}

};


int main(int argc, char **argv)
{
  // setup ros node
  ros::init(argc, argv, "listener_class");
  ros::NodeHandle nh;
  
  ros::Rate r(100);

  

  vrui_mdf::Vive vive;

  ros::Time time;
  std::cout<<vive<<std::endl;

  while(ros::ok())
  {
  ros::spinOnce(); 
  // ros::spin() works too, but extra code can run outside the callback function between each spinning if spinOnce() is used
  
  //std::cout<<clock.clock.secs<<std::endl;
  
  vive.stamp = time.now();
  std::cout<<vive<<std::endl;

  r.sleep();
  }






  return 0;
}
