// CHECK AUTHENTICATION
function checkAuthentication() {
    const token = localStorage.getItem('token');
    const userName = localStorage.getItem('username');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (token) {
        fetchPlaces(token);
        loginLink.style.display = 'none';
        logoutLink.style.display = 'inlink';
        logoutLink.innerText = `Log Out (${userName})`
    } else {
        loginLink.style.display = 'inlink';
        logoutLink.style.display = 'none';
        window.location.href = 'login.html';
    }
};

// LOGOUT BUTTON
const logOut = document.getElementById('logout-link')
logOut.addEventListener('click', (event) => {
    event.preventDefault();

    localStorage.clear()
    window.location.href = 'login.html';
});

// GET ALL PLACES
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {

            method: 'GET',
            mode: "cors",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayPlaces(data);
        } else {
            console.error(`Error displaying the places; ${response.statusText}`);
        }
    } catch (error) {
        console.error(`Error fetching the places: ${error}`);
    }
};

// SHOW THE PLACES WITH THE NEXT FORMAT:
function displayPlaces(places) {
    const placeList = document.getElementById('places-list');
    placeList.innerHTML = '';

    places.forEach(place => {
        const placeArt = document.createElement('article');
        placeArt.setAttribute('data-place-price', place.price);
        placeArt.classList.add('place-card');
        placeArt.innerHTML = `
            <h2 class="place-title"><strong>${place.title}</strong></h2>
            <br>
            <p class="place-parg"><strong>Price per night: $${place.price}</strong></p>
            <p class="place-parg"><strong>Location: X:${place.longitude} Y:${place.latitude}</strong></p>
            <br>
            <button class="details-button" data-place-id="${place.id}">View Details</button>
        `;
        placeList.appendChild(placeArt);    

        // GO TO DETAILLS PAGE BUTTON #todo: cuidado, capas que explota
        placeList.addEventListener('click', (event) => {
            try {
                if (event.target.classList.contains('details-button')) {
                    const placeId = event.target.getAttribute('data-place-id');
                    window.location.href = `place.html?place_id=${placeId}`;
                }
            } catch (error) {
                console.error('No se puede');
            }
        });
    });
};

// PRICE FILTER DROPDOWN BUTTON
document.getElementById('price-filter').addEventListener('change', (event) => {
    event.preventDefault();

    const places_list = document.getElementById('places-list');
    const places = places_list.querySelectorAll('.place-card');

    places.forEach(place => {
        
        const price = parseFloat(place.getAttribute('data-place-price'));

        if (event.target.value === 'All' || price <= parseFloat(event.target.value)) {
            console.log()
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
});

// FONDOS ALTERNOS
const backgrounds = [
    "images/backgraunds/aldea.png",
    "images/backgraunds/arbol_ancestral.png",
    "images/backgraunds/atlantis.png",
    "images/backgraunds/campo_fantasia.png",
    "images/backgraunds/castillo.png",
    "images/backgraunds/city.png",
    "images/backgraunds/ciudad_fantasia.png",
    "images/backgraunds/cyber_city.png",
    "images/backgraunds/japon_pueblo.jpg",
    "images/backgraunds/japon_pueblo2.png",
    "images/backgraunds/laguito.png",
    "images/backgraunds/lluvia.png",
    "images/backgraunds/molino.png",
    "images/backgraunds/punkmodern.png",
    "images/backgraunds/work_ofice.png"
];

const randomImage = backgrounds[Math.floor(Math.random() * backgrounds.length)];


document.body.style.backgroundImage = `url('${randomImage}')`;
document.body.style.backgroundSize = "cover";
document.body.style.backgroundPosition = "center";

checkAuthentication();
