#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

FILE* fp;
char* ptr;
char flag[100]; // For this PoC, the aim is to read in arbitrary data into 'flag'

int main()
{
  char buf[100];

  /* Stimulating a use-after-free with which we can modify the file structure */

  ptr=malloc(0x200);
  free(ptr);

  fp=fopen("inp","rw");
  read(0,ptr,0x1000);
  fscanf(fp,"%s",buf); 

  puts(flag); // This is just to show the current value in 'flag'
}
