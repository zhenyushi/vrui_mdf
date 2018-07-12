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


    pastelinesnum = [1,2,3,4,5,6,7,8,9,10,11,12,
                     13,14,15,16,17,18,19,20,21,22,23,
                     24,25,
                     27,27,27,28,29,30,
                     31,32,33,34,35,36,37,38,39,
                     40,41,
                     42,43,
                     44,45,46,
                     47,48,
                     49,50,51,
                     52,53,54,54,54,
                     55,
                     56,57,58,59,60,61,62,63,64,
                     65,
                     66,67,68,69,70,
                     71,72,73,74,77,78,79,80,82,83,
                     84]



    pastelocatenum = [41,42,43,44,45,47,48,49,50,52,53,54,
                      84,85,86,87,88,89,93,94,95,96,97,
                      115,116,
                      138,139,140,143,146,150,
                      153,154,155,156,157,158,159,160,161,
                      165,166,
                      167,168,
                      169,170,171,
                      172,173,
                      226,227,228,
                      230,231,235,247,254, #second replace loop needed
                      335,
                      340,341,342,343,344,345,346,347,348,
                      351,
                      357,358,359,360,361,
                      364,365,366,367,370,371,372,373,374,375,
                      377]
    cnt_paste = 0

    replacelinesnum = [139,140,155,247,254]
    cnt_replace = 0
    rep_bef = ['trackerIndex=0','trackerIndex=0','.c_str()','ts','ts']
    rep_aft = ['trackerIndex_left=1','trackerIndex_right=2','','ts_left','ts_right']

    replacelinesnum_1 = [247,254]
    cnt_replace_1 = 0
    rep_bef_1 = ['trackerIndex','trackerIndex']
    rep_aft_1 = ['trackerIndex_left','trackerIndex_right']

    inserlinesnum = [  62,65,66,67,69,70,71,72,73,74,76,77,78,79,80,
                       119,120,121,122,124,125,126,127,129,130,131,137,
                       175,176,177,178,179,180,181,182,183,184,185,186,
                       188,189,190,191,192,193,194,195,
                       197,198,
                       200,201,202,203,204,
                       206,207,208,209,210,
                       214,215,
		       221,222,
                       223,224,
                       236,237,238,239,
                       248,249,250,251,
                       255,256,257,258,
                       265,266,267,
                       269,270,
                       275,276,277,279,280,281,282,284,
                       288,291,292,293,295,296,297,298,300,301,302,303,304,
                       311,312,313,315,316,317,318,320,321,322,323,324,330,
                       353,355]
    cnt_inser = 0

    inserlines = [  '#include "vrui_mdf.h"',
                    '#include <ros/ros.h>',
                    '#include <gazebo_msgs/ModelState.h>',
                    '#include <tf/transform_broadcaster.h>',
                    '#include "tf/transform_datatypes.h"',
                    '#include <geometry_msgs/Quaternion.h>',
                    '#include <cmath>',
                    '#include <math.h>',
                    '#include<fstream>',
                    '#include <vrui_mdf/Vive.h>',
                    '#include <geometry_msgs/Twist.h>',
                    '#include <gazebo_msgs/SetModelState.h>',
                    '#include "gazebo_msgs/GetModelState.h"',
                    '#include "gazebo_msgs/DeleteModel.h"',
                    '#include "gazebo_msgs/SpawnModel.h"',
                    'ros::init(argc, argv, "camera_state");',
                    'ros::NodeHandle n;',
                    'ros::Rate r(90);',
		    'ros::service::waitForService("/gazebo/spawn_urdf_model", -1);',
                    'ros::Publisher gazebo_pub = n.advertise<gazebo_msgs::ModelState>("gazebo/set_model_state", 10);',
                    'gazebo_msgs::ModelState camera;',
                    'camera.model_name = "vr_view";',
                    'camera.reference_frame="world";',
                    'vrui_mdf::Vive vive;',
                    'vive.user_name = "vive";',
                    'ros::Publisher vive_state = n.advertise<vrui_mdf::Vive>("vrui/vive", 10);',
                    'char* serverName=0;',
                    'gazebo_msgs::SpawnModel sm;',
                    'ros::ServiceClient spawn_model;',
                    'spawn_model = n.serviceClient<gazebo_msgs::SpawnModel>("/gazebo/spawn_sdf_model");',
                    'std::ifstream ifs,ifs1;',
                    'ifs.open("/home/zhenyushi/.gazebo/models/controller/model.sdf");',
                    'std::stringstream stringstream;',
                    'stringstream << ifs.rdbuf();',
                    'sm.request.model_name = "base_test";',
                    'sm.request.model_xml = stringstream.str();',
                    'sm.request.robot_namespace = ros::this_node::getNamespace();',
                    'sm.request.reference_frame = "world";',
                    'spawn_model.call(sm);',
                    'ifs1.open("/home/zhenyushi/.gazebo/models/vr_view/model.sdf");',
                    'std::stringstream stringstream1;',
                    'stringstream1 << ifs1.rdbuf();',
                    'sm.request.model_name = "vr_view";',
                    'sm.request.model_xml = stringstream1.str();',
                    'sm.request.robot_namespace = ros::this_node::getNamespace();',
                    'sm.request.reference_frame = "world";',
                    'spawn_model.call(sm);',
                    'ros::ServiceClient client_set = n.serviceClient<gazebo_msgs::SetModelState>("/gazebo/set_model_state");',
                    'gazebo_msgs::SetModelState Setmodelstate;',
                    'Setmodelstate.request.model_state.model_name = "base_test";',
                    'Setmodelstate.request.model_state.reference_frame="world";',
                    'Setmodelstate.request.model_state.pose.position.x = 0;',
                    'Setmodelstate.request.model_state.pose.position.y = 0;',
                    'Setmodelstate.request.model_state.pose.position.z = 0;',
                    'Setmodelstate.request.model_state.pose.orientation.x = 0;',
                    'Setmodelstate.request.model_state.pose.orientation.y = 0;',
                    'Setmodelstate.request.model_state.pose.orientation.z = 0;',
                    'Setmodelstate.request.model_state.pose.orientation.w = 1;',
                    'client_set.call(Setmodelstate);',
                    'ros::ServiceClient client = n.serviceClient<gazebo_msgs::GetModelState>("/gazebo/get_model_state");',
                    'gazebo_msgs::GetModelState getmodelstate;',
		    'system("rosrun gazebo_ros spawn_model -file $(find vrui_mdf)/models/vr_view/model.sdf -sdf -model vr_view -y 0 -x 0 -z 1");',
		    'system("rosrun gazebo_ros spawn_model -file $(find vrui_mdf)/models/controller/model.sdf -sdf -model base_test -y 0 -x 0 -z 0");',
                    'while(ros::ok())',
                    '{',
                    'Point pos=ts.positionOrientation.getOrigin();',
                    'Rotation rot=ts.positionOrientation.getRotation();',
                    'const float* quaternion;',
                    'quaternion=rot.getQuaternion();',
                    'Point pos_left=ts_left.positionOrientation.getOrigin();',
                    'Rotation rot_left=ts_left.positionOrientation.getRotation();',
                    'const float* quaternion_left;',
                    'quaternion_left=rot_left.getQuaternion();',
                    'Point pos_right=ts_right.positionOrientation.getOrigin();',
                    'Rotation rot_right=ts_right.positionOrientation.getRotation();',
                    'const float* quaternion_right;',
                    'quaternion_right=rot_right.getQuaternion();',
                    'float bias_0 = -0.191;',
                    'float bias_1 = 2.2;',
                    'float bias_2 = 1.98;',
                    'getmodelstate.request.model_name = "base_test";',
                    'client.call(getmodelstate);',
                    'camera.pose.position.x = -1*pos[2] - bias_2 + getmodelstate.response.pose.position.x;',
                    'camera.pose.position.y = -1*pos[0] - bias_0 + getmodelstate.response.pose.position.y;',
                    'camera.pose.position.z = pos[1] + bias_1 + getmodelstate.response.pose.position.z;',
                    'camera.pose.orientation.x = -1*quaternion[2];',
                    'camera.pose.orientation.y = -1*quaternion[0];',
                    'camera.pose.orientation.z = quaternion[1];',
                    'camera.pose.orientation.w = quaternion[3];',
                    'gazebo_pub.publish(camera);',
                    'vive.headset = camera.pose;',
                    'vive.ctrl_left.pose.position.x = -1*pos_left[2] - bias_2 + getmodelstate.response.pose.position.x;',
                    'vive.ctrl_left.pose.position.y = -1*pos_left[0] - bias_0 + getmodelstate.response.pose.position.y;',
                    'vive.ctrl_left.pose.position.z = pos_left[1] + bias_1 + getmodelstate.response.pose.position.z;',
                    'vive.ctrl_left.pose.orientation.x = -1*quaternion_left[2];',
                    'vive.ctrl_left.pose.orientation.y = -1*quaternion_left[0];',
                    'vive.ctrl_left.pose.orientation.z = quaternion_left[1];',
                    'vive.ctrl_left.pose.orientation.w = quaternion_left[3];',
                    'vive.ctrl_left.buttons.system = state.getButtonState(2);',
                    'vive.ctrl_left.buttons.grip = state.getButtonState(3);',
                    'vive.ctrl_left.buttons.menu = state.getButtonState(4);',
                    'vive.ctrl_left.buttons.trigger = state.getButtonState(5);',
                    'vive.ctrl_left.buttons.trackpad = state.getButtonState(6);',
                    'vive.ctrl_right.pose.position.x = -1*pos_right[2] - bias_2 + getmodelstate.response.pose.position.x;',
                    'vive.ctrl_right.pose.position.y = -1*pos_right[0] - bias_0 + getmodelstate.response.pose.position.y;',
                    'vive.ctrl_right.pose.position.z = pos_right[1] + bias_1 + getmodelstate.response.pose.position.z;',
                    'vive.ctrl_right.pose.orientation.x = -1*quaternion_right[2];',
                    'vive.ctrl_right.pose.orientation.y = -1*quaternion_right[0];',
                    'vive.ctrl_right.pose.orientation.z = quaternion_right[1];',
                    'vive.ctrl_right.pose.orientation.w = quaternion_right[3];',
                    'vive.ctrl_right.buttons.system = state.getButtonState(8);',
                    'vive.ctrl_right.buttons.grip = state.getButtonState(9);',
                    'vive.ctrl_right.buttons.menu = state.getButtonState(10);',
                    'vive.ctrl_right.buttons.trigger = state.getButtonState(11);',
                    'vive.ctrl_right.buttons.trackpad = state.getButtonState(12);',
                    'vive_state.publish(vive);',
                    'r.sleep();',
                    '}']

    commitmentnum = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
		     41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,
		     56,57,58,59,60,61,64,67,83,92,100,102,104,105,107,108,110,111,113,118,123,133,134,136,137,138,139,140,143,
		     146,149,152,
		     164,213,216,217,218,219,220,225,230,234,240,241,244,245,246,253,261,262,264,271,273,274,286,287,290,
		     306,307,308,310,326,327,328,333,334,335,339,350,353,355,357,363,364,369,377]

    cnt_commit = 0
    commitment = [  '/********************************************************************',
                    '',
                    'Vrui_mdf/tracking - Node to read the tracking and buttons status from',
                    'a VR Device, plug the data into messages with a specific formate and',
                    'publush the message on a specific topic.',
                    '',
                    'The codes here to read the tracking data are from Vrui/DeviceTest, which',
                    'is a sample program of the Virtual Reality User Interface Library(Vrui),',
                    '',
                    'Current it only publishes to update the state for headset and left',
                    'controller models in Gazebo. - 03/19/2018',
                    '',
                    '---',
                    '',
                    'LICENSE INFORMATION:',
                    '',
                    'This file was generated by code written by Zhenyu Shi, a member of the',
                    'AS4SR Lab at the University of Cincinnati.',
                    '',
                    'The source code used to generate this file, and the code snippets in',
                    'the github.com/zhenyushi/Vrui_mdf repository included in this file are',
                    'released under a BSD 3-clause license:',
                    '',
                    'Copyright 2018 University of Cincinnati',
                    'All rights reserved. See LICENSE file at:',
                    'https://github.com/zhenyushi/Vrui_mdf',
                    'Additional copyright is held by others, as reflected in the commit',
                    'history and as listed below.',
                    '',
                    'The code snippets from the Vrui 4.5-001 library included in this file are',
                    'released under a GPL license, see below (in the "DeviceTest" section):',
                    '',
                    '/***********************************************************************',
                    'DeviceTest - Program to test the connection to a Vrui VR Device Daemon',
                    'and to dump device positions/orientations and button states.',
                    'Copyright (c) 2002-2016 Oliver Kreylos',
                    '',
                    'This file is part of the Virtual Reality User Interface Library (Vrui).',
                    '',
                    'The Virtual Reality User Interface Library is free software; you can',
                    'redistribute it and/or modify it under the terms of the GNU General',
                    'Public License as published by the Free Software Foundation; either',
                    'version 2 of the License, or (at your option) any later version.',
                    '',
                    'The Virtual Reality User Interface Library is distributed in the hope',
                    'that it will be useful, but WITHOUT ANY WARRANTY; without even the',
                    'implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR',
                    'PURPOSE.  See the GNU General Public License for more details.',
                    '',
                    'You should have received a copy of the GNU General Public License along',
                    'with the Virtual Reality User Interface Library; if not, write to the',
                    'Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA',
                    '02111-1307 USA',
                    '***********************************************************************/',
                    '/*',
                    '',
                    'The code sections that came from Vrui/Vrui-4.5-001/Vrui/Utilities/DeviceTest.cpp are the following:',
                    '-- lines 177 - 201 (codes to Initialize device client)',
                    '-- lines 235 - 286 (function to read tracking data from Vive headset)',
                    '',
                    '***********************************************************************/',
                    '',
                    '/*',
                    'GENERATED CODE STARTS HERE:',
                    '*/',
                    '',
                    '/* header files used in Vrui/DeviceTest */',
                    '/* file path needs to be define in CMakeLists.txt*/',
                    '/*',
                    'Vrui is built by a script, some of the classes and functions are',
                    'defined in .cpp or .icpp files, to import Vrui into ros package,',
                    'those files also need to be included. This vrui_mdf.h includes',
                    'all extra files that are needed.',
                    '*/',
                    '/* ros header files for model state publishing in Gazebo, added for Gazebo application */',
                    '// translation between Eular angle and Quaternion, unnecessary for tracking since Quaternion can be received directly',
                    '/* VIVE tracking data reading definitions, come directly from Vrui/DeviceTest */',
                    '/* VIVE headset configuration reading definitions, come directly from Vrui/DeviceTest */',
                    '/* main function, VIVE tracking parts are from Vrui/DeviceTest directly */',
                    '/***********************************************************************',
                    'The main thread here is to read position and orientation data from headset',
                    'and controllers, and publish it to the VR camera model in gazebo.',
                    'Originally, Vrui/DeviceTest has many different tracking and printing modes,',
                    'so it"s a very good sample to understand how Vrui works.',
                    'For this Gazebo application, codes for Vrui/DeviceTest are refered,',
                    'and unnecessary printing modes for this application are removed.',
                    '***********************************************************************/',
                    '/* Set up ros node and define publisher for gazebo */',
                    '/* gazebo model state publisher and topic */',
                    '/********************************************************************/',
                    '/* Vrui/DeviceTest code starts (order and detail might be modified) */',
                    '/* Parse command line: (original commitment)*/',
                    '//necessary, but usually fixed if only one headset are used',
                    '//index for headset',
                    '//index for left controller',
                    '//index for right controller',
                    '//switch for printing button in terminal, unnecessary for gazebo',
                    '//portnumber come from input in original Vrui/DeviceTest code, usually fixed if only one headset are used',
                    '/* Initialize device client: (original commitment)*/',
                    '/* a while loop can be used to replace this try, so that the code will wait for RunViveTracker.sh while using roslaunch (original commitment)*/',
                    '/* Run main loop: (original commitment)*/',
                    '//std::cout<<Setmodelstate.request<<std::endl;',
                    '/*',
                    'getmodelstate.request.model_name = "base_test";',
                    'client.call(getmodelstate);',
                    'std::cout<<getmodelstate.response<<std::endl;',
                    '*/',
                    '/* Get packet timestamp: (original commitment)*/',
                    '//devices state needs to be locked before read',
                    '/* read state of headset, trackerIndex=0 */',
                    '/* Eular angle representation is used in original Vrui/DeviceTest code,',
                    'getQuaternion() is defined in header files and works better for ros publishers */',
                    '/* read state of left controller, trackerIndex=1',
                    'extra chunks are added to track headset and controllers in the same cycle',
                    'controllers are symmetric and identical, left and right can be defined in downstream codes  */',
                    '/* read state of right controller, trackerIndex=2 */',
                    '/* Vrui/DeviceTest code ends */',
                    '/*****************************/',
                    '// headset bias, roomsetup will be further tested',
                    '//std::cout<<getmodelstate.response<<std::endl;',
                    '// plug in the data to message and publish it to gazebo',
                    '// coordinate in VIVE is different from gazebo, rotation matrix from VIVE to Gazebo is R = [0,0,-1; -1,0,0; 0,1,0]',
                    '/* Custom message for ROS controller */',
                    '/* headset */',
                    '/* left controller */',
                    '/* trackpad touching data not available yet */',
                    '//vive.ctrl_left.trackpad.x = ;',
                    '//vive.ctrl_left.trackpad.y = ;',
                    '/* right controller */',
                    '/* trackpad touching data not available yet */',
                    '//vive.ctrl_left.trackpad.x = ;',
                    '//vive.ctrl_left.trackpad.y = ;',
                    '/******************************************/',
                    '/* following code is from Vrui/DeviceTest */',
                    '//devices state needs to be unlocked after read',
                    '/* Check for a key press event: (original commitment)*/',
                    '/* Wait for next packet: (original commitment)*/',
                    '// rate control from ros, unnecessary, VIVE packet comes at a rate of 90hz',
                    '//end of while(ros::ok()) loop',
                    '//end of the huge try loop',
                    '// After ros is shut down',
                    '//to end (delete the if loop(946-949))',
                    '/* Clean up and terminate: (original commitment)*/',
                    '// end of int main()']

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

    total_lines = 377 + drifting_lines

    while cnt_2 <= total_lines:

        currentline = ''
        commit = ''
        space_while = ''
        space_try = ''
        space_main = ''

        if 224 + drifting_lines < cnt_2 < 355+ drifting_lines:
            space_while = '     '
        if 168 + drifting_lines < cnt_2 < 357 + drifting_lines:
            space_try = '     '
        if 116 + drifting_lines < cnt_2 < 377 + drifting_lines:
            space_main = '     '

        if cnt_2 > 68:
            drifting_commitment = 28
        else:
            drifting_commitment = 0


        if commitmentnum[cnt_commit] + drifting_commitment == cnt_2:
        
            commit = commitment[cnt_commit]
            if cnt_commit+1 < len(commitmentnum):
                cnt_commit += 1


        if pastelocatenum[cnt_paste] + drifting_lines == cnt_2:

            currentline = wanttedlines[pastelinesnum[cnt_paste] - 1]
            if cnt_paste+1 < len(pastelocatenum):
                cnt_paste += 1

        if inserlinesnum[cnt_inser] + drifting_lines == cnt_2:

            currentline = inserlines[cnt_inser]
            if cnt_inser+1 < len(inserlinesnum):
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
