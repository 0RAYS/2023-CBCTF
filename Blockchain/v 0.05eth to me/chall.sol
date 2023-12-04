// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

contract challenge {

    mapping (uint8 => uint8) private ROT13_MAP;
    address immutable receiver = 0xe24C5c44a7c4E75d5E2e461C35d863db0385E3c9;

    constructor() {

        for (uint8 i = 65; i <= 90; i++) {
            uint8 newChar = i + 13;
            if (newChar > 90) {
                newChar -= 26;
            }
            ROT13_MAP[i] = newChar;
        }

        for (uint8 i = 97; i <= 122; i++) {
            uint8 newChar = i + 13;
            if (newChar > 122) {
                newChar -= 26;
            }
            ROT13_MAP[i] = newChar;
        }
    }

    function encodeROT13(bytes memory _input) internal view returns (string memory) {
        bytes memory inputBytes = bytes(_input);
        bytes memory outputBytes = new bytes(inputBytes.length);

        for (uint256 i = 0; i < inputBytes.length; i++) {
            uint8 char = uint8(inputBytes[i]);
            uint8 newChar = ROT13_MAP[char];
            if (newChar == 0) {
                newChar = char;
            }
            outputBytes[i] = bytes1(newChar);
        }

        return string(outputBytes);
    }

    function getFlag() external payable returns (string memory) {
        require(msg.value >= 0.05 ether, "According to our agreement, you need to pay 0.05 eth in exchange for FLAG");
        bytes memory NEFh = bytes("POPGS");
        bytes memory bKhQ = bytes("Gu4Axf_s0e_he_Rgu&&Rawblvat_PGS!");
        bytes memory FLAG = abi.encodePacked(encodeROT13(NEFh), "{", encodeROT13(bKhQ), "}");
        payable(receiver).transfer(address(this).balance);
        return string(FLAG);
    }
}