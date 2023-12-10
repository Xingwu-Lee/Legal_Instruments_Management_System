// Base URL of your Flask server
const BASE_URL = 'http://127.0.0.1:8080';


function modalControl(newModalName, closeCurrent) {
    // 获取当前打开的模态弹框
    var currentModal = document.querySelector(".modal.show");
    if (closeCurrent) {
        // 如果需要关闭当前模态弹框
        if (currentModal) {
            var modal = new bootstrap.Modal(currentModal);
            // 手动关闭当前模态弹框（不触发 "hidden.bs.modal" 事件）
            modal.hide();
        }
    }
    if (newModalName) {
        // 如果需要打开新的模态弹框
        setTimeout(function () {
            var newClientModal = document.getElementById(newModalName);
            if (newClientModal) {
                var modal = new bootstrap.Modal(newClientModal);
                modal.show();
            }
        }, 50);
    }
}

//客户档案收集
function newClient() {
    var name = document.getElementById('clientName').value;
    var phone = document.getElementById('clientPhone').value;
    var email = document.getElementById ('clientEmail').value;
    var citizen_id = document.getElementById('citizen_id').value;
    var postal_code = document.getElementById ('postal_code').value;
    var address = document.getElementById ('address').value;

    // AJAX request to Flask backend for registration
    fetch(BASE_URL + '/newClient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, phone: phone, email: email, citizen_id: citizen_id, postal_code: postal_code, address: address }),
    })
    .then(response => {
        if (response.status === 201) {
            response.json().then(data => {
                alert('消息：' + data.message); // 显示自定义错误消息
                modalControl(null, true)
            });
         } else if (response.status === 409){
            alert('消息：' + data.message); // 显示自定义错误消息
         }
         else if (response.status === 400){
            response.json().then(data => {
            alert('消息：' + data.error()); //输入有空项
            });
        }
    });
}

//案件收集
function newCase() {
    var name = document.getElementById('client_name').value;
    var opposite_party_name = document.getElementById('opposite_party_name').value;
    var case_type = document.getElementById ('case_type').value;
    var court = document.getElementById('court').value;
    var dispute_subject = document.getElementById ('dispute_subject').value;
    var agency_fee = document.getElementById ('agency_fee').value;
    var c_permission = document.getElementById ('c_permission').value;

    // AJAX request to Flask backend for registration
    fetch(BASE_URL + '/newCase', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, opposite_party_name: opposite_party_name, case_type: case_type,
            court: court, dispute_subject: dispute_subject, agency_fee: agency_fee, c_permission: c_permission }),
    })
    .then(response => {
        if (response.status === 201) {
            response.json().then(data => {
                alert('消息：' + data.message); // 显示自定义错误消息
                modalControl(null, true)
            });
         } else if (response.status === 409){
            alert('消息：' + data.message); // 显示自定义错误消息
         }
         else if (response.status === 400){
            response.json().then(data => {
            alert('消息：' + data.error()); //输入有空项
            });
        }
    });
}


document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('clientNameSearchInput');
    var searchResults = document.getElementById('clientNameSearchResults');
    
    searchInput.addEventListener('input', function() {
        var query = searchInput.value;
            // 创建XMLHttpRequest对象
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/search_clients?query=' + query, true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var data = JSON.parse(xhr.responseText);
                    var resultsDropdown = searchResults.querySelector('.dropdown-menu');
                    resultsDropdown.innerHTML = '';
                    data.forEach(function(client) {
                        var link = document.createElement('a');
                        link.classList.add('dropdown-item');
                        link.href = '#';
                        link.textContent = client.name;
                        resultsDropdown.appendChild(link);

                        link.addEventListener('click', function(e) {
                            e.preventDefault();
                            searchInput.value = client.name;
                            resultsDropdown.innerHTML = '';
                            resultsDropdown.style.display = 'none';
                        });
                    });
                    resultsDropdown.style.display = 'block';
                } else {
                    console.error('请求失败：' + xhr.status);
                }
            };
            xhr.send();
        });
    });