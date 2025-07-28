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
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
async function fetchPlaces(token) {
    const response = await fetch('http://localhost:5000/api/v1/places', {
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    });
    
    if (response.ok) {
        const data = await response.json();
        displayPlaces(data);
    } else {
        console.error('Failed to fetch places:', response.statusText);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    const container = placesList.querySelector('.cards-container');
    if (!container) return;

    container.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('li');
        card.className = 'card';
        
        const title = document.createElement('h3');
        title.textContent = place.name;
        
        const price = document.createElement('p');
        price.textContent = `Price per night: $${place.price_by_night}`;
        
        const button = document.createElement('button');
        button.textContent = 'View Details';
        
        card.appendChild(title);
        card.appendChild(price);
        card.appendChild(button);
        
        container.appendChild(card);
    });
}
// Initialiser le filtre de prix
function initPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    // Ajouter les options de prix
    const priceOptions = [10, 50, 100, 'All'];
    priceOptions.forEach(price => {
        const option = document.createElement('option');
        option.value = price === 'All' ? 'all' : price;
        option.textContent = price;
        priceFilter.appendChild(option);
    });

    // Gérer le changement de sélection
    priceFilter.addEventListener('change', (event) => {
        const selectedValue = event.target.value;
        const cards = document.querySelectorAll('.card');
        
        cards.forEach(card => {
            if (selectedValue === 'all') {
                card.style.display = 'block';
                return;
            }

            const priceText = card.querySelector('p').textContent;
            // Extraire uniquement les chiffres du prix
            const priceValue = parseInt(priceText.replace(/\D/g, ''));
            const maxPrice = parseInt(selectedValue);
            
            if (priceValue <= maxPrice) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// Appeler l'initialisation du filtre au chargement du DOM
document.addEventListener('DOMContentLoaded', () => {
    initPriceFilter();
    checkAuthentication();
});