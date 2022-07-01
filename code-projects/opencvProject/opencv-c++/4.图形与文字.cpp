#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

////////////// Draw Shapes and Text //////////////////////

int main() {

	// Blank Image
// 参数含义依次是图片长、图片宽、图像格式（8bit，三通道）、颜色（B G R)
	Mat img(512, 512, CV_8UC3, Scalar(255, 255, 255));

//参数含义依次是目标图片、圆心坐标、半径长、颜色、填充（如果为数字则代表圆线条粗细）
	circle(img, Point(256, 256), 155, Scalar(0, 69, 255), FILLED);

//参数含义：目标图片、矩形左上角点坐标、矩形右上角点坐标、颜色、填充（如果为数字则代表圆线条粗细）
	rectangle(img, Point(130, 226), Point(382, 286), Scalar(255, 255, 255), FILLED);

//参数含义：目标图片、线段起点坐标、线段终点坐标、颜色、数字则表圆线条粗细
	line(img, Point(130, 296), Point(382, 296), Scalar(255, 255, 255), 2);

	putText(img, "nothing on you", Point(137, 262), FONT_HERSHEY_DUPLEX, 0.75, Scalar(0, 69, 255), 2);

	imshow("Image", img);
	waitKey(0);
}