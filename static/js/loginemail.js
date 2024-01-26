let cookie = document.cookie
let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
window.onload = function() {
    document.getElementById("hided_section").style.display = "none";


document.getElementById("check_email").addEventListener("click", function() {
<<<<<<< Updated upstream
    // document.getElementById("check_email").style.display = "none";
    event.preventDefault();

    $.ajax({
    type: "POST",


    url: `/member/check_email/`,
         headers: {
           'X-CSRFToken': csrfToken
         },
    data: { "email": $("#emaill").val() },
    success: function(data) {
        if (data === "true") {
            document.getElementById("hided_section").style.display = "block";
    document.getElementById("check_email").style.display = "none";
        }
    }//end success post
});//end ajax

}, { passive: false });//end lessener








=======
     document.getElementById("hided_section").style.display = "block";
    document.getElementById("check_email").style.display = "none";
    // document.getElementById("check_email").style.display = "none";
    // event.preventDefault();
    //
    // $.ajax({
    // type: "POST",
    // url: `/member/check_email/`,
    // data: { "email": $("#emaill").val() },
    // success: function(data) {
    //     if (data === "true") {
    //         document.getElementById("hided_section").style.display = "block";
    // document.getElementById("check_email").style.display = "none";
    //     }
    // }
// });

});
// , { passive: false });
>>>>>>> Stashed changes

};//end load