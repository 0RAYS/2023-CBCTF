// TIVM_run.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <stdio.h>
#include <stdlib.h>

#define FILE_SIZE 0x763

int code[0x800];
const char file_name[] = "traceme.bin";

void read_code()
{
    FILE _f;
    FILE *fp = &_f;
    fopen_s(&fp, file_name, "rb");
    if (!fp)
    {
        printf("找不到文件%s\n", file_name);
        exit(0);
    }
    fread(code, 4, FILE_SIZE, fp);
    fclose(fp);
}

void run()
{
    int ip = 0;
    int a1, a2, a3;
    int nj;

    while (ip < FILE_SIZE - 2)
    {
        a1 = code[ip];
        a2 = code[ip + 1];
        a3 = code[ip + 2];
        nj = ip + 3;

        if (a2 < 0)
        {
            putchar(code[a1]);
        }
        else if (a1 < 0)
        {
            code[a2] = getchar();
        }
        else
        {
            if ((code[a2] -= code[a1]) <= 0)
            {
                nj = a3;
            }
        }
        ip = nj;
    }
}

int main()
{
    read_code();
    run();
}

// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
