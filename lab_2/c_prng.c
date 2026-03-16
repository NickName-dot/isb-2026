#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

uint64_t lcg_seed = 0;

void lcg_srand(uint64_t seed) {
    lcg_seed = seed;
}

uint64_t lcg_rand() {
    lcg_seed = lcg_seed * 6364136223846793005ULL + 1442695040888963407ULL;
    return lcg_seed;
}

int main(int argc, char *argv[]) {
    int count = 10;
    FILE *output = stdout;
    char *filename = NULL;
    
    if (argc > 1) {
        count = atoi(argv[1]);
        if (count <= 0) count = 10;
    }
    if (argc > 2) {
        filename = argv[2];
        output = fopen(filename, "w");
        if (!output) {
            perror("File opening error");
            return 1;
        }
    }
    
    lcg_srand((uint64_t)time(NULL));

    for (int i = 0; i < count; i++) {
        fprintf(output, "%llu\n", lcg_rand() % 100);
    }
    
    if (filename) {
        fclose(output);
        printf("%d numbers wrote to %s\n", count, filename);
    }
    
    return 0;
}