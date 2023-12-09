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
    .then(response => {
        if (response.status === 200) {
            // Store token or handle login success
            response.json().then(data => {
                console.log ('Login successful', data);
                window.location.href = data.redirect;
            });
        }
        else if (response.status === 401){
            response.json().then(data => {
            alert('消息：' + data.message); //登录失败
            });
        }
    });
}

// Function for user registration
function register() {
    var name = document.getElementById('newUserName').value;
    var password = document.getElementById('newUserPassword').value;
    var phone = document.getElementById('phone').value;
    // AJAX request to Flask backend for registration
    fetch(BASE_URL + '/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, password: password, phone: phone }),
    })
    .then(response => {
        if (response.status === 201) { //注册成功
            response.json().then(data => {
                alert('消息：' + data.message); // 显示自定义错误消息
                // 回到登录界面
                document.getElementById('register-form').style.display = 'none';
                document.getElementById('login-form').style.display = 'block';
            });
        } else if (response.status === 409) {  //用户名已存在
            alert('消息：' + data.message);
        }
    });
}

function registerPage(){
    //切换注册界面
    document.getElementById('register-form').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
}
// The registration function will be similar, making a POST request to the Flask registration route.
