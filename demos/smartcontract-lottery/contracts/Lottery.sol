// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol"; // it didn't work, it returns "VirtualMachineError: revert: Ownable: caller is not the owner"
//import "@openzeppelin/contracts-ethereum-package/contracts/ownership/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

//AggregatorV3Interface: tool to get various priceFeeds

// inherit OwnableUpgradeSafe instead Ownable
contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    uint256 public usdEntryFee;
    address payable public recentWinner;
    uint256 public randomness;
    AggregatorV3Interface internal ethUsdPriceFeed;

    // enmu: to represent statement, OPEN:0, CLOSE:1, CALCULATING_WINNER:2
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyHash; // to identifier the vrf node to get random number
    event RequestedRandomness(bytes32 requestId); // to store the information of the event

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        // include the constructor of inherited one
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED; //1
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        //$50 minimum
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        players.push(payable(msg.sender)); //if you use above 0.8.0 ver, you have to add payable
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // this price has already 8 decimals(https://docs.chain.link/docs/ethereum-addresses/), so I added 10 decimals to make it 18
        // $50, $4000/ETH
        // so what I want is 50/4000, but decimals doesn't work in solidity
        // so I have to add big number: 50 * 100000 / 4000
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice; // you have to add additional 18decimals to make the answer outputted with 18 decimals(in solidity, basis is 18deci)
        return costToEnter;
    }

    // this function can be handled by only admin. So I added "onlyOwner"
    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery state yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        // to express randomness, it's so hard to express it on decentralized network
        // keccak256: hashing algorhithm
        /*
        uint256(
            keccak256(
                abi.encodePacked(
                    nonce, // nonce is predictable (aka, transaction number)
                    msg.sender, // msg.sender is predictable
                    block.difficulty, // can actually be manipulated by the miners!
                    block.timestamp // timestamp is predictable
                )
            )
        ) % players.length;
        */
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee); // request to node, and node responds with "fulfillRandomness" function

        emit RequestedRandomness(requestId); // show the information of the event
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You aren't there yet!"
        );
        require(_randomness > 0, "random-not-found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance); // transfering all currencies collected from players to winner
        // Reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;

        // Example:
        // 7 players
        // random_number = 22
        // 22 % 7 = 1
    }
}
