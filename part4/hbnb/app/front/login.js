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
                localStorage.setItem('username', email);
                alert('Login succesfull');
                window.location.href = 'index.html';
            } else {
                alert(`Login failed: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Error during login:', error);
        }
    }
});

// FONDOS ALTERNOS
const backgrounds = [
    "images/backgraunds/aldea.png",
    "images/backgraunds/arbol_ancestral.png",
    "images/backgraunds/atlantis.png",
    "images/backgraunds/campo_fantasia.png",
    "images/backgraunds/castillo.png",
    "images/backgraunds/city.png",
    "images/backgraunds/ciudad_fantasia.png",
    "images/backgraunds/cyber_city.png",
    "images/backgraunds/japon_pueblo.jpg",
    "images/backgraunds/japon_pueblo2.png",
    "images/backgraunds/laguito.png",
    "images/backgraunds/lluvia.png",
    "images/backgraunds/molino.png",
    "images/backgraunds/punkmodern.png",
    "images/backgraunds/work_ofice.png"
];

const randomImage = backgrounds[Math.floor(Math.random() * backgrounds.length)];


document.body.style.backgroundImage = `url('${randomImage}')`;
document.body.style.backgroundSize = "cover";
document.body.style.backgroundPosition = "center";