#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <ctime>
#include "combo.hpp"
#include <unistd.h>

cv::Scalar color[7] = { // in BGR order
  cv::Scalar(0, 0, 255),  // red
  cv::Scalar(0, 255, 0),  // green
  cv::Scalar(255, 0, 0),  // blue
  cv::Scalar(0, 255, 255),  // yellow
  cv::Scalar(68, 18, 62),  // purple
  cv::Scalar(147, 20, 255),  // pink
  cv::Scalar(0, 0, 0)  // black
};

void make_random_map(int* M){
  for(int i=0; i<30;i++){
    M[i] = rand() % 6;
  }
}

void draw_state(int* M, cv::Mat &img){
  for(int i=0; i<6;i++){
    for(int j=0;j<5;j++){
      cv::circle(img, cv::Point(50 + 100*i, 50 + 100*j), 40, color[M[i*5+j]], -1, CV_AA);

      // if (M[i*5+j] == 0) { //red
      //   cv::circle(img, cv::Point(50 + 100*i, 50 + 100*j), 40, cv::Scalar(0, 0, 255), -1, CV_AA);
      // }
      // else if (M[i*5+j] == 1) { // green
      //   cv::circle(img, cv::Point(50 + 100*i, 50 + 100*j), 40, cv::Scalar(0, 255, 0), -1, CV_AA);
      // }
      // else if (M[i*5+j] == 2) { // blue
      //   cv::circle(img, cv::Point(50 + 100*i, 50 + 100*j), 40, cv::Scalar(255, 0, 0), -1, CV_AA);
      // }
      // else if (M[i*5+j] == 3) { // yellow
      //   cv::circle(img, cv::Point(50 + 100*i, 50 + 100*j), 40, cv::Scalar(0, 255, 255), -1, CV_AA);
      // }
      // else if (M[i*5+j] == 4) { // purple
      //   cv::circle(img, cv::Point(50 + 100*i, 50 + 100*j), 40, cv::Scalar(68, 18, 62), -1, CV_AA);
      // }
      // else if (M[i*5+j] == 5) { // pink
      //   cv::circle(img, cv::Point(50 + 100*i, 50 + 100*j), 40, cv::Scalar(147, 20, 255), -1, CV_AA);
      // }
      // else if (M[i*5+j] == 6) { // black
      //   cv::circle(img, cv::Point(50 + 100*i, 50 + 100*j), 40, cv::Scalar(255, 255, 255), -1, CV_AA);
      // }

    }
  }
}

bool in_map(int i, int j){
  return (i >= 0) && (i < 6) &&(j>= 0)&&(j < 5);
}

void search_around(int i, int j, int* M, bool* check, std::vector<Combo>& combos){
  int left = 1;
  int down = 1;
  // Find combos in left direction
  for (int id = i+1; id<6; id++) {
    if (M[id*5+j] == M[i*5+j]) {
      left++;
    }
    else {
      break;
    }
  }
  // Find combos in down direction
  for (int jd = j+1; jd<5; jd++) {
    if (M[i*5+jd] == M[i*5+j]) {
      down++;
    }
    else {
      break;
    }
  }
  // IF combo found
  Combo cb(i*5+j);
  cb.AddNode(i*5+j);
  bool has_combo = false;
  if (left >= 3) {
    has_combo = true;
    for (int id = i+1; id < i+left; id++) {
      check[id*5+j] = true;
      cb.AddNode(id*5+j);
    }
  }

  if (down >= 3) {
    has_combo = true;
    for (int jd = j+1; jd < j+down; jd++) {
      check[i*5+jd] = true;
      cb.AddNode(i*5+jd);
    }
  }
  if (has_combo) {
    combos.push_back(cb);
  }
}

void kill_combo(int* M, std::vector<Combo>& combos){
  bool check[30];
  int i;
  for(i=0; i<30;i++){
    check[i] = false;
  }
  // Find combos
  int col, row;
  for(i=0; i<30; i++){
    if(check[i]) continue;
    check[i] = true;
    col = i/5;
    row = i%5;
    search_around(col, row, M, check, combos);
  }
  // Kill combos
  for(i=0;i<combos.size();i++){
    for (int j=0; j <combos.at(i).combo_node.size(); j++){
      M[combos.at(i).combo_node.at(j)] = 6;
    }
  }
}

int main(int argc, char* argv[])
{
  cv::Mat img = cv::Mat::zeros(500, 600, CV_8UC3);
  int Map[30];
  std::vector<Combo> combos;
  /* initialize random seed: */
  // srand (time(NULL));

  // DrawBoard: Horizontal Lines
  cv::line(img, cv::Point(0, 0), cv::Point(600, 0), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(0, 100), cv::Point(600, 100), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(0, 200), cv::Point(600, 200), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(0, 300), cv::Point(600, 300), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(0, 400), cv::Point(600, 400), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(0, 500), cv::Point(600, 500), cv::Scalar(200, 200, 200), 5, CV_AA);

  // Vertical Lines
  cv::line(img, cv::Point(0, 0), cv::Point(0, 500), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(100, 0), cv::Point(100, 500), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(200, 0), cv::Point(200, 500), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(300, 0), cv::Point(300, 500), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(400, 0), cv::Point(400, 500), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(500, 0), cv::Point(500, 500), cv::Scalar(200, 200, 200), 5, CV_AA);
  cv::line(img, cv::Point(600, 0), cv::Point(600, 500), cv::Scalar(200, 200, 200), 5, CV_AA);

  make_random_map(Map);
  cv::namedWindow("Map", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);

  draw_state(Map, img);
  cv::imshow("Map", img);
  // sleep(5000);
  cv::waitKey(5000);

  kill_combo(Map, combos);
  draw_state(Map, img);
  cv::imshow("Map", img);
  cv::waitKey(0);

  cv::destroyWindow("Map");
  return 0;
}
