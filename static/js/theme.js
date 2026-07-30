const themeToggle = document.getElementById("theme-toggle");

if(themeToggle){

    if(localStorage.getItem("theme") === "dark"){

        document.body.classList.add("dark-mode");

        themeToggle.innerHTML = "☀️";

    }

    themeToggle.addEventListener("click",function(){

        document.body.classList.toggle("dark-mode");

        if(document.body.classList.contains("dark-mode")){

            localStorage.setItem("theme","dark");

            themeToggle.innerHTML="☀️";

        }
        else{

            localStorage.setItem("theme","light");

            themeToggle.innerHTML="🌙";

        }

    });

}