//gcc -o pwn main.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h> 
#include <unistd.h>
#include <fcntl.h>

char buf[0x100];

void init()
{
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
}


int main()
{
	char name[0x10];
	init();
	memset(name,0,sizeof(name));
	printf("Welcome2CyberClub!\n");
	printf("Your name:");
	read(0,name,0x10);
	printf("Hello:");
	printf(name);
	
	printf("\nIt's a test about FMT,try your best to solve it !\n");
	printf("context:\n");
	read(0,buf,0x10);
	scanf(buf);
	
	printf("context:\n");
	read(0,buf,0x10);
	scanf(buf);
	printf("Hope you can go where you want!\n");	
	
	return 0;
}
