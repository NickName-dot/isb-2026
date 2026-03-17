#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

uint64_t lcg_seed = 0;

void lcg_srand(uint64_t seed) {
    lcg_seed = seed;
}

int lcg_next_bit() {
    lcg_seed = lcg_seed * 6364136223846793005ULL + 1442695040888963407ULL;
    return (lcg_seed & 1);
}

int main(int argc, char *argv[]) {
    int count = 128;
    FILE *output = stdout;
    char *filename = NULL;
    
    if (argc > 1) {
        count = atoi(argv[1]);
        if (count <= 0) count = 128;
    }
    if (argc > 2) {
        filename = argv[2];
        output = fopen(filename, "w");
        if (!output) {
            perror("File opening error");
            return 1;
        }
    }
    
    lcg_srand(12345);

    for (int i = 0; i < count; i++) {
        fprintf(output, "%d", lcg_next_bit());
    }
    
    if (filename) {
        fclose(output);
        printf("%d БИТОВ записано в %s\n", count, filename);
    }
    
    return 0;
}
