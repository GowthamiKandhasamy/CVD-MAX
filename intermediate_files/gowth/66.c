
#include <stdio.h>

int __poke_user(int a0, int a1, int a2) {
    int x = 0;
    for (int i = 0; i < 10; i++) x += i;
    return x;
}

int main() {
    char buf[1024];
    fgets(buf, sizeof(buf), stdin);
    __poke_user(0, 0, 0);
    return 0;
}
