// Base URL of your Flask server
const BASE_URL = 'http://127.0.0.1:8080';

function modalControl(newModalName, closeCurrent) {
    // 获取当前打开的模态弹框
    var currentModal = document.querySelector(".modal.show");
    if (closeCurrent) {
        // 如果需要关闭当前模态弹框
        if (currentModal) {
            var modal = new bootstrap.Modal(currentModal);
            setTimeout(function () {
                modal.hide();
            }, 100); // 100毫秒延迟
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
    // 防止表单默认提交行为
    //event.preventDefault();
    var trialLevelSelect = document.getElementById('trial_level');
    var cPermissionSelect = document.getElementById('c_permission');

    if (trialLevelSelect.value === "选择审级" || cPermissionSelect.value === "选择授权选项") {
        alert('请选择有效的审级和授权选项！');
    } else {
    var clientName = document.getElementById('clientNameSearchInput').value;
        clientId = document.getElementById('clientIdDisplay').textContent.replace('客户身份证：', '').trim();
        opposite_party_name = document.getElementById ('opposite_party_name').value,
        case_number = document.getElementById ('case_number').value,
        case_type = document.getElementById ('case_type').value, court = document.getElementById ('court').value,
        dispute_subject = document.getElementById ('dispute_subject').value,
        agency_fee = document.getElementById ('agency_fee').value,
        trial_level = document.getElementById ('trial_level').value, c_permission = document.getElementById ('c_permission').value;
        // AJAX request to Flask backend for registration
         fetch (BASE_URL + '/newCase', {
             method: 'POST',
             headers: {
                 'Content-Type': 'application/json',
             },
             
             body: JSON.stringify ({
                 client_name: clientName, client_id: clientId,
                  opposite_party_name: opposite_party_name, 
                 case_number: case_number, case_type: case_type, court: court,
                 dispute_subject: dispute_subject, agency_fee: agency_fee,
                 trial_level: trial_level, c_permission: c_permission}),
                     //user_name: user_name, user_id: user_id,
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


//加载客户列表
document.addEventListener('DOMContentLoaded', function() {
    fetch(BASE_URL + '/get_clients')
    .then(response => response.json())
    .then(clients => {
        var clientList = document.getElementById('client-list');
        clientList.innerHTML = '';
        clients.forEach((client, index) => {
            var row = `<tr>
                        <th scope="row">${index + 1}</th>
                        <td>${client.name}</td>
                        <td>${client.phone}</td>
                        <td>${client.citizen_id}</td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="editClient('${client.id}')">编辑</button>
                            <button class="btn btn-sm btn-danger" onclick="deleteClient('${client.id}')">删除</button>
                        </td>
                        </tr>`;
            clientList.innerHTML += row;
        });
    });
});


//删除客户
function deleteClient(clientId) {
    if (!confirm("确定要删除该客户吗？")) {
        return;
    }
    fetch(BASE_URL + '/delete_client/' + clientId, { method: 'DELETE' })
    .then(response => {
        if(response.ok) {
            alert('客户删除成功');
            location.reload(); // 重新加载页面以更新客户列表
        } else {
            alert('客户删除失败');
        }
    });
}


// 编辑客户信息
//获取客户信息
function editClient(clientId) {
    fetch(BASE_URL + '/get_client/' + clientId)
    .then(response => response.json())
    .then(client => {
        document.getElementById('edit-client-id').value = client.id;
        document.getElementById('edit-clientName').value = client.name;
        document.getElementById('edit-clientPhone').value = client.phone;
        document.getElementById('edit-clientEmail').value = client.email;
        document.getElementById('edit-citizen_id').value = client.citizen_id;
        document.getElementById('edit-postal_code').value = client.postal_code;
        document.getElementById('edit-address').value = client.address;

        var modal = new bootstrap.Modal(document.getElementById('editClientModal'));
        modal.show();
    });
}

function updateClient() {
    var clientId = document.getElementById('edit-client-id').value;
    var name = document.getElementById('edit-clientName').value;
    var phone = document.getElementById('edit-clientPhone').value;
    var email = document.getElementById('edit-clientEmail').value;
    var citizen_id = document.getElementById('edit-citizen_id').value;
    var postal_code = document.getElementById('edit-postal_code').value;
    var address = document.getElementById('edit-address').value;

    fetch(BASE_URL + '/update_client/' + clientId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, phone, email, citizen_id, postal_code, address })
    })
    .then(response => {
        if (response.ok) {
            alert('客户信息更新成功');
            location.reload();
        } else {
            alert('客户信息更新失败');
        }
    });
}

// Load case list
document.addEventListener('DOMContentLoaded', function() {
    fetch(BASE_URL + '/get_cases')
    .then(response => response.json())
    .then(cases => {
        var caseList = document.getElementById('case-list');
        caseList.innerHTML = '';
        cases.forEach((caseItem, index) => {
            var row = `<tr>
                        <th scope="row">${index + 1}</th>
                        <td>${caseItem.case_number}</td>
                        <td>${caseItem.client_name}</td>
                        <td>${caseItem.case_type}</td>
                        <td>${caseItem.lawyer_name}</td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="editCase('${caseItem.case_number}')">编辑</button>
                            <button class="btn btn-sm btn-danger" onclick="deleteCase('${caseItem.case_number}')">删除</button>
                        </td>
                        </tr>`;
            caseList.innerHTML += row;
        });
    });
});

// Delete case
function deleteCase(case_number) {
    if (!confirm("确定要删除该案件吗？")) {
        return;
    }
    fetch(BASE_URL + '/delete_case/' + case_number, { method: 'DELETE' })
    .then(response => {
        if(response.ok) {
            alert('案件删除成功');
            location.reload(); // Reload the page to update the case list
        } else {
            alert('案件删除失败');
        }
    });
}

// Edit case information
function editCase(case_number) {
    fetch(BASE_URL + '/get_case/' + case_number)
    .then(response => response.json())
    .then(caseData => {
        document.getElementById('edit-opposite_party_name').value = caseData.opposite_party_name;
        document.getElementById('edit-case_number').value = caseData.case_number;
        document.getElementById('edit-case_type').value = caseData.case_type;
        document.getElementById('edit-court').value = caseData.court;
        document.getElementById('edit-agency_fee').value = caseData.agency_fee;
        document.getElementById('edit-dispute_subject').value = caseData.dispute_subject;
        document.getElementById('edit-trial_level').value = caseData.trial_level;
        document.getElementById('edit-c_permission').value = caseData.c_permission;

        // Assuming you have an edit modal with an ID 'editCaseModal'
        var modal = new bootstrap.Modal(document.getElementById('editCaseModal'));
        modal.show();

        // Store the case ID in a hidden field or in a global variable for use in the update function
        //document.getElementById('edit-case-id').value = case_number; // Assuming you have an input field with ID 'edit-case-id'
    });
}

// Update case
function updateCase() {
    var opposite_party_name = document.getElementById('edit-opposite_party_name').value;
    var case_number = document.getElementById('edit-case_number').value;
    var case_type = document.getElementById('edit-case_type').value;
    var court = document.getElementById('edit-court').value;
    var agency_fee = document.getElementById('edit-agency_fee').value;
    var dispute_subject = document.getElementById('edit-dispute_subject').value;
    var trial_level = document.getElementById('edit-trial_level').value;
    var c_permission = document.getElementById('edit-c_permission').value;

    fetch(BASE_URL + '/update_case/' + case_number, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ opposite_party_name, case_number, case_type, court, agency_fee, dispute_subject, trial_level, c_permission })
    })
    .then(response => {
        if (response.ok) {
            alert('案件信息更新成功');
            location.reload(); // Reload the page to update the case list
        } else {
            alert('案件信息更新失败');
        }
    });
}




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


```
//身份证信息提取
function extractIDCardInfo(idCard) {
    // 检查身份证号码长度是否合法
    if (idCard.length !== 18) {
      return "身份证号码长度不合法";
    }
  
    // 提取出生年月日
    const year = idCard.substring(6, 10);
    const month = idCard.substring(10, 12);
    const day = idCard.substring(12, 14);
    const birthday = year + "-" + month + "-" + day;
  
    // 提取性别
    const genderCode = idCard.substring(16, 17);
    const gender = parseInt(genderCode) % 2 === 0 ? "女" : "男";
  
    // 提取籍贯（前6位）
    const nativePlace = idCard.substring(0, 6);
  
    // 计算年龄
    const currentYear = new Date().getFullYear();
    const age = currentYear - parseInt(year);
  
    return {
      birthday,
      age,
      gender,
      nativePlace,
    };
  }
  
  const idCard = "身份证号码"; // 请替换为实际的身份证号码
  const info = extractIDCardInfo(idCard);
  console.log(info);  
```