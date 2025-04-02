// document.addEventListener('DOMContentLoaded', () => {

//     let placeId;
//     try {
//         const urlParams = new URLSearchParams(window.location.search);
//         if (urlParams) {
//             placeId = urlParams.get('place_id');
//         } else {
//             console.error('The place ID not found');
//         }
//     } catch (error) {
//         console.error(`Error to try extract the placeID from the URL: ${error}`);
//     };

//     // CHECK AUTHENTICATION
//     function checkAuthentication() {
//         const token = localStorage.getItem('token');
    
//         if (!token) {
//             window.location.href = 'login.html'
//         }
//     };

//     // SUBMIT A REVIEW
//     const reviewForm = document.getElementById('review-form');

//     if (reviewForm) {
//         reviewForm.addEventListener('submit', (event) => {
//             event.preventDefault();

//             const token = localStorage.getItem('token');
//             const comment = document.getElementById('comment').value;
//             const rating = document.getElementById('rating').value;

//             /*await */submitReview(token, comment, rating, placeId);
//         });
//     }

//     async function submitReview(token, comment, rating, placeId) {
//         try {
//             const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'Authorization': `Bearer ${token}`
//                 },
//                 body: JSON.stringify({ comment, rating, placeId })
//             });

//             if (response.ok) {
//                 alert('Review submitted successfully!');
//             } else {
//                 alert('Failed to submit review');
//             }
//         } catch (error) {
//             console.error(`Failed to fetch function: ${error}`);
//         };
//     };
//     checkAuthentication();
// });