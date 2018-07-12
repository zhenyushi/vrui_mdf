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
#include <sensor_msgs/Joy.h>

// define callback function in a class so that data running inside the class can be used globally


class Joy_Listener
{
public:
	void joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
	{

		for(int i=0; i<11;++i)
		{
			if(i<8){  axes[i] = joy->axes[i];}
			buttons[i] = joy->buttons[i];		
		}

	}

	float axes[8];
	int buttons[11];

};


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

	gazebo_msgs::ModelState waypoint;

        gazebo_msgs::SpawnModel sm;

	gazebo_msgs::DeleteModel deletemodel;

	int trigger;// 0

	std::string waypoint_name;//"waypoint"

	std::string model_name; //"mobile_base"

	bool once;

        int scale;
	double yaw_headset;

	ros::ServiceClient delete_model;
        ros::ServiceClient spawn_model;

   	void readmodel(const char* path)
	  {

		std::ifstream ifs;
		ifs.open(path);
		std::stringstream stringstream;
    		stringstream << ifs.rdbuf();
  		sm.request.model_name = waypoint_name;
  		sm.request.model_xml = stringstream.str();
    		sm.request.robot_namespace = ros::this_node::getNamespace();
    		sm.request.reference_frame = "world";

	  }

	void controller(const vrui_mdf::Vive& vive,const Joy_Listener& joy)
	  {
		if(trigger==0 & joy.axes[5] < -0.9)
		  {
			spawn_model.call(sm);
			trigger = 1;
			double roll, pitch, yaw;
                        tf::Quaternion Qua(vive.headset.orientation.x, vive.headset.orientation.y, vive.headset.orientation.z, vive.headset.orientation.w);
			tf::Matrix3x3 m(Qua); //rotation matrix from Quaternion
			m.getRPY(roll, pitch, yaw); //eular angle form rotation matrix

			yaw_headset = yaw;
		  }
		
		if(joy.axes[5]  < -0.9)
		  {


			waypoint.model_name = waypoint_name;
			waypoint.reference_frame="world";

			waypoint.pose.position.x = cos(yaw_headset)*(joy.axes[4]+0.3) * scale - sin(yaw_headset)*joy.axes[3] * scale + vive.headset.position.x;
			waypoint.pose.position.y = sin(yaw_headset)*(joy.axes[4]+0.3) * scale + cos(yaw_headset)*joy.axes[3] * scale + vive.headset.position.y;
			waypoint.pose.position.z = 0;


			waypoint.pose.orientation.x = 0;
			waypoint.pose.orientation.y = 0;
			waypoint.pose.orientation.z = 0;
			waypoint.pose.orientation.w = 1;
		  }

		if(trigger==1 & joy.axes[5]  > -0.9)
		  {
			throw_state = waypoint;
			throw_state.pose.position.z = 0.3;
			throw_state.model_name = model_name;

			once = true;
                        trigger=0;

			//deletemodel.request.model_name = waypoint_name;

			//delete_model.call(deletemodel);


		  }
	  }

};



class Waypointcontroller
{
public:
	ros::ServiceClient client_get;//= n.serviceClient<gazebo_msgs::GetModelState>("/gazebo/get_model_state");

	ros::Publisher base_control;//= n.advertise<geometry_msgs::Twist>("mobile_base/commands/velocity", 1);

	gazebo_msgs::GetModelState get_state;

	geometry_msgs::Twist base_motion;

	float x_tar;
	float y_tar;
	float x_cur;
	float y_cur;
        float dis;

	float kp_ang;
	float kp_lin;

	float psidot;
	float v;

	int trigger;// 0
	bool once;

        int scale;
	double yaw_headset;

	ros::ServiceClient delete_model;
        ros::ServiceClient spawn_model;

        gazebo_msgs::SpawnModel sm;
	gazebo_msgs::DeleteModel deletemodel;

	gazebo_msgs::ModelState waypoint;
	
	std::string waypoint_name;//"waypoint"

   	void readmodel(const char* path)
	  {

		std::ifstream ifs;
		ifs.open(path);
		std::stringstream stringstream;
    		stringstream << ifs.rdbuf();
  		sm.request.model_name = waypoint_name;
  		sm.request.model_xml = stringstream.str();
    		sm.request.robot_namespace = ros::this_node::getNamespace();
    		sm.request.reference_frame = "world";

	  }


	void init()
	{

		client_get.call(get_state);
		x_tar = get_state.response.pose.position.x;
                y_tar = get_state.response.pose.position.y;
		
	}

	void waypoint_controller(const Joy_Listener& joy)
	{

		if(trigger==0 & joy.axes[5] > -0.9)
		{

			client_get.call(get_state);
			double roll, pitch, yaw;
                        tf::Quaternion Qua(get_state.response.pose.orientation.x, get_state.response.pose.orientation.y, get_state.response.pose.orientation.z, get_state.response.pose.orientation.w);
			tf::Matrix3x3 m(Qua); //rotation matrix from Quaternion
			m.getRPY(roll, pitch, yaw); //eular angle form rotation matrix

                        x_cur = get_state.response.pose.position.x;
                        y_cur = get_state.response.pose.position.y;

			float psid = atan2(y_tar-y_cur, x_tar-x_cur);
			float err_ang = psid - yaw;

                        psidot = 0;
                        v = 0;

			dis = pow( (pow((y_tar-y_cur), 2) + pow((x_tar-x_cur), 2)), 1);
			if (dis >= 0.15)
 			{
            			v = kp_lin*dis;
           			psidot = kp_ang*(err_ang);

				if (v>0.5){v = 0.5;}
				if (psidot>0.8){psidot = 0.8;}
			}


			std::cout<< x_tar << " , "<< y_tar<<" ; "<<x_cur<<" , "<< y_cur<<" ; "<< v<<" , "<<psidot<<std::endl;

	

                        if( abs(get_state.response.twist.angular.z)>0.8){psidot = 0;}

			base_motion.linear.x = v;
                        base_motion.angular.z = psidot;

			std::cout<<base_motion<<std::endl;
                        base_control.publish(base_motion);
		}
	}


	void controller(const vrui_mdf::Vive& vive,const Joy_Listener& joy)
	  {
		if(trigger==0 & joy.axes[5] < -0.9)
		  {
			spawn_model.call(sm);
			trigger = 1;

			base_motion.linear.x = 0;
                        base_motion.angular.z = 0;

                        base_control.publish(base_motion);

			double roll, pitch, yaw;
                        tf::Quaternion Qua(vive.headset.orientation.x, vive.headset.orientation.y, vive.headset.orientation.z, vive.headset.orientation.w);
			tf::Matrix3x3 m(Qua); //rotation matrix from Quaternion
			m.getRPY(roll, pitch, yaw); //eular angle form rotation matrix

			yaw_headset = yaw;
		  }
		
		if(joy.axes[5] < -0.9)
		  {


			waypoint.model_name = waypoint_name;
			waypoint.reference_frame="world";

			waypoint.pose.position.x = cos(yaw_headset)*(joy.axes[4]+0.3) * scale - sin(yaw_headset)*joy.axes[3] * scale + vive.headset.position.x;
			waypoint.pose.position.y = sin(yaw_headset)*(joy.axes[4]+0.3) * scale + cos(yaw_headset)*joy.axes[3] * scale + vive.headset.position.y;
			waypoint.pose.position.z = 0;

			waypoint.pose.orientation.x = 0;
			waypoint.pose.orientation.y = 0;
			waypoint.pose.orientation.z = 0;
			waypoint.pose.orientation.w = 1;
		  }

		if(trigger==1 & joy.axes[5] > -0.9)
		  {

			x_tar = waypoint.pose.position.x;
			y_tar = waypoint.pose.position.y;
			
			once = true;
                        trigger=0;

			//deletemodel.request.model_name = waypoint_name;

			//delete_model.call(deletemodel);


		  }
	  }



};




class velocitycontroller
{
public:
	ros::ServiceClient client_get;//= n.serviceClient<gazebo_msgs::GetModelState>("/gazebo/get_model_state");

	ros::Publisher base_control;//= n.advertise<geometry_msgs::Twist>("mobile_base/commands/velocity", 1);

	gazebo_msgs::GetModelState get_state;

	geometry_msgs::Twist base_motion;

	float x_vec;
	float y_vec;

	float kp_ang;
	float kp_lin;

	float psidot;
	float v;

	int trigger;// 0
	bool once;

	ros::ServiceClient delete_model;
        ros::ServiceClient spawn_model;

        gazebo_msgs::SpawnModel sm;
	gazebo_msgs::DeleteModel deletemodel;

/*
	gazebo_msgs::ModelState waypoint;
	
	std::string waypoint_name;//"waypoint"

   	void readmodel(const char* path)
	  {
#include <sensor_msgs/Joy.h>
		std::ifstream ifs;
		ifs.open(path);
		std::stringstream stringstream;
    		stringstream << ifs.rdbuf();
  		sm.request.model_name = waypoint_name;
  		sm.request.model_xml = stringstream.str();
    		sm.request.robot_namespace = ros::this_node::getNamespace();
    		sm.request.reference_frame = "world";

	  }
*/

	void controller(const vrui_mdf::Vive& vive,const Joy_Listener& joy)
	  {



		//vive.headset.orientation

		double roll, pitch, yaw;
                tf::Quaternion Qua(vive.headset.orientation.x, vive.headset.orientation.y, vive.headset.orientation.z, vive.headset.orientation.w);
		tf::Matrix3x3 m(Qua); //rotation matrix from Quaternion
		m.getRPY(roll, pitch, yaw); //eular angle form rotation matrix

		x_vec = cos(yaw)*joy.axes[4] - sin(yaw)*joy.axes[3];
		y_vec = sin(yaw)*joy.axes[4] + cos(yaw)*joy.axes[3];



		client_get.call(get_state);
		double roll_tur, pitch_tur, yaw_tur;
                tf::Quaternion Qua_tur(get_state.response.pose.orientation.x, get_state.response.pose.orientation.y, get_state.response.pose.orientation.z, get_state.response.pose.orientation.w);
		tf::Matrix3x3 m_tur(Qua_tur); //rotation matrix from Quaternion
		m_tur.getRPY(roll_tur, pitch_tur, yaw_tur); //eular angle form rotation matrix

		float yaw_tar = atan2(y_vec, x_vec);
		float yaw_diff = yaw_tar - yaw_tur;
		float scale =  pow( (pow((x_vec), 2) + pow((y_vec), 2)), 1);

		psidot = kp_ang*(yaw_diff);
		v = kp_lin*scale;

		if (v>0.5){v = 0.5;}
		if (psidot>0.8){psidot = 0.8;}
		if( abs(get_state.response.twist.angular.z)>0.8){psidot = 0;}

		base_motion.linear.x = v;
                base_motion.angular.z = psidot;

                base_control.publish(base_motion);



	  }

};
	


int num_controllers = 3;
int controller_switch = 1;



std::string first_controller = "1 - Velocity";
std::string second_controller = "2 - Waypoint";
std::string third_controller = "3 - Throw";




int main(int argc, char **argv)
{
  // setup ros node
  ros::init(argc, argv, "vive_controller");
  ros::NodeHandle nh;

  ros::Rate r(90);

  //define class for callback class and subscriber
  Vive_Listener vive_data;
  ros::Subscriber sub_vive = nh.subscribe("vrui/vive", 1, &Vive_Listener::callback, &vive_data);

  Joy_Listener Joy_listen;
  ros::Subscriber joy_sub = nh.subscribe("joy", 10, &Joy_Listener::joyCallback, &Joy_listen);


    ros::Publisher gazebo_pub = nh.advertise<gazebo_msgs::ModelState>("gazebo/set_model_state", 10);
    gazebo_msgs::ModelState controller_left,controller_right,controller_throw,controller_line;

    controller_left.model_name = "Vive_Controller_left";
    controller_left.reference_frame="world";

    controller_right.model_name = "Vive_Controller_right";
    controller_right.reference_frame="world";


    /* turtlebot twist command */
    ros::Publisher base_control = nh.advertise<geometry_msgs::Twist>("/mobile_base/commands/velocity", 1);
    geometry_msgs::Twist base_motion;

    /* get mobile base state*/
    ros::ServiceClient client_get = nh.serviceClient<gazebo_msgs::GetModelState>("/gazebo/get_model_state");
    gazebo_msgs::GetModelState get_state;
    get_state.request.model_name = "mobile_base";


    /* previous value */
    vrui_mdf::Vive vive_previ;
    float axes_previ[8];
    int buttons_previ[11];

    Joy_Listener Joy_listen_previ;

    /* controller 1 */
    velocitycontroller velocity_controller;
    velocity_controller.trigger = 0;
    velocity_controller.client_get = nh.serviceClient<gazebo_msgs::GetModelState>("/gazebo/get_model_state");
    velocity_controller.base_control = nh.advertise<geometry_msgs::Twist>("/mobile_base/commands/velocity", 1);
    velocity_controller.get_state.request.model_name = "mobile_base";
    velocity_controller.kp_ang = 4;
    velocity_controller.kp_lin = 30;


    /* controller 2 */
    Waypointcontroller Way_point_controller;
    Way_point_controller.trigger = 0;
    Way_point_controller.scale = 5;
    Way_point_controller.waypoint_name = "waypoint";
    Way_point_controller.once = false;
    Way_point_controller.delete_model = nh.serviceClient<gazebo_msgs::DeleteModel>("/gazebo/delete_model");
    Way_point_controller.spawn_model = nh.serviceClient<gazebo_msgs::SpawnModel>("/gazebo/spawn_sdf_model");
    Way_point_controller.readmodel("/home/zhenyushi/.gazebo/models/controller/model.sdf");
    Way_point_controller.client_get = nh.serviceClient<gazebo_msgs::GetModelState>("/gazebo/get_model_state");
    Way_point_controller.base_control = nh.advertise<geometry_msgs::Twist>("/mobile_base/commands/velocity", 1);
    Way_point_controller.get_state.request.model_name = "mobile_base";
    Way_point_controller.kp_ang = 4;
    Way_point_controller.kp_lin = 0.3;

    /* controller 3 */
    ThrowMethod ThrowTo;
    ThrowTo.trigger = 0;
    ThrowTo.scale = 5;
    ThrowTo.waypoint_name = "waypoint";
    ThrowTo.model_name = "mobile_base";
    ThrowTo.once = false;
    ThrowTo.delete_model = nh.serviceClient<gazebo_msgs::DeleteModel>("/gazebo/delete_model");
    ThrowTo.spawn_model = nh.serviceClient<gazebo_msgs::SpawnModel>("/gazebo/spawn_sdf_model");
    ThrowTo.readmodel("/home/zhenyushi/.gazebo/models/controller/model.sdf");


    //system("rosrun gazebo_ros spawn_model -file ~/.gazebo/models/Vive_Controller/model.sdf -sdf -model Vive_Controller_left -y 0 -x 0 -z 3");
    //system("rosrun gazebo_ros spawn_model -file ~/.gazebo/models/Vive_Controller/model.sdf -sdf -model Vive_Controller_right -y 0 -x 0 -z 3");


    /* for display */
    ros::Publisher ToDisplay = nh.advertise<std_msgs::String>("control_method", 10);
    std_msgs::String msg;
    msg.data = first_controller ;
    ToDisplay.publish(msg);




  while(ros::ok())
  {
  ros::spinOnce(); 
  // ros::spin() works too, but extra code can run outside the callback function between each spinning if spinOnce() is used

/*
  controller_left.pose = vive_data.vive.ctrl_left.pose;
  controller_right.pose = vive_data.vive.ctrl_right.pose;
  gazebo_pub.publish(controller_left); 
  gazebo_pub.publish(controller_right); 
*/


  if(Joy_listen_previ.axes[7] == 0 & Joy_listen.axes[7] < -0.5)
	{
		if(controller_switch<3)
			controller_switch++;
		else
			controller_switch = 1;

		switch(controller_switch) {
		   case 1  :
			std::cout<<first_controller<<std::endl;
    			msg.data = first_controller ;
			break;
		   case 2  :
			Way_point_controller.init();
			std::cout<<second_controller<<std::endl;
	    		msg.data = second_controller ;
			break;
		   case 3  :
			std::cout<<third_controller<<std::endl;
	    		msg.data = third_controller ;
			break;
		  }
	}

 if(Joy_listen_previ.axes[7] == 0 & Joy_listen.axes[7] > 0.5)
	{
		if(controller_switch>1)
			controller_switch--;
		else
			controller_switch = 3;

		switch(controller_switch) {
		   case 1  :
			std::cout<<first_controller<<std::endl;
    			msg.data = first_controller ;
			break;
		   case 2  :
			Way_point_controller.init();
			std::cout<<second_controller<<std::endl;
	    		msg.data = second_controller ;
			break;
		   case 3  :
			std::cout<<third_controller<<std::endl;
	    		msg.data = third_controller ;
			break;
		  }
	}


  ToDisplay.publish(msg);


  switch(controller_switch) {
   case 1  : //"Velocity"

        velocity_controller.controller(vive_data.vive,Joy_listen);


	break;
   case 2  : //"Waypoint"

        Way_point_controller.waypoint_controller(Joy_listen);
        Way_point_controller.controller(vive_data.vive,Joy_listen);

	if(Way_point_controller.trigger){gazebo_pub.publish(Way_point_controller.waypoint);}
	if(Way_point_controller.once)
	  {
		Way_point_controller.once = false;
	  }

	break;
   case 3  : //"Throw"

	ThrowTo.controller(vive_data.vive,Joy_listen);
	if(ThrowTo.trigger){gazebo_pub.publish(ThrowTo.waypoint);}
	if(ThrowTo.once)
	  {
		gazebo_pub.publish(ThrowTo.throw_state);
		ThrowTo.once = false;
	  }
	
	break;
  }

/*
if(vive_data.vive.ctrl_left.buttons.system == 1)
{
	std::cout<<"left"<<std::endl;
}
*/


  /* over write previous value  */
  vive_previ = vive_data.vive;
  Joy_listen_previ = Joy_listen;

  r.sleep();
  }

  return 0;
}









