let projectsURL = "http://localhost:8000/api/projects/";

let loginBtn = document.getElementById("login-btn");
let logoutBtn = document.getElementById("logout-btn");

let token = localStorage.getItem("token");


if (token) {
  loginBtn.remove();
} else {
  logoutBtn.remove();
}
loginBtn.addEventListener('click', ()=>{
  window.location = "file:///home/ubaydulloh/Desktop/Frontend(Other%20Server)/login.html"
})
logoutBtn.addEventListener('click', ()=>{
  localStorage.removeItem("token")
})


let getProjects = () => {
  fetch(projectsURL)
    .then((response) => response.json())
    .then((data) => {
      buildProjects(data);
    });
};


let buildProjects = (projects) => {
  let projectsWrapper = document.getElementById("projects-wrapper");
  projectsWrapper.innerHTML = "";
  for (let i = 0; i < projects.length; i++) {
    let project = projects[i];

    let project__div = `
        <div class="columns box my-4">
          
        <div class="column is-4 image is-flex is-align-items-center">
            <img src="http://localhost:8000${
              project.featured_img
            }" alt="image" />
          </div>
          
          <div class="column">  
          <h1 class="title has-text-info is-4">${project.title}</h1>
            <p class="has-text-info"><i>by ${project.owner.name}</i></p><br/>
            <p class="content is-6">${project.description.slice(0, 200)}...</p>
            <p class="has-text-${
              project.vote_ratio >= 60 ? "success" : "danger"
            }">${project.vote_ratio}% positive of ${project.vote_total} vote${
      project.vote_total == 1 ? "" : "s"
    }</p><br>            
            <div>
              <span class="button button-vote mx-4" data-vote="up" data-project="${
                project.id
              }">👍</span>
              <span class="button button-vote" data-vote="down" data-project="${
                project.id
              }">👎</span>
            </div>
            <div class="is-flex is-justify-content-end"><small>
            ${project.created.slice(11, 13)}:${project.created.slice(14, 16)}
            ${project.created.slice(8, 10)}/${project.created.slice(
      5,
      7
    )}/${project.created.slice(0, 4)}
            </small></div>
          </div>
        </div>
      `;
    projectsWrapper.innerHTML += project__div;
  }

  let projectAddVote = () => {
    let voteButtons = document.getElementsByClassName("button-vote");

    for (let i = 0; i < voteButtons.length; i++) {

      voteButtons[i].addEventListener("click", (e) => {
        let vote = e.target.dataset.vote;
        let project = e.target.dataset.project;
        let token = localStorage.getItem("token");

        if (token) {
          voteButtons[i].classList.toggle("is-success")
          fetch(`http://localhost:8000/api/projects/${project}/vote/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ value: vote }),
        })
          .then((response) => response.json())
          .then((data) => {
            getProjects()
          });
        }else{
          alert("You are not authorisized! Please Login.")
        }
      });
    }
  };

  projectAddVote();
};


getProjects();
