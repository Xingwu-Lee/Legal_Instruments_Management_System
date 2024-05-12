// Base URL of your Flask server
const BASE_URL = 'http://127.0.0.1:8080';

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-form').onsubmit = function(event) {
        event.preventDefault();
        const name = document.getElementById('name').value;
        const password = document.getElementById('password').value;

        // Send login request to backend
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name, password: password }),
        })
        .then(response => {
            if (response.status === 200) {
                // Store token or handle login success
                response.json().then(data => {
                    localStorage.setItem('access_token', data.access_token);
                    const jwtPayload = parseJwt(data.access_token);
                    const userName = jwtPayload.name;
                    const userPhone = jwtPayload.phone;
                    const userId = jwtPayload.sub;
                    window.location.href = `/main.html?name=${userName}&phone=${userPhone}&id=${userId}`; // Redirect to main page with user data
                });
            }
            else if (response.status === 401){
                response.json().then(data => {
                alert('消息：' + data.message); //登录失败
                });
            }
        });
    };

    document.getElementById('register-form').onsubmit = function(event) {
        event.preventDefault();
        const newUserName = document.getElementById('newUserName').value;
        const newUserPassword = document.getElementById('newUserPassword').value;
        const phone = document.getElementById('phone').value;

        // Send registration request to backend
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: newUserName, password: newUserPassword, phone: phone }),
        })
        .then(response => {
            if (response.status === 201) {
                response.json().then(data => {
                    alert('消息：' + data.message); // 注册成功
                    document.getElementById('register-form').style.display = 'none';
                    document.getElementById('login-form').style.display = 'block';
                });
            } else if (response.status === 409) {
                alert('消息：' + data.message); //用户名已
            }
        });
    };

    function parseJwt(token) {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0
