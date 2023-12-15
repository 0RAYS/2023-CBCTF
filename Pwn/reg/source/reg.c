#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include <sys/prctl.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
void sandbox(){
	struct sock_filter filter[] = {
	BPF_STMT(BPF_LD+BPF_W+BPF_ABS,4),
	BPF_JUMP(BPF_JMP+BPF_JEQ,0xc000003e,0,3),
	BPF_STMT(BPF_LD+BPF_W+BPF_ABS,0),
	BPF_JUMP(BPF_JMP+BPF_JEQ,59,0,2),
	BPF_JUMP(BPF_JMP+BPF_JEQ,322,0,1),
	BPF_STMT(BPF_RET+BPF_K,SECCOMP_RET_KILL),
	BPF_STMT(BPF_RET+BPF_K,SECCOMP_RET_ALLOW),
	};
	struct sock_fprog prog = {
	.len = (unsigned short)(sizeof(filter)/sizeof(filter[0])),
	.filter = filter,
	};
	prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0);
	prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&prog);
}
void set(long long *a){
    int pos,type;
    long long val;
    scanf("%d%d%lld",&pos,&type,&val);
    if(pos<0 || pos>0x20)return;
    if(type==1)
        a[pos]=val;
    else if(type==2){
        if(val<0 || val>0x20)
            return;
        a[pos]=a[val];
    }
}
void add(long long *a){
    int pos,type;
    long long val;
    scanf("%d%d%lld",&pos,&type,&val);
    if(pos<0 || pos>0x20)return;
    if(type==1)
        a[pos]+=val;
    else if(type==2){
        if(val<0 || val>0x20)
            return;
        a[pos]+=a[val];
    }
    
}
void func(long long val){
    long long a[0x20];
    int op;
    while(1){
        scanf("%d",&op);       
        switch(op){
            case 1:{
                set(a);
                break;
            } case 2:{
                add(a);
                break;
            } case 3:{
                return;
                break;
            }
        }
    }
}
int main(){
	long long val=0;
	sandbox();
	setbuf(stdin, val);
	setbuf(stdout, val);
	setbuf(stderr, val);
    func(val);
}
