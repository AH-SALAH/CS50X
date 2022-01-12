#include <stdio.h>
#include <string.h>

void mario(int n);

int main()
{
    int n = 0;

    do
    {
        printf("Height: ");
        scanf("%i", &n);
    }
    while (n < 1 || n > 8);

    mario(n);

    return 0;
}

void mario(int n)
{
    int i = 0;
    int x = n;
    char c[9] = "#";
    char s[9] = "";

    while (x > i)
    {
        strcat(s, " ");
        x--;
    }

    while (i < n)
    {
        if (s[i] != '\0')
        {
            printf("%s%s\n", &s[i + 1], c);
        }
        strcat(c, "#");
        i++;
    }
}