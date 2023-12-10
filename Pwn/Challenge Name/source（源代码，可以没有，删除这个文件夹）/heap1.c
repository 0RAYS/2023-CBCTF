#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>

struct NODE{
	long long key;
	char*ptr[0x20];
	long long size[0x1f];
	long long max_node;
}node;
void Add(){
	int idx,siz;
	printf("idx:");
	scanf("%d",&idx);
	printf("size:");
	scanf("%d",&siz);
	if(idx<0 || idx>=node.max_node){puts("out of range");return;}
	node.ptr[idx]=malloc(siz);
	node.size[idx]=siz;
}
void Free(){
	int idx;
	printf("idx:");
	scanf("%d",&idx);
        if(node.ptr[idx]==0){puts("no chunk");return;}
	free(node.ptr[idx]);
	node.ptr[idx]=0;
	node.size[idx]=0;
}
void myread(char *s,int siz){
	int len = read(0,s,siz);
	for(int i=len; i; i--){
		if(s[i]=='\n'){
			s[i]=0;
			return;
		}
	}
}
void Edit(){
        int idx,siz;
        printf("idx:");
        scanf("%d",&idx);
        if(node.ptr[idx]==0){puts("no chunk");return;}
        printf("content:");
	myread(node.ptr[idx],node.size[idx]);
}
void Show(){
	int idx;
	printf("idx:");
	scanf("%d",&idx);
        if(node.ptr[idx]==0){puts("no chunk");return;}
	write(1,node.ptr[idx],node.size[idx]);
}
void menu(){
	puts("1.add");
	puts("2.free");
	puts("3.edit");
	puts("4.show");
	puts("5.exit");
	printf("choice:");
}
void init(){
	node.max_node=0x20;
	setbuf(stdin, 0LL);
	setbuf(stdout, 0LL);
	setbuf(stderr, 0LL);
}
int main(){
	init();
	while(1){
		menu();
		int choice=0;
		scanf("%d",&choice);
		switch(choice){
			case 1:{
				Add();
				break;
			} case 2:{
				Free();
				break;
			} case 3:{
				Edit();
				break;
			} case 4:{
				Show();
				break;
			} case 5:{
				if(node.key==0x656572545f676553)
					system("/bin/sh");
				return 0;
			} default:puts("wrong choice!");
		}
	}
	return 0;
}
