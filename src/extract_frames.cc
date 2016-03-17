#include <opencv2/core/core.hpp>
//#include <opencv2/video/video.hpp>
//#include <opencv2/photo/photo.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

void extract_frames(const string &videoFilePath, vector<Mat>& frames) {

	try {
		
		VideoCapture cap(videoFilePath);
		if (!cap.isOpened())
			CV_Error(CV_StsError, "Can't open");
		
		for (int frameNum = 0; frameNum < cap.get(CV_CAP_PROP_FRAME_COUNT); frameNum++) {
			Mat frame;
			cap >> frame;
			frames.push_back(frame);
		}
	}
	
	catch ( cv::Exception& e) {
		cerr << e.msg << endl;
		exit(1);
	}
}


void save_frames(vector<Mat>& frames, const string& outputDir) {
	vector<int> compression_params;
	compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);
	int frameNumber;
	std::vector<Mat>::iterator frame;
	for (frameNumber=0, frame = frames.begin();
		 frame != frames.end(); ++frame, ++frameNumber) {
		string filePath = outputDir + to_string(static_cast<long long>(frameNumber)) + ".jpg";
		imwrite(filePath, *frame, compression_params);
	}
}

void save_vid() {
	VideoCapture in_cap("/home/walpurisnacht/Downloads/vid/%3d.jpg");
	Mat img;
	
	VideoWriter out_cap("/home/walpurisnacht/Downloads/vid/vid.mp4", CV_FOURCC('F','M','P','4'), 30, Size(560,360));
	
	while (true) {
		
		in_cap >> img;
		
		if (img.empty()) break;
		
		out_cap.write(img);
	}
}

int main() {
	vector<Mat> frames;
	extract_frames("/home/walpurisnacht/Downloads/vid/[AKROSS_Con_2015]_Sutrue_-_The_love_story_of_the_crab_and_the_Vampire.mp4",frames);
	save_frames(frames, "/home/walpurisnacht/Downloads/vid/");
	//save_vid();
	return 1;
}