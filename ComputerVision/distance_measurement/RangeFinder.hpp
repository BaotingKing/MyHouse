#include <tuple>
#include <vector>
using namespace std;
class RangeFinder
{
public:
	RangeFinder() { };
	~RangeFinder() { };

	// void updateTrackingWindow(std::vector<std::tuple<int, float, cv::Rect> > trackingBoxes, const cv::Mat &frame);
	//std::vector<std::pair<int, cv::Rect> > trackingObjects(const cv::Mat &frame);
	//void forceReset();
	int getRange(int BoxBtm, int CameraHeight);
	void initialize();

private:
	short vanishingPoffset=0;
	
	//<pixels from image btm/image height,distant >
	
	vector<tuple<int, int>> RangeTable140;
	vector<tuple<int, int>> RangeTable150;
	vector<tuple<int, int>> RangeTable160;
	vector<tuple<int, int>> RangeTable170;

	/*
	if(Angle == 0)
	a=0;
	else if(Angle==10)
	a=160;
	else if(Angle==20)
	a=341;
	*/
};
