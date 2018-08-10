class Combo {
public:
  int start;
  std::vector<int> combo_node;

public:
  Combo(const int _start){
    start = _start;
  }
  ~Combo() {}

  void AddNode(int node){
    combo_node.push_back(node);
  }
};
