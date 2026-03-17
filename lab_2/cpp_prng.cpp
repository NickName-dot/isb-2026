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
    int next_bit() {
        state = A * state + C;
        return (state & 1);
    }
};

int main(int argc, char* argv[]) {
    LCG gen;
    gen.init(12345);
    
    int count = 128;
    std::ofstream out(argc > 2 ? argv[2] : "");
    
    if (argc > 1) {
        count = std::atoi(argv[1]);
        if (count <= 0) count = 128;
    }
    
    if (!out.is_open()) {
        std::cerr << "Ошибка файла!" << std::endl;
        return 1;
    }
    
    for (int i = 0; i < count; i++) {
        out << gen.next_bit();
    }
    
    out.close();
    std::cout << count << " БИТОВ записано" << std::endl;
    return 0;
}
