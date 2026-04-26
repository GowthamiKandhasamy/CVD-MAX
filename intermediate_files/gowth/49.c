#include <stdio.h>

int target(int a) {
    int x = a;
    if (x == 12345) printf("rare\n");
    return x;
}

int main() {
    char buf[1024];
    fgets(buf, sizeof(buf), stdin);
    target(1);
    return 0;
}
