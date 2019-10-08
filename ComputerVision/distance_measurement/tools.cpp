#include <iostream>
#include "opencv_inc.h"
#include <opencv2/opencv.hpp>  
#include <opencv/cv.hpp>  
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
using namespace std;
using namespace cv;


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

int image_save()
{
	VideoCapture capture(1);

	capture.set(CAP_PROP_FRAME_WIDTH, 1280);
	capture.set(CAP_PROP_FRAME_HEIGHT, 720);

	if (!capture.isOpened())
		return -1;
	cout << "Image will be save..." << endl;
	cv::namedWindow("Image");
	while (true)
	{
		Mat frame;
		int num = 0;

		capture >> frame;

		line(frame, Point(640 / 2, 240 - 25), Point(640 / 2, 240 + 25), Scalar(0, 33, 133), 1);
		line(frame, Point(0, 480 / 2), Point(639, 480 / 2), Scalar(33, 33, 133), 1);

		int y = 457;
		line(frame, Point(0, y), Point(639, y), Scalar(0, 0, 0), 1);
		setMouseCallback("Image", on_mouse);
		imshow("Image", frame);
		if (waitKey(1) == 's') 
		{
			num++;
		}
		else if (waitKey(1) == 'q') {
			cvDestroyWindow("Image");
			break;
		}

	}
	cout << "333..." << endl;
	return 0;
}