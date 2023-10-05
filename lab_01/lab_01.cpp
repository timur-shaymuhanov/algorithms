#include <iostream>
#include <vector>
 
int main() {
    std::vector<int> data = {1, 2, 3, 4, 5};
    for (int elem : data) {
        std::cout << elem << " ";
    }
    std::cout << "\n";
}