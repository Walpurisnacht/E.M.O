#include <dlib/opencv.h>
#include <opencv2/highgui/highgui.hpp>
#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <ctime>
#include <sys/stat.h>
#include <string>

using namespace std;
using namespace dlib;

struct arg_param {
    char* face_model = (char*)"model.dat";
    char* svm_model = (char*)"600.model";
    char* neutral = (char*)"neutral.csv";
    char* rec_path = (char*)"./";
    bool record = false;
};

void exit_with_help()
{
    cout << "Usage: ./cam_overlay [options]\n"
         << "Options:\n"
         << "-s : data in different locations, set path to [face_model] [svm_model] [neutral.csv]\n"
         << "-r : toggle frame extractor, set path to save image\n"
         << "Default: data in current working dir, no recording" << endl;
    exit(1);
}

void parse_command_line(int argc, char** argv, arg_param &app_arg)
{
    int i;
    for (i = 1; i < argc; i++) {
        if (argv[i][0] != '-') break;
        if (++i >= argc) exit_with_help();

        switch(argv[i-1][1])
        {
            case 's':
                app_arg.face_model = argv[i];
                app_arg.svm_model = argv[i+1];
                app_arg.neutral = argv[i+2];
                i+=2;
                break;

            case 'r':
                app_arg.rec_path = argv[i];
                app_arg.record = true;
                break;

            default:
                cout << "Unknown options" << endl;
                exit_with_help();
        }
    }
}
