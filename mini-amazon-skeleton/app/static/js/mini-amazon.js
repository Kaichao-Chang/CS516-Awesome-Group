function renderRating(stars, n) {
    const starClassActive = "rating-star fas fa-star";
    const starClassUnactive = "rating-star far fa-star";
    const starsLength = stars.length;

    var i = 0;
    for (i; i < n; i++) stars[i].className = starClassActive;
    for (i; i < starsLength; i++) stars[i].className = starClassUnactive;
 }

function hid_component(component_id) {
    var x = document.getElementById(component_id);
    x.style.display = "none";
}

function show_component(component_id) {
    var x = document.getElementById(component_id);
    if (x.style.display == "none"){
        x.style.display = "block";
    }
}

function change_value(component_id, value) {
    var x = document.getElementById(component_id);
    x.value = value;
}

function click_edit_review() {
    show_component('review-editor'); 
    hid_component('edit-button');
    change_value('review-type', "update")
}
