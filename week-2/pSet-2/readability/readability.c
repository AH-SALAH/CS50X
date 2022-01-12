#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int getLvls(const char *str);
int getLvlGrd(int c, int w, int s);

int main()
{
    char str[1000];

    do
    {
        printf("Text: ");
        scanf("%[^\n]%*c", str);
    }
    while (strlen(str) <= 0 || str[0] == '\n');

    getLvls(str);

    return 0;
}


int getLvls(const char *str)
{
    int ttlChar = 0, ttlS = 0, ttlW = 0, len = strlen(str), isChar, isWord, isSen;
    char c;
    // int sEnd;
    // int cSigns;

    for (int i = 0; i < len; i++)
    {
        c = str[i],
        isChar = isupper(c) || islower(c),
        isWord = (c == ' ' && str[i - 1] && str[i - 1] != ' ') ||
                 c == '\0' ||
                 (c == '.' && (!str[i + 1] || str[i + 1] != ' ')) ||
                 (c == '?' && (!str[i + 1] || str[i + 1] != ' ')) ||
                 (c == '!' && (!str[i + 1] || str[i + 1] != ' ')),
                 isSen = ((c == '.' || c == '?' || c == '!') && str[i + 1] == ' ') || c == '\0' || i == len - 1;
        // sEnd = ((int)c + (int)' ' == (int)'.' + (int)' ');
        // cSigns = c != '!' && c != '.' && c != ',' && c != '?' && c != ';',

        if (isChar)
        {
            printf("lower: %d | upper: %d \n", islower(c), isupper(c));
            //if(cSigns)
            ttlChar += 1;
            printf("ttlChar: %d\n%c\n", ttlChar, c);
        }
        if (isWord)
        {
            ttlW += 1;
            printf("ttlW: %d | char: %c\n", ttlW, c);
        }
        if (isSen)
        {
            ttlS += 1;
            printf("ttlS: %d\n", ttlS);
        }
    }

    printf("%d Letter(s)\n", ttlChar);
    printf("%d Word(s)\n", ttlW);
    printf("%d Sentence(s)\n", ttlS);

    getLvlGrd(ttlChar, ttlW, ttlS);

    return 0;
}

int getLvlGrd(int c, int w, int s)
{
    if ((!c && !w && !s) || w == 0)
    {
        return 1;
    }

    float avgL = ((float)c / (float)w) * 100;
    float avgS = ((float)s / (float)w) * 100;
    int index = round(0.0588 * avgL - 0.296 * avgS - 15.8);

    printf("avgL: %f\navgS: %f\nindex: %d\n", avgL, avgS, index);

    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %d\n", (int)index);
    }

    return 0;
}