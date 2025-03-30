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

const fetchPlaces = async (token) => {
  const optsget = {
    method: 'GET',
    headers: createHeaders(token)
  };

  try {
    const response = await fetch('http://localhost:5000/api/v1/places/', optsget);
    if (!response.ok) throw new Error(`Error: ${response.status}`);
    const data = await response.json();
    place_data = data;
    displayPlaces(data, 'all');
  } catch (error) {
    console.error('Error en la solicitud:', error);
  }
};

const setSSid = (id) => {
  sessionStorage.setItem('place_id', id);
  window.location.href = './place.html';
};

const displayPlaces = (data, price) => {
  const PLACE_LIST = document.getElementById('places-list');
  let htmlContentToAppend = '';

  if (PLACE_LIST) {
    data.forEach((place) => {
      if (price === 'all' || parseInt(price) >= place.price) {
        htmlContentToAppend += `
          <div class="place-box">
            <h2 class="place-title">${place.title}</h2>
            <p class="place-price">price per night: $${place.price}</p>
            <button onclick="setSSid('${place.id}')" class="details-button" id="${place.id}">View Details</button>
          </div>
        `;
      }
    });

    PLACE_LIST.innerHTML = htmlContentToAppend;
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
    const price = price_filter.value;
    displayPlaces(place_data, price);
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
  const id = sessionStorage.getItem('place_id');
  const optsget = {
    method: 'GET',
    headers: createHeaders(token)
  };

  try {
    const placeResponse = await fetch(`http://localhost:5000/api/v1/places/${id}`, optsget);
    if (!placeResponse.ok) throw new Error(`Error: ${placeResponse.status}`);
    place_data = await placeResponse.json();
    show_place(place_data);

    const reviewResponse = await fetch(`http://localhost:5000/api/v1/places/${id}/reviews`, optsget);
    if (!reviewResponse.ok) throw new Error(`Error: ${reviewResponse.status}`);
    review_data = await reviewResponse.json();
    show_review(review_data);
  } catch (error) {
    console.error('Error en la solicitud:', error);
  }
};

const show_review = async (review_info) => {
  const token = getCookie('token');
  const optsget = {
    method: 'GET',
    headers: createHeaders(token)
  };

  try {
    const userResponse = await fetch('http://localhost:5000/api/v1/users/', optsget);
    if (!userResponse.ok) throw new Error(`Error: ${userResponse.status}`);
    const userlist = await userResponse.json();

    const userMap = new Map(userlist.map((user) => [user.id, user]));
    const REVIEW_DETAILS = document.getElementById('reviews');
    let htmlreviewscontent = '';

    review_info.forEach((review) => {
      const userinfo = userMap.get(review.user_id);
      if (userinfo) {
        htmlreviewscontent += `
          <div class="review-box">
            <strong>${userinfo.first_name} ${userinfo.last_name}</strong>
            <p>${review.text}</p>
            <div>
              <p>Rating</p>
              <p>${review.rating}</p>
            </div>
          </div>
        `;
      }
    });

    REVIEW_DETAILS.innerHTML = htmlreviewscontent;
  } catch (error) {
    console.error('Error en la solicitud:', error);
  }
};

const show_place = (place_info) => {
  const PLACE_TITLE = document.getElementById('place-title');
  PLACE_TITLE.innerHTML = place_info.title;

  const PLACE_DETAILS = document.getElementById('place-details');
  const amenities = place_info.amenities.map((amenity) => amenity.name).join(', ') || 'None';

  const htmlContentToAppend = `
    <div class="place-box">
      <p><strong>Host:</strong> ${place_info.owner.first_name} ${place_info.owner.last_name}</p>
      <p><strong>Price per night:</strong> $${place_info.price} usd</p>
      <p><strong>Description:</strong> ${place_info.description}</p>
      <p><strong>Amenities:</strong> ${amenities}</p>
    </div>
  `;

  PLACE_DETAILS.innerHTML = htmlContentToAppend;
};

document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const LOGIN_BTN = document.getElementById('login-btn');
  const PRICE_FILTER = document.getElementById('price-filter');

  if (LOGIN_BTN) LoginFunct(LOGIN_BTN);
  if (PRICE_FILTER) fill_prices_filter(PRICE_FILTER);
  if (window.location.pathname.endsWith('place.html')) getPlaceData();
});