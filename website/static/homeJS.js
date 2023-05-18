function myFunction() {
    var dots = document.getElementById("dots");
    var moreText = document.getElementById("more");
    var btnText = document.getElementById("myBtn");

    if (moreText.style.display === "inline") {
        moreText.style.display = "none";
        btnText.innerHTML = "Show more";
    } else {
        moreText.style.display = "inline";
        btnText.innerHTML = "Show less";
    }
}