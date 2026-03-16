#include <iostream>
#include <fstream>
#include <cstdint>

class LCG {
private:
    uint64_t state = 0;
    static constexpr uint64_t A = 6364136223846793005ULL;
    static constexpr uint64_t C = 1442695040888963407ULL;
    
public:
    void init(uint64_t s) { state = s; }
    uint64_t next() {
        state = A * state + C;
        return state;
    }
};

int main(int argc, char* argv[]) {
    LCG gen;
    gen.init(12345);
    
    int n = argc > 1 ? std::atoi(argv[1]) : 10;
    std::ofstream out(argc > 2 ? argv[2] : "");
    
    if (!out.is_open()) out.open("output.txt");
    
    for (int i = 0; i < n; ++i) {
        out << gen.next() << '\n';
    }
    
    return 0;
}
