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

  //loading a chat after clicking the name
  function loadChat(str) {
    if (str.length == 0) {
      document.getElementById("chat_content").innerHTML = "";
      return;
    } else {
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("chat_content").innerHTML = this.responseText;
          
        }
      };
      xmlhttp.open("GET", "/loadingChat?userName2=" + str, true);
      xmlhttp.send();

    }
  }

  //sending a message
    //sending a message after clicking the button
    function sendMessage() {
      str=document.getElementById("input").value //the content of the input
      alert(str);//show the content
      if (str.length == 0) {
        return;
      } else {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            if(this.responseText)
              alert(this.responseText)
          }
        };
        //get the current time
        var currentdate = new Date();          var mm,dd,hh,minute,ss;
        if(currentdate.getMonth()+1<10)  mm="0"+(currentdate.getMonth()+1);//add the zero
        else mm=currentdate.getMonth()+1;
        if(currentdate.getDate()<10)  dd="0"+(currentdate.getDate());//add the zero
        else dd=currentdate.getDate();
        if(currentdate.getHours()<10)  hh="0"+(currentdate.getHours());//add the zero          else hh=currentdate.getHours();
        if(currentdate.getMinutes()<10)  minute="0"+(currentdate.getMinutes());//add the zero
        else minute=currentdate.getMinutes();
        if(currentdate.getSeconds()<10)  ss="0"+(currentdate.getSeconds());//add the zero
        else ss=currentdate.getSeconds();
        var time_string = currentdate.getFullYear()+"-"                    +mm+"-"  
                  +dd + " "
                  + hh + ":"  
                  + minute + ":" 
                  + ss ;
        xmlhttp.open("GET", "/sendMessage?content=" + str+"&time="+time_string, true);
        xmlhttp.send();
    }
  }