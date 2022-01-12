#include <stdio.h>
#include <cs50.h>

int main(void)
{

    string name;

    do
    {
        name = get_string("What is your name?\n");
    }
    while (!name);

    printf("hello, %s\n", name);

    return 0;
}