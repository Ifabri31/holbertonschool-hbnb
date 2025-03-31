document.addEventListener('DOMContentLoaded', () => {

    // LOGIN SECTION
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }

    async function loginUser(email, password) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                document.cookie = `token=${data.access_token}; path=/`;
                window.location.href = 'index.html';
            } else {
                alert(`Login failed: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    }

    // CHECK AUTHENTICATION
    checkAuthentication();

    function checkAuthentication() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');
    
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
            // Fetch places data if the user is authenticated
            fetchPlaces(token);
        }
    }
    function getCookie(name) {
        // Function to get a cookie value by its name
        const cookies = document.cookie.split('; ');
        for (let cookie of cookies) {
            const [cookieName, cookieValue] = cookie.split('=');
            if (cookieName === name) {
                return cookieValue
            }
        }
        return null;
    }

    // GET ALL PLACES
    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
                method: 'GET',
                headers: {
                    'Authorization': `${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                displayPlaces(data);
            } else {
                console.error(`Error fetching places; ${response.statusText}`);
            }
        } catch (error) {
            console.error(`Error fetching places: ${error}`);
        }
    }

    function displayPlaces(places) {
        const placeList = document.getElementById('placed-list').value;
        placeList.innerHTML = '';

        places.array.forEach(place => {
            const placeDiv = document.createElement('div');
            placeDiv.classList.add('place-card');
            placeDiv.innerHTML = `
                <h3 class="place-title">${place.name}</h3>
                <p class="place-parg">Price per night: $${place.price}</p>
                <p class="place-parg">Location: X${place.longitude} Y${place.latitude}</p>
                <button class="details-button">View Details</button>
            `;
            placeList.appendChild(placeDiv);
        });
    }

    // PRICE FILTER DROPDOWN
    document.getElementById('price-filter').addEventListener('change', (event) => {
        event.preventDefault();

        const places_list = document.getElementById('places-list');
        const select = document.getElementById('price-filter');
        const places = document.querySelectorAll(places_list);

        for (let place of places) {
            if (place.price < event.target.value) {
                event.target.value = "flex";
            } else {
                event.target.value = "none"
            }
        }
    });

    // FONDOS ALTERNOS
    // const backgrounds = [
    //     "images/aldea.png",
    //     "images/arbol_ancestral.png",
    //     "images/campo_fantasia.png",
    //     "images/castillo.png",
    //     "images/city.png",
    //     "images/molino.png"
    // ];

    // const randomImage = backgrounds[Math.floor(Math.random() * backgrounds.length)];


    // document.body.style.backgroundImage = `url('${randomImage}')`;
    // document.body.style.backgroundSize = "cover";
    // document.body.style.backgroundPosition = "center";

});
