pragma solidity ^0.8.12;

contract MyContract {
    struct Scheme {
        uint id;
        string title;
        string totalAmount;
        string totalCount;
        string description;
        string photoPath;
        string status;
        uint catid;
    }

    Scheme[] public schemes;

    function addScheme(uint _id, string memory _title, string memory _totalAmount, string memory _totalCount, string memory _description, string memory _photoPath, string memory _status, uint _catid) public {
        schemes.push(Scheme(_id, _title, _totalAmount, _totalCount, _description, _photoPath, _status, _catid));
    }

    function getSchemeCount() public view returns (uint) {
        return schemes.length;
    }

    function getScheme(uint _index) public view returns (uint, string memory, string memory, string memory, string memory, string memory, string memory, uint) {
        require(_index < schemes.length, "Index out of bounds");
        Scheme memory scheme = schemes[_index];
        return (scheme.id, scheme.title, scheme.totalAmount, scheme.totalCount, scheme.description, scheme.photoPath, scheme.status, scheme.catid);
    }

    // SchemeRequest Starts Here
    struct SchemeRequest {
        uint id;
        string date;
        string userid;
        string purpose;
        string idPath;
        uint schemeid;
    }

    SchemeRequest[] public request;

    function addSchemeRequest(uint _id, string memory _date, string memory _userid, string memory _purpose, string memory _idPath, uint _schemeid) public {
        request.push(SchemeRequest(_id, _date, _userid, _purpose, _idPath, _schemeid));
    }

    function getSchemeRequestCount() public view returns (uint) {
        return request.length;
    }

    function getSchemeRequest(uint _index) public view returns (uint, string memory, string memory, string memory, string memory, uint) {
        require(_index < request.length, "Index out of bounds");
        SchemeRequest memory req = request[_index];
        return (req.id, req.date, req.userid, req.purpose, req.idPath, req.schemeid);
    }
    // SchemeRequest Ends Here


    function transferEther(address payable _recipient, uint _amount) external {
        require(address(this).balance >= _amount, "Insufficient balance in the contract");
        _recipient.transfer(_amount);
    }
    //transfer ends here

    fallback() external payable {
        // Optional: Perform any additional logic here
    }
}
