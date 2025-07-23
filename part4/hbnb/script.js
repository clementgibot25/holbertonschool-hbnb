document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          
          const email = loginForm.querySelector('input[type="email"]').value.trim();
          const password = loginForm.querySelector('input[type="password"]').value.trim();

          loginUser(email, password);
          
          async function loginUser(email, password) {
          const response = await fetch('http://localhost:5000/api/v1/auth/login', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ email, password }),
          });
          
          if (response.ok) {
            const data = await response.json();
            const date = new Date();
            date.setTime(date.getTime() + (24 * 60 * 60 * 1000));
            document.cookie = `token=${data.access_token}; expires=${date.toUTCString()}; path=/; SameSite=Lax`;
            window.location.href = 'index.html';
            console.log(date);
        } else {
            alert('Login failed: ' + response.statusText);
        }
      }});
  }
});