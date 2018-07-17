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


// define callback function in a class so that data running inside the class can be used globally
class Listener_image
{
public:
	  cv::Mat image;

	  void callback(const sensor_msgs::ImageConstPtr& msg)
	    {
            cv_bridge::toCvShare(msg, "bgr8")->image.copyTo(image); //copy image data to the image under the same class, which will be assign as a pointer
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


int main(int argc, char **argv)
{
  // setup ros node
  ros::init(argc, argv, "listener_class");
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
  image_transport::Subscriber sub_left = it.subscribe("/camera/rgb/left_eye", 1, &Listener_image::callback, &listener_left);
  image_transport::Subscriber sub_right = it.subscribe("/camera/rgb/right_eye", 1, &Listener_image::callback, &listener_right);

  Listener_ctrlMethod ctrl_methods;
  ctrl_methods.control_method = "Velocity";
  ros::Subscriber ctrl_sub = nh.subscribe("control_method", 10, &Listener_ctrlMethod::chatterCallback,&ctrl_methods);
  

  // fial image, left half shows left eye, right half shows right eye
  cv::Mat image_final(1200,1920, CV_8UC3,cv::Scalar(0,255,255));


  // assign the images under listerner classes as pointers pointing at left or right half of final image
  // so that the copyTo() will copy the data directly to the final image
  listener_left.image = image_final(cv::Range(0,1200),cv::Range(0,960));
  listener_right.image = image_final(cv::Range(0,1200),cv::Range(960,1920));



    cv::Point left;
    left.x = 300;
    left.y = 500;
    cv::Point right;
    right.x = left.x + 960 - 60;
    right.y = left.y;

    double textsize = 1;
    int thickness=3;
    

  while(ros::ok())
  {
  ros::spinOnce(); 
  // ros::spin() works too, but extra code can run outside the callback function between each spinning if spinOnce() is used
  


    std::cout<<ros::Time::now()<<std::endl;
    cv::putText( image_final, ctrl_methods.control_method, left, 0,textsize, cv::Scalar(0,255,255), thickness, 8);
    cv::putText( image_final, ctrl_methods.control_method, right, 0,textsize, cv::Scalar(0,255,255), thickness, 8);


    if(listener_left.image.cols!=0 && listener_right.image.cols!=0) 
    {
    cv::imshow("view", image_final);
    cv::waitKey(1); // necessary for imshow()
    }
  r.sleep();
  }






  return 0;
}
