#include <iostream>
#include <cstdio>
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/optional_debug_tools.h"
#include <iostream>
#include <fstream>
#include <time.h>
#include <math.h>
#include <opencv/cv.hpp>
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace cv::ml;
using namespace std;
using namespace tflite;
#define LOG(x) std::cerr
#define TFLITE_MINIMAL_CHECK(x)                              \
  if (!(x)) {                                                \
    fprintf(stderr, "Error at %s:%d\n", __FILE__, __LINE__); \
    exit(1);                                                 \
  }

int PROCESS_H = 180;
int PROCESS_W = 320;

std::vector<uint32_t> lane_result_proc(std::vector<float> out_vect);
std::vector<uint8_t> decode_bmp(const uint8_t* input, int row_size, int width,int height, int channels, bool top_down);


int main() {
    const char* filename = "../model/LwdsModel.tflite";
    std::string ImgPath = "/home/zack/studio/test_videos/20190723_001.avi";
    clock_t start, finish;
    double duration;

    VideoCapture capture;
    cv::Mat frame;
    // Load model
    std::unique_ptr<tflite::FlatBufferModel> model =
            tflite::FlatBufferModel::BuildFromFile(filename);
    TFLITE_MINIMAL_CHECK(model != nullptr);

    // Build the interpreter
    tflite::ops::builtin::BuiltinOpResolver resolver;
    InterpreterBuilder builder(*model, resolver);
    std::unique_ptr<Interpreter> interpreter;
    builder(&interpreter);
    TFLITE_MINIMAL_CHECK(interpreter != nullptr);

    // Allocate tensor buffers.
    TFLITE_MINIMAL_CHECK(interpreter->AllocateTensors() == kTfLiteOk);
    printf("=== Pre-invoke Interpreter State ===\n");
    tflite::PrintInterpreterState(interpreter.get());
//    LOG(INFO) << "tensors size: " << interpreter->tensors_size() << "\n";
//    LOG(INFO) << "nodes size: " << interpreter->nodes_size() << "\n";
//    LOG(INFO) << "inputs: " << interpreter->inputs().size() << "\n";
//    LOG(INFO) << "input(0) name: " << interpreter->GetInputName(0) << "\n";
//    LOG(INFO) << "outputs: " << interpreter->outputs().size() << "\n";
//    LOG(INFO) << "output(0) name: " << interpreter->GetOutputName(0) << "\n";
//    const std::vector<int> inputs = interpreter->inputs();
//    const std::vector<int> outputs = interpreter->outputs();
//    LOG(INFO) << "number of inputs: " << inputs.size() << " " << inputs[0] << "\n";
//    LOG(INFO) << "number of outputs: " << outputs.size() << "  " << outputs[0] << "\n";

    int input = interpreter->inputs()[0];
    TfLiteIntArray* dims = interpreter->tensor(input)->dims;
    int wanted_height = dims->data[1];
    int wanted_width = dims->data[2];
    int wanted_channels = dims->data[3];
    std::cout << "Input dimension: " << wanted_height << "  "<< wanted_width << "  " << wanted_channels << "\n";


    frame = capture.open(ImgPath);
    if(!capture.isOpened())
    {
        printf("can not open ...\n");
        return -1;
    }
    namedWindow("output", CV_WINDOW_AUTOSIZE);

    cv::Mat in_mat;
    cv::Mat img_last;
    uint16_t cnt = 0;
    ofstream Save("axis_c.txt");
    while (capture.read(frame)){		
        cv::resize(frame, in_mat, Size (wanted_width, wanted_height), INTER_LINEAR);
        cv::resize(frame, img_last, Size (320, 180), INTER_LINEAR);

//        float temp_clr;
//        for (int row = 0; row < wanted_width;row++)
//        {
//            for (int col = 0; col < wanted_height;col++)
//            {
//                temp_clr = in_mat.at<Vec3b>(row, col)[0];
//                in_mat.at<Vec3b>(row, col)[0] = in_mat.at<Vec3b>(row, col)[2];
//                in_mat.at<Vec3b>(row, col)[2] = temp_clr;
//            }
//        }

        std::vector<float> in = in_mat.reshape(1, wanted_width*wanted_height*wanted_channels);              // Fill input buffers 
        for(int i=0; i<in.size(); i++)
        {
            interpreter->typed_tensor<float>(input)[i] = in[i];
        }

        // Run inference
        // Read output buffers
        // TODO(user): Insert getting data out code.
        start = clock();
        if (interpreter->Invoke() != kTfLiteOk)
        {
            return false;
        }
        finish = clock();
        duration = (double)(finish - start) / CLOCKS_PER_SEC;
//    float *output_data = interpreter->typed_tensor<float>(output);
//        cout << "seconds: " << duration << endl;

		// TODO(user): Insert code to fill input tensors
        int output = interpreter->outputs()[0];
//        cout << "test_print: " << "input tensor node number: " << input << " output tensor node number:  " << output << endl;
        TfLiteIntArray* dims2 = interpreter->tensor(output)->dims;
        std::vector<float> out_result;
        for(int i=0; i<dims2->data[1]; i++){
            out_result.push_back(interpreter->typed_tensor<float>(output)[i]);
        }
        vector<uint32_t> lane_points = lane_result_proc(out_result);
        cv::line(img_last, cv::Point(lane_points[0], lane_points[1]), cv::Point(lane_points[2], lane_points[3]), cv::Scalar(255,0,0),2,1);
        cv::line(img_last, cv::Point(lane_points[0], lane_points[1]), cv::Point(lane_points[4], lane_points[5]), cv::Scalar(255,0,0),2,1);

        imshow("output", img_last);

//        cout << "========"<< img_last.size << endl;
        cout << "out_result" << cnt << ":   " << out_result[0] << "  "<< out_result[1]<< "  "<< out_result[2] << "  "<< out_result[3] << endl;
        cnt++;


        //if(delay>=0&&waitKey (delay)>=0)
            waitKey(0);

    }
    Save.close();
    capture.release();
    return 0;
}


std::vector<uint32_t> lane_result_proc(std::vector<float> out_vect){
    vector<uint32_t> lane_points;
    uint32_t x;
    uint32_t y;
    uint32_t temp;
    for(int i = 0; i < out_vect.size(); i++){
        temp = std::round(out_vect.data()[i]);
        if (i < 2){
            lane_points.push_back(temp);
            continue;
        }

        if(0 <= temp && temp < PROCESS_H){
            x = 0;
            y = temp;
        } else if(PROCESS_H <= temp && temp < (PROCESS_H + PROCESS_W - 2)){
            x = round(temp - PROCESS_H);
            y = PROCESS_H - 1;
        } else if((PROCESS_H + PROCESS_W - 2) <= temp && temp < (PROCESS_H + PROCESS_W + PROCESS_H - 3)){
            x = PROCESS_W - 1;
            y = round(2 * PROCESS_H - temp + PROCESS_W - 2);
        }

        lane_points.push_back(x);
        lane_points.push_back(y);
    }
    return lane_points;

}

