document.addEventListener('DOMContentLoaded', () => {

    // CHECK AUTHENTICATION
    function checkAuthentication() {
        const token = localStorage.getItem('token');
    
        if (token) {
            fetchPlaces(token);
        } else {
            window.location.href = 'login.html'
        }
    };

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
                <h3 class="place-title">${place.title}</h3>
                <p class="place-parg">Price per night: $${place.price}</p>
                <p class="place-parg">Location: X${place.longitude} Y${place.latitude}</p>
                <button class="details-button">View Details</button>
            `;
            placeList.appendChild(placeArt);
        });
    };

    // PRICE FILTER DROPDOWN
    document.getElementById('price-filter').addEventListener('change', (event) => {
        event.preventDefault();

        const places_list = document.getElementById('places-list');
        const places = places_list.querySelectorAll('.place-card');

        places.forEach(place => {
            
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
    });

    checkAuthentication();
});