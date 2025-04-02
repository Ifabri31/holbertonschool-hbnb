let place_data = [];
let review_data;

// Verificar autenticación del usuario
const checkAuthentication = () => {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
    // Usuario no autenticado
    if (loginLink) loginLink.style.display = 'block';
    if (logoutLink) loginLink.style.display = 'none';
    // Ocultar el formulario de agregar reseñas si el usuario no está autenticado
    if (addReviewSection) addReviewSection.style.display = 'none';
  } else {
    // Usuario autenticado
    if (loginLink) loginLink.style.display = 'none';
    if (logoutLink) {
      logoutLink.style.display = 'block';
      logoutLink.addEventListener('click', (e) => {
        e.preventDefault(); // Evita el comportamiento predeterminado del enlace
        logout();
      });
    }
    // Mostrar el formulario de agregar reseñas si el usuario está autenticado
    if (addReviewSection) addReviewSection.style.display = 'block';
    fetchPlaces(token); // Cargar los lugares solo si el usuario está autenticado
  }
  return token;
};

// Obtener el valor de una cookie por su nombre
const getCookie = (name) => {
  const cookies = document.cookie.split('; ');
  for (const cookie of cookies) {
    const [key, value] = cookie.split('=');
    if (key === name) {
      return value;
    }
  }
  return null;
};

const createHeaders = (token) => ({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${token}`
});

// Realizar una solicitud para obtener los lugares
const fetchPlaces = async (token) => {
  const optsget = {
    method: 'GET',
    mode: 'cors',
    headers: createHeaders(token)
  };

  try {
    const response = await fetch('http://localhost:5000/api/v1/places/', optsget);
    if (!response.ok) throw new Error(`Error: ${response.status}`);
    const data = await response.json();
    place_data = data;
    displayPlaces(data, 'all'); // Mostrar todos los lugares inicialmente
  } catch (error) {
    console.error('Error en la solicitud:', error);
  }
};

// Guardar el ID del lugar en sessionStorage y redirigir a la página de detalles
const setSSid = (id) => {
  sessionStorage.setItem('place_id', id);
  window.location.href = './place.html';
};

// Mostrar los lugares en la página
const displayPlaces = (data, price) => {
  const PLACE_LIST = document.getElementById('places-list');
  let htmlContentToAppend = '';

  if (PLACE_LIST) {
    data.forEach((place) => {
      if (price === 'all' || parseInt(price) >= place.price) {
        htmlContentToAppend += `
          <div class="place-box">
            <h2 class="place-title">${place.title}</h2>
            <p class="place-price">Price per night: $${place.price}</p>
            <button onclick="setSSid('${place.id}')" class="details-button" id="${place.id}">View Details</button>
          </div>
        `;
      }
    });

    PLACE_LIST.innerHTML = htmlContentToAppend;
  }
};

// Configurar el filtro de precios
const fill_prices_filter = (price_filter) => {
  price_filter.innerHTML += `
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
    <option value="all" selected>All</option>
  `;
  price_filter.addEventListener('change', (event) => {
    const price = price_filter.value;
    displayPlaces(place_data, price); // Filtrar los lugares según el precio seleccionado
  });
};

const LoginFunct = (logbtn) => {
  logbtn.addEventListener('click', async (e) => {
    e.preventDefault();
    const EMAIL = document.getElementById('email').value;
    const PASSWORD = document.getElementById('password').value;

    if (EMAIL.length >= 10 && PASSWORD.length >= 5) {
      const postopts = {
        method: 'POST',
        mode: 'cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: EMAIL, password: PASSWORD })
      };

      try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', postopts);
        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          alert('Login failed: ' + response.statusText);
        }
      } catch (error) {
        console.error('Error en la solicitud:', error);
      }
    } else {
      alert('Empty fields left.');
    }
  });
};

const getPlaceData = async () => {
  const token = getCookie('token');
  const placeId = sessionStorage.getItem('place_id');
  const optsget = {
    method: 'GET',
    mode: 'cors',
    headers: createHeaders(token)
  };

  try {
    // Obtener los detalles del lugar
    const placeResponse = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, optsget);
    if (!placeResponse.ok) throw new Error(`Error: ${placeResponse.status}`);
    const placeData = await placeResponse.json();
    show_place(placeData); // Mostrar los detalles del lugar

    // Obtener las reseñas del lugar
    const reviewResponse = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, optsget);
    if (!reviewResponse.ok) throw new Error(`Error: ${reviewResponse.status}`);
    const reviewData = await reviewResponse.json();
    show_review(reviewData); // Mostrar las reseñas
  } catch (error) {
    console.error('Error al obtener los datos del lugar:', error);
  }
};

const show_review = (review_info) => {
  const REVIEW_SECTION = document.getElementById('reviews');
  let htmlContent = '';

  review_info.forEach((review) => {
    htmlContent += `
      <div class="review-box">
        <p><strong>${review.user.first_name} ${review.user.last_name}</strong></p>
        <p>${review.comment}</p>
        <p><strong>Rating:</strong> ${review.rating}</p>
      </div>
    `;
  });

  REVIEW_SECTION.innerHTML = htmlContent;
};

const show_place = (place_info) => {
  const PLACE_TITLE = document.getElementById('place-title');
  PLACE_TITLE.innerHTML = place_info.title;

  const PLACE_DETAILS = document.getElementById('place-details');
  const amenities = place_info.amenities.map((amenity) => amenity.name).join(', ') || 'None';

  const htmlContentToAppend = `
    <div class="place-box">
      <p><strong>Host:</strong> ${place_info.owner.first_name} ${place_info.owner.last_name}</p>
      <p><strong>Price per night:</strong> $${place_info.price}</p>
      <p><strong>Description:</strong> ${place_info.description}</p>
      <p><strong>Amenities:</strong> ${amenities}</p>
    </div>
  `;

  PLACE_DETAILS.innerHTML = htmlContentToAppend;
};

// Cerrar sesión
const logout = () => {
  document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
  window.location.href = 'login.html';
};

const getPlaceIdFromURL = () => {
  const params = new URLSearchParams(window.location.search);
  return params.get('place_id');
};

const fetchPlaceDetails = async (token, placeId) => {
  const optsget = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  };

  try {
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, optsget);
    if (!response.ok) throw new Error(`Error: ${response.status}`);
    const placeData = await response.json();
    displayPlaceDetails(placeData);

    // Obtener las reseñas del lugar
    const reviewResponse = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, optsget);
    if (!reviewResponse.ok) throw new Error(`Error: ${reviewResponse.status}`);
    const reviews = await reviewResponse.json();
    displayReviews(reviews);
  } catch (error) {
    console.error('Error al obtener los detalles del lugar:', error);
  }
};

const displayPlaceDetails = (place) => {
  const PLACE_DETAILS = document.getElementById('place-details');
  const amenities = place.amenities.map((amenity) => amenity.name).join(', ') || 'None';

  const htmlContent = `
    <div class="place-box">
      <h2>${place.title}</h2>
      <p><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
      <p><strong>Price per night:</strong> $${place.price}</p>
      <p><strong>Description:</strong> ${place.description}</p>
      <p><strong>Amenities:</strong> ${amenities}</p>
    </div>
  `;

  PLACE_DETAILS.innerHTML = htmlContent;
};

const displayReviews = (reviews) => {
  const REVIEW_SECTION = document.getElementById('reviews');
  let htmlContent = '';

  reviews.forEach((review) => {
    htmlContent += `
      <div class="review-box">
        <p><strong>${review.user.first_name} ${review.user.last_name}</strong></p>
        <p>${review.comment}</p>
        <p><strong>Rating:</strong> ${review.rating}</p>
      </div>
    `;
  });

  REVIEW_SECTION.innerHTML = htmlContent;
};

// Configurar los eventos al cargar la página
document.addEventListener('DOMContentLoaded', () => {
  // Verificar autenticación
  const token = checkAuthentication();

  // Obtener el ID del lugar desde sessionStorage
  const placeId = sessionStorage.getItem('place_id');

  // Si estamos en la página de detalles del lugar, obtener los datos del lugar
  if (placeId && window.location.pathname.endsWith('place.html')) {
    getPlaceData(); // Obtener y mostrar los datos del lugar
  }

  // Configurar eventos existentes
  const LOGIN_BTN = document.getElementById('login-btn');
  const PRICE_FILTER = document.getElementById('price-filter');

  if (LOGIN_BTN) LoginFunct(LOGIN_BTN);
  if (PRICE_FILTER) fill_prices_filter(PRICE_FILTER);

  // Si estamos en la página principal, cargar los datos de los lugares
  if (window.location.pathname.endsWith('index.html')) {
    fetchPlaces(token);
  }
});