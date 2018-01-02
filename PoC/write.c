#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

FILE* fp;
char* ptr;
char* flag="A message you can never see !"; // This is what is to be printed out

int main()
{
  char buf[100];

  /* Stimulating a use-after-free with which we can modify the file structure */

  ptr=malloc(0x200);
  free(ptr);

  fp=fopen("inp","rw");
  read(0,ptr,0x1000); //This is actually reading data into the file structure

  fprintf(fp,"%s",buf);
}
