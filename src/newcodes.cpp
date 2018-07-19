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

#include <tf/tf.h>

#include <gazebo_msgs/SetModelState.h>
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

     ros::Publisher gazebo_pub = nh.advertise<gazebo_msgs::ModelState>("gazebo/set_model_state", 10);
     gazebo_msgs::ModelState camera;
     camera.model_name = "vr_view";
     camera.reference_frame="world";
     ros::Time time;
     vrui_mdf::Vive vive;
     vive.user_name = "vive";
     ros::Publisher vive_state = nh.advertise<vrui_mdf::Vive>("vrui/vive", 10);

  system("rosrun gazebo_ros spawn_model -file $(find vrui_mdf)/models/vr_view/model.sdf -sdf -model vr_view -y 0 -x 0 -z 1");

  int i=0;

  while(ros::ok())
  {
  ros::spinOnce(); 
  // ros::spin() works too, but extra code can run outside the callback function between each spinning if spinOnce() is used
  
  //std::cout<<clock.clock.secs<<std::endl;
  
  vive.stamp = time.now();


  

               camera.pose.position.x = 0;
               camera.pose.position.y = 0;
               camera.pose.position.z = 1.5;
               
               geometry_msgs::Quaternion q = tf::createQuaternionMsgFromRollPitchYaw(0, 0, (float)i/1800*3.1415926);
               
               camera.pose.orientation = q;
               
               gazebo_pub.publish(camera);


  i++;
  if(i>1800){i=0;}

  r.sleep();
  }






  return 0;
}
