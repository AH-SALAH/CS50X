// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
const unsigned int N = (LENGTH + 1) *'z';
// words count
unsigned int wrds_c = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int i = hash(word);
    node *crsr = table[i];

    while (crsr != NULL)
    {
        if (strcasecmp(crsr->word, word) == 0)
        {
            return true;
        }
        crsr = crsr->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hv = 0;
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        // https://stackoverflow.com/questions/2624192/good-hash-function-for-strings?noredirect=1&lq=1
        hv += 33 + tolower(word[i]); // [prime 33 as mentioned in djb2] http://www.cse.yorku.ca/~oz/hash.html
    }

    return hv % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    char w[LENGTH + 1];

    while (fscanf(dict, "%s", w) != EOF)
    {
        node *nd = malloc(sizeof(node));

        if (nd == NULL)
        {
            return false;
        }

        strcpy(nd->word, w);

        unsigned int i = hash(w);

        nd->next = table[i];
        table[i] = nd;

        wrds_c++;
    }

    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wrds_c;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            node *crsr = table[i];
            node *tmp = crsr;

            while (crsr != NULL)
            {
                tmp = crsr;
                crsr = crsr->next;
                free(tmp);
            }
        }
    }

    return true;
}
