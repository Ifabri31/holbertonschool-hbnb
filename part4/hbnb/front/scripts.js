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
                localStorage.setItem('token', data.access_token);
                alert('Login succesfull');
                window.location.href = 'index.html';
            } else {
                alert(`Login failed: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    }

    // CHECK AUTHENTICATION
    function checkAuthentication() {
        const token = localStorage.getItem('token');
    
        if (token) {
            fetchPlaces(token);
        } else {
            window.location.href = 'login.html'
        }
    }

    // GET ALL PLACES
    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {

                method: 'GET',
                mode: "cors", // Asegura que es una solicitud CORS
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                displayPlaces(data);
            } else {
                console.error(`Error fetching places; ${response.statusText}`);
            }
        } catch (error) {
            console.error(`Error fetching puto places: ${error}`);
        }
    }

    function displayPlaces(places) {
        const placeList = document.getElementById('places-list');
        placeList.innerHTML = '';

        places.forEach(place => {
            const placeArt = document.createElement('article');
            placeArt.setAttribute('data-place-price', place.price);
            placeArt.classList.add('place-card');
            placeArt.innerHTML = `
                <h3 class="place-title">${place.title}</h3>
                <p class="place-parg">Price per night: $${place.price}</p>
                <p class="place-parg">Location: X${place.longitude} Y${place.latitude}</p>
                <button class="details-button">View Details</button>
            `;
            placeList.appendChild(placeArt);
        });
    }



    // PRICE FILTER DROPDOWN
    document.getElementById('price-filter').addEventListener('change', (event) => {
        event.preventDefault();

        const places_list = document.getElementById('places-list');
        const places = places_list.querySelectorAll('.place-card');

        places.forEach(place => {
            console.log(place);
            
            const price = parseFloat(place.getAttribute('data-place-price'));

            console.log(event.target.value);
            console.log(price);
            

            if (event.target.value === 'All' || price <= parseFloat(event.target.value)) {
                console.log()
                place.style.display = 'block';
            } else {
                place.style.display = 'none';
            }
        });

        checkAuthentication();

    });

    // DISPLAY DETAILS INFORMATION OF A PLACE


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
