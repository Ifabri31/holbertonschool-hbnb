// EXTRACT THE ID FROM THE URL
let placeId;
try {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams) {
        placeId = urlParams.get('place_id');
    } else {
        console.error(`The place ID not found`);
    }
} catch (error) {
    console.error(`Error to try extract the placeID from the URL: ${error}`);
};

// CHECK AUTHENTICATION
function checkAuthentication() {
    const token = localStorage.getItem('token');
    const userName = localStorage.getItem('username');
    const logoutLink = document.getElementById('logout-link');

    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        addReviewSection.style.display = 'none';
        logoutLink.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        logoutLink.style.display = 'inlink';
        logoutLink.innerText = `Log Out (${userName})`
        fetchPlaceDetails(token, placeId)
    }
};

// LOGOUT BUTTON
const logOut = document.getElementById('logout-link')
logOut.addEventListener('click', (event) => {
    event.preventDefault();

    localStorage.clear()
    window.location.href = 'login.html';
})

// GET PLACE BY ID
async function fetchPlaceDetails(token, placeID) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeID}`, {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error(`Error displaying the place details: ${response.statusText}`);
        }
    } catch (error) {
        console.error(`Error fetching the palce: ${error}`);
    }
};

// SHOW THE PLACE DETAILS WITH THE NEXT FORMAT:
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    placeDetails.innerHTML = '';

    const placeArt = document.createElement('article');
    placeArt.classList.add('place-info');

    let reviewsHTML = '<h4 class="place-review">REVIEWS</h4><br>';

    if (place.reviews && place.reviews.length > 0) {
        reviewsHTML += '<dl class="review-block">';
        place.reviews.forEach(review => {
            reviewsHTML += `
                <dt>${review.first_name} ${review.last_name}</dt>
                <dt>${review.rating}</dt>
                <dt>${review.comment}</dt>
            `;
        });
        reviewsHTML += '</dl>';
    } else {
        reviewsHTML += '<p>No reviews yet.</p>';
    }

    placeArt.innerHTML = `
        <h3 class="place-title">${place.title}</h3>
        ${place.description ? `<p class="place-parg">Description: ${place.description}</p>` : ''}
        <p class="place-parg">Owner: ${place.owner.first_name} ${place.owner.last_name}</p>
        <p class="place-parg">Price per night: $${place.price}</p>
        <p class="place-parg">Location: X${place.longitude} Y${place.latitude}</p>
        <p class="place-parg">Amenities: ${place.amenities}</p>
        <br>
        ${reviewsHTML}
    `;

    placeDetails.appendChild(placeArt);
};

// SUBMIT A REVIEW
const reviewForm = document.getElementById('review-form');

if (reviewForm) {
    reviewForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const token = localStorage.getItem('token');
        const comment = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;

        /*await */submitReview(token, comment, rating, placeId);
    });
}

async function submitReview(token, comment, rating, placeId) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ comment, rating, place_id: placeId })
        });

        if (response.ok) {
            alert('Review submitted successfully!');
        } else {
            alert('Failed to submit review');
        }
    } catch (error) {
        console.error(`Failed to fetch function: ${error}`);
    };
};

// FONDOS ALTERNOS
const backgrounds = [
    "images/aldea.png",
    "images/arbol_ancestral.png",
    "images/campo_fantasia.png",
    "images/castillo.png",
    "images/city.png",
    "images/molino.png"
];

const randomImage = backgrounds[Math.floor(Math.random() * backgrounds.length)];


document.body.style.backgroundImage = `url('${randomImage}')`;
document.body.style.backgroundSize = "cover";
document.body.style.backgroundPosition = "center";

checkAuthentication();
