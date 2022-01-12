#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
// #include <cs50.h>

const int BUFFER_SIZE = 512;

// int isJPG();
// void handleJPG();

int main(int argc, char *argv[])
{
    // printf("argv[1]: %s\n", argv[1]);
    if (argc != 2 || !argv[1])
    {
        printf("Usage: ./recover image\n");
        return 3;
    }

    // open file from arg
    FILE *inFile = fopen(argv[1], "r");

    if (inFile == NULL)
    {
        printf("Couldn't Open The %s File!", argv[1]);
        return 4;
    }

    typedef uint8_t BYTE;
    BYTE buf[BUFFER_SIZE]; // create buffer holder

    int fData = 1;
    int fCount = 0;
    int picFound = 0;
    FILE *outFile = NULL;

    do
    {
        // read file & update fData
        fData = fread(buf, sizeof(BYTE), BUFFER_SIZE, inFile);
        // printf("see! b0: %x b1: %x b2: %x b3: %x what? %s is it? %d\n", buf[0], buf[1], buf[2], buf[3], buf, buf[0] == 0xff);
        // jpeg start
        if (buf[0] == 0xff && buf[1] == 0xd8 && buf[2] == 0xff && (buf[3] & 0xe0) == 0xe0)
        {
            if (picFound)
            {
                fclose(outFile); // close current
            }
            else
            {
                picFound = 1; // found
            }

            // open outfile
            char outF[8];
            sprintf(outF, "%03d.jpg", fCount);
            outFile = fopen(outF, "a");

            // printf("started! picFound: %d fCount: %d fData: %d\n", picFound, fCount, fData);

            fCount++;
        }

        if (picFound)
        {
            fwrite(buf, sizeof(BYTE), BUFFER_SIZE, outFile); // write
        }
        // printf("what's going on! picFound: %d fCount: %d fData: %d\n", picFound, fCount, fData);

    }
    while (fData >= 1);

    fclose(inFile);
    fclose(outFile);

    return 0;
}