let cookie = document.cookie
let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
window.onload = function() {
    document.getElementById("hided_section").style.display = "none";
    document.getElementById("error-email").style.display = "none";
  // console.log("lll");


document.getElementById("check_email").addEventListener("click", function(e) {



//     $.ajax({
//     type: "POST",
//
//
//     url: `/member/check_email/`,
//          headers: {
//            'X-CSRFToken': csrfToken
//          },
//     data: { "email": $("#emaill").val() },
//     success: function(data) {
//         if (data === "true") {
//             document.getElementById("hided_section").style.display = "block";
//     document.getElementById("check_email").style.display = "none";
//         }
//     }//end success post
// });//end ajax
//     console.log("hereeee")
//






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
}


);//end lessener







};//end load












