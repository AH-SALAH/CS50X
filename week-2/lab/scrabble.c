#include <stdio.h>
#include <string.h>
#include <ctype.h>

int calcScore(const char *w1, const char *w2, int points[]);
int getStrValue(const char *str, int points[]);

int main()
{
    int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    char str1[100];
    char str2[100];

    do
    {
        printf("Player1: ");
        scanf("%s", str1);
    }
    while (str1[0] == '\n');
    // while(((int)w1[100] < (int)'A' && (int)w1[100] > (int)'Z') && ((int)w1[100] < (int)'a' && (int)w1[100] > (int)'z') || !w1);

    do
    {
        printf("Player2: ");
        scanf("%s", str2);
    }
    while (str2[0] == '\n');

    calcScore(str1, str2, points);

    return 0;
}

int calcScore(const char *str1, const char *str2, int points[])
{


    if (!str1 && !str2 && !points)
    {
        printf("calcScore fn needs its parameters!");
        return 1;
    }

    int sum1 = getStrValue(str1, points);
    int sum2 = getStrValue(str2, points);

    if (sum1 > sum2)
    {
        printf("Player 1 Wins!\n");
    }
    else if (sum1 < sum2)
    {
        printf("Player 2 Wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}

int getStrValue(const char *str, int points[])
{

    if (!str && !points)
    {
        printf("getStrValue fn needs its parameters!");
        return 1;
    }

    int sum = 0;
    char c;

    // we get the char index in ascii &
    // map with points
    for (int i = 0, length = strlen(str); i < length; i++)
    {
        c = str[i];

        if (isupper(c))
        {
            // for(int x = 0, j = (int)'A'; j < (int)'Z'; j++,x++){
            // if(c == j) {
            sum += points[(int)c - (int)'A'];
            // }
            // }
        }

        if (islower(str[i]))
        {
            // for(int x = 0, j = (int)'a'; j < (int)'z'; j++,x++){
            // if(c == j) {
            sum += points[(int)c - (int)'a'];
            // }
            // }
        }
    }

    return sum;
}
