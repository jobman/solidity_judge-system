// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

contract Solomon {
    struct Deal {
        bytes32 id;
        address customer;
        address implementor;
        uint256 value;
        uint256 implementorResponsibility;
        uint256 expirationDate;
        bool implementorPayed;
    }

    address public judgeSystem;
    uint256 public minimalDeal;
    uint256 public judgeRewardPart;

    constructor() public {
        judgeSystem = msg.sender;
        minimalDeal = 0.01 ether;
        judgeRewardPart = 200;
    }

    uint256 private developmentFound;
    uint256 private judgeFound;

    mapping(bytes32 => Deal) public currentDeals;

    function makeContract(
        bytes32 id,
        address implementor,
        uint256 implementorResponsibility,
        uint256 expirationDate,
        uint256 value,
        uint256 fee
    ) public payable {
        require(msg.value >= minimalDeal);
        require(msg.value == (value + fee));
        require(fee >= (value / 100));
        developmentFound += fee / 2;
        judgeFound += fee / 2;
        bool implementorPayed;
        currentDeals[id] = Deal(
            id,
            msg.sender,
            implementor,
            msg.value - fee,
            implementorResponsibility,
            expirationDate,
            implementorPayed = false
        );
    }

    function approveContract(bytes32 id) public {
        require(
            msg.sender == currentDeals[id].customer || msg.sender == judgeSystem
        );
        if (currentDeals[id].implementorPayed) {
            payable(currentDeals[id].implementor).transfer(
                currentDeals[id].implementorResponsibility +
                    currentDeals[id].value
            );
        } else {
            payable(currentDeals[id].implementor).transfer(
                currentDeals[id].value
            );
        }

        delete currentDeals[id];
    }

    function payResponsibility(bytes32 id) public payable {
        require(msg.sender == currentDeals[id].implementor);
        require(currentDeals[id].implementorResponsibility != 0);
        require(currentDeals[id].implementorPayed == false);
        require(currentDeals[id].implementorResponsibility == msg.value);
        currentDeals[id].implementorPayed = true;
    }

    function giveUpContract(bytes32 id) public {
        require(msg.sender == currentDeals[id].implementor);
        payable(currentDeals[id].customer).transfer(currentDeals[id].value);
        if (currentDeals[id].implementorPayed) {
            payable(currentDeals[id].customer).transfer(
                currentDeals[id].implementorResponsibility
            );
        }
        delete currentDeals[id];
    }

    function judgeContract(
        bytes32 id,
        bool isImplementorFail,
        address[] memory judges
    ) public {
        require(msg.sender == judgeSystem);

        if (isImplementorFail && currentDeals[id].implementorPayed) {
            payable(currentDeals[id].customer).transfer(
                currentDeals[id].implementorResponsibility +
                    currentDeals[id].value
            );
        } else if (isImplementorFail && !currentDeals[id].implementorPayed) {
            payable(currentDeals[id].customer).transfer(currentDeals[id].value);
        } else if (!isImplementorFail && currentDeals[id].implementorPayed) {
            payable(currentDeals[id].implementor).transfer(
                currentDeals[id].implementorResponsibility +
                    currentDeals[id].value
            );
        } else {
            payable(currentDeals[id].implementor).transfer(
                currentDeals[id].value
            );
        }
        delete currentDeals[id];

        uint256 reward = judgeFound / judgeRewardPart;
        for (uint256 i = 0; i < judges.length; i++) {
            payable(judges[i]).transfer(reward);
            judgeFound -= reward;
        }
    }

    function systemFailureWithdrawFunds(bytes32 id) public {
        require(msg.sender == currentDeals[id].customer);
        require(block.timestamp > currentDeals[id].expirationDate);
        payable(currentDeals[id].customer).transfer(currentDeals[id].value);
        if (currentDeals[id].implementorPayed) {
            payable(currentDeals[id].implementor).transfer(
                currentDeals[id].implementorResponsibility
            );
        }
        delete currentDeals[id];
    }

    function terminateSystem(address[] memory judges) public {
        require(msg.sender == judgeSystem);
        require(judges.length >= 1);
        payable(judgeSystem).transfer(developmentFound);
        developmentFound = 0;
        uint256 reward = judgeFound / 200;
        for (uint256 i = 0; i < judges.length - 1; i++) {
            payable(judges[i]).transfer(reward);
            judgeFound -= reward;
        }
        payable(judges[judges.length - 1]).transfer(judgeFound);
        judgeFound = 0;
    }

    function changeMinimalDeal(uint256 minDeal) public {
        require(msg.sender == judgeSystem);
        minimalDeal = minDeal;
    }

    function changeJudgeRewardPart(uint256 part) public {
        require(msg.sender == judgeSystem);
        judgeRewardPart = part;
    }
}
