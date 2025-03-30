/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {

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
                alert('Login failed: ' + response.statusText);
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    }

    // Fondos aleatorios
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
