#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

/////////////// Warp Images //////////////////////

int main() {

	string path = "/home/devil/code-projects/opencvProject/cards.jpg";
	Mat img = imread(path);
	Mat matrix, imgWarp;
	float w = 250, h = 350;
//用画图软件打开会标坐标，或者用Python的OpenCV输出也可以看到
	Point2f src[4] = { {529,142},{771,190},{405,395},{674,457} };//四个点
	Point2f dst[4] = { {0.0f,0.0f},{w,0.0f},{0.0f,h},{w,h} };

	matrix = getPerspectiveTransform(src, dst);  //获取变换矩阵
	warpPerspective(img, imgWarp, matrix, Point(w, h)); //透视变换

	for (int i = 0; i < 4; i++)
	{
		circle(img, src[i], 10, Scalar(0, 0, 255), FILLED); //标记四个角
	}

	imshow("Image", img);
	imshow("Image Warp", imgWarp);
	waitKey(0);

}