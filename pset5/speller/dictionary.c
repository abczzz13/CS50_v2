// Implements a dictionary's functionality
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

int counter = 0;
// Number of buckets in hash table
const unsigned int N = 10000; // approx total time 0.09

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO

    // Iterate through the linked list of the hashed word
    for (node *tmp = table[hash(word)]; tmp != NULL; tmp = tmp->next)
    {
        // Compare input to hash table and return true if it's found
        if (strcasecmp(word, tmp->word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    // Hash djb2 by Dan Bernstein from http://www.cse.yorku.ca/~oz/hash.html
    unsigned long hash = 5381;
    int c;

    while ((c = *word++)) // (c = *str++)
    {
        hash = ((hash << 5) + hash) + tolower(c); /* hash * 33 + c */
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{

    // TODO
    // Open file and check if successful
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Declarations
    char buffer[LENGTH + 1];
    unsigned int hash_num;

    // Start reading from file until EOF (end of file)
    while (fscanf(file, "%s", buffer) != EOF)
    {
        // Allocate memory for node n
        node *n = malloc(sizeof(node));

        // Check if it went successfully, otherwise free, close and return
        if (n == NULL)
        {
            free(n);
            fclose(file);
            return false;
        }

        // Fill in the node from the buffer
        strcpy(n->word, buffer);

        // Hash the word
        hash_num = hash(n->word);

        // Insert into the hash table
        n->next = table[hash_num];
        table[hash_num] = n;

        // Counter
        counter++;
    }
    // Close file
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{

    // TODO
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // For loop to go through all the hash tables
    for (int i = 0; i < N; i++)
    {
        // While loop to iterate to traverse over the linked list
        while (table[i] != NULL)
        {
            // Create temporary node to point to the next node in the list, free list
            node *tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp;
        }
    }
    // Return true if list is completely empty
    if (table[N - 1] == NULL)
    {
        return true;
    }
    return false;
}
