#include <stdio.h>
#include <stdlib.h>

int balance = 20; // User's initial balance
int humbleCount = 0; // Number of 'Humble' items owned
int yolbbyCount = 0; // Number of 'Yolbby' items owned
int flagCount = 0;   // Number of 'Flag' items owned

void showMenu() {
    printf("\nWelcome to the Shop! Your balance is: %d\n", balance);
    printf("1. Buy\n");
    printf("2. Sell\n");
    printf("3. Exit\n");
    printf("Choose an option (1-3): ");
}

void printFlag() {
    FILE* file = fopen("flag", "r");
    if (file == NULL) {
        printf("Unable to open the flag file.\n");
        return;
    }

    char line[1024];
    while (fgets(line, sizeof(line), file)) {
        printf("%s", line);
    }
    fclose(file);
}

void buyItem() {
    int itemChoice, quantity;
    printf("You have chosen to buy.\n");
    printf("Available items and their prices:\n");
    printf("  1. Humble (5)\n");
    printf("  2. Yolbby (10)\n");
    printf("  3. Flag (1000)\n");
    printf("Select an item (1-3): ");
    scanf("%d", &itemChoice);
    printf("Enter the quantity to buy: ");
    scanf("%d", &quantity);

    int cost = 0;
    switch (itemChoice) {
    case 1:
        cost = 5 * quantity;
        if (balance >= cost) {
            balance -= cost;
            humbleCount += quantity;
            printf("You bought %d Humble(s) for %d, current balance: %d.\n", quantity, cost, balance);
        }
        else {
            printf("Insufficient balance to buy Humble.\n");
        }
        break;
    case 2:
        cost = 10 * quantity;
        if (balance >= cost) {
            balance -= cost;
            yolbbyCount += quantity;
            printf("You bought %d Yolbby(s) for %d, current balance: %d.\n", quantity, cost, balance);
        }
        else {
            printf("Insufficient balance to buy Yolbby.\n");
        }
        break;
    case 3:
        cost = 1000 * quantity;
        if (balance >= cost) {
            balance -= cost;
            flagCount += quantity;
            printf("Congratulations, you bought %d Flag(s) for %d, current balance: %d.\n", quantity, cost, balance);
            printFlag();
        }
        else {
            printf("Insufficient balance to buy Flag.\n");
        }
        break;
    default:
        printf("Invalid option, please choose again.\n");
    }
}

void sellItem() {
    int itemChoice, quantity;
    printf("You have chosen to sell.\n");
    printf("Your inventory:\n");
    printf("  Humble: %d\n", humbleCount);
    printf("  Yolbby: %d\n", yolbbyCount);
    printf("  Flag: %d\n", flagCount);
    printf("Select the item to sell (1. Humble, 2. Yolbby, 3. Flag): ");
    scanf("%d", &itemChoice);
    printf("Enter the quantity to sell: ");
    scanf("%d", &quantity);

    int income = 0;
    switch (itemChoice) {
    case 1:
        if (humbleCount >= quantity) {
            humbleCount -= quantity;
            income = 5 * quantity;
            balance += income;
            printf("You sold %d Humble(s) for %d, current balance: %d.\n", quantity, income, balance);
        }
        else {
            printf("You do not have enough Humble to sell.\n");
        }
        break;
    case 2:
        if (yolbbyCount >= quantity) {
            yolbbyCount -= quantity;
            income = 10 * quantity;
            balance += income;
            printf("You sold %d Yolbby(s) for %d, current balance: %d.\n", quantity, income, balance);
        }
        else {
            printf("You do not have enough Yolbby to sell.\n");
        }
        break;
    case 3:
        if (flagCount >= quantity) {
            flagCount -= quantity;
            income = 1000 * quantity;
            balance += income;
            printf("You sold %d Flag(s) for %d, current balance: %d.\n", quantity, income, balance);
        }
        else {
            printf("You do not have enough Flag to sell.\n");
        }
        break;
    default:
        printf("Invalid option, please choose again.\n");
    }
}

int main() {
    int choice;

    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    while (1) {
        showMenu();
        scanf("%d", &choice);

        switch (choice) {
        case 1:
            buyItem();
            break;
        case 2:
            sellItem();
            break;
        case 3:
            printf("Thank you for visiting, goodbye!\n");
            return 0;
        default:
            printf("Invalid option, please choose again.\n");
        }
    }

    return 0;
}
