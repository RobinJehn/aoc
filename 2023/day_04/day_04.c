#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
  FILE *fp;
  char *line = NULL;
  size_t len = 0;
  ssize_t read;

  const bool debug = false;

  // const char *file_name = "test.txt";
  // const int num_win_nums = 5;

  const char *file_name = "input.txt";
  const int num_win_nums = 10;

  fp = fopen(file_name, "r");
  if (fp == NULL)
    exit(EXIT_FAILURE);

  int total = 0;
  while ((read = getline(&line, &len, fp)) != -1) {
    // Skip the first part
    int skip_idx = 0;
    while (*(line + skip_idx) != ':') {
      skip_idx++;
    }

    char *game_str = line + skip_idx + 2;
    printf("line: %s", game_str);
    int num = -1;
    int win_nums[num_win_nums];
    int idx = 0;
    bool second_half = false;
    int count = 0;
    const unsigned int len = strlen(game_str);
    for (int i = 0; i < len; i++) {
      if (game_str[i] == ' ' && game_str[i + 1] == ' ') {
        continue;
      } else if (game_str[i] == '|') {
        second_half = true;
      } else if (num == -1) {
        num = atoi(&game_str[i]);
        if (second_half) {
          for (int i = 0; i < num_win_nums; i++) {
            if (win_nums[i] == num) {
              count++;
              break;
            }
          }
        } else {
          win_nums[idx++] = num;
        }
      } else if (game_str[i] == ' ') {
        num = -1;
      }
    }

    if (count == 0) {
      continue;
    }
    total += pow(2, count - 1);
  }
  printf("\ntotal: %d\n", total);

  fclose(fp);
  if (line)
    free(line);
  exit(EXIT_SUCCESS);
}