// Base URL of your Flask server
const BASE_URL = 'http://127.0.0.1:8080';


function modalControl(newModalName, closeCurrent) {
    // Get the currently open modal
    var currentModal = document.querySelector(".modal.show");

    if (closeCurrent && currentModal) {
        // If closing the current modal is needed and a modal is open
        var modal = new bootstrap.Modal(currentModal);
        modal.hide();
    }

    if (newModalName) {
        // If opening a new modal is needed
        var newClientModal = document.getElementById(newModalName);

        if (newClientModal) {
            var modal = new bootstrap.Modal(newClientModal);
            modal.show();
        }
    }
}


```
function modalControl(newModalName, closeCurrent) {
    // 获取当前打开的模态弹框
    var currentModal = document.querySelector(".modal.show");
    if (closeCurrent) {
        // 如果需要关闭当前模态弹框
        if (currentModal) {
            var modal = new bootstrap.Modal(currentModal);
            setTimeout(function () {
                modal.hide();
            }, 100); // 100毫秒延迟 您可以根据需要进行调整
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
        }, 100);
    }
}
```

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
    var trialLevelSelect = document.getElementById('trial_level');
    var cPermissionSelect = document.getElementById('c_permission');

    if (trialLevelSelect.value === "选择审级" || cPermissionSelect.value === "选择授权选项") {
        alert('请选择有效的审级和授权选项！');
    } else {
         //var client_citizen_id = document.getElementById('client_citizen_id').value;
    var opposite_party_name = document.getElementById ('opposite_party_name').value,
        case_number = document.getElementById ('case_number').value,
        case_type = document.getElementById ('case_type').value, court = document.getElementById ('court').value,
        dispute_subject = document.getElementById ('dispute_subject').value,
        agency_fee = document.getElementById ('agency_fee').value,
        trial_level = document.getElementById ('trial_level').value, c_permission = document.getElementById ('c_permission').value,
        client_name = client.name, client_citizen_id = client.citizen_id, user_name = user.name, user_id = user.id;
        // AJAX request to Flask backend for registration
         fetch (BASE_URL + '/newCase', {
             method: 'POST',
             headers: {
                 'Content-Type': 'application/json',
             },
             body: JSON.stringify ({
                 client_name: client_name, client_citizen_id: client_citizen_id,
                 opposite_party_name: opposite_party_name, user_name: user_name, user_id: user_id,
                 case_number: case_number, case_type: case_type, court: court,
                 dispute_subject: dispute_subject, agency_fee: agency_fee,
                 trial_level: trial_level, c_permission: c_permission}),
         })
             .then (response => {
                 if (response.status === 201) {
                     response.json ().then (data => {
                         alert ('消息：' + data.message); // 显示自定义错误消息
                         modalControl (null, true)
                     });
                 } else if (response.status === 409) {
                     alert ('消息：' + data.message); // 显示自定义错误消息
                 } else if (response.status === 400) {
                     response.json ().then (data => {
                         alert ('消息：' + data.error ()); //输入有空项
                     });
                 }
             });
     }
}

//实时客户名搜索实现
document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('clientNameSearchInput');
    var searchResults = document.getElementById('clientNameSearchResults');
    
    searchInput.addEventListener('input', function() {
        var query = searchInput.value;
            // 创建XMLHttpRequest对象
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/searchClients?query=' + query, true);
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
                            clientIdDisplay.textContent = '客户身份证：' + client.citizen_id;
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


//文件上传功能
document.getElementById('uploadFileForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();
    var fileInput = document.getElementById('fileInput');
    var fileDescription = document.getElementById('fileDescription').value;

    formData.append('file', fileInput.files[0]);
    formData.append('description', fileDescription);

    fetch('/upload_file', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // 可以在此处添加代码来处理上传后的响应，如刷新文件列表
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

//文件列表加载
document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_file_list')
    .then(response => response.json())
    .then(files => {
        var tableBody = document.querySelector('#file-management table tbody');
        tableBody.innerHTML = ''; // 清空现有内容
        files.forEach((file, index) => {
            var row = `<tr>
                        <th scope="row">${index + 1}</th>
                        <td>${file.name}</td>
                        <td>${file.description}</td>
                        <td>${file.uploadDate}</td>
                        <td>
                            <button class="btn btn-sm btn-primary">预览</button>
                            <a href="${file.downloadUrl}" class="btn btn-sm btn-success" download>下载</a>
                            <button class="btn btn-sm btn-danger" onclick="deleteFile('${file.id}')">删除</button>
                        </td>
                        </tr>`;
            tableBody.innerHTML += row;
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


function deleteFile(fileId) {
    fetch(`/delete_file/${fileId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // 删除成功后重新加载文件列表
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
