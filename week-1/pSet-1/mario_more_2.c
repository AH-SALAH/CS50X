#include <stdio.h>
#include <string.h>
#include <cs50.h>

void marioPlus(int n);
// void print (char c, int n);

int main()
{
    int n = 0;

    do
    {
        // printf("Height: ");
        // scanf("%i", &n);
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    marioPlus(n);

    return 0;
}

void marioPlus(int n)
{
    int i = 0;
    int x = n;
    char c[9] = "";
    char s[9] = "";

    while (x > i)
    {
        x--;
        strcat(s, " ");
        // s[x] = '.';
        // printf("x1: %i slen: %i s[x]: %s s: %s\n", x, strlen(s), &s[x], s);
    }

    while (i < n)
    {

        i++;
        strcat(c, "#");
        // print(' ', n - 1 - i);
        // print('#', i + 1);
        // print(' ', 2);
        // print('#', i + 1);

        // printf("\n");
        printf("%s%s  %s\n", &s[i], c, c);
        // printf("s: %s c: %s clen: %d\n", &s[i+1], &c[i], strlen(c));
    }
}

// void print (char c, int n)
// {
//     int x = 0;
//     while (x < n)
//     {
//         printf("%c", c);
//         x++;
//     }

// }
