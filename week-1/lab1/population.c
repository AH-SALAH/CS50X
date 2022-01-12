#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt for start size
    int s_size;
    do
    {
        s_size = get_int("Start Size: ");
    }
    while (s_size < 9);

    // Prompt for end size

    int e_size;
    do
    {
        e_size = get_int("End Size: ");
    }
    while (e_size < s_size);

    // Calculate number of years until we reach threshold
    int y = 0;
    while (s_size < e_size)
    {
        s_size += (s_size / 3) - (s_size / 4);
        y++;
    }

    // Print number of years
    printf("Years: %i\n", y);

    return 0;
}