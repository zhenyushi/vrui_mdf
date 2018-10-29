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
#include <image_transport/image_transport.h>
#include "std_msgs/String.h"
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <time.h>
#include <vrui_mdf/Vive.h>
#include <tf/transform_broadcaster.h> 
#include <math.h> 

// define callback function in a class so that data running inside the class can be used globally
class Listener_image
{
public:
	  cv::Mat image;

	  void callback(const sensor_msgs::CompressedImageConstPtr& msg)
	    {
            //cv_bridge::toCvShare(msg, "bgr8")->image.copyTo(image); //copy image data to the image under the same class, which will be assign as a pointer
            cv::imdecode(cv::Mat(msg->data),1).copyTo(image);;
	    }

};


class Listener_ctrlMethod
{
public:

	std::string control_method;

	void chatterCallback(const std_msgs::String::ConstPtr& msg)
	{
	   control_method = msg->data.c_str();
	}

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

int main(int argc, char **argv)
{
  // setup ros node
  ros::init(argc, argv, "image_sub");
  ros::NodeHandle nh;
  image_transport::ImageTransport it(nh);

  // define and modify window
  cv::namedWindow("view",cv::WINDOW_NORMAL); // cv::WINDOW_NORMAL means the window size can be changed
  cv::moveWindow("view",1921,0);      // move the window to the VIVE monitor, which is the second moniter on the right side of main monitor, and main monitor has a width of 1920
  cv::setWindowProperty("view",0,1);  // setWindowProperty(window name, type of window property(full screen = 0), value of window property(full screen = 1))
  cv::startWindowThread();
  
  ros::Rate r(100);

  //define class for callback class and subscriber
  Listener_image listener_left,listener_right;
  //image_transport::Subscriber sub_left = it.subscribe("/camera/rgb/left_eye/compressed", 1, &Listener_image::callback, &listener_left);
  //image_transport::Subscriber sub_right = it.subscribe("/camera/rgb/right_eye/compressed", 1, &Listener_image::callback, &listener_right);

  ros::Subscriber sub_le = nh.subscribe("/camera/rgb/left_eye/compressed", 1, &Listener_image::callback, &listener_left);
  ros::Subscriber sub_ri = nh.subscribe("/camera/rgb/right_eye/compressed", 1, &Listener_image::callback, &listener_right);


  Listener_ctrlMethod ctrl_methods;
  ctrl_methods.control_method = "Velocity";
  ros::Subscriber ctrl_sub = nh.subscribe("control_method", 10, &Listener_ctrlMethod::chatterCallback,&ctrl_methods);
  

  // fial image, left half shows left eye, right half shows right eye
  cv::Mat image_final(1200,1920, CV_8UC3,cv::Scalar(0,255,255));


  // assign the images under listerner classes as pointers pointing at left or right half of final image
  // so that the copyTo() will copy the data directly to the final image
  listener_left.image = image_final(cv::Range(0,1200),cv::Range(0,960));
  listener_right.image = image_final(cv::Range(0,1200),cv::Range(960,1920));

  Vive_Listener vive_data;
  ros::Subscriber sub_vive = nh.subscribe("vrui/vive", 1, &Vive_Listener::callback, &vive_data);

    cv::Point left,left_lower;
    left.x = 250;
    left.y = 500;
    cv::Point right,right_lower;
    right.x = left.x + 960 - 60;
    right.y = left.y;

    left_lower = left;
    right_lower = right;
   
    double textsize = 0.8;
    int thickness=1.7;
    
    //cv::VideoWriter video("/home/zhenyushi/catkin_ws/src/vrui_mdf/out.avi",CV_FOURCC('M','J','P','G'),30, cv::Size(1920,1200),true);


  while(ros::ok())
  {
  ros::spinOnce(); 
  // ros::spin() works too, but extra code can run outside the callback function between each spinning if spinOnce() is used

    cv::putText( image_final, ctrl_methods.control_method, left, 0,textsize, cv::Scalar(0,0,255), thickness, 8);
    cv::putText( image_final, ctrl_methods.control_method, right, 0,textsize, cv::Scalar(0,0,255), thickness, 8);

    left_lower.y = left.y + 60;
    right_lower.y = right.y + 60;

    char text[255];
    sprintf(text, "%d . %d", (int)ros::Time::now().sec,(int)ros::Time::now().nsec);

    cv::putText( image_final, text, left_lower, 0,textsize, cv::Scalar(50,0,255), thickness, 8);
    cv::putText( image_final, text, right_lower, 0,textsize, cv::Scalar(50,0,255), thickness, 8);

/*
    double roll, pitch, yaw;
    tf::Quaternion Qua(vive_data.vive.headset.orientation.x,vive_data.vive.headset.orientation.y,vive_data.vive.headset.orientation.z,vive_data.vive.headset.orientation.w);
    tf::Matrix3x3 m(Qua); //rotation matrix from Quaternion
    m.getRPY(roll, pitch, yaw); //eular angle form rotation matrix

    left_lower.y = left_lower.y + 60;
    right_lower.y = right_lower.y + 60;


    double yaw_de = (yaw/3.1415926535897)*180;

    std::cout<<yaw_de<<std::endl;

    double fractpart, intpart;
    fractpart = modf (yaw_de, &intpart);

    fractpart = fractpart*100;
    char text1[255];
    sprintf(text1, "Yaw : %d . %d",(int)intpart, (int)fractpart);

    cv::putText( image_final, text1, left_lower, 0,textsize, cv::Scalar(100,0,255), thickness, 8);
    cv::putText( image_final, text1, right_lower, 0,textsize, cv::Scalar(100,0,255), thickness, 8);

    cv::Point p_up(960+480,0),  p_down(960+480, 1200);
    cv::line(image_final, p_up, p_down, cv::Scalar(0,255,0), 2, 8, 0);
*/
    if(listener_left.image.cols!=0 && listener_right.image.cols!=0) 
    {

    //video.write(image_final);

    cv::imshow("view", image_final);
    cv::waitKey(1); // necessary for imshow()
    }
  r.sleep();
  }






  return 0;
}
