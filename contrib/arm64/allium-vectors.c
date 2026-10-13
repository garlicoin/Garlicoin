/* Cross-architecture build regression vectors. No production crypto changes. */
#include <stdio.h>
#include <string.h>
#include "crypto/allium/allium.h"

int main(void) {
    unsigned char input[80], result[32];
    for (int vector = 0; vector < 3; ++vector) {
        for (int i = 0; i < 80; ++i) input[i] = vector == 0 ? 0 : vector == 1 ? i : 255;
        allium_hash((const char *)input, (char *)result);
        for (int i = 0; i < 32; ++i) printf("%02x", result[i]);
        puts("");
    }
    return 0;
}
