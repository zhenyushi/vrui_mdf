#!/usr/bin/python

def replace (line):
    line = line.replace("include","includeeeeeeeee")
    return line

def insert (cnt_inser,inserlines, f_tar):
    f_tar.write("{} \n".format(inserlines[cnt_inser]))
    return f_tar


if __name__ == '__main__':

    f = open("../src/Vrui-4.5-001/Vrui/Utilities/DeviceTest.cpp",'r')

    line = f.readline()
    cnt_lines = 1
    wanttedlinesnum = [24,25,27,28,29,32,35,38,39,41,43,44,    #header files    12
                       46,47,48,49,50,51,231,232,233,234,235,  #definations     11
                       499,500,                                #main()          2
                       502,505,507,604,614,                    #definations in main()  5
                       615,616,617,618,619,620,621,622,623,    #first try loop         9
                       793,794,                                #defination timer       2
                       795,796,                                #main try loop          2
                       797,798,799,                            #activate&startStream   3
                       800,801,                                #defination             2
                       805,806,807,                            #defination in while loop  3
                       812,813,834,                            #lockState define state    3
                       907,                                    #unlockState()             1
                       914,915,916,917,918,919,920,921,922,    #key checking              9
                       925,                                    #getPacket                 1
                       928,929,930,933,934,                    #end of the main try loop  5
                       935,936,937,938,939,940,941,942,943,944,945,950,951, #finishing up 13
                       952]                                    #end of the main()         1



    wanttedlines = ["" for x in range(len(wanttedlinesnum))]
    cnt_wanted = 0


    pastelines = [     [1,41],
                       [2,42],
                       [3,43],
                       [4,44],
                       [5,45],
                       [6,47],
                       [7,48],
                       [8,49],
                       [9,50],
                       [10,52],
                       [11,53],
                       [12,54],
                       [13,84],
                       [14,85],
                       [15,86],
                       [16,87],
                       [17,88],
                       [18,89],
                       [19,93],
                       [20,94],
                       [21,95],
                       [22,96],
                       [23,97],
                       [24,115],
                       [25,116],
                       [27,138],
                       [27,139],
                       [27,140],
                       [28,143],
                       [29,146],
                       [30,150],
                       [31,153],
                       [32,154],
                       [33,155],
                       [34,156],
                       [35,157],
                       [36,158],
                       [37,159],
                       [38,160],
                       [39,161],
                       [40,165],
                       [41,166],
                       [42,167],
                       [43,168],
                       [44,169],
                       [45,170],
                       [46,171],
                       [47,172],
                       [48,173],
                       [49,226],
                       [50,227],
                       [51,228],
                       [52,230],
                       [53,231],
                       [54,235],
                       [54,247],
                       [54,254],
                       [55,345],
                       [56,350],
                       [57,351],
                       [58,352],
                       [59,353],
                       [60,354],
                       [61,355],
                       [62,356],
                       [63,357],
                       [64,358],
                       [65,361],
                       [66,367],
                       [67,368],
                       [68,369],
                       [69,370],
                       [70,371],
                       [71,374],
                       [72,375],
                       [73,376],
                       [74,377],
                       [77,380],
                       [78,381],
                       [79,382],
                       [80,383],
                       [82,384],
                       [83,385],
                       [84,387]]


    cnt_paste = 0

    replacelinesnum = [139,140,155,247,254]
    cnt_replace = 0
    rep_bef = ['trackerIndex=0','trackerIndex=0','.c_str()','ts','ts']
    rep_aft = ['trackerIndex_left=1','trackerIndex_right=2','','ts_left','ts_right']

    replacelinesnum_1 = [247,254]
    cnt_replace_1 = 0
    rep_bef_1 = ['trackerIndex','trackerIndex']
    rep_aft_1 = ['trackerIndex_left','trackerIndex_right']

    cnt_inser = 0

    inserlines = [     [62,'#include "vrui_mdf.h"'],
                       [65,'#include <ros/ros.h>'],
                       [66,'#include <gazebo_msgs/ModelState.h>'],
                       [67,'#include <tf/transform_broadcaster.h>'],
                       [69,'#include "tf/transform_datatypes.h"'],
                       [70,'#include <geometry_msgs/Quaternion.h>'],
                       [71,'#include <cmath>'],
                       [72,'#include <math.h>'],
                       [73,'#include<fstream>'],
                       [74,'#include <vrui_mdf/Vive.h>'],
                       [76,'#include <geometry_msgs/Twist.h>'],
                       [77,'#include <gazebo_msgs/SetModelState.h>'],
                       [78,'#include "gazebo_msgs/GetModelState.h"'],
                       [79,'#include "gazebo_msgs/DeleteModel.h"'],
                       [80,'#include "gazebo_msgs/SpawnModel.h"'],
                       [119,'ros::init(argc, argv, "camera_state");'],
                       [120,'ros::NodeHandle n;'],
                       [121,'ros::Rate r(90);'],
                       [122,'ros::service::waitForService("/gazebo/spawn_urdf_model", -1);'],
                       [124,'ros::Publisher gazebo_pub = n.advertise<gazebo_msgs::ModelState>("gazebo/set_model_state", 10);'],
                       [125,'gazebo_msgs::ModelState camera;'],
                       [126,'camera.model_name = "vr_view";'],
                       [127,'camera.reference_frame="world";'],
                       [128,'ros::Time time;'],
                       [129,'vrui_mdf::Vive vive;'],
                       [130,'vive.user_name = "vive";'],
                       [131,'ros::Publisher vive_state = n.advertise<vrui_mdf::Vive>("vrui/vive", 10);'],
                       [137,'char* serverName=0;'],
                       [175,'gazebo_msgs::SpawnModel sm;'],
                       [176,'ros::ServiceClient spawn_model;'],
                       [177,'spawn_model = n.serviceClient<gazebo_msgs::SpawnModel>("/gazebo/spawn_sdf_model");'],
                       [178,'std::ifstream ifs,ifs1;'],
                       [179,'ifs.open("/home/zhenyushi/.gazebo/models/controller/model.sdf");'],
                       [180,'std::stringstream stringstream;'],
                       [181,'stringstream << ifs.rdbuf();'],
                       [182,'sm.request.model_name = "base_test";'],
                       [183,'sm.request.model_xml = stringstream.str();'],
                       [184,'sm.request.robot_namespace = ros::this_node::getNamespace();'],
                       [185,'sm.request.reference_frame = "world";'],
                       [186,'spawn_model.call(sm);'],
                       [188,'ifs1.open("/home/zhenyushi/.gazebo/models/vr_view/model.sdf");'],
                       [189,'std::stringstream stringstream1;'],
                       [190,'stringstream1 << ifs1.rdbuf();'],
                       [191,'sm.request.model_name = "vr_view";'],
                       [192,'sm.request.model_xml = stringstream1.str();'],
                       [193,'sm.request.robot_namespace = ros::this_node::getNamespace();'],
                       [194,'sm.request.reference_frame = "world";'],
                       [195,'spawn_model.call(sm);'],
                       [197,'ros::ServiceClient client_set = n.serviceClient<gazebo_msgs::SetModelState>("/gazebo/set_model_state");'],
                       [198,'gazebo_msgs::SetModelState Setmodelstate;'],
                       [200,'Setmodelstate.request.model_state.model_name = "base_test";'],
                       [201,'Setmodelstate.request.model_state.reference_frame="world";'],
                       [202,'Setmodelstate.request.model_state.pose.position.x = 0;'],
                       [203,'Setmodelstate.request.model_state.pose.position.y = 0;'],
                       [204,'Setmodelstate.request.model_state.pose.position.z = 0;'],
                       [206,'Setmodelstate.request.model_state.pose.orientation.x = 0;'],
                       [207,'Setmodelstate.request.model_state.pose.orientation.y = 0;'],
                       [208,'Setmodelstate.request.model_state.pose.orientation.z = 0;'],
                       [209,'Setmodelstate.request.model_state.pose.orientation.w = 1;'],
                       [210,'client_set.call(Setmodelstate);'],
                       [214,'ros::ServiceClient client = n.serviceClient<gazebo_msgs::GetModelState>("/gazebo/get_model_state");'],
                       [215,'gazebo_msgs::GetModelState getmodelstate;'],
                       [221,'system("rosrun gazebo_ros spawn_model -file $(find vrui_mdf)/models/vr_view/model.sdf -sdf -model vr_view -y 0 -x 0 -z 1");'],
                       [222,'system("rosrun gazebo_ros spawn_model -file $(find vrui_mdf)/models/controller/model.sdf -sdf -model base_test -y 0 -x 0 -z 0");'],
                       [223,'while(ros::ok())'],
                       [224,'{'],
                       [236,'Point pos=ts.positionOrientation.getOrigin();'],
                       [237,'Rotation rot=ts.positionOrientation.getRotation();'],
                       [238,'const float* quaternion;'],
                       [239,'quaternion=rot.getQuaternion();'],
                       [248,'Point pos_left=ts_left.positionOrientation.getOrigin();'],
                       [249,'Rotation rot_left=ts_left.positionOrientation.getRotation();'],
                       [250,'const float* quaternion_left;'],
                       [251,'quaternion_left=rot_left.getQuaternion();'],
                       [255,'Point pos_right=ts_right.positionOrientation.getOrigin();'],
                       [256,'Rotation rot_right=ts_right.positionOrientation.getRotation();'],
                       [257,'const float* quaternion_right;'],
                       [258,'quaternion_right=rot_right.getQuaternion();'],
                       [265,'float bias_0 = -0.191;'],
                       [266,'float bias_1 = 2.2;'],
                       [267,'float bias_2 = 1.98;'],
                       [269,'getmodelstate.request.model_name = "base_test";'],
                       [270,'client.call(getmodelstate);'],
                       [275,'camera.pose.position.x = -1*pos[2] - bias_2 + getmodelstate.response.pose.position.x;'],
                       [276,'camera.pose.position.y = -1*pos[0] - bias_0 + getmodelstate.response.pose.position.y;'],
                       [277,'camera.pose.position.z = pos[1] + bias_1 + getmodelstate.response.pose.position.z;'],
                       [279,'camera.pose.orientation.x = -1*quaternion[2];'],
                       [280,'camera.pose.orientation.y = -1*quaternion[0];'],
                       [281,'camera.pose.orientation.z = quaternion[1];'],
                       [282,'camera.pose.orientation.w = quaternion[3];'],
                       [284,'camera.twist.linear.x = -1 * ts.linearVelocity[2];'],
                       [285,'camera.twist.linear.y = -1 * ts.linearVelocity[0];'],
                       [286,'camera.twist.linear.z = ts.linearVelocity[1];'],
                       [288,'camera.twist.angular.x = -1 * ts.angularVelocity[2];'],
                       [289,'camera.twist.angular.y = -1 * ts.angularVelocity[0];'],
                       [290,'camera.twist.angular.z =  ts.angularVelocity[1];'],
                       [294,'gazebo_pub.publish(camera);'],
                       [298,'vive.headset = camera.pose;'],
                       [301,'vive.ctrl_left.pose.position.x = -1*pos_left[2] - bias_2 + getmodelstate.response.pose.position.x;'],
                       [302,'vive.ctrl_left.pose.position.y = -1*pos_left[0] - bias_0 + getmodelstate.response.pose.position.y;'],
                       [303,'vive.ctrl_left.pose.position.z = pos_left[1] + bias_1 + getmodelstate.response.pose.position.z;'],
                       [305,'vive.ctrl_left.pose.orientation.x = -1*quaternion_left[2];'],
                       [306,'vive.ctrl_left.pose.orientation.y = -1*quaternion_left[0];'],
                       [307,'vive.ctrl_left.pose.orientation.z = quaternion_left[1];'],
                       [308,'vive.ctrl_left.pose.orientation.w = quaternion_left[3];'],
                       [310,'vive.ctrl_left.buttons.system = state.getButtonState(2);'],
                       [311,'vive.ctrl_left.buttons.grip = state.getButtonState(3);'],
                       [312,'vive.ctrl_left.buttons.menu = state.getButtonState(4);'],
                       [313,'vive.ctrl_left.buttons.trigger = state.getButtonState(5);'],
                       [314,'vive.ctrl_left.buttons.trackpad = state.getButtonState(6);'],

                       [315,'vive.ctrl_left.buttons.trigger_Valuator = state.getValuatorState(0);'],
                       [316,'vive.ctrl_left.trackpad.touched = state.getButtonState(7);'],
                       [317,'vive.ctrl_left.trackpad.x = state.getValuatorState(1);'],
                       [318,'vive.ctrl_left.trackpad.y = state.getValuatorState(2);'],

                       [321,'vive.ctrl_right.pose.position.x = -1*pos_right[2] - bias_2 + getmodelstate.response.pose.position.x;'],
                       [322,'vive.ctrl_right.pose.position.y = -1*pos_right[0] - bias_0 + getmodelstate.response.pose.position.y;'],
                       [323,'vive.ctrl_right.pose.position.z = pos_right[1] + bias_1 + getmodelstate.response.pose.position.z;'],
                       [325,'vive.ctrl_right.pose.orientation.x = -1*quaternion_right[2];'],
                       [326,'vive.ctrl_right.pose.orientation.y = -1*quaternion_right[0];'],
                       [327,'vive.ctrl_right.pose.orientation.z = quaternion_right[1];'],
                       [328,'vive.ctrl_right.pose.orientation.w = quaternion_right[3];'],
                       [330,'vive.ctrl_right.buttons.system = state.getButtonState(8);'],
                       [331,'vive.ctrl_right.buttons.grip = state.getButtonState(9);'],
                       [332,'vive.ctrl_right.buttons.menu = state.getButtonState(10);'],
                       [333,'vive.ctrl_right.buttons.trigger = state.getButtonState(11);'],
                       [334,'vive.ctrl_right.buttons.trackpad = state.getButtonState(12);'],

                       [335,'vive.ctrl_right.buttons.trigger_Valuator = state.getValuatorState(3);'],
                       [336,'vive.ctrl_right.trackpad.touched = state.getButtonState(13);'],
                       [337,'vive.ctrl_right.trackpad.x = state.getValuatorState(4);'],
                       [338,'vive.ctrl_right.trackpad.y = state.getValuatorState(5);'],

                       [339,'vive.stamp = time.now();'],
                       [340,'vive_state.publish(vive);'],
                       [363,'r.sleep();'],
                       [365,'}']]


    cnt_commit = 0
    commitment = [  [1,'/********************************************************************'],
                    [2,''],
                    [3,'Vrui_mdf/tracking - Node to read the tracking and buttons status from'],
                    [4,'a VR Device, plug the data into messages with a specific formate and'],
                    [5,'publush the message on a specific topic.'],
                    [6,''],
                    [7,'The codes here to read the tracking data are from Vrui/DeviceTest, which'],
                    [8,'is a sample program of the Virtual Reality User Interface Library(Vrui),'],
                    [9,''],
                    [10,'Current it only publishes to update the state for headset and left'],
                    [11,'controller models in Gazebo. - 03/19/2018'],
                    [12,''],
                    [13,'---'],
                    [14,''],
                    [15,'LICENSE INFORMATION:'],
                    [16,''],
                    [17,'This file was generated by code written by Zhenyu Shi, a member of the'],
                    [18,'AS4SR Lab at the University of Cincinnati.'],
                    [19,''],
                    [20,'The source code used to generate this file, and the code snippets in'],
                    [21,'the github.com/zhenyushi/Vrui_mdf repository included in this file are'],
                    [22,'released under a BSD 3-clause license:'],
                    [23,''],
                    [24,'Copyright 2018 University of Cincinnati'],
                    [25,'All rights reserved. See LICENSE file at:'],
                    [26,'https://github.com/zhenyushi/Vrui_mdf'],
                    [27,'Additional copyright is held by others, as reflected in the commit'],
                    [28,'history and as listed below.'],
                    [29,''],
                    [30,'The code snippets from the Vrui 4.5-001 library included in this file are'],
                    [31,'released under a GPL license, see below (in the "DeviceTest" section):'],
                    [32,''],
                    [33,'/***********************************************************************'],
                    [34,'DeviceTest - Program to test the connection to a Vrui VR Device Daemon'],
                    [35,'and to dump device positions/orientations and button states.'],
                    [36,'Copyright (c) 2002-2016 Oliver Kreylos'],
                    [37,''],
                    [38,'This file is part of the Virtual Reality User Interface Library (Vrui).'],
                    [39,''],
                    [40,'The Virtual Reality User Interface Library is free software; you can'],
                    [41,'redistribute it and/or modify it under the terms of the GNU General'],
                    [42,'Public License as published by the Free Software Foundation; either'],
                    [43,'version 2 of the License, or (at your option) any later version.'],
                    [44,''],
                    [45,'The Virtual Reality User Interface Library is distributed in the hope'],
                    [46,'that it will be useful, but WITHOUT ANY WARRANTY; without even the'],
                    [47,'implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR'],
                    [48,'PURPOSE.  See the GNU General Public License for more details.'],
                    [49,''],
                    [50,'You should have received a copy of the GNU General Public License along'],
                    [51,'with the Virtual Reality User Interface Library; if not, write to the'],
                    [52,'Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA'],
                    [53,'02111-1307 USA'],
                    [54,'***********************************************************************/'],
                    [55,'/*'],
                    [56,''],
                    [57,'The code sections that came from Vrui/Vrui-4.5-001/Vrui/Utilities/DeviceTest.cpp are the following:'],
                    [58,'-- lines 177 - 201 (codes to Initialize device client)'],
                    [59,'-- lines 235 - 286 (function to read tracking data from Vive headset)'],
                    [60,''],
                    [61,'***********************************************************************/'],
                    [62,''],
                    [63,'/*'],
                    [64,'GENERATED CODE STARTS HERE:'],
                    [65,'*/'],
                    [66,''],
                    [67,'/* header files used in Vrui/DeviceTest */'],
                    [68,'/* file path needs to be define in CMakeLists.txt*/'],
                    [56,'/*'],
                    [57,'Vrui is built by a script, some of the classes and functions are'],
                    [58,'defined in .cpp or .icpp files, to import Vrui into ros package,'],
                    [59,'those files also need to be included. This vrui_mdf.h includes'],
                    [60,'all extra files that are needed.'],
                    [61,'*/'],
                    [64,'/* ros header files for model state publishing in Gazebo, added for Gazebo application */'],
                    [67,'// translation between Eular angle and Quaternion, unnecessary for tracking since Quaternion can be received directly'],
                    [83,'/* VIVE tracking data reading definitions, come directly from Vrui/DeviceTest */'],
                    [92,'/* VIVE headset configuration reading definitions, come directly from Vrui/DeviceTest */'],
                    [100,'/* main function, VIVE tracking parts are from Vrui/DeviceTest directly */'],
                    [102,'/***********************************************************************'],
                    [104,'The main thread here is to read position and orientation data from headset'],
                    [105,'and controllers, and publish it to the VR camera model in gazebo.'],
                    [107,'Originally, Vrui/DeviceTest has many different tracking and printing modes,'],
                    [108,'so it"s a very good sample to understand how Vrui works.'],
                    [110,'For this Gazebo application, codes for Vrui/DeviceTest are refered,'],
                    [111,'and unnecessary printing modes for this application are removed.'],
                    [113,'***********************************************************************/'],
                    [118,'/* Set up ros node and define publisher for gazebo */'],
                    [123,'/* gazebo model state publisher and topic */'],
                    [133,'/********************************************************************/'],
                    [134,'/* Vrui/DeviceTest code starts (order and detail might be modified) */'],
                    [136,'/* Parse command line: (original commitment)*/'],
                    [137,'//necessary, but usually fixed if only one headset are used'],
                    [138,'//index for headset'],
                    [139,'//index for left controller'],
                    [140,'//index for right controller'],
                    [143,'//switch for printing button in terminal, unnecessary for gazebo'],
                    [146,'//portnumber come from input in original Vrui/DeviceTest code, usually fixed if only one headset are used'],
                    [149,'/* Initialize device client: (original commitment)*/'],
                    [152,'/* a while loop can be used to replace this try, so that the code will wait for RunViveTracker.sh while using roslaunch (original commitment)*/'],
                    [164,'/* Run main loop: (original commitment)*/'],
                    [213,'//std::cout<<Setmodelstate.request<<std::endl;'],
                    [216,'/*'],
                    [217,'getmodelstate.request.model_name = "base_test";'],
                    [218,'client.call(getmodelstate);'],
                    [219,'std::cout<<getmodelstate.response<<std::endl;'],
                    [220,'*/'],
                    [225,'/* Get packet timestamp: (original commitment)*/'],
                    [230,'//devices state needs to be locked before read'],
                    [234,'/* read state of headset, trackerIndex=0 */'],
                    [240,'/* Eular angle representation is used in original Vrui/DeviceTest code,'],
                    [241,'getQuaternion() is defined in header files and works better for ros publishers */'],
                    [244,'/* read state of left controller, trackerIndex=1'],
                    [245,'extra chunks are added to track headset and controllers in the same cycle'],
                    [246,'controllers are symmetric and identical, left and right can be defined in downstream codes  */'],
                    [253,'/* read state of right controller, trackerIndex=2 */'],
                    [261,'/* Vrui/DeviceTest code ends */'],
                    [262,'/*****************************/'],
                    [264,'// headset bias, roomsetup will be further tested'],
                    [271,'//std::cout<<getmodelstate.response<<std::endl;'],
                    [273,'// plug in the data to message and publish it to gazebo'],
                    [274,'// coordinate in VIVE is different from gazebo, rotation matrix from VIVE to Gazebo is R = [0,0,-1; -1,0,0; 0,1,0]'],
                    [296,'/* Custom message for ROS controller */'],
                    [297,'/* headset */'],
                    [300,'/* left controller */'],
                    [320,'/* right controller */'],
                    [343,'/******************************************/'],
                    [344,'/* following code is from Vrui/DeviceTest */'],
                    [345,'//devices state needs to be unlocked after read'],
                    [349,'/* Check for a key press event: (original commitment)*/'],
                    [360,'/* Wait for next packet: (original commitment)*/'],
                    [363,'// rate control from ros, unnecessary, VIVE packet comes at a rate of 90hz'],
                    [365,'//end of while(ros::ok()) loop'],
                    [367,'//end of the huge try loop'],
                    [373,'// After ros is shut down'],
                    [374,'//to end (delete the if loop(946-949))'],
                    [379,'/* Clean up and terminate: (original commitment)*/'],
                    [387,'// end of int main()']]


    while line:

        if wanttedlinesnum[cnt_wanted] == cnt_lines:
            wanttedlines[cnt_wanted] = line.strip()
            if cnt_wanted+1 < len(wanttedlinesnum):
                cnt_wanted += 1

        line = f.readline()
        cnt_lines += 1

    f.close()

    f_tar= open("src/vrui_mdf/src/tracking.cpp","w+")
    #line_tar = f_tar.readline()
    cnt_2 = 1

    
    drifting_lines = 28

    total_lines = 387 + drifting_lines

    while cnt_2 <= total_lines:

        currentline = ''
        commit = ''
        space_while = ''
        space_try = ''
        space_main = ''

        if 224 + drifting_lines < cnt_2 < 365+ drifting_lines:
            space_while = '     '
        if 168 + drifting_lines < cnt_2 < 367 + drifting_lines:
            space_try = '     '
        if 116 + drifting_lines < cnt_2 < 387 + drifting_lines:
            space_main = '     '

        if cnt_2 > 68:
            drifting_commitment = 28
        else:
            drifting_commitment = 0


        if commitment[cnt_commit][0] + drifting_commitment == cnt_2:
        
            commit = commitment[cnt_commit][1]
            if cnt_commit+1 < len(commitment):
                cnt_commit += 1


        if pastelines[cnt_paste][1] + drifting_lines == cnt_2:

            currentline = wanttedlines[pastelines[cnt_paste][0] - 1]
            if cnt_paste+1 < len(pastelines):
                cnt_paste += 1

        if inserlines[cnt_inser][0] + drifting_lines == cnt_2:

            currentline = inserlines[cnt_inser][1]
            if cnt_inser+1 < len(inserlines):
                cnt_inser += 1

        if replacelinesnum[cnt_replace] + drifting_lines == cnt_2:

            currentline = currentline.replace(rep_bef[cnt_replace],rep_aft[cnt_replace])
            if cnt_replace+1 < len(replacelinesnum):
                cnt_replace += 1

        if replacelinesnum_1[cnt_replace_1] + drifting_lines == cnt_2:

            currentline = currentline.replace(rep_bef_1[cnt_replace_1],rep_aft_1[cnt_replace_1])
            if cnt_replace_1+1 < len(replacelinesnum_1):
                cnt_replace_1 += 1


        f_tar.write("{}{}{}{}{}\n".format(space_while,space_try,space_main,currentline,commit))
        cnt_2 += 1

#EOF
