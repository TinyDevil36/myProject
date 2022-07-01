#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

/////////////// Basic Functions //////////////////////

int main() {

	string path = "/home/devil/code-projects/opencvProject/paper.jpg";
	Mat img = imread(path);
	Mat imgGray, imgBlur, imgCanny, imgDil, imgErode;

	cvtColor(img, imgGray, COLOR_BGR2GRAY);  //转换颜色空间
	GaussianBlur(imgGray, imgBlur, Size(3, 3), 3, 0); //高斯滤波模糊
	Canny(imgBlur, imgCanny, 25, 75);

	Mat kernel = getStructuringElement(MORPH_RECT, Size(3, 3)); //定义内核，  具体原理去查函数
	dilate(imgCanny, imgDil, kernel); //膨胀
	erode(imgDil, imgErode, kernel); //侵蚀

	imshow("Image", img);
	imshow("Image Gray", imgGray);
	imshow("Image Blur", imgBlur);
	imshow("Image Canny", imgCanny);
	imshow("Image Dilation", imgDil);
	imshow("Image Erode", imgErode);
	waitKey(0);
}