#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_io.h>
#include <iostream>

using namespace std;
using namespace dlib;

void draw_img(unsigned long start, unsigned long end, array2d<rgb_pixel> &img, rgb_pixel color, full_object_detection shape)
{
	for (unsigned long z = start; z <= end; ++z)
	{
		draw_line(img, shape.part(z), shape.part(z-1), color);
	}
}

int main(int argc, char** argv)
{
	try
	{
		if (argc == 1)
		{
			cout << "Program parameter:" << endl;
			cout << "[path to model] [path to jpg]/*.jpg" << endl;
		}
		
		frontal_face_detector detector = get_frontal_face_detector();
		
		
		shape_predictor sp;
		deserialize(argv[1]) >> sp;
		
		image_window win;
		
		const rgb_pixel color = rgb_pixel(0,255,0);
		
		for (int i = 2; i < argc; ++i)
		{
			//Face
			cout << "Processing image " << argv[i] << endl;
			
			array2d<rgb_pixel> img;
			load_image(img, argv[i]);
			
			pyramid_up(img);
			
			std::vector<rectangle> dets = detector(img);
			cout << "Number of faces detected: " << dets.size() << endl;
			
			//Landmark
			std::vector<full_object_detection> shapes;
			for (unsigned long j = 0; j < dets.size(); ++j)
			{
				full_object_detection shape = sp(img, dets[j]);
				/*
				cout << shape.part(n) << endl;
				*/
				
				if (shape.num_parts() == 0) continue;
				
				//Draw
				draw_img(1,16,img,color,shape);
				
				draw_img(28,30,img,color,shape);
				
				draw_img(18,21,img,color,shape);
				
				draw_img(23,26,img,color,shape);
				
				draw_img(31,35,img,color,shape);
				draw_line(img, shape.part(30), shape.part(35), color);
				
				draw_img(37,41,img,color,shape);
				draw_line(img, shape.part(36), shape.part(41), color);
				
				draw_img(43,47,img,color,shape);
				draw_line(img, shape.part(42), shape.part(47), color);
				
				draw_img(49,59,img,color,shape);
				draw_line(img, shape.part(48), shape.part(59), color);
				
				draw_img(61,67,img,color,shape);				
				draw_line(img, shape.part(60), shape.part(67), color);
				
				extract_image_chip(img, get_face_chip_details(shape), img);
				
				shapes.push_back(shape);
			}
			
			//array2d<rgb_pixel> face_chip;
			
			
			//Preview
			win.clear_overlay();
			win.set_image(img);
			//win.add_overlay(render_face_detections(shapes));
			
			//Next
			cout << "Enter to proceed" << endl;
			cin.get();
		}
	}
	catch (exception& e)
	{
		cout << e.what() << endl;
	}
}