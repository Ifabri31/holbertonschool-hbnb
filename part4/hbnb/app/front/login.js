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