// Verificar autenticación del usuario
const checkAuthentication = () => {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
  
    if (!token) {
      if (loginLink) loginLink.style.display = 'block';
      if (logoutLink) logoutLink.style.display = 'none';
    } else {
      if (loginLink) loginLink.style.display = 'none';
      if (logoutLink) {
        logoutLink.style.display = 'block';
        logoutLink.addEventListener('click', (e) => {
          e.preventDefault();
          logout();
        });
      }
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
  
  // Cerrar sesión
  const logout = () => {
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    window.location.href = 'login.html';
  };
  
  // Cargar los lugares
  document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    if (token) {
      fetchPlaces(token);
    }
  
    const PRICE_FILTER = document.getElementById('price-filter');
    if (PRICE_FILTER) fill_prices_filter(PRICE_FILTER);
  });
  
  // Obtener y mostrar los lugares
  const fetchPlaces = async (token) => {
    const optsget = {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      }
    };
  
    try {
      const response = await fetch('http://localhost:5000/api/v1/places/', optsget);
      if (!response.ok) throw new Error(`Error: ${response.status}`);
      const data = await response.json();
      displayPlaces(data, 'all');
    } catch (error) {
      console.error('Error al obtener los lugares:', error);
    }
  };
  
  // Mostrar los lugares en la página
  const displayPlaces = (data, price) => {
    const PLACE_LIST = document.getElementById('places-list');
    if (!PLACE_LIST) {
      console.error('El contenedor #places-list no está presente en el HTML.');
      return;
    }
  
    let htmlContentToAppend = '';
  
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
  };
  
  // Guardar el ID del lugar y redirigir a la página de detalles
  const setSSid = (id) => {
    sessionStorage.setItem('place_id', id);
    window.location.href = './place.html';
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
      displayPlaces(place_data, price);
    });
  };