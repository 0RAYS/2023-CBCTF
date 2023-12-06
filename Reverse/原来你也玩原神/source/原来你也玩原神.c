#include<stdio.h>
#include<string.h>
int main() {
	printf("原来你也玩原神\n");
	printf("请告诉我你最喜欢的原神角色:\n");
	char a[256];
	gets(a);
	if (strcmp(a, "我不玩原神")==0) {
		printf("CBCTF{I_hate_Genshin_Impact_and_Two_spiny_newts}");
	}
	else {
		printf("你真的玩原神吗?");
	}
	getch();

	return 0;
}