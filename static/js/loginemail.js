function setCookie(name, value, days) {
    var expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000); // 2 days in milliseconds
    document.cookie = name + "=" + value + "; expires=" + expires.toUTCString() + "; path=/";
}



let cookie = document.cookie
let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
window.onload = function () {
    document.getElementById("hided_section").style.display = "none";
    document.getElementById("error-email").style.display = "none";
    // console.log("lll");


    document.getElementById("check_email").addEventListener("click", function (e) {

        fetch("http://127.0.0.1:8000/member/check_email/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({"email": document.getElementById("emaill").value})
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

    document.getElementById("check_code").addEventListener("click", function (event) {
        event.preventDefault()
        debugger
        fetch("http://127.0.0.1:8000/member/check_code/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                "code": document.getElementById("code").value,
                "email": document.getElementById("emaill").value
            })
        })


            .then(response => {
                if (response.status === 200) {

                    return response.json(); // Parse the response body as JSON
                } else {
                    throw new Error('Error fetching data'); // Handle other status codes
                }
            })
            .then(data => {
                console.log(data.token);
                setCookie("jwt", data.token, 2)
                window.location.href = 'http://127.0.0.1:8000/'
            })
            .catch(error => {
                console.error('Error:', error);
                alert("somthing went wrong please try again")

            });
    });//end lessener


}//end load













