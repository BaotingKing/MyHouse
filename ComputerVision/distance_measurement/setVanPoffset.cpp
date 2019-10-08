/*------setVanPoffset.cpp 2019-07-04-------*/
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

const String keys =
        "{ proto-caffe           | MobileNetSSD_deploy.prototxt   | MNSSD-300 model configuration - caffe}"
        "{ mnssdmodel-caffe      | MobileNetSSD_deploy.caffemodel | MNSSD-300 model weights - caffe}"
        "{ proto-tensorflow      | dn.pbtxt   | MNSSD-300 model configuration - tensorflow}"
        "{ mnssdmodel-tensorflow | frozen_inference_graph.pb      | MNSSD-300 model weights - tensorflow}"
        "{ camera_device         |  0  | camera device number }"
        "{ camera_width          | 640   | camera device width  }"
        "{ camera_height         | 480    | camera device height }"
        "{ video1                |20180525_ACC_Short_80km_30m_flipped.mov| video or image for detection }"
        "{ video2                | 20180525_ACC_Short_86km_40m_Truck_flipped.mov | video or image for detection }"
        "{ video3                | 20180525_ACC_Mid_76km_50m_flipped.mov | video or image for detection }"
        "{ video4                | 20180525_Front_70m_rotated.mp4 | video or image for detection }"
        "{ min_confidence        | 0.3 | min confidence  }"
        "{ opencl                | false  | enable OpenCL   }"
        "{ class_names           | coco.names | File with class names }"

        "{ video_num             | 2 |    1, 2,3,4}"
        "{ camerainstall_angle          | 0 | Camera angle }"
        "{ camerainstall_height  | 150| Camera inst height}";


#define DATASET 1       // 0 : PASCAL VOC, 1 : COCO dataset.
#define TRACKING_FRAMES 0

Mat *debugFrame = NULL;
short CameraInstallheight = 0;

static void on_mouse(int event, int x, int y, int flags, void* YiTa)
{
	char debugMessage[256] = { 0 };
	//sprintf(debugMessage, "click (%d, %d)\n", x, y);
	//printf("%s\n", debugMessage);
	switch (event) {
	case CV_EVENT_LBUTTONUP:
		/*
		unsigned char B = *(debugFrame->data + x*debugFrame->cols + y);
		unsigned char G = *(debugFrame->data + x*debugFrame->cols + y + 1) ;
		unsigned char R = *(debugFrame->data + x*debugFrame->cols + y + 2);
		*/
		sprintf_s(debugMessage, "click (%d, %d)\n", x, y);
		printf("%s\n", debugMessage);
		break;
	}
}


void locVanPoffset(Mat frame, Mat framegray, CommandLineParser parser) {
	int vanishingPoffset = 0;
	// adjust box position			
	short boardarealeft = (parser.get<int>("camera_width") >> 1) - (80 >> 1);                                //Set the size of the white box
	short boardarearight = (parser.get<int>("camera_width") >> 1) + (80 >> 1);
	short boardareatop = (parser.get<int>("camera_height") >> 1) - (160 >> 1);
	short boardareabtm = (parser.get<int>("camera_height") >> 1) + (170 >> 1);
	short boardareaheight = boardareabtm - boardareatop + 1;
	short boardareawidth = boardarearight - boardarealeft + 1;

	rectangle(frame, Point(boardarealeft, boardareatop), Point(boardarearight, boardareabtm), Scalar(255, 255, 255), 4);

	//   cout<<"!!!!"<<vanishingPoffset;
	short line1 = 0;                  //line记录的是标定板上面的黑白交替的位置，下面的for循环就是找这些值的过程
	short line2 = 0;
	short line3 = 0;
	short line4 = 0;
	short line5 = 0;
	short line6 = 0;
	short line7 = 0;
	short line8 = 0;
	short blockheight = 0;
	int _stride = framegray.step;
	uint8_t *myData = framegray.data;
	int cnt = 0;
	int totalyinrow = 0;
	int totalyinnxtrow = 0;
	short totalyinrowave = 0;
	short totalyinnxtrowave = 0;

	for (int il = boardareatop; il < boardareatop + (boardareaheight >> 1); il++)       ////black to white;
	{
		cnt = 0;
		totalyinrow = 0;
		totalyinnxtrow = 0;

		for (int jl = boardarealeft + (boardareawidth >> 2); jl <= boardarearight - (boardareawidth >> 2); jl++)
		{
			totalyinrow += myData[il * _stride + jl];
			totalyinnxtrow += myData[(il + 1) * _stride + jl];
			cnt++;
		}

		totalyinrowave = totalyinrow / cnt;
		totalyinnxtrowave = totalyinnxtrow / cnt;

		if (totalyinnxtrowave > totalyinrowave * 5 / 4 && totalyinnxtrowave - totalyinrowave > 40)
		{
			line1 = il;
			cout << "line1found" << endl;
			break;
		}
	}

	for (int il = line1 + (boardareaheight >> 4); il < line1 + (boardareaheight >> 4) + (boardareaheight >> 2); il++)       ////white to black;
	{
		cnt = 0;
		totalyinrow = 0;
		totalyinnxtrow = 0;
		for (int jl = boardarealeft + (boardareawidth >> 2); jl <= boardarearight - (boardareawidth >> 2); jl++)
		{
			totalyinrow += myData[il * _stride + jl];
			totalyinnxtrow += myData[(il + 1) * _stride + jl];
			cnt++;
		}

		totalyinrowave = totalyinrow / cnt;
		totalyinnxtrowave = totalyinnxtrow / cnt;

		if (totalyinrowave > totalyinnxtrowave * 5 / 4 && totalyinrowave - totalyinnxtrowave > 40)
		{
			line2 = il;
			blockheight = line2 - line1;
			break;
		}
	}

	for (int il = line2 + (blockheight * 9 / 10); il < line2 + (blockheight * 9 / 10) + blockheight * 11 / 10; il++)       ////black to white;
	{
		cnt = 0;
		totalyinrow = 0;
		totalyinnxtrow = 0;
		for (int jl = boardarealeft + (boardareawidth >> 2); jl <= boardarearight - (boardareawidth >> 2); jl++)
		{
			totalyinrow += myData[il * _stride + jl];
			totalyinnxtrow += myData[(il + 1) * _stride + jl];
			cnt++;
		}

		totalyinrowave = totalyinrow / cnt;
		totalyinnxtrowave = totalyinnxtrow / cnt;

		if (totalyinnxtrowave > totalyinrowave * 5 / 4 && totalyinnxtrowave - totalyinrowave > 40)
		{
			line3 = il;
			break;
		}
	}

	for (int il = line3 + (blockheight * 9 / 10); il < line3 + (blockheight * 9 / 10) + blockheight * 11 / 10; il++)       ////w to b;
	{
		cnt = 0;
		totalyinrow = 0;
		totalyinnxtrow = 0;
		for (int jl = boardarealeft + (boardareawidth >> 2); jl <= boardarearight - (boardareawidth >> 2); jl++)
		{
			totalyinrow += myData[il * _stride + jl];
			totalyinnxtrow += myData[(il + 1) * _stride + jl];
			cnt++;
		}

		totalyinrowave = totalyinrow / cnt;
		totalyinnxtrowave = totalyinnxtrow / cnt;
		if (totalyinrowave > totalyinnxtrowave * 5 / 4 && totalyinrowave - totalyinnxtrowave > 40)
		{
			line4 = il;
			break;
		}
	}

	for (int il = line4 + (blockheight * 9 / 10); il < line4 + (blockheight * 9 / 10) + blockheight * 11 / 10; il++)       ////b to w;
	{
		cnt = 0;
		totalyinrow = 0;
		totalyinnxtrow = 0;
		for (int jl = boardarealeft + (boardareawidth >> 2); jl <= boardarearight - (boardareawidth >> 2); jl++)
		{
			totalyinrow += myData[il * _stride + jl];
			totalyinnxtrow += myData[(il + 1) * _stride + jl];
			cnt++;
		}

		totalyinrowave = totalyinrow / cnt;
		totalyinnxtrowave = totalyinnxtrow / cnt;

		if (totalyinnxtrowave > totalyinrowave * 5 / 4 && totalyinnxtrowave - totalyinrowave > 40)
		{
			line5 = il;
			break;
		}
	}

	for (int il = line5 + (blockheight * 9 / 10); il < line5 + (blockheight * 9 / 10) + blockheight * 11 / 10; il++)       ////w to b;
	{
		cnt = 0;
		totalyinrow = 0;
		totalyinnxtrow = 0;
		for (int jl = boardarealeft + (boardareawidth >> 2); jl <= boardarearight - (boardareawidth >> 2); jl++)
		{
			totalyinrow += myData[il * _stride + jl];
			totalyinnxtrow += myData[(il + 1) * _stride + jl];
			cnt++;
		}
		totalyinrowave = totalyinrow / cnt;
		totalyinnxtrowave = totalyinnxtrow / cnt;

		if (totalyinrowave > totalyinnxtrowave * 5 / 4 && totalyinrowave - totalyinnxtrowave > 40)
		{
			line6 = il;
			break;
		}
	}

	for (int il = line6 + (blockheight * 9 / 10); il < line6 + (blockheight * 9 / 10) + blockheight * 11 / 10; il++)       ////b to w;
	{
		cnt = 0;
		totalyinrow = 0;
		totalyinnxtrow = 0;
		for (int jl = boardarealeft + (boardareawidth >> 2); jl <= boardarearight - (boardareawidth >> 2); jl++)
		{
			totalyinrow += myData[il * _stride + jl];
			totalyinnxtrow += myData[(il + 1) * _stride + jl];
			cnt++;
		}
		totalyinrowave = totalyinrow / cnt;
		totalyinnxtrowave = totalyinnxtrow / cnt;

		if (totalyinnxtrowave > totalyinrowave * 5 / 4 && totalyinnxtrowave - totalyinrowave > 40)
		{
			line7 = il;
			break;
		}
	}

	//adjust according to how cali board is made
	short offset190 = line1 - (parser.get<int>("camera_height") >> 1);  //Since the height of the calibration plate is 1m,1m above ground, so line1 is at 190cm...Line7 in 130 cm
	short offset180 = line2 - (parser.get<int>("camera_height") >> 1);
	short offset170 = line3 - (parser.get<int>("camera_height") >> 1);
	short offset160 = line4 - (parser.get<int>("camera_height") >> 1);
	short offset150 = line5 - (parser.get<int>("camera_height") >> 1);
	short offset140 = line6 - (parser.get<int>("camera_height") >> 1);
	short offset130 = line7 - (parser.get<int>("camera_height") >> 1);

	if (line1)     //??????
		cout << line1 << " " << line2 << " " << line3 << " " << line4 << " " << line5 << " " << line6 << endl;

	if (line1&&line2&&line3&&line4&&line5&&line6)
	{
		line(frame, Point(boardarealeft, line1), Point(boardarearight, line1), Scalar(255, 0, 0), 2);
		line(frame, Point(boardarealeft, line2), Point(boardarearight, line2), Scalar(0, 0, 255), 2);
		line(frame, Point(boardarealeft, line3), Point(boardarearight, line3), Scalar(0, 0, 255), 2);
		line(frame, Point(boardarealeft, line4), Point(boardarearight, line4), Scalar(0, 0, 255), 2);
		line(frame, Point(boardarealeft, line5), Point(boardarearight, line5), Scalar(0, 0, 255), 2);
		line(frame, Point(boardarealeft, line6), Point(boardarearight, line6), Scalar(0, 0, 255), 2);

		//cout<<"vanishpointset"<<endl;
		if (CameraInstallheight >= 140 && CameraInstallheight < 150)   //The following the if...Else is interpolation to find the location of vanishongpoint at any camera height
		{
			vanishingPoffset = (offset150 - offset140)*(CameraInstallheight - 140) / 10 + offset140;
		}
		else if (CameraInstallheight >= 150 && CameraInstallheight < 160)
		{
			vanishingPoffset = (offset160 - offset150)*(CameraInstallheight - 150) / 10 + offset150;
			//  cout<<offset160<<" "<<offset150<<" "<< ((CameraInstallheight-150)/10)<<" "<<offset150<<endl;
			//    cout<<vanishingPoffset<<endl;
		}
		else if (CameraInstallheight >= 160 && CameraInstallheight < 170)
		{
			vanishingPoffset = (offset170 - offset160)*(CameraInstallheight - 160) / 10 + offset160;
		}
		else if (CameraInstallheight >= 170 && CameraInstallheight < 180)
		{
			vanishingPoffset = (offset180 - offset170)*(CameraInstallheight - 170) / 10 + offset170;
		}
		else if (CameraInstallheight >= 180 && CameraInstallheight < 190)
		{
			vanishingPoffset = (offset190 - offset180)*(CameraInstallheight - 180) / 10 + offset180;
		}
		cout << "parameter: " << vanishingPoffset << endl;
	}

	ofstream file;
	file.open("vanishingPoffset.txt");
	file << vanishingPoffset;
	file.close();

}


int main_setVanPoffset(int argc, const char * argv[]) {
    CommandLineParser parser(argc, argv, keys);

    /////down 180523   nothing used 
    int CameraInstallAngle = parser.get<int>("camerainstall_angle");
    int Distant=0;
    int BoxBtmfor720;    
    int BoxArea =0;
	RangeFinder RangeFinder1;
    RangeFinder1.initialize();

	ifstream input2("CameraIsntallHeight.txt");
	if(input2.is_open()){
		string number;
		getline(input2,number); //read number
		CameraInstallheight = atoi(number.c_str()); //convert to integer
		cout<<"CameraInstallheight:"<<CameraInstallheight<<endl; //print it out
	}
	
	///////////////////////////////////////////////
	VideoCapture cap;
    string targetvid;
	if (parser.has("camera_device")) {
		int cameraDevice = parser.get<int>("camera_device");
		cap = VideoCapture(cameraDevice);
		if (!cap.isOpened()) {
			cout << "Couldn't find camera: " << cameraDevice << endl;
			return -1;
		}
		cout << "********************************************" << endl;
		cout << cap.get(CV_CAP_PROP_FRAME_WIDTH) << cap.get(CV_CAP_PROP_FRAME_HEIGHT) << endl;
		cap.set(CAP_PROP_FRAME_WIDTH, parser.get<int>("camera_width"));
		cap.set(CAP_PROP_FRAME_HEIGHT, parser.get<int>("camera_height"));
		cout << "---------------------------------------------" << endl;
		cout << cap.get(CV_CAP_PROP_FRAME_WIDTH) << cap.get(CV_CAP_PROP_FRAME_HEIGHT) << endl;
	} else {
		if(parser.get<String>("video_num")=="1")
			targetvid=parser.get<String>("video1");
		//    cap.open(parser.get<String>("video1"));
		else if(parser.get<String>("video_num")=="2")
			targetvid=parser.get<String>("video2");
		else if (parser.get<String>("video_num")=="3")
			targetvid=parser.get<String>("video3");
		else if (parser.get<String>("video_num")=="4")
			targetvid=parser.get<String>("video4");		
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

    cv::namedWindow("Detection-VanishPoint");
	while (true)
	{
		if (!paused) {
			Mat frame;
			debugFrame = &frame;
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
			setMouseCallback("Detection-VanishPoint", on_mouse);
			//    DebugDraw(frame);			
			frameCount++;	
			locVanPoffset(frame, framegray, parser);
			line(frame, Point(0, parser.get<int>("camera_height")>>1), Point(parser.get<int>("camera_width") - 1, parser.get<int>("camera_height")>>1), Scalar(0, 255, 255), 1);
			//line(frame, Point(0, CameraInstallheight), Point(parser.get<int>("camera_width") - 1, CameraInstallheight), Scalar(255, 255, 255), 1);
			// =====  End of Algorithm  ===== //	

            imshow("Detection-VanishPoint", frame);
        }
		
		char c = (char)waitKey(10);
		if (c == 'q') {
			cvDestroyWindow("Detection-VanishPoint");
			break;
		} else if (c > 0) {
			paused = !paused;
		}
	}  
	return 0;
}

