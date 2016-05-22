#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_io.h>

using namespace cv;
using namespace std;
using namespace dlib;

void extract_frames(const string &videoFilePath) {

	try {
		
		VideoCapture cap(videoFilePath);
		if (!cap.isOpened())
			CV_Error(CV_StsError, "Can't open");
		
		std::vector<int> compression_params;
		compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);
		
		for (int frameNum = 0; frameNum < cap.get(CV_CAP_PROP_FRAME_COUNT); frameNum++) {
			Mat frame;
			cap >> frame;
			
			string filePath = "/home/walpurisnacht/Downloads/vid/" + to_string(static_cast<long long>(frameNum)) + ".jpg";
			imwrite(filePath, frame, compression_params);
			cout << "Writing: " << filePath << endl;
		}
	}
	
	catch ( cv::Exception& e) {
		cerr << e.msg << endl;
		exit(1);
	}
}


/*void save_frames(std::vector<Mat>& frames, const string& outputDir) {
	std::vector<int> compression_params;
	compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);
	int frameNumber;
	std::std::vector<Mat>::iterator frame;
	for (frameNumber=0, frame = frames.begin();
		 frame != frames.end(); ++frame, ++frameNumber) {
		string filePath = outputDir + to_string(static_cast<long long>(frameNumber)) + ".jpg";
		imwrite(filePath, *frame, compression_params);
	}
}*/

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

int main(int argc, char** argv) {
	try {
		
		if (argc == 1)
		{
			cout << "./[exec] [path to model] [path to source]" << endl;
			return 0;
		}
		
		frontal_face_detector detector = get_frontal_face_detector();
		shape_predictor sp;
		deserialize(argv[1]) >> sp; //load train model
		
		image_window win, win_faces;
		
		for (int i = 2; i < argc; ++i)
		{
			cout << "Processing img " << argv[i] << endl;
			array2d<rgb_pixel> img;
			load_image(img, argv[i]);
			pyramid_up(img);
			
			std::vector<dlib::rectangle> dets = detector(img);
			cout << "Number of faces detected: " << dets.size() << endl;
			
			std::vector<full_object_detection> shapes;
            for (unsigned long j = 0; j < dets.size(); ++j)
            {
                full_object_detection shape = sp(img, dets[j]);
                cout << "number of parts: "<< shape.num_parts() << endl;
                cout << "pixel position of first part:  " << shape.part(0) << endl;
                cout << "pixel position of second part: " << shape.part(1) << endl;
                shapes.push_back(shape);
            }
			
			win.clear_overlay();
            win.set_image(img);
            win.add_overlay(render_face_detections(shapes));
			
			dlib::array<array2d<rgb_pixel> > face_chips;
            extract_image_chips(img, get_face_chip_details(shapes), face_chips);
            win_faces.set_image(tile_images(face_chips));

            cout << "Hit enter to process the next image..." << endl;
            cin.get();
		}
		
	}
	catch (exception& e)
	{
		cerr << "\nException thrown!" << endl;
		cerr << e.what() << endl;
	}
	//extract_frames("/home/walpurisnacht/Downloads/vid/vid.mp4");
	return 1;
}