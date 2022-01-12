#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

const char ERRMSG_USAGE[] = "Usage ./substitution.c key\n";
const char ERRMSG_COUNT[] = "Key must contains 26 characters.\n";
const char ERRMSG_ISALPHA[] = "Key must be alpha.\n";
const char ERRMSG_ISALPHA_ONCE[] = "Every char should be exists once.\n";

void handleCipher(char *k);
int isValidKey(int argc, char *argv[]);
char calcCipher(char c, char *k);
char *cipher(char *str, char *key);

int main(int argc, char *argv[])
{

    int k = isValidKey(argc, argv);

    if (k != 1)
    {
        handleCipher(argv[1]);
    }

    return 0;
}

int isValidKey(int argc, char *argv[])
{

    const char *s = argv[1];

    // if args are other than 2 args, revoke
    if (argc != 2)
    {
        printf(ERRMSG_USAGE);
        exit(1);
        return 1;
    }

    // - chk if they are not equal 26 char in count
    // - chk if they are alpha
    // - chk if each alpha char exists once

    int len = strlen(s);

    if (strlen(s) != 26)
    {
        printf(ERRMSG_COUNT);
        exit(1);
        return 1;
    }

    int c;
    for (int i = 0; i < len; i++)
    {
        // if not alpha, revoke
        if (!isalpha(s[i]))
        {
            printf(ERRMSG_ISALPHA);
            exit(1);
            return 1;
        }

        c = s[i];
        for (int x = 0; x < len; x++)
        {
            // if current char in both loop match and it's not the same index,
            // then it's a repeated char,
            // it's not unique, revoke!
            if (((c == s[x] - 32 || c == s[x] + 32) || c == s[x]) && x != i)
            {
                printf(ERRMSG_ISALPHA_ONCE);
                exit(1);
                return 1;
            }
        }
    }

    // return s;
    return 0;
}

void handleCipher(char *k)
{
    char str[1000];

    do
    {
        printf("plaintext: ");
        scanf("%[^\n]%*c", str);
    }
    while (str[0] == '\n' || str[0] == '\0');

    // do cipher
    char *c = cipher(str, k);

    printf("ciphertext: %s\n", c);
}

char calcCipher(char c, char *k)
{
    char ki;
    int ci;

    if (isupper(c))
    {
        // get char index in both plaintext (c-'A') & key[]
        ki = k[(c - 'A')];
        // convert it to upper if it's not
        ci = isupper(ki) ? ki : ki - 32;

        return (char)ci;
    }
    else
    {
        // get char index in both plaintext (c-'a') & key[]
        ki = k[(c - 'a')];
        // convert it to lower if it's not
        ci = islower(ki) ? ki : ki + 32;

        return (char)ci;
    }
}

char *cipher(char *str, char *k)
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