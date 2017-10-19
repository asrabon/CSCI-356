#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <string.h>
#include <fcntl.h>
#include <signal.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <stdbool.h>

#define ROCK 1
#define PAPER 2
#define SCISSORS 3

void *throw();
void determine_round_winner();
void determine_winner();

//pointer to player one shared memory object
int* p_one_ptr;
//pointer to player two shared memory object
int* p_two_ptr;
//strings that represent rock, paper, scissors in array
const char *rps[3];
//scores for the game
int player_one_score;
int player_two_score;

int main(int argc, char** argv) {
  rps[0] = "Rock";
  rps[1] = "Paper";
  rps[2] = "Scissors";

  player_one_score = 0;
  player_two_score = 0;

  int num_rounds = atoi(argv[1]);

  printf("Beginning %d Rounds...\n", num_rounds);
  printf("Fight\n");
  printf("---------------------------------------\n");


  for(int i=0; i<num_rounds; i++) {
    printf("Round %d:\n", i+1);
    pthread_t player_one_thread;
    pthread_create(&player_one_thread, NULL, throw, &p_one_ptr);
    pthread_t player_two_thread;
    pthread_create(&player_two_thread, NULL, throw, &p_two_ptr);
    pthread_join(player_one_thread, NULL);
    pthread_join(player_two_thread, NULL);
    determine_round_winner();
    printf("---------------------------------------\n");
  }
  determine_winner();
  return 0;
}

void *throw(void *choice_void_ptr) {
    int *choice_ptr = (int *)choice_void_ptr;

    printf("%d\n", syscall(SYS_gettid));

    srand(time(NULL) * syscall(SYS_gettid) );
    int choice = rand() % 3 + 1;
    *choice_ptr = choice;
  }

void determine_round_winner() {
  int player_one_choice = p_one_ptr;
  int player_two_choice = p_two_ptr;
  bool player_one_win = false;
  bool player_two_win = false;

  if(player_one_choice != player_two_choice) {
    if(player_one_choice == ROCK && player_two_choice == PAPER) {
      player_two_win = true;
    } else if(player_one_choice == ROCK && player_two_choice == SCISSORS) {
      player_one_win = true;
    } else if(player_one_choice == PAPER && player_two_choice == ROCK) {
      player_one_win = true;
    } else if(player_one_choice == PAPER && player_two_choice == SCISSORS) {
      player_two_win = true;
    } else if(player_one_choice == SCISSORS && player_two_choice == ROCK) {
      player_two_win = true;
    } else {
      player_one_win = true;
    }
  }

  printf("Child 1 throws %s!\n", rps[player_one_choice - 1]);
  printf("Child 2 throws %s!\n", rps[player_two_choice - 1]);
  if(player_one_win) {
    printf("Child 1 Wins!\n");
    player_one_score++;
  } else if(player_two_win) {
    printf("Child 2 Wins!\n");
    player_two_score++;
  } else {
    printf("Draw!\n");
  }
}

void determine_winner() {
  printf("---------------------------------------\n");
  printf("Results:\n");
  printf("Child 1: %d\n", player_one_score);
  printf("Child 2: %d\n", player_two_score);

  if(player_one_score > player_two_score) {
    printf("Child 1 Wins!\n");
  } else if(player_two_score > player_one_score) {
    printf("Child 2 Wins!\n");
  } else {
    printf("Draw!\n");
  }
}
