// static/dashboard.js

document.addEventListener('DOMContentLoaded', () => {
    loadExpenses();

    const form = document.getElementById('expenseForm');
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const title = formData.get('title');
        const amount = formData.get('amount');
        const date = formData.get('date');

        fetch('/add-expense', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category: title, amount: parseFloat(amount), date: date })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            form.reset();
            loadExpenses();
        })
        .catch(err => console.error('Error:', err));
    });
});

function loadExpenses() {
    fetch('/view-expenses')
        .then(res => res.json())
        .then(data => {
            const tableBody = document.getElementById('expenseTableBody');
            tableBody.innerHTML = '';
            data.forEach(exp => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${exp.category}</td>
                    <td>₹${exp.amount.toFixed(2)}</td>
                    <td>${exp.date}</td>
                    <td><button class="btn btn-danger btn-sm" onclick="deleteExpense(${exp.id})">Delete</button></td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function deleteExpense(id) {
    fetch(`/delete-expense/${id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || 'Deleted');
        loadExpenses();
    })
    .catch(err => console.error('Delete error:', err));
}
