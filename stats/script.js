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
    const paymentMethod = document.getElementById(`payment-${book_id}`).value;
    fetch('/buy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ book_id, payment_method: paymentMethod })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else if (data.authorization_url) {
            window.location.href = data.authorization_url;  // Redirect to Paystack
        } else {
            alert(data.message || "Unknown response");
        }
    });
}

function updatePaymentMethod(book_id) {
    // Optional: Update UI
}
