#include <iostream>
#include <fstream>
#include <cstdint>
#include <string>

class PCG {
private:
    uint64_t state, inc;
    
    uint64_t pcg_rotr_64(uint64_t x, uint64_t r) {
        return (x >> r) | (x << (64 - r));
    }
    
public:
    PCG(uint64_t initstate = 0x853c49e6748fea9bULL, 
        uint64_t initseq = 0xda3e39cb94b95bdbULL) {
        state = 0U;
        inc = (initseq << 1u) | 1u;
        seed(initstate);
    }
    
    void seed(uint64_t seed) {
        state = seed + inc;
        next();
    }
    
    uint64_t next() {
        uint64_t oldstate = state;
        state = oldstate * 6364136223846793005ULL + inc;
        uint32_t xorshifted = ((oldstate >> 18u) ^ oldstate) >> 27u;
        uint32_t rot = oldstate >> 59u;
        return (pcg_rotr_64((xorshifted << 1u) ^ oldstate, rot)) | 1;
    }
    
    int next_bit() {
        return (next() >> 63) & 1;
    }
};

int main(int argc, char* argv[]) {
    int count = 1000;
    std::ofstream out;
    std::string filename;
    
    if (argc > 1) {
        count = std::stoi(argv[1]);
        if (count <= 0) count = 1000;
    }
    if (argc > 2) {
        filename = argv[2];
        out.open(filename);
        if (!out.is_open()) {
            std::cerr << "File opening error\n";
            return 1;
        }
    }
    
    PCG rng(12345);
    
    auto& output = out.is_open() ? out : std::cout;
    
    for (int i = 0; i < count; i++) {
        output << rng.next_bit();
    }
    
    if (out.is_open()) {
        out.close();
        std::cout << count << " БИТОВ записано в " << filename << "\n";
    }
    
    return 0;
}
