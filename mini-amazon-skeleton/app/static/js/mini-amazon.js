function renderRating(stars, n) {
    const starClassActive = "rating-star fas fa-star";
    const starClassUnactive = "rating-star far fa-star";
    const starsLength = stars.length;

    var i = 0;
    for (i; i < n; i++) stars[i].className = starClassActive;
    for (i; i < starsLength; i++) stars[i].className = starClassUnactive;
 }