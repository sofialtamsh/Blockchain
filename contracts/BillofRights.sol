// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BillOfRights {
    struct Right {
        string name;
        address holder;
        bool isActive;
        uint256 startTime;
        uint256 endTime;
    }

    mapping(uint256 => Right) public rights;
    uint256 public rightCount;

    event RightAssigned(uint256 indexed rightId, address indexed holder);
    event RightRevoked(uint256 indexed rightId);
    event RightTransferred(uint256 indexed rightId, address indexed newHolder);

    function assignRight(address _holder, string memory _name, uint256 _duration) public returns (uint256) {
        rightCount++;
        uint256 rightId = rightCount;
        rights[rightId] = Right({
            name: _name,
            holder: _holder,
            isActive: true,
            startTime: block.timestamp,
            endTime: block.timestamp + _duration
        });

        emit RightAssigned(rightId, _holder);
        return rightId;
    }

    function revokeRight(uint256 _rightId) public {
        require(rights[_rightId].isActive, "Right is not active");
        rights[_rightId].isActive = false;
        emit RightRevoked(_rightId);
    }

    function transferRight(uint256 _rightId, address _newHolder) public {
        require(rights[_rightId].isActive, "Right is not active");
        require(rights[_rightId].holder == msg.sender, "Only the current holder can transfer the right");
        
        rights[_rightId].holder = _newHolder;
        emit RightTransferred(_rightId, _newHolder);
    }

    function getRightDetails(uint256 _rightId) public view returns (Right memory) {
        return rights[_rightId];
    }
}
