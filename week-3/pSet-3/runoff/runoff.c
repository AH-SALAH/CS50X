#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
// #include <cs50.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    const char *name;
    int votes;
    int eliminated;
} candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
int vote(int voter, int rank, const char *name);
void tabulate(void);
int print_winner(void);
int find_min(void);
int is_tie(int min);
void eliminate(int min);

int main(int argc, const char *argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = 0;
    }

    // voter_count = get_int("Number of voters: ");
    printf("Number of voters: ");
    scanf("%d", &voter_count);

    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // const char *name = malloc(10 * sizeof(char));
    char name[30];
    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            // string name = get_string("Rank %i: ", j + 1);
            printf("Rank %i: ", j + 1);
            scanf("%s", name);
            // printf("Name: %s ", &name);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (1)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        int won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        int tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }

    // free(name);

    return 0;
}

// Record preference if vote is valid
int vote(int voter, int rank, const char *name)
{
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
        // if name equal 1 of them vote up this cand
        if (strcmp(cName, name) == 0)
        {
            preferences[voter][rank] = i;
            found += 1;
        }

        // printf("pref: %d found: %d\n", preferences[voter][rank], found);

        if (found)
        {
            return 2;
        }
        // printf("Name: %s cname: %s strcmp: %d found: %d\n", name, cName, strcmp(cName, name), found);
    }

    // printf("Name not exist.\n");
    return 0;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    int *voter;
    candidate cand;

    for (int i = 0; i < voter_count; i++)
    {
        voter = preferences[i];

        for (int j = 0; j < candidate_count; j++)
        {
            cand = candidates[voter[j]];

            // if not eliminated vote up this cand
            if (!cand.eliminated)
            {
                candidates[voter[j]].votes += 1;
                // printf("Tabulate: voter: %i pref %i: %i cand: %s votes: %i\n", i, j, voter[j], candidates[voter[j]].name, candidates[voter[j]].votes);
                break;
            }
        }
    }

    return;
}

// Print the winner of the election, if there is one
int print_winner(void)
{
    int half = voter_count / 2;
    candidate cand;

    for (int i = 0; i < candidate_count; i++)
    {
        cand = candidates[i];
        // printf("cand: %s votes: %i half: %i \n", candidates[i].name, candidates[i].votes, half);
        if (cand.votes > half && !cand.eliminated)
        {
            printf("%s\n", cand.name);
            return 1;
        }
    }

    return 0;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    int min = voter_count;
    candidate cand;
    // candidate cache;
    // candidate c2;

    for (int i = 0; i < candidate_count; i++)
    {
        cand = candidates[i];
        // c2 = candidates[i + 1];

        if (cand.votes < voter_count && !cand.eliminated)
        {
            min = cand.votes;
        }
    }

    // printf("min: %i \n", min);
    return min;
}

// Return 1 if the election is tied between all candidates, 0 otherwise
int is_tie(int min)
{
    candidate cand;

    for (int i = 0; i < candidate_count; i++)
    {
        cand = candidates[i];
        if (cand.votes != min && !cand.eliminated)
        {
            return 0;
        }
    }

    // printf("isTie: candVotes: %i min: %i\n", cand.votes, min);

    return 2;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    candidate cand;

    for (int i = 0; i < candidate_count; i++)
    {
        cand = candidates[i];
        if (cand.votes == min && !cand.eliminated)
        {
            candidates[i].eliminated = 1;
            // printf("eliminated: name: %s votes: %i \n", cand.name, cand.votes);
        }
    }

    return;
}