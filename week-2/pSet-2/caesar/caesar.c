#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

const char ERRMSG[] = "Usage ./caesar.c key\n";

void handleCipher(int k);
int isValidDigit(int argc, char *argv[]);
char calcCipher(char c, int k);
char *cipher(char *str, int key);

int main(int argc, char *argv[])
{

    int k = isValidDigit(argc, argv);

    if (k)
    {
        handleCipher(k);
    }

    return 0;
}

int isValidDigit(int argc, char *argv[])
{

    const char *s = argv[1];

    // if args are other than 2 args, revoke
    if (argc != 2)
    {
        printf(ERRMSG);
        exit(1);
        return 0;
    }

    for (int i = 0; i < strlen(s); i++)
    {
        // if it's not a digit, revoke
        if (!isdigit(s[i]))
        {
            printf(ERRMSG);
            exit(1);
            return 0;
        }
    }

    return atoi(s);
}

void handleCipher(int k)
{
    char str[1000];
    do
    {
        printf("plaintext: ");
        scanf("%[^\n]%*c", str); // regex from stackoverflow search..
    }
    while (!str[0] || str[0] == '\n');

    // do cipher
    char *c = cipher(str, k);
    printf("ciphertext: %s\n", c);
}

char calcCipher(char c, int k)
{
    if (isupper(c))
    {
        int upper = c + k; // move by key value

        // chk if exceeds last upper char, then wrap
        if (upper > 'Z')
        {
            // wrap formula
            int upperExceed = (((c - 'A') + k) % 26) + 'A';

            return (char)upperExceed;
        }
        else
        {
            return (char)upper;
        }
    }
    else
    {
        int lower = c + k; // move by key value

        // chk if exceeds last lower char, then wrap
        if (lower > 'z')
        {
            // wrap formula
            int lowerExceed = (((c - 'a') + k) % 26) + 'a';

            return (char)lowerExceed;
        }
        else
        {
            return (char)lower;
        }
    }
}

char *cipher(char *str, int k)
{
    char *cipher = str;

    // loop over user plainText input chars
    for (int i = 0; i < strlen(str); i++)
    {
        // if it's alpha calc, else serve as it is
        cipher[i] = isalpha(str[i]) ? calcCipher(str[i], k) : str[i];
    }

    return cipher;
}