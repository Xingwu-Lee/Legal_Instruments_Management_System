// Base URL of your Flask server
const BASE_URL = 'http://127.0.0.1:5000/api';

// Function for user login
function login() {
    var name = document.getElementById('name').value;
    var password = document.getElementById('password').value;

    // AJAX request to Flask backend for login
    fetch(BASE_URL + '/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (response.status === 200) {
            // Store token or handle login success
            console.log('Login successful', data);
            // Redirect or update UI accordingly
        elseif (response.status === 401)
            alert('用户名或密码错误，来自boostrap');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function for user registration
function register() {
    var name = document.getElementById('name').value;
    var password = document.getElementById('password').value;
    var role = document.getElementById('role').value;
    var phone = document.getElementById('phone').value;

    // AJAX request to Flask backend for registration
    fetch(BASE_URL + '/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, password: password, role:role, phone: phone }),
    })
    .then(response => response.json())
    .then(data => {
        if (response.status === 201) {
            console.log('Registration successful', data);
            document.getElementById('register-form').style.display = 'none';
            document.getElementById('login-form').style.display = 'block';
            // Redirect or update UI accordingly
        }
        elseif (response.status === 409)
            alert('Registration failed');

    })
    .catch(error => console.error('Error:', error));
}

function register_page(){
    document.getElementById('register-form').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
}
// The registration function will be similar, making a POST request to the Flask registration route.
