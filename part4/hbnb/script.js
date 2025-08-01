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
  
  function initPlaceDetailsPage() {
    const placeDetailsSection = document.getElementById('place-details');
    const reviewsSection = document.getElementById('reviews');
    const addReviewSection = document.getElementById('add-review');

    if (!placeDetailsSection || !reviewsSection || !addReviewSection) {
        return; // Not on the place details page
    }

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    const token = getCookie('token');

    addReviewSection.style.display = token ? 'block' : 'none';

    if (!placeId) {
        placeDetailsSection.innerHTML = '<p>Error: No place ID provided in URL.</p>';
        return;
    }

    // Fetch Place Details
    fetch(`http://localhost:5000/api/v1/places/${placeId}`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch place details.');
            return response.json();
        })
        .then(data => {
            const hostName = data.owner ? `${data.owner.first_name} ${data.owner.last_name}`.trim() : 'N/A';
            placeDetailsSection.innerHTML = `
                <h2 class="place-info">${data.title}</h2>
                <ul>
                    <li><b>Host:</b> ${hostName}</li>
                    <li><b>Price per night:</b> $${data.price}</li>
                    <li><b>Description:</b> ${data.description}</li>
                    <li><b>Amenities:</b> ${data.amenities && data.amenities.length ? data.amenities.map(a => a.name).join(', ') : 'None'}</li>
                </ul>
            `;
        })
        .catch(error => {
            placeDetailsSection.innerHTML = `<p>Error loading place details: ${error.message}</p>`;
        });

    // Fetch Reviews
    fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`)
        .then(response => {
            if (response.status === 404) return []; // No reviews is not an error
            if (!response.ok) throw new Error('Failed to fetch reviews.');
            return response.json();
        })
        .then(reviews => {
            let reviewsHtml = '<h2>Reviews</h2>';
            if (reviews && reviews.length > 0) {
                reviewsHtml += reviews.map(review => {
                    return `
                        <div>
                            <p><b>User ID: ${review.user_id}</b></p>
                            <p>Rating: ${review.rating} stars</p>
                            <p>${review.text}</p>
                        </div>
                    `;
                }).join('');
            } else {
                reviewsHtml += '<p>No reviews yet.</p>';
            }
            reviewsSection.innerHTML = reviewsHtml;
        })
        .catch(error => {
            reviewsSection.innerHTML = '<h2>Reviews</h2><p>Could not load reviews.</p>';
        });
}

function initAddReviewPage() {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) {
        return; // Not on the add review page
    }

    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to add a review.');
        window.location.href = 'login.html';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    if (!placeId) {
        alert('Error: No place ID provided.');
        window.location.href = 'index.html';
        return;
    }
    document.getElementById('place_id').value = placeId;

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;

        try {
            const response = await fetch('http://localhost:5000/api/v1/reviews/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: parseInt(rating),
                    place_id: placeId
                })
            });

            if (response.ok) {
                alert('Review submitted successfully!');
                window.location.href = `place.html?id=${placeId}`;
            } else {
                const errorData = await response.json();
                alert(`Failed to submit review: ${errorData.message || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('An error occurred while submitting your review.');
        }
    });
}

// Appeler l'initialisation au chargement du DOM
  document.addEventListener('DOMContentLoaded', () => {
      initPriceFilter();
      checkAuthentication();
      initPlaceDetailsPage();
      initAddReviewPage();
  });