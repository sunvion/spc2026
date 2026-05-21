// js/auth.js

// Simple auth handling using localStorage
// Session stored as "currentUser" key (user id)

function login(userId, password) {
    const users = JSON.parse(localStorage.getItem('users')) || [];
    const match = users.find(u => u.id === userId && u.password === password);
    if (match) {
        localStorage.setItem('currentUser', userId);
        updateAuthUI();
        return true;
    }
    return false;
}

function logout() {
    localStorage.removeItem('currentUser');
    updateAuthUI();
    // optional redirect to home
    location.href = 'index.html';
}

function getCurrentUser() {
    return localStorage.getItem('currentUser');
}

function isLoggedIn() {
    return !!getCurrentUser();
}

function updateAuthUI() {
    const authLink = document.getElementById('authLink');
    if (!authLink) return; // called on pages without nav
    if (isLoggedIn()) {
        authLink.textContent = 'Logout';
        authLink.href = '#';
        authLink.onclick = function(e) {
            e.preventDefault();
            logout();
        };
    } else {
        authLink.textContent = 'Login';
        authLink.href = 'login.html';
        authLink.onclick = null;
    }
}
