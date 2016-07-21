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
//    char* face_model = (char*)"model.dat";
//    char* svm_model = (char*)"600.model";
//    char* neutral = (char*)"neutral.csv";
    char* face_model;
    char* svm_model;
    char* neutral;
    char* rec_path;
    char* vid_path;
    bool record = false;
    bool cam_input = true;
    bool debug = false;
};

void exit_with_help()
{
    cout << "Usage: ./emo [options]\n"
         << "Options:\n"
         << "-s : data in different locations, set path to [face_model] [svm_model] [neutral.csv]\n"
         << "-r [path]: toggle frame extractor, set path to save image\n"
         << "-v [path]: video input from path\n"
         << "-a [path]: all data in [path]" << endl;
    exit(1);
}

void parse_command_line(int argc, char** argv, arg_param &app_arg)
{
    int i;
    std::string tmp;
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

            case 'v':
                app_arg.cam_input = false;
                app_arg.vid_path = argv[i];
                break;

            case 'a':
                tmp = std::string(argv[i]) + "model.dat";
                app_arg.face_model = strdup(tmp.c_str());
                tmp = std::string(argv[i]) + "600.model";
                app_arg.svm_model = strdup(tmp.c_str());
                tmp = std::string(argv[i]) + "neutral.csv";
                app_arg.neutral = strdup(tmp.c_str());
                break;

            //Developer debug mode
            case 'd':
                app_arg.debug = true;
                tmp = std::string(argv[i]) + "model.dat";
                app_arg.face_model = strdup(tmp.c_str());
                tmp = std::string(argv[i]) + "600.model";
                app_arg.svm_model = strdup(tmp.c_str());
                tmp = std::string(argv[i]) + "neutral.csv";
                app_arg.neutral = strdup(tmp.c_str());
                break;

            default:
                cout << "Unknown options" << endl;
                exit_with_help();
        }
    }
}
