
let cookie = document.cookie
let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
window.onload = function() {
    document.getElementById("hided_section").style.display = "none";
    document.getElementById("error-email").style.display = "none";
  // console.log("lll");


document.getElementById("check_email").addEventListener("click", function(e) {

    fetch("http://127.0.0.1:8000/member/check_email/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ "email": document.getElementById("emaill").value })
    }).then(response => {
        if (response.status == 200) {
            document.getElementById("hided_section").style.display = "block";
            document.getElementById("check_email").style.display = "none";
            console.log(response.status);

        } else {
            document.getElementById("error-email").style.display = "block";
        }
    });
});

document.getElementById("check_code").addEventListener("click", function(event) {
        event.preventDefault()
    fetch("http://127.0.0.1:8000/member/check_code/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ "code": document.getElementById("code").value ,"email": document.getElementById("emaill").value })
    }).then(response => {
        if (response.status == 200) {
            console.log(response.status);
            window.location.href ="http://127.0.0.1:8000/home/"


        } else {
            alert("your code is not correct\n wait 2 minute for refresh page and try again")
            document.getElementById("check_code").display=none;
            setTimeout(function () {
                location.reload();
            }, 120000);
        }
    });
    }


);//end lessener







}//end load













