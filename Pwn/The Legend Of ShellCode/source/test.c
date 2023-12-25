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
        printf(" _____ _            _                              _    ___   __ \n");
        printf("|_   _| |__   ___  | |    ___  __ _  ___ _ __   __| |  / _ \\ / _|\n");
        printf("  | | | '_ \\ / _ \\ | |   / _ \\/ _` |/ _ \\ '_ \\ / _` | | | | | |_ \n");
        printf("  | | | | | |  __/ | |__|  __/ (_| |  __/ | | | (_| | | |_| |  _|\n");
        printf("  |_| |_| |_|\\___| |_____\\___|\\__, |\\___|_| |_|\\__,_|  \\___/|_|  \n");
        printf("                              |___/\n");
        printf(" ____  _          _ _  ____          _      \n");
        printf("/ ___|| |__   ___| | |/ ___|___   __| | ___ \n");
        printf("\\___ \\| '_ \\ / _ \\ | | |   / _ \\ / _` |/ _ \\\n");
        printf(" ___) | | | |  __/ | | |__| (_) | (_| |  __/\n");
        printf("|____/|_| |_|\\___|_|_|\\____\\___/ \\__,_|\\___|\n");      
}


int main()
{
	//char name[0x10];
	char a[0x10];
	char b[0x10];
	char c[0x10];
	char d[0x10];
	char e[0x10];
	char f[0x10];
	init();
	memset(a,0xc3,0x60);
	puts("Welcome2TheLegendOfShellCode!");
	puts("Now show me your wisdom:");
	read(0,a,9);
	puts("Now show me your courage:");
	read(0,b,9);
	puts("Now show me your strength:");
	read(0,c,9);	
	puts("Now show me your flesh:");
	read(0,d,9);
	puts("Now show me your thought:");
	read(0,e,9);
	puts("Now show me your soul:");
	read(0,f,9);	
	puts("Keep going!Wish you could bring peace to hararu");
	((void (*)(void))a)();
	return 0;
}
