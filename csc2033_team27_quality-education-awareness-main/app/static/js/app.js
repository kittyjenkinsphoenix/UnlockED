import { fs } from 'fs';

function showWelcome(name) {
    if (typeof Swal === 'undefined') {
        console.error('SweetAlert2 not loaded');
        return;
    }
    Swal.fire({
        title: 'Welcome!',
        text: `Hello, ${name}`,
        icon: 'success'
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('greet-btn');
    if (btn) {
        btn.addEventListener('click', () => {
            const name = btn.dataset.username || 'there';
            showWelcome(name);
        });
    }
});

const data = {
    labels: pieLabels,
    datasets: [{
        data: pieValues,
        backgroundColor: [
            '#3f8f94',
            '#5dd5e0',
            '#f6ad55',
            '#fc8181'
        ],
        borderWidth: 0
    }]
};