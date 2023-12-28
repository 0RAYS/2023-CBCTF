#include <stdio.h>
#include <stdint.h>
#include<string.h>
#include<stdlib.h>

double ewma_weight = 1.0;
double alpha = 0.5;

double ewma(double prev_avg, double value, double alpha) {
    return alpha * value + (1 - alpha) * prev_avg;
}


int main(void) {
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);

    double serial[7] = { 0,};

    unsigned char buffer[7];
    //int bitmap[44] = { 0,0 };

    printf("Give me your seial ,i will give you the flag:\n");
    printf("Your serial:");


    if (!fgets(buffer, sizeof(buffer), stdin)) {
        printf("bad serial");
        exit(0);
    }
    for (int i = 0; i < 6; i++) {
        buffer[i] =buffer[i] - '0';
        serial[i] = (double)buffer[i];

        if (buffer[i] != 0 && buffer[i] != 1) {
            printf("bad serial");
            exit(0);
        }
    }



    FILE* file;

    file = fopen("flag", "r");
    if (file == NULL) {
        perror("Error opening file");
        return -1;
    }

   

    fclose(file);


    unsigned char flag[44];


    file = fopen("flag", "r");
    if (file == NULL) {
        perror("Error opening file");
        return -1;
    }

    fgets(flag, sizeof(flag), file);

    fclose(file);


    int r = sizeof(flag) / sizeof(flag[0]) - 1;
    int l = 0;

        int count = 0;

        printf("flag:");
        while (l <= r) {



            int m = l + (r - l) / 2;
            
            //bitmap[m] = 1;
            printf("%c", flag[m]);
            
            ewma_weight = ewma(ewma_weight, serial[count++], alpha);
            
            //printf("i=%d,l=%d,r=%d,ewma_weight=%.2f\n", m, l, r, ewma_weight);

            if (ewma_weight > 0.5)
                l = m + 1;

            else
                r = m - 1;
        }


        printf("\n");
        return 0;
    /*for (int t = 0; t < 44; t++) {
        printf("%d,", bitmap[t]);
    }*/
}
