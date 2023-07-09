document.addEventListener('DOMContentLoaded', function() {
    const scrapeBtn = document.getElementById('scrape-btn');
    scrapeBtn.addEventListener('click', scrapeAmazon);
  });
  
  function scrapeAmazon() {
    const urlInput = document.getElementById('url');
    const url = urlInput.value.trim();
  
    if (url === '') {
      alert('Please enter the Amazon search URL.');
      return;
    }
  
    const scrapeData = { url };
  
    fetch('/api/scrape', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(scrapeData)
    })
    .then(response => response.json())
    .then(data => displayResults(data))
    .catch(error => console.error('Error:', error));
  }
  
  function displayResults(data) {
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '';
  
    if (data.error) {
      resultsContainer.textContent = `Error: ${data.error}`;
      return;
    }
  
    if (data.data.length === 0) {
      resultsContainer.textContent = 'No results found.';
      return;
    }
  
    const table = document.createElement('table');
    table.innerHTML = `
      <tr>
        <th>Name</th>
        <th>Price</th>
        <th>Brand</th>
        <th>Reviews</th>
        <th>Rating</th>
      </tr>
    `;
  
    data.data.forEach(item => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${item.name}</td>
        <td>${item.price}</td>
        <td>${item.brand}</td>
        <td>${item.reviews}</td>
        <td>${item.rating}</td>
      `;
      table.appendChild(row);
    });
  
    resultsContainer.appendChild(table);
  }
  