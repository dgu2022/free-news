let spanOption = document.querySelectorAll(".sign span");

spanOption.forEach(function (span) {
    span.addEventListener("click", function (e) {
        
        //Remove class active
        e.target.parentElement.querySelectorAll(".active").forEach(function (element) {
            element.classList.remove("active");
        });
        //Add class active
        e.target.classList.add("active");
      
       if (e.target.classList.contains("sign-in")) {
         
        document.querySelectorAll(".sign-in-up form").forEach(function (element) {
            element.classList.remove("active");
        });
         
        document.querySelector(".sign-in-form").classList.add("active");
        
       } else {
         
        document.querySelectorAll(".sign-in-up form").forEach(function (element) {
            element.classList.remove("active");
        });
         
        document.querySelector(".sign-up-form").classList.add("active");
       }
    })
})