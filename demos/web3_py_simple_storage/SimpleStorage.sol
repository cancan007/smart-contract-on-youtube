//SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

// If your account is related to this, your metamask pops up every time you edit with yellow buttons

contract SimpleStorage {
    //this will get initialized to 0
    uint256 favoriteNumber; //uint: 符号なしなので、マイナスの値は入れられない, 256bitsまで表現
    //public: You can see the value with blue button
    bool favoriteBool;
    bool favoriteBool2;

    // this list related to other values for each other
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber; //this is to implement dictionary func

    //People public person = People({favoriteNumber:2, name: "Patrick"});

    function store(uint256 _favoriteNumber) public {
        //privateにすると、引数を代入できなくなる
        favoriteNumber = _favoriteNumber;
    }

    //view: just for reading the value(blue buttons)
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    // Add a person in Array
    // memory: the value is stored during this execution,  storage: the value is stored even after execution
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    function retrieve2(uint256 favoriteNumber) public pure {
        favoriteNumber + favoriteNumber;
    }

    /*
    bool favoriteBool = true;
    string favoriteString = "String";
    int256 favoriteInt = -5;
    address favoriteAddress = 0xcfc443e8602D14Ba48541e0B3BBb3D4D4B8aC747;
    bytes32 favoriteByte = "cat";
    */
}
