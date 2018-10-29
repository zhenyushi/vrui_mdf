#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>
#include <time.h>
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

int main(int argc, char** argv)
{

  ros::init(argc, argv, "joyReading");
  ros::NodeHandle n;
  ros::Rate r(90);

  Joy_Listener Joy_listen,Joy_listen_previous;

  ros::Subscriber joy_sub = n.subscribe("joy", 10, &Joy_Listener::joyCallback, &Joy_listen);

  ros::Publisher base_control;
  base_control = n.advertise<geometry_msgs::Twist>("/mobile_base/commands/velocity", 1);
  geometry_msgs::Twist base_motion;
  //ros::service::waitForService("/gazebo/spawn_urdf_model", -1);
  system("rosservice call /enable_motors true");

  float ra = 3;

  while(ros::ok())
  {
  ros::spinOnce(); 

  std::cout << Joy_listen.axes[0] << " , "<< Joy_listen.axes[1] <<std::endl;

  std::cout << Joy_listen.axes[3] << " , "<< Joy_listen.axes[4] <<std::endl;

  std::cout << Joy_listen.axes[2] << " , "<< Joy_listen.axes[5] <<std::endl;

/*
  std::cout << Joy_listen.buttons[0] << " , "<< Joy_listen.buttons[1] 
    << " , "<< Joy_listen.buttons[2]<< " , "<< Joy_listen.buttons[3]
    << " , "<< Joy_listen.buttons[4]<< " , "<< Joy_listen.buttons[5]
    << " , "<< Joy_listen.buttons[6]<< " , "<< Joy_listen.buttons[7]
    << " , "<< Joy_listen.buttons[8]<< " , "<< Joy_listen.buttons[9]
    << " , "<< Joy_listen.buttons[10]<<std::endl;
*/


  std::cout<<ros::Time::now()<<std::endl;


  base_motion.linear.x = Joy_listen.axes[4] * ra;
  base_motion.linear.y = Joy_listen.axes[3] * ra;
  base_motion.linear.z = Joy_listen.axes[1] * ra;

  base_motion.angular.z = Joy_listen.axes[0] * ra;

  base_control.publish(base_motion);



  Joy_listen_previous = Joy_listen;

  r.sleep();

  }

}
