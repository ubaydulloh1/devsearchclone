let form = document.getElementById("login--form");


let loginForm = ()=>{
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        console.log("Form Submitted!");
      
        if(e.target.username.value){
          fetch("http://localhost:8000/api/users/token/", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                username: e.target.username.value,
                password: e.target.password.value,
              }),
            })
              .then((response) => response.json())
              .then((data) => {
                if(data.access){
                    let token = data.access
                    localStorage.setItem("token", token)
                    window.location = "file:///home/ubaydulloh/Desktop/Frontend(Other%20Server)/projects_list.html"
                }
              });
        }else{
            alert("Form is not valid!")
        }
      });
      
}

loginForm()