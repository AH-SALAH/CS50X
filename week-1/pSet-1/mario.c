#include <stdio.h>
#include <string.h>
// #include <cs50.h>

void marioPlus(int n);

int main()
{
    int n = 0;

    do
    {
        printf("Height: ");
        scanf("%i", &n);
        // n = get_int("Height: ");
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
    }

    while (i < n)
    {
        i++;
        strcat(c, "#");
        printf("%s%s  %s\n", &s[i], c, c);
    }
}