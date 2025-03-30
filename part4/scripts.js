let place_data = [];
let review_data;

const checkAuthentication = () => {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';
    window.href = 'index.html';
  } else {
    loginLink.style.display = 'none';
    fetchPlaces(token);
  }
};

const fill_prices_filter = (price_filter) => {
  price_filter.innerHTML += `
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
    <option value="all" selected>All</option>
  `;
  price_filter.addEventListener('change', (event) => {
    let price = price_filter.value;
    displayPlaces(place_data, price);
  });
};

const getPlaceData = () => {
  const token = getCookie('token');
  const id = sessionStorage.getItem('place_id');
  let optsget = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  };

  // GET PLACE INFO
  fetch(`http://localhost:5000/api/v1/places/${id}`, optsget)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      place_data = data;
      show_place(place_data);
    })
    .catch((error) => {
      console.error('Error en la solicitud:', error);
    });

  // GET REVIEWS
  fetch(`http://localhost:5000/api/v1/places/${id}/reviews`, optsget)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      review_data = data;
      show_review(review_data);
    })
    .catch((error) => {
      console.error('Error en la solicitud:', error);
    });
};

document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const LOGIN_BTN = document.getElementById('login-btn');
  const PRICE_FILTER = document.getElementById('price-filter');

  if (LOGIN_BTN) {
    LoginFunct(LOGIN_BTN);
  }
  if (PRICE_FILTER) {
    fill_prices_filter(PRICE_FILTER);
  }
  if (window.location.pathname.endsWith('place.html')) {
    getPlaceData();
  }
});