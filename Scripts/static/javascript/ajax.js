function checkUserName(str) {
    if (str.length == 0) {
      document.getElementById("check_userName_message").innerHTML = "";
      return;
    } else {
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("check_userName_message").innerHTML = this.responseText;
          
        }
      };
      xmlhttp.open("GET", "/checkUserName?userName=" + str, true);
      xmlhttp.send();

    }
  }
  //search user
  function searchUserName(str) {
    if (str.length == 0) {
      document.getElementById("searchResult").innerHTML = "";
      return;
    } else {
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("searchResult").innerHTML = this.responseText;
          
        }
      };
      xmlhttp.open("GET", "/searchUserName?userName=" + str, true);
      xmlhttp.send();

    }
  }