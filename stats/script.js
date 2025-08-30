function getRecommendations() {
    const query = document.getElementById('search').value;
    fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('recommendations');
        container.innerHTML = '<h2>Recommendations:</h2><ul>' + data.map(b => `<li>${b.title}</li>`).join('') + '</ul>';
    });
}

function message(receiver_id, book_id) {
    const msg = prompt('Enter message:');
    fetch('/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ receiver_id, book_id, message: msg })
    }).then(() => alert('Message sent!'));
}

function buy(book_id) {
    fetch('/buy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ book_id })
    }).then(response => response.json()).then(data => alert(data.message));
}