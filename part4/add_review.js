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
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(reviewData)
      });
  
      handleResponse(response);
    } catch (error) {
      console.error('Error al enviar la reseña:', error);
      alert('Ocurrió un error al enviar la reseña.');
    }
  };
  
  // Manejar la respuesta del backend
  const handleResponse = async (response) => {
    if (response.ok) {
      alert('¡Reseña enviada con éxito!');
      document.getElementById('review-form').reset();
    } else {
      const errorData = await response.json();
      alert(`Error al enviar la reseña: ${errorData.error || 'Error desconocido'}`);
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
  
        if (reviewText && rating) {
          await submitReview(token, placeId, reviewText, rating);
        } else {
          alert('Por favor, completa todos los campos.');
        }
      });
    }
  });