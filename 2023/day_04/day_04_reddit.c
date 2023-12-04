#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUM_WIN 10
#define NUM_HAVE 25

// #define NUM_WIN 5
// #define NUM_HAVE 8

int main() {
  FILE *f = fopen("input.txt", "r");

  int cardNumber;

  int winning[NUM_WIN];
  int have[NUM_HAVE];

  int sum = 0;

  while (!feof(f)) {
    fscanf(f, "Card %d: ", &cardNumber);

    for (int i = 0; i < NUM_WIN; i++) {
      fscanf(f, "%d ", &winning[i]);
    }

    fscanf(f, "| ");

    for (int i = 0; i < NUM_HAVE; i++) {
      fscanf(f, "%d ", &have[i]);
    }

    int score = 0;

    for (int i = 0; i < NUM_WIN; i++) {
      for (int j = 0; j < NUM_HAVE; j++) {
        if (winning[i] == have[j]) {
          if (score == 0) {
            score = 1;
          } else {
            score *= 2;
          }
        }
      }
    }
    sum += score;
  }

  printf("%d\n", sum);

  fclose(f);
}