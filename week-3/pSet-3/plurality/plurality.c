// #include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
// #include <cs50.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    const char *name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
int vote(const char *name);
void print_winner(void);

int main(int argc, const char *argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    // int voter_count = get_int("Number of voters: ");

    int voter_count;
    do
    {
        printf("Number of voters: ");
        scanf("%d", &voter_count);
    }
    while (!voter_count);

    // Loop over all voters
    int i = 0;
    char name[30];
    do
    {

        printf("Vote: ");
        scanf("%s", name);

        // printf("name: %s \n", name);

        // const char *n = name;
        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
        else
        {
            i++;
        }

    }
    while (i < voter_count);

    // Display winner of election
    print_winner();

}

// Update vote totals given a new vote
int vote(const char *name)
{
    // printf("name: %s", name);
    if (!name)
    {
        printf("Please, choose a name.\n");
        return 0;
    }

    // loop over candidates &
    int found = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        const char *cName = candidates[i].name;
        // int cVote = candidates[i].votes;

        // if name equal 1 of them vote up this cand
        if (strcmp(cName, name) == 0)
        {
            candidates[i].votes += 1;
            found += 1;
            // printf("up: %s: %i\n", cName, candidates[i].votes);
        }

        if (found)
        {
            return 2;
        }

    }

    // if name not found among candidates, return;
    if (found == 0)
    {
        printf("Name not exist.\n");
        return 0;
    }

    return 1;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // TODO
    candidate biggest;
    candidate cCache;
    for (int i = 0; i < candidate_count; i++)
    {
        // sort

        if (i + 1 <= candidate_count - 1 && candidates[i].votes > candidates[i + 1].votes)
        {
            // biggest = candidates[i];
            cCache = candidates[i];
            candidates[i] = candidates[i + 1];
            candidates[i + 1] = cCache;
        }
        // printf("cname: %s cnamenext: %s \n", candidates[i].name, candidates[i + 1].name);
        biggest = candidates[i];
    }

    // & get the biggest votes numbers name
    for (int x = 0; x < candidate_count; x++)
    {
        // printf("candName: %s candVote: %i biggest: %s: %i \n", candidates[x].name, candidates[x].votes, biggest.name, biggest.votes);
        if (candidates[x].votes == biggest.votes)
        {
            // printf("Candidate: %s\nVotes: %i\n", candidates[x].name, candidates[x].votes);
            printf("%s\n", candidates[x].name);
        }
    }

    return;
}
