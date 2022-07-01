#include<opencv2/imgcodecs.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>
#include<iostream>
using namespace std;
using namespace cv;
 
void getContours(Mat imgDil, Mat img) {
	//imgDil是传入的扩张边缘的图像用来查找轮廓，img是要在其上绘制轮廓的图像
	vector<vector<Point>> contours;//轮廓检测到的轮廓。每个轮廓线存储为一个点的向量
 
	//包含关于映像拓扑的信息  typedef Vec<int, 4> Vec4i;具有4个整数值
	vector<Vec4i> hierarchy;
	//在二值图像中查找轮廓。该函数利用该算法从二值图像中提取轮廓
	findContours(imgDil, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
	vector<vector<Point>> conPoly(contours.size());//定义approxCurve
	vector<Rect> boundRect(contours.size());//定义存储边界框的变量
	for (int i = 0; i < contours.size(); i++) {//遍历检测到的轮廓
		int area = contourArea(contours[i]);
		//cout << area << endl;		
		string objectType;//定义轮廓类型，便于添加文字到边界框
		if (area > 1000) {//轮廓面积＞1000才绘制
			//定义 0.02*轮廓周长为给定的界限（精度）
			float peri = arcLength(contours[i], true);
			//以指定的精度近似多边形曲线。第二个参数conPloy[i]存储近似的结果，是输出。
			approxPolyDP(contours[i], conPoly[i], 0.02 * peri, true);
			boundRect[i] = boundingRect(conPoly[i]);//计算边界矩形
			//找近似多边形的角点,三角形有3个角点，矩形/正方形有4个角点，圆形>4个角点
			int objCor = (int)conPoly[i].size();
			//cout << objCor << endl;
			if (objCor == 3) { objectType = "Tri"; }
			else if (objCor == 4) {//四个角点进一步判断是正方形还是长方形
				float aspRatio = (float)boundRect[i].width / (float)boundRect[i].height;//宽高比
				if (aspRatio > 0.95 && aspRatio < 1.05) { objectType = "Square"; }
				else objectType = "Rect";
			}
			//这里 objCor 大于4 就判断为圆形过于绝对了，但是在示例图片是可以的
			else if (objCor > 4) { objectType = "Circle"; }
			//drawContours(img, conPoly, i, Scalar(255, 0, 255), 2);
			//绘制边界矩形
			rectangle(img, boundRect[i].tl(), boundRect[i].br(), Scalar(0, 255, 0), 5);
			//添加标注，boundRect[i].y-5 是为了将文字房子框的上方
			putText(img, objectType, { boundRect[i].x,boundRect[i].y - 5 }/*文字坐标*/, FONT_HERSHEY_PLAIN, 1, Scalar(0, 69, 255), 1);
		}
	}
}
 
int main() {
	string path = "/home/devil/code-projects/opencvProject/shapes.png";
	Mat img = imread(path);
	Mat imgGray, imgBlur, imgCanny, imgDil;
	cvtColor(img, imgGray, COLOR_BGR2GRAY);
	//cvt是convert的缩写，将图像从一种颜色空间转换为另一种颜色空间。
	GaussianBlur(imgGray, imgBlur, Size(3, 3), 3, 0);
	//使用高斯滤波器模糊图像。该函数将源图像与指定的高斯核进行卷积,Size(7,7)是核大小,数字越大越模糊
	Canny(imgBlur, imgCanny, 25, 75);
	//边缘检测，阈值1，2可调，目的：显示更多的边缘
	Mat kernel = getStructuringElement(MORPH_RECT, Size(3, 3));
	//创建一个核，增加Size（只能是奇数）会扩张/侵蚀更多
	dilate(imgCanny, imgDil, kernel);//扩张边缘（增加边缘厚度
 
	getContours(imgDil, img);//img是在其上绘轮廓的图片
 
	imshow("Image", img);
	waitKey(0);//增加延时，0表示无穷
}