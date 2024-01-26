window.onload = function() {
    document.getElementById("hided_section").style.display = "none";


document.getElementById("check_email").addEventListener("click", function() {
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

};