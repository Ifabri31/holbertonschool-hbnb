// Verificar autenticación del usuario
const checkAuthentication = () => {
    const token = getCookie('token');
    if (!token) {
      window.location.href = 'index.html';
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
  
  // Cargar los detalles del lugar
  document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = sessionStorage.getItem('place_id');
    if (placeId) {
      getPlaceData(token, placeId);
    }
  });
  
  // Obtener y mostrar los detalles del lugar
  const getPlaceData = async (token, placeId) => {
    const optsget = {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        }
    };

    try {
        const placeResponse = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, optsget);
        if (!placeResponse.ok) throw new Error(`Error: ${placeResponse.status}`);
        const placeData = await placeResponse.json();
        show_place(placeData);

        const reviewResponse = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, optsget);
        if (!reviewResponse.ok) throw new Error(`Error: ${reviewResponse.status}`);
        const reviewData = await reviewResponse.json();
        show_review(reviewData);
    } catch (error) {
        console.error('Error al obtener los datos del lugar:', error);
    }
};
  
  // Mostrar los detalles del lugar
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
  
// Convertir calificación numérica a estrellas
const getStars = (rating) => {
    const fullStar = '★';
    const emptyStar = '☆';
    return fullStar.repeat(rating) + emptyStar.repeat(5 - rating);
};

// Mostrar las reseñas del lugar
const show_review = (review_info) => {
    const REVIEW_SECTION = document.getElementById('reviews');
    if (!REVIEW_SECTION) {
        console.error('El contenedor #reviews no está presente en el HTML.');
        return;
    }

    let htmlContent = '';

    review_info.forEach((review) => {
        htmlContent += `
            <div class="review-box">
                <p>${review.comment}</p>
                <p><strong>Rating:</strong> <span class="stars">${getStars(review.rating)}</span></p>
            </div>
        `;
    });

    if (htmlContent === '') {
        htmlContent = '<p>No reviews available for this place.</p>';
    }

    REVIEW_SECTION.innerHTML = htmlContent;
};

// Enviar la reseña al backend
const submitReview = async (token, placeId, reviewText, rating) => {
    const reviewData = {
        comment: reviewText,
        rating: parseInt(rating, 10),
        place_id: placeId
    };

    try {
        const response = await fetch('http://localhost:5000/api/v1/reviews', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(reviewData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error desconocido');
        }

        alert('¡Reseña enviada con éxito!');
        document.getElementById('review-form').reset();

        // Recargar las reseñas después de enviar
        getPlaceData(token, placeId);
    } catch (error) {
        console.error('Error al enviar la reseña:', error);
        alert(`Ocurrió un error al enviar la reseña: ${error.message}`);
    }
};

// Configurar el evento para el formulario de reseñas
document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = sessionStorage.getItem('place_id');

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;

            if (reviewText && rating && placeId && token) {
                await submitReview(token, placeId, reviewText, rating);
            } else {
                alert('Por favor, completa todos los campos y asegúrate de estar autenticado.');
            }
        });
    }
});

// Configurar el evento para el botón de logout
document.addEventListener('DOMContentLoaded', () => {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', (event) => {
            event.preventDefault();
            document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            sessionStorage.clear();
            window.location.href = 'index.html';
        });
    }
});