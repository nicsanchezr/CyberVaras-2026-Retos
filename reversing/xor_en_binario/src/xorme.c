#include <stdio.h>
#include <string.h>
int main(void) {
    unsigned char enc[] = { 80, 126, 248, 10, 104, 79, 195, 44, 76, 82, 194, 1, 103, 94, 201, 51, 99, 88, 243, 58, 118, 104, 201, 52, 118, 84, 217, 61, 122, 88, 194, 35 };
    unsigned char key[] = { 19, 55, 172, 94 };
    int n = sizeof(enc);
    char flag[256];
    for (int i = 0; i < n; i++) flag[i] = enc[i] ^ key[i % sizeof(key)];
    flag[n] = 0;                 // <- la flag vive aqui en runtime
    char buf[64];
    printf("Clave de activacion: ");
    if (!fgets(buf, sizeof buf, stdin)) return 1;
    buf[strcspn(buf, "\n")] = 0;
    if (strcmp(buf, flag) == 0) printf("Activado.\n");
    else printf("Clave incorrecta.\n");
    return 0;
}
