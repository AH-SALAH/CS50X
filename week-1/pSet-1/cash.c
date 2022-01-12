#include <stdio.h>
#include <stdbool.h>
#include <math.h>

void calcCents(float input);

int main(void)
{
    float input = 0.00;

    do
    {
        printf("Change owed: ");
        scanf("%f", &input);
    }
    while (input <= 0);

    calcCents(input);

    return 0;
}


void calcCents(float input)
{
    // int tracker = round(input > 0.999999 ? (input / 100) * 100 : input * 100);
    int tracker = round(input * 100);
    int coins = 0;
    int count = 0;

    printf("Coin Type:\t");

    for (int dimeVal = 25; dimeVal > 0; dimeVal--)
    {
        if (
            dimeVal == 25 ||
            dimeVal == 10 ||
            dimeVal == 5 ||
            dimeVal == 1
        )
        {
            count = 0;
            for (int cCount = 1; cCount <= floor(tracker / dimeVal); cCount++)
            {
                coins += 1;
                count = cCount;
            }

            tracker %= dimeVal;

            if (count >= 1)
            {
                printf("%ic x%i\t", dimeVal, count);
            }
            else
            {
                printf("------\t");
            }
        }
    }

    printf("\nTotal Coins: %i\n", coins);
    printf("%i\n", coins);

}
