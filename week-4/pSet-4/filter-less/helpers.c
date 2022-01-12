#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // printf("height: %i width: %i\n", height, width);
    int avg;
    for (int i = 0; i < height; i++)
    {
        for (int x = 0; x < width; x++)
        {
            avg = round((image[i][x].rgbtRed + image[i][x].rgbtGreen + image[i][x].rgbtBlue) / 3.00);
            // printf("avg: %i\n", avg);
            image[i][x].rgbtRed = image[i][x].rgbtGreen = image[i][x].rgbtBlue = avg;
        }
    }

    return;
}

// set RGB limit
int limit(int n)
{
    if (n > 255)
    {
        return 255;
    }
    return n;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int originalRed, originalGreen, originalBlue;

    for (int i = 0; i < height; i++)
    {
        for (int x = 0; x < width; x++)
        {
            // cache'm
            originalRed = image[i][x].rgbtRed;
            originalGreen = image[i][x].rgbtGreen;
            originalBlue = image[i][x].rgbtBlue;
            // calc & replace
            image[i][x].rgbtRed = limit(round(0.393 * originalRed + 0.769 * originalGreen + 0.189 * originalBlue));
            image[i][x].rgbtGreen = limit(round(0.349 * originalRed + 0.686 * originalGreen + 0.168 * originalBlue));
            image[i][x].rgbtBlue = limit(round(0.272 * originalRed + 0.534 * originalGreen + 0.131 * originalBlue));
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
    {
        for (int x = 0; x < width; x++)
        {
            if (x == width / 2)
            {
                break;
            }

            temp = image[i][x];
            image[i][x] = image[i][width - x - 1];
            image[i][width - x - 1] = temp;
        }
    }

    return;
}

// const float INTENSITY = 0.5;
// calc avg sum
int calcAvg(int avgSum, float avgCount)
{
    return limit(round(avgSum / avgCount));
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // loop for rows
    // loop for col
    // check if row - 1 exist
    // check if row + 1 exist
    // get row -1 px after & before of the current org px if exist
    // get row +1 px after & before of the current org px if exist
    // calc avg for all rgb around + org px inclusive

    int avgSumR, avgSumG, avgSumB;
    float avgCount;
    // copy 4 operations
    RGBTRIPLE imgCopy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            imgCopy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int x = 0; x < width; x++)
        {
            RGBTRIPLE currentPx = imgCopy[i][x],
                      beforePx = imgCopy[i][x - 1 > -1 ? x - 1 : x],
                      afterPx = imgCopy[i][x + 1 < width ? x + 1 : x];
            avgSumR = avgSumG = avgSumB = 0;
            avgCount = 0.00;

            // add row before pxs
            if (i - 1 > -1)
            {
                for (int j = x - 1 > -1 ? x - 1 : x; (j < width || x + 1 < width) && j <= x + 1; j++)
                {
                    beforePx = imgCopy[i - 1][j];

                    avgSumR += beforePx.rgbtRed;
                    avgSumG += beforePx.rgbtGreen;
                    avgSumB += beforePx.rgbtBlue;

                    avgCount++;
                }
            }
            // add row after pxs
            if (i + 1 < height)
            {
                for (int j = x - 1 > -1 ? x - 1 : x; (j < width || x + 1 < width) && j <= x + 1; j++)
                {
                    afterPx = imgCopy[i + 1][j];

                    avgSumR += afterPx.rgbtRed;
                    avgSumG += afterPx.rgbtGreen;
                    avgSumB += afterPx.rgbtBlue;

                    avgCount++;
                }
            }

            // add current row pxs
            for (int j = x - 1 > -1 ? x - 1 : x; (j < width || x + 1 < width) && j <= x + 1; j++)
            {
                currentPx = imgCopy[i][j];

                avgSumR += currentPx.rgbtRed;
                avgSumG += currentPx.rgbtGreen;
                avgSumB += currentPx.rgbtBlue;

                avgCount++;
            }

            // apply avg
            image[i][x].rgbtRed = calcAvg(avgSumR, avgCount);
            image[i][x].rgbtGreen = calcAvg(avgSumG, avgCount);
            image[i][x].rgbtBlue = calcAvg(avgSumB, avgCount);

        }
    }

    return;
}

// // Blur image
// // make blur with more clear steps
// void blur(int height, int width, RGBTRIPLE image[height][width])
// {
//     // loop for rows
//     // loop for col
//     // check if row - 1 exist
//     // check if row + 1 exist
//     // get row -1 px after & before of the current org px if exist
//     // get row +1 px after & before of the current org px if exist
//     // calc avg for all rgb around + org px inclusive

//     int avgSumR, avgSumG, avgSumB;
//     float avgCount;
//     // copy 4 operations
//     RGBTRIPLE imgCopy[height][width];
//     for (int i = 0; i < height; i++)
//     {
//          for (int j = 0; j < width; j++)
//          {
//              imgCopy[i][j] = image[i][j];
//          }
//      }

//     for (int i = 0; i < height; i++)
//     {
//         for (int x = 0; x < width; x++)
//         {
//             RGBTRIPLE currentPx = { .rgbtBlue = 0, .rgbtGreen = 0, .rgbtRed = 0 },
//                       beforePx = { .rgbtBlue = 0, .rgbtGreen = 0, .rgbtRed = 0 },
//                       afterPx = { .rgbtBlue = 0, .rgbtGreen = 0, .rgbtRed = 0 };
//             avgSumR = avgSumG = avgSumB = 0;
//             avgCount = 0.00;


//             currentPx = image[i][x];

//             // add row before pxs
//             if (i - 1 > -1)
//             {
//                 // before same curr px index in this row
//                 if (x - 1 > -1)
//                 {
//                     avgSumR += image[i - 1][x - 1].rgbtRed;
//                     avgSumG += image[i - 1][x - 1].rgbtGreen;
//                     avgSumB += image[i - 1][x - 1].rgbtBlue;

//                     avgCount++;
//                 }
//                 // after same curr px index in this row
//                 if (x + 1 < width)
//                 {
//                     avgSumR += image[i - 1][x + 1].rgbtRed;
//                     avgSumG += image[i - 1][x + 1].rgbtGreen;
//                     avgSumB += image[i - 1][x + 1].rgbtBlue;

//                     avgCount++;
//                 }
//                 // curr px index in this row
//                 avgSumR += image[i - 1][x].rgbtRed;
//                 avgSumG += image[i - 1][x].rgbtGreen;
//                 avgSumB += image[i - 1][x].rgbtBlue;

//                 avgCount++;

//             }
//             // add row after pxs
//             if (i + 1 < height)
//             {
//                 // before same curr px index in this row
//                 if (x - 1 > -1)
//                 {
//                     avgSumR += image[i + 1][x - 1].rgbtRed;
//                     avgSumG += image[i + 1][x - 1].rgbtGreen;
//                     avgSumB += image[i + 1][x - 1].rgbtBlue;

//                     avgCount++;
//                 }
//                 // after same curr px index in this row
//                 if (x + 1 < width)
//                 {
//                     avgSumR += image[i + 1][x + 1].rgbtRed;
//                     avgSumG += image[i + 1][x + 1].rgbtGreen;
//                     avgSumB += image[i + 1][x + 1].rgbtBlue;

//                     avgCount++;
//                 }
//                 // curr px index in this row
//                 avgSumR += image[i + 1][x].rgbtRed;
//                 avgSumG += image[i + 1][x].rgbtGreen;
//                 avgSumB += image[i + 1][x].rgbtBlue;

//                 avgCount++;

//             }

//             // add currentPx's before
//             if (x - 1 > -1)
//             {
//                 avgSumR += image[i][x - 1].rgbtRed;
//                 avgSumG += image[i][x - 1].rgbtGreen;
//                 avgSumB += image[i][x - 1].rgbtBlue;

//                 avgCount++;
//             }
//             // add currentPx's after
//             if (x + 1 < width)
//             {
//                 avgSumR += image[i][x + 1].rgbtRed;
//                 avgSumG += image[i][x + 1].rgbtGreen;
//                 avgSumB += image[i][x + 1].rgbtBlue;

//                 avgCount++;
//             }

//             // add currentPx
//             avgSumR += currentPx.rgbtRed;
//             avgSumG += currentPx.rgbtGreen;
//             avgSumB += currentPx.rgbtBlue;

//             avgCount++;

//             // apply avg
//             image[i][x].rgbtRed = calcAvg(avgSumR, avgCount);
//             image[i][x].rgbtGreen = calcAvg(avgSumG, avgCount);
//             image[i][x].rgbtBlue = calcAvg(avgSumB, avgCount);

//         }
//     }

//     return;
// }