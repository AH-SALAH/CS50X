#include <stdio.h>

int isValid(long n, char *errMsg);
int checkSum(long n, char *cType, char *errMsg);

int main()
{
    long n;
    int valid;
    // char* errMsg;
    // char* cType;

    do
    {
        printf("Card #: ");
        scanf("%ld", &n);
    }
    while (n <= 0);

    return isValid(n, "INVALID");
}

int isValid(long n, char *errMsg)
{
    long f2 = n;
    long lenCache = n;
    int len = 0;
    char *errorMsg = errMsg ? errMsg : "Not a Valid Card!";
    char *type = "Not a Valid Card!";

    while (lenCache >= 0)
    {
        if (lenCache < 1)
        {
            break;
        }
        else
        {
            lenCache /= 10;
            len++;
        }
    }

    if (len != 13 && len != 15 && len != 16)
    {
        printf("%s\n", errorMsg);
        return 0;
    }

    while (f2 > 100)
    {
        f2 /= 10;
    }

    switch (f2)
    {
        case 51 :
        case 52 :
        case 53 :
        case 54 :
        case 55 :
        case 22 :
            type = "MASTERCARD";
            break;
        case 34 :
        case 37 :
            type = "AMEX";
            break;

        default :
            if (f2 >= 10)
            {
                f2 /= 10;
            }

            if (f2 == 4)
            {
                type = "VISA";
            }
            // else type = 0;

    }

    char *msg = "Not a Valid Card!";
    if (type != msg)
    {
        return checkSum(n, type, errorMsg);
    }
    else
    {
        printf("%s\n", errorMsg);
        return 0;
    }

    // return 0;
}

int checkSum(long n, char *cType, char *errMsg)
{
    char *errorMsg = errMsg ? errMsg : "Not a Valid Card!";
    long tracker = n;
    // long nth2 = n;
    int cache1 = 0;
    int cache2 = 0;
    int sum1 = 0;
    int sum2 = 0;
    int ttl = 0;

    while (tracker > 0)
    {
        cache1 = ((tracker / 10) % 10) * 2;
        sum1 += cache1 > 9 ? (cache1 / 10) + (cache1 % 10) : cache1;
        cache2 = ((tracker * 10) % 100) / 10;
        sum2 += cache2;
        tracker /= 100;
        // printf("tracker: %ld sum1: %i cache1: %i \n", tracker, sum1, cache1);
        // printf("tracker: %ld sum2: %i cache2: %i \n", tracker, sum2, cache2);
    }

    ttl = sum1 + sum2;

    if (ttl % 10 == 0)
    {
        printf("CheckSum total: %i\t Last Digit: %i\t Is Valid: %s \n", ttl, ttl % 10, "true");
        printf("%s\n", cType);
        // return 0;
    }
    else
    {
        printf("%s\n", errorMsg);
    }

    return 0;
}
