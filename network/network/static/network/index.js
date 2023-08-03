document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            like_unlike(event.target.id)
        })
    })
    document.querySelectorAll(".edit_btn").forEach(btn => {
        btn.addEventListener("click", () => {
            edit_post(event.target.id);
            event.preventDefault();
        })
    })
})

function like_unlike(post_id) {
    if (document.querySelector(`#${post_id}`).innerHTML.slice(2) === "Like") {
        post_id = Number(post_id.slice(5));
        context = {
            method: "PUT",
            body: JSON.stringify({
                action: "like",
                post_id: post_id
            })
        }
    }
    else {
        post_id = Number(post_id.slice(5));
        context = {
            method: "PUT",
            body: JSON.stringify({
                action: "unlike",
                post_id: post_id
            })
        }
    }
    fetch("/react", context)
    .then(response => {
        if (response.status === 400) {
            window.location = "/";
        }
        else if (response.status === 401) {
            alert("You must be logged in to like/unlike posts!");
            window.location = "/login";
        }
        else {
            return response.json();
        }
    })
    .then(data => {
        let like_bar = document.querySelector(`#num-likes-${post_id}`);
        let like_btn = document.querySelector(`#like-${post_id}`);
        like_bar.innerHTML = `${data.likes} likes`;
        if (data.message === "liked") {
            like_btn.style.color = "red";
            like_btn.innerHTML = "♥ Liked";
        }
        else if (data.message === "unliked") {
            like_btn.style.color = "white";
            like_btn.innerHTML = "♥ Like";
        }
    })
}

function edit_post(post_id) {
    post_id = Number(post_id.slice(5));
    let main = document.querySelector(`#content-${post_id}`);
    let text = main.innerHTML;
    let form = document.createElement("form");
    form.setAttribute("id", `edit-form-${post_id}`);
    let txtarea = document.createElement("div");
    txtarea.setAttribute("class", "form-group");
    let t2 = document.createElement("textarea");
    t2.setAttribute("class", "form-control");
    t2.setAttribute("id", `edited-stuff-${post_id}`);
    t2.setAttribute("name", "edited");
    t2.setAttribute("required", "");
    t2.setAttribute("rows", "5");
    t2.textContent = text;
    txtarea.appendChild(t2);
    form.appendChild(txtarea);
    let btn = document.createElement("div");
    btn.setAttribute("class", "form-group");
    let b2 = document.createElement("button");
    b2.setAttribute("class", "btn btn-primary");
    b2.setAttribute("type", "submit");
    b2.textContent = "Edit";
    btn.appendChild(b2);
    form.appendChild(btn);
    main.innerHTML = "";
    main.appendChild(form);
    b2.addEventListener("click", () => {
        event.preventDefault();
        let content = document.querySelector(`#edited-stuff-${post_id}`).value;
        if (content === "") {
            alert("The post must have some content");
        } 
        else {
            send_data(content, post_id);
        }
    });
}

function send_data(data, post_id) {
    fetch("/edit", {
        method: "PUT",
        body: JSON.stringify({
            edited_data: data,
            post_id: post_id
        })
    }).then(response => {
        if (response.status === 400) {
            window.location = "/";
        }
        else if (response.status === 401) {
            alert("You must be logged in to like/unlike posts!");
            window.location = "/login";
        }
        else if (response.status === 403) {
            alert("You cannot edit someone else's post");
        }
        else {
            return response.json();
        }
    })
    .then(document.querySelector(`#content-${post_id}`).innerHTML = data)
}