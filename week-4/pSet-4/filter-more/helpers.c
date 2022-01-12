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

// calc sqrt sum
int calcSqrt(int gx, int gy)
{
    return limit(round(sqrt((gx * gx) + (gy * gy))));
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

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
            RGBTRIPLE currentPx, currentPxBefore, currentPxAfter, beforePx1, beforePx2, beforePx3, afterPx1, afterPx2, afterPx3;
            int gxSumR, gxSumG, gxSumB, gySumR, gySumG, gySumB;
            gxSumR = gxSumG = gxSumB = gySumR = gySumG = gySumB = 0;
            currentPx = imgCopy[i][x];

            // https://medium.com/swlh/cs50-pset-4-filter-8cbf734b0dbc
            // For each pixel, loop vertical and horizontal
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // Check if pixel is outside rows
                    if (i + k < 0 || i + k >= height)
                    {
                        continue;
                    }
                    // Check if pixel is outside columns
                    if (x + l < 0 || x + l >= width)
                    {
                        continue;
                    }
                    // Otherwise add to sums
                    gxSumR += imgCopy[i + k][x + l].rgbtRed * gx[k + 1][l + 1];
                    gxSumG += imgCopy[i + k][x + l].rgbtGreen * gx[k + 1][l + 1];
                    gxSumB += imgCopy[i + k][x + l].rgbtBlue * gx[k + 1][l + 1];

                    gySumR += imgCopy[i + k][x + l].rgbtRed * gy[k + 1][l + 1];
                    gySumG += imgCopy[i + k][x + l].rgbtGreen * gy[k + 1][l + 1];
                    gySumB += imgCopy[i + k][x + l].rgbtBlue * gy[k + 1][l + 1];
                }
            }

            // apply sqr
            image[i][x].rgbtRed = calcSqrt(gxSumR, gySumR);
            image[i][x].rgbtGreen = calcSqrt(gxSumG, gySumG);
            image[i][x].rgbtBlue = calcSqrt(gxSumB, gySumB);

        }
    }

    return;
}
