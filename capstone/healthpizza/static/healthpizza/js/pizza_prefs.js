document.addEventListener("DOMContentLoaded", () => {
    // select important html elements
    let next_btn = document.querySelector("#next");
    let consent_form = document.querySelector("#consent-form");
    let submit_btn = document.querySelector("#submit-btn");
    let consent_check = document.querySelector("#consent_check");
    let no_allergs = document.querySelector("#no-allergies");
    let lactose = document.querySelector("#dairy");
    let fish = document.querySelector("#fish");
    let spice = document.querySelector("#spice");
    let diet_pref_veg = document.querySelector("#veg");
    let wait = document.querySelector("#wait");
    let final_submit_btn = document.querySelector("#final-submit-btn");

    // add event listener on the "next" button to show the disclaimer
    next_btn.addEventListener("click", () => {
        consent_form.style.display = "inline-block";
        next_btn.style.display = "none";
        submit_btn.style.display = "inline";

        // add event listener to submit form
        submit_btn.addEventListener("click", () => {
            event.preventDefault();
            // make sure the user has agreed to the terms of the disclaimer
            if (!consent_check.checked) {
                alert("You must agree to the disclaimer T&Cs");
            }
            else {
                let allergies = "";
                let isveg = false;
                if (no_allergs.checked) {
                    allergies = "none";
                }
                else {
                    if (fish.checked) {
                        allergies += "fish ";
                    }
                    if (lactose.checked) {
                        allergies += "dairy ";
                    }
                    if (spice.checked) {
                        allergies += "spice";
                    }
                }
                if (diet_pref_veg.checked) {
                    isveg = true;
                }
                finalise_pizza_prefs(allergies, isveg);
            }
        })
    });

    // add event listeners on the checkboxes for allergies
    no_allergs.addEventListener("click", () => no_allergies(no_allergs, lactose, fish, spice));
    lactose.addEventListener("click", () => yes_allergies(no_allergs, lactose, fish, spice));
    fish.addEventListener("click", () => yes_allergies(no_allergs, lactose, fish, spice));
    spice.addEventListener("click", () => yes_allergies(no_allergs, lactose, fish, spice));

    // add event listeners on the final forms
    wait.addEventListener("click", () => {
        location.reload();
    });
    final_submit_btn.addEventListener("click", () => {
        document.querySelector("#form2").submit();
    })
})


// when the no allergies option is selected, remove checks from the other options
function no_allergies(n, l, f, s) {
    if (n.checked) {
        l.checked = false;
        f.checked = false;
        s.checked = false;
    }
}

// when an allergy option is selected, remove the check from the no allergies option
function yes_allergies(n, l, f, s) {
    if (l.checked || f.checked || s.checked) {
        n.checked = false;
    }
}

// function to show and finalise pizza prefs
function finalise_pizza_prefs(a, i) {
    document.querySelector("#form1").style.display = "none";
    document.querySelector("#final").style.display = "inline"
    document.querySelector("#hr").style.display = "none";
    let form = document.querySelector("#form2");
    form.style.display = "none"
    let text = "";
    if (i) {
        text += "Vegetarian/Vegan<br><br>";
    }
    else {
        text += "No dietary preference(non veg and veg both ok)<br><br>";
    }
    let allergies = a.split(" ");
    if (allergies.includes("fish")) {
        text += "Fish product allergies<br><br>";
    }
    if (allergies.includes("dairy")) {
        text += "Dairy products allergies<br><br>";
    }
    if (allergies.includes("spice")) {
        text += "Not spicy<br><br>"
    }
    document.querySelector("#finalchoices").innerHTML = text;
    document.querySelector("#input-allergies").value = a;
    document.querySelector("#input-isveg").value = i;
}