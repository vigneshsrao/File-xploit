#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main()
{

	setbuf(stdin,NULL);
	setbuf(stdout,NULL);
	void *ptr=malloc(400);
	malloc(200);
	free(ptr);
	printf("Heap leak - %lu\n",(unsigned long)ptr);
	printf("libc leak - %lu\n",*(unsigned long*)ptr);
	read(0,ptr-8,400);
	malloc(0x10);
}
	
