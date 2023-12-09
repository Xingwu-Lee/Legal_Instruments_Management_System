
function switchModal(newModalName) {
    // 获取当前打开的模态弹框
    var currentModal = document.querySelector(".modal.show");
    if (currentModal) {
        var modal = new bootstrap.Modal(currentModal);

        // 手动关闭当前模态弹框（不触发 "hidden.bs.modal" 事件）
        modal.hide();

        // 等待一段时间后，再打开新的模态弹框
        setTimeout(function () {
            var newClientModal = document.getElementById(newModalName);
            if (newClientModal) {
                var modal = new bootstrap.Modal(newClientModal);
                modal.show();
            }
        }, 0);
    }
}




//客户档案收集
function newClient() {
    var name = document.getElementById('name').value;
    var phone = document.getElementById('phone').value;
    var email = document.getElementById ('email').value;
    var citizen_id = document.getElementById('citizen_id').value;
    var postal_code = document.getElementById ('postal_code').value;
    var address = document.getElementById ('address').value;

    // AJAX request to Flask backend for registration
    fetch(BASE_URL + '/client', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, phone: phone, email:email, citizen_id: citizen_id, postal_code:postal_code, address:address }),
    })
    .then(response => response.json())
    .then(data => {
        if (response.status === 201) {
            console.log('保存成功', data);
            var currentModal = document.querySelector(".modal.show"); // 获取当前打开的模态弹框
            if (currentModal) {
                var modal = new bootstrap.Modal(currentModal);
                modal.hide(); // 关闭当前模态弹框
                }
            //
        }
        elseif (response.status === 409)
            alert('保存失败');

    })
    .catch(error => console.error('Error:', error));
}