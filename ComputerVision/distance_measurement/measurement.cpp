/* --- measurement.cpp 2019-07-04--- */
#include <iostream>
#include "opencv_inc.h"
#include <fstream>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include "RangeFinder.hpp"
#include <tuple>

using namespace cv;
//using namespace cv::dnn;
using namespace std;

#define DATASET 1       // 0 : PASCAL VOC, 1 : COCO dataset.
#define TRACKING_FRAMES 0


const String keys =
        "{ proto-caffe           | MobileNetSSD_deploy.prototxt   | MNSSD-300 model configuration - caffe}"
        "{ mnssdmodel-caffe      | MobileNetSSD_deploy.caffemodel | MNSSD-300 model weights - caffe}"
        "{ proto-tensorflow      | dn.pbtxt   | MNSSD-300 model configuration - tensorflow}"
        "{ mnssdmodel-tensorflow | frozen_inference_graph.pb      | MNSSD-300 model weights - tensorflow}"
        "{ camera_device         |   0 | camera device number }"
        "{ camera_width          | 640   | camera device width  }"
        "{ camera_height         | 480    | camera device height }"
        "{ video1                |20180525_ACC_Short_80km_30m_flipped.mov| video or image for detection }"
        "{ video2                | 20180525_ACC_Short_86km_40m_Truck_flipped.mov | video or image for detection }"
        "{ video3                | 20180525_ACC_Mid_76km_50m_flipped.mov | video or image for detection }"
        "{ video4                | 20180525_ACC_Far_76Km_50m_flipped.mov | video or image for detection }"
        "{ min_confidence        | 0.3 | min confidence  }"
        "{ opencl                | false  | enable OpenCL   }"
        "{ class_names           | coco.names | File with class names }"
        "{ front_or_rear         | 1      |    1=front, 2= rear}"
        "{ video_num             | 4 |    1, 2,3,4}"
        "{ camerainstall_height          | 150 | Camera inst height }"
        "{ camerainstall_angle         | 0 | Camera inst angle }";


short gCameraInstallheight=0;
short gcamera_height = 0;

static void on_mouse(int event, int x, int y, int flags, void* YiTa)
{
	char debugMessage[256] = {0};
	RangeFinder RangeFinder2;
	RangeFinder2.initialize();
	
	int Distant2;
	float Distancef2;
	
	short vanishingPoffset;
	ifstream input("vanishingPoffset.txt");
	if(input.is_open()){
		string number;
		getline(input,number); //read number
		vanishingPoffset = atoi(number.c_str()); //convert to integer
	}
	
	switch(event) {
	case CV_EVENT_LBUTTONUP:
		cout << "===============:" << gcamera_height << endl;
		cout << "===============CameraInstallheight:" << gCameraInstallheight << endl;
		Distant2 = RangeFinder2.getRange(gcamera_height - y,gCameraInstallheight);
		if (Distant2<1000)
		{
			Distancef2=(float)Distant2/100;
			float tominus = Distant2%(10);
			cout<<tominus<<endl;
			Distancef2-=tominus/100;
			cout<<"distance:"<<Distancef2<<endl;
		}
		else
		{
			Distant2/=100;
			cout<<"distance:"<<Distant2<<endl;
		}
		
		//cout<<"vanishingPoffset"<<vanishingPoffset<<endl;
		//cout<<"y-vanishing point value: "<<y-360-vanishingPoffset<<endl;
		
		sprintf_s(debugMessage, "click (%d, %d)\n", x, y);
		printf("%s\n", debugMessage);
		break;
	}
}

int main_measure(int argc, const char * argv[]){
	CommandLineParser parser(argc, argv, keys);
	
	/////down 180523
	int Distant = 0;
	int BoxBtmfor720;
	int vanishingPoffset = 0;
	int BoxArea = 0;

	ifstream input2("CameraIsntallHeight.txt");
	if (input2.is_open()) {
		string number;
		getline(input2, number); //read number
		gCameraInstallheight = atoi(number.c_str()); //convert to integer
	}

	VideoCapture cap;
	string targetvid;
	if (parser.has("camera_device") && parser.get<int>("camera_device") < 5) {
		int cameraDevice = parser.get<int>("camera_device");
		cap = VideoCapture(cameraDevice);
		if (!cap.isOpened()) {
			cout << "Couldn't find camera: " << cameraDevice << endl;
			return -1;
		}
		
		cap.set(CAP_PROP_FRAME_WIDTH, parser.get<int>("camera_width"));
		cap.set(CAP_PROP_FRAME_HEIGHT, parser.get<int>("camera_height"));
	}
	else {
		if (parser.get<String>("video_num") == "1")
			targetvid = parser.get<String>("video1");
		//    cap.open(parser.get<String>("video1"));
		else if (parser.get<String>("video_num") == "2")
			targetvid = parser.get<String>("video2");
		else if (parser.get<String>("video_num") == "3")
			targetvid = parser.get<String>("video3");
		else if (parser.get<String>("video_num") == "4")
			targetvid = parser.get<String>("video4");
		cap.open(targetvid);
		if (!cap.isOpened()) {
			cout << "Couldn't open image or video: " << parser.get<String>("video") << endl;
			return -1;
		}
	}
	
	bool paused = false;
	int frameCount = 0;
	float accFPS = 0.0f;
	int trackingFrames = (TRACKING_FRAMES == 0) ? -1 : TRACKING_FRAMES;
	gcamera_height = parser.get<int>("camera_height");

	cv::namedWindow("Detection-measure");
	while (true)
	{
		if (!paused) {
			Mat frame;
			cap >> frame;
			
			if (frame.empty()) {
				break;
			}
			
			if (frame.channels() == 4) {
				cvtColor(frame, frame, COLOR_BGRA2BGR);
			}
			
			Mat framegray;
			// convert RGB image to gray
			cvtColor(frame, framegray, CV_BGR2GRAY);
			int64 start = getTickCount();

			// ===== Start of Algorithm ===== //
			////////////////////////// transform detectBoxes back to ori size
			setMouseCallback("Detection-measure", on_mouse);
			imshow("Detection-measure", frame);
		}

		char c = (char)waitKey(10);
		if (c == 'q') {
			cvDestroyWindow("Detection-measure");
			break;
		}
		else if (c > 0) {
			paused = !paused;
		}
	}
	return 0;
}


