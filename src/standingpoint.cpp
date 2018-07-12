/*



*/
#include <stdlib.h>
#include<iostream>
#include<fstream>

#include <ros/ros.h>
#include <vrui_mdf/Vive.h>

#include "std_msgs/String.h"
#include <tf/transform_broadcaster.h>  // translation between Eular angle and Quaternion, unnecessary for tracking since Quaternion can be received directly
#include "tf/transform_datatypes.h"
#include <geometry_msgs/Twist.h>
#include <gazebo_msgs/SetModelState.h>
#include "gazebo_msgs/GetModelState.h"
#include "gazebo_msgs/DeleteModel.h"
#include "gazebo_msgs/SpawnModel.h"

// define callback function in a class so that data running inside the class can be used globally
class Vive_Listener
{
public:
	  vrui_mdf::Vive vive;

	  void callback(const vrui_mdf::Vive& msg)
	    {
		vive = msg;
	    }
};



class ThrowMethod
{
public:
	gazebo_msgs::ModelState throw_state;

	gazebo_msgs::ModelState standingpoint;

	gazebo_msgs::ModelState base_point;

        gazebo_msgs::SpawnModel sm;

	gazebo_msgs::DeleteModel deletemodel;

	int trigger;// 0

	std::string standingpoint_name;//"standingpoint"

	std::string model_name; //"mobile_base"

	bool once;

	ros::ServiceClient delete_model;
        ros::ServiceClient spawn_model;

   	void readmodel(const char* path)
	  {

		std::ifstream ifs;
		ifs.open(path);
		std::stringstream stringstream;
    		stringstream << ifs.rdbuf();
  		sm.request.model_name = standingpoint_name;
  		sm.request.model_xml = stringstream.str();
    		sm.request.robot_namespace = ros::this_node::getNamespace();
    		sm.request.reference_frame = "world";

	  }

	void controller(const vrui_mdf::Vive& vive)
	  {
		if(trigger==0 & (int)vive.ctrl_left.buttons.trigger == 1)
		  {
			spawn_model.call(sm);
			trigger = 1;
		  }
		
		if((int)vive.ctrl_left.buttons.trigger == 1)
		  {
			double roll, pitch, yaw;
                        tf::Quaternion Qua(vive.ctrl_left.pose.orientation.x,vive.ctrl_left.pose.orientation.y,vive.ctrl_left.pose.orientation.z,vive.ctrl_left.pose.orientation.w);
			tf::Matrix3x3 m(Qua); //rotation matrix from Quaternion
			m.getRPY(roll, pitch, yaw); //eular angle form rotation matrix

			standingpoint.model_name = standingpoint_name;
			standingpoint.reference_frame="world";

			standingpoint.pose.position.x = vive.ctrl_left.pose.position.x - 2*(m[0][0]*vive.ctrl_left.pose.position.z);
			standingpoint.pose.position.y = vive.ctrl_left.pose.position.y - 2*(m[1][0]*vive.ctrl_left.pose.position.z);
			standingpoint.pose.position.z = 0;

			standingpoint.pose.orientation.x = 0;
			standingpoint.pose.orientation.y = 0;
			standingpoint.pose.orientation.z = 0;
			standingpoint.pose.orientation.w = 1;
		  }

		if(trigger==1 & (int)vive.ctrl_left.buttons.trigger == 0)
		  {
			
			throw_state.pose.position.x = standingpoint.pose.position.x + base_point.pose.position.x - vive.headset.position.x;
			throw_state.pose.position.y = standingpoint.pose.position.y + base_point.pose.position.y - vive.headset.position.y;

			throw_state.pose.position.z = 0;
			throw_state.model_name = model_name;

			once = true;
                        trigger=0;

			deletemodel.request.model_name = standingpoint_name;

			//delete_model.call(deletemodel);


		  }
	  }

};



	




int main(int argc, char **argv)
{
  // setup ros node
  ros::init(argc, argv, "standingpoint");
  ros::NodeHandle nh;

  ros::Rate r(90);
  ros::service::waitForService("/gazebo/spawn_urdf_model", -1);
  //define class for callback class and subscriber
  Vive_Listener vive_data;
  ros::Subscriber sub_vive = nh.subscribe("vrui/vive", 1, &Vive_Listener::callback, &vive_data);



    ros::Publisher gazebo_pub = nh.advertise<gazebo_msgs::ModelState>("gazebo/set_model_state", 10);
    gazebo_msgs::ModelState controller_left,controller_right,controller_throw,controller_line;

    controller_left.model_name = "Vive_Controller_left";
    controller_left.reference_frame="world";

    controller_right.model_name = "Vive_Controller_right";
    controller_right.reference_frame="world";


	ros::ServiceClient client = nh.serviceClient<gazebo_msgs::GetModelState>("/gazebo/get_model_state");
	gazebo_msgs::GetModelState getmodelstate;
	getmodelstate.request.model_name = "base_test";


    /* previous value */
    vrui_mdf::Vive vive_previ;

    /* controller 3 */
    ThrowMethod ThrowTo;
    ThrowTo.trigger = 0;
    ThrowTo.standingpoint_name = "standingpoint";
    ThrowTo.model_name = "base_test";
    ThrowTo.once = false;
    ThrowTo.delete_model = nh.serviceClient<gazebo_msgs::DeleteModel>("/gazebo/delete_model");
    ThrowTo.spawn_model = nh.serviceClient<gazebo_msgs::SpawnModel>("/gazebo/spawn_sdf_model");
    ThrowTo.readmodel("/home/zhenyushi/.gazebo/models/controller/model.sdf");


    system("rosrun gazebo_ros spawn_model -file ~/.gazebo/models/Vive_Controller/model.sdf -sdf -model Vive_Controller_left -y 0 -x 0 -z 3");
    system("rosrun gazebo_ros spawn_model -file ~/.gazebo/models/Vive_Controller/model.sdf -sdf -model Vive_Controller_right -y 0 -x 0 -z 3");






  while(ros::ok())
  {
  ros::spinOnce(); 
  // ros::spin() works too, but extra code can run outside the callback function between each spinning if spinOnce() is used


  controller_left.pose = vive_data.vive.ctrl_left.pose;
  controller_right.pose = vive_data.vive.ctrl_right.pose;
  gazebo_pub.publish(controller_left); 
  gazebo_pub.publish(controller_right); 


	client.call(getmodelstate);
	ThrowTo.base_point.pose = getmodelstate.response.pose;


	ThrowTo.controller(vive_data.vive);
	if(ThrowTo.trigger){gazebo_pub.publish(ThrowTo.standingpoint);}
	if(ThrowTo.once)
	  {
		gazebo_pub.publish(ThrowTo.throw_state);
		ThrowTo.once = false;
	  }




  /* over write previous value  */
  vive_previ = vive_data.vive;

  r.sleep();
  }

  return 0;
}









