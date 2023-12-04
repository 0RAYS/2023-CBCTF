import random 
import os

qa_list = [
    {
        "q": """
contract StorageChallenge1 {
    address[2] private investor;
    uint64 private password;
    bytes32 private user;
    address private owner;
}
""",
        "a": 2
    },
    {
        "q": """
contract StorageChallenge2 {
    uint64 private password;
    bytes32 private user;
    address[2] private investor;
    bytes32 immutable passphrase;
    address private owner;
}
""",
        "a": 0
    },
    {
        "q": """
contract StorageChallenge3 {
    bytes32 private key;
    bytes4 private key_1;
    bytes16 private key_2;
    address private owner;
    uint256 private Token;
    address private immutable Investor;
    address private Courier;
    bytes32 private immutable password;
}
""",
        "a": 0
    },
    {
        "q": """
contract StorageChallenge4 {
    bytes32 private unique_code;
    bytes32 private key_12;
    address private owner;
    address[20] public player;
    bool private valid;
    bytes32 private password;
    address private enemy;
    bool private answered;
}
""",
        "a": 24
    },
    {
        "q": """
contract StorageChallenge5 {
    bool private string_true;
    bool private number_false;
    bool private user_true;
    bytes32 private username;
    bytes32 private password;
    bool public status_creds;
}
""",
        "a": 2
    },
    {
        "q": """
contract StorageChallenge6 {
    bytes32 private code;
    bytes8 immutable private enter_key;
    bool private user_true;
    bytes32 private username;
    bytes32 private password;
}
""",
        "a": 3
    },
    {
        "q": """
contract StorageChallenge7 {
    struct Info {
        uint256 a ;
        uint256 b ;
    }
    Info info1;
    Info info2;
    bytes32 public username;
    bytes32 private password;
}
""",
        "a": 5
    },
    {
        "q": """
contract StorageChallenge8 {
    mapping(uint256 => uint256) Balance;
    bytes16 status;
    address owner;
    bytes32 password;
    bytes32 plain;
}
""",
        "a": 3
    },
    {
        "q": """
contract StorageChallenge9 {
    uint [] private Balance;
    bytes16 private status;
    address immutable owner;
    bytes32 private password;
    bytes32 public plain;
}
""",
        "a": 2
    },
    {
        "q": """
contract StorageChallenge10 {
    bytes32 private key;
    bytes4 private key_1;
    bytes16 private key_2;
    address private owner;
    uint256 private Token;
    string public Info = "Be careful with that";
    bytes32 private password;
}
""",
        "a": 5
    }
]


def info():
    print("""====Going to The Party====

To Find the party location
You need to solve a simple riddle regarding a SLOT
Answer everything correctly, and find the exact location!

Question: In which Slot is Password Stored?

You'll answer with and ONLY WITH [numbers]
ex: 
0,1,2,3,4.....,99

Note: 
    -   Slot start from 0
    -   If it doesn't stored on SLOT, answer 0
    -   Answer correctly 10 times to get the flag
""")

def main():
    info()
    print("Identification Required for Guest")
    print()
    correct = 0
    selected_qa = random.sample(qa_list, 10)

    for qa in selected_qa:

        print("Question:")
        print(qa["q"])

        answer = int(input("Answer: "))

        if answer == qa["a"]:
            correct += 1;
            if correct == 10:
                print("GooooooooooooooodJob! Here's your flag:")
                print(os.environ.get("FLAG"))
        else:
            print("You failed to attend the party...")
            break

        print("===================================") 

    
        
    
if __name__=="__main__":
    main()
