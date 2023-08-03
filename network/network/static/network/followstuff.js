document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#follow-btn").addEventListener("click", followstuff);
    user = document.querySelector("#user_id").innerHTML;
})

function followstuff() {
    let action = "a";
    let follow_btn = document.querySelector("#follow-btn");
    if (follow_btn.innerHTML === "Follow") {
        action = "follow";
    }
    else {
        action = "unfollow";
    }

    fetch("/followstuff", {
        method: "PUT",
        body: JSON.stringify({
            action: action,
            followee: user,
        })
    })
    .then(response => {
        console.log(response);
        if (response.status === 400) {
            window.location = "/";
        }
        else if (response.status === 401) {
            alert("You must be logged in to follow/unfollow a user!");
            window.location = "/login";
        }
        else {
            return response.json();
        }
    })
    .then(data => {
        let num_followers = data.num_followers;
        let num_followings = data.num_followings;
        document.querySelector("#num_followers").innerHTML = `${num_followers}<br>Followers`;
        document.querySelector("#num_followings").innerHTML = `${num_followings}<br>Following`;
        if (data.message === "following") {
            follow_btn.innerHTML = "Unfollow";
            follow_btn.className = "unfollow-btn";
        }
        else {
            follow_btn.innerHTML = "Follow";
            follow_btn.className = "follow-btn";
        }
    })
}