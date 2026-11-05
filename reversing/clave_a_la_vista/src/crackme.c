#include <stdio.h>
#include <string.h>
int main(void) {
    char input[128];
    const char *pass = "v6_acceso_total";
    unsigned char enc[] = { 53, 127, 11, 53, 24, 16, 17, 1, 6, 49, 19, 28, 43, 19, 9, 0, 83, 51, 0, 60, 15, 4, 44, 12, 51, 21, 25, 17, 28 };
    int n = sizeof(enc);
    printf("Ingrese la contrasena: ");
    if (!fgets(input, sizeof input, stdin)) return 1;
    input[strcspn(input, "\n")] = 0;
    if (strcmp(input, pass) == 0) {
        char out[256]; int pl = strlen(pass);
        for (int i = 0; i < n; i++) out[i] = enc[i] ^ pass[i % pl];
        out[n] = 0;
        printf("Acceso concedido: %s\n", out);
    } else {
        printf("Acceso denegado.\n");
    }
    return 0;
}
