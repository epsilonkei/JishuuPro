#include <ctime>

class Map{
private:
  int matrix[6][5];
  int count_combo;
  std::vector<Combo *> combos;

public:
  Map() {}
  ~Map() {}

  void MakeRandomMap() {
    for(int i=0; i<6;i++){
      for(int j=0; j<5; j++){
	matrix[i] = rand() % 6;
      }
    }
  }
