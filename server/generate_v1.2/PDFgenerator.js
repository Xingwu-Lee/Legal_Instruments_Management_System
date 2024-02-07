function createFormGroup() {
    var formGroup = document.createElement('div');
    formGroup.className = 'form-group';
    return formGroup;
}
function createLabel(inputId, text) {
    var label = document.createElement('label');
    label.setAttribute('for', inputId);
    label.textContent = text;
    return label;
}

function createInput(inputId, inputType, name, required, placeholder = '') {
    var input = document.createElement('input');
    input.className = 'form-control';
    input.setAttribute('type', inputType);
    input.setAttribute('id', inputId);
    input.setAttribute('name', name);
    if (required) input.required = true;
    if (placeholder && inputType === 'date') input.setAttribute('placeholder', placeholder); 
    return input;
}



function createTextArea(inputId, name, rows, cols, required) {
    var textarea = document.createElement('textarea');
    textarea.className = 'form-control';
    textarea.setAttribute('id', inputId);
    textarea.setAttribute('name', name);
    textarea.setAttribute('rows', rows);
    textarea.setAttribute('cols', cols);
    if (required) textarea.required = true;
    return textarea;
}
function addFormField(container, label, input) {
    var formGroup = createFormGroup();
    formGroup.appendChild(label);
    formGroup.appendChild(input);
    container.appendChild(formGroup);
}

function updateFormFields() {
    var templateChoice = document.getElementById('template_choice').value;
    var formFieldsDiv = document.getElementById('formFields');
          
            
    while (formFieldsDiv.firstChild) {
        formFieldsDiv.removeChild(formFieldsDiv.firstChild);
    }

    
    if (templateChoice === 'default') {
                
        addFormField(formFieldsDiv, createLabel('party_a', 'Party A:'), createInput('party_a', 'text', 'party_a', true));
        addFormField(formFieldsDiv, createLabel('party_b', 'Party B:'), createInput('party_b', 'text', 'party_b', true));
        addFormField(formFieldsDiv, createLabel('agreement_content', 'Agreement Content:'), createTextArea('agreement_content', 'agreement_content', 4, 50, true));
    

                
    } else if (templateChoice === 'authorization_letter') {
                
        addFormField(formFieldsDiv, createLabel('client_name', '委托人：'), createInput('client_name', 'text', 'client_name', true));
        addFormField(formFieldsDiv, createLabel('lawyer_name', '受委托人姓名：'), createInput('lawyer_name', 'text', 'lawyer_name', true));
        addFormField(formFieldsDiv, createLabel('opposite_party_name', '工作单位：'), createInput('opposite_party_name', 'text', 'opposite_party_name', false));
        addFormField(formFieldsDiv, createLabel('position', '职务：'), createInput('position', 'text', 'position', false));
        addFormField(formFieldsDiv, createLabel('phone', '电话：'), createInput('phone', 'tel', 'phone', false));
        addFormField(formFieldsDiv, createLabel('case_name', '案件：'), createInput('case_name', 'text', 'case_name', true));
        addFormField(formFieldsDiv, createLabel('case_type', '案由：'), createInput('case_type', 'text', 'case_type', true));
        addFormField(formFieldsDiv, createLabel('c_permission', '代理权限：'), createTextArea('c_permission', 'c_permission', 4, 50, true));
   
    }else if (templateChoice === 'legal_rep_identity') {
        addFormField(formFieldsDiv, createLabel('rep_name', '代表人姓名：'), createInput('rep_name', 'text', 'rep_name', true));
        addFormField(formFieldsDiv, createLabel('position', '职务：'), createInput('position', 'text', 'position', true));
        addFormField(formFieldsDiv, createLabel('unit_name', '单位全称：'), createInput('unit_name', 'text', 'unit_name', true));
        addFormField(formFieldsDiv, createLabel('date', '日期：'), createInput('date', 'date', 'date', true));
        addFormField(formFieldsDiv, createLabel('address', '地址：'), createInput('address', 'text', 'address', true));
        addFormField(formFieldsDiv, createLabel('phone', '电话：'), createInput('phone', 'tel', 'phone', true));
    } else if (templateChoice === 'lawyer_agency_contract') {
        addFormField(formFieldsDiv, createLabel('client_address', '甲方地址：'), createInput('client_address', 'text', 'client_address', true));
        addFormField(formFieldsDiv, createLabel('client_postcode', '邮政编码：'), createInput('client_postcode', 'text', 'client_postcode', true));
        addFormField(formFieldsDiv, createLabel('client_phone', '电话：'), createInput('client_phone', 'tel', 'client_phone', true));
        addFormField(formFieldsDiv, createLabel('opponent_name', '对方当事人名称或者姓名：'), createInput('opponent_name', 'text', 'opponent_name', true));
        addFormField(formFieldsDiv, createLabel('case_reason', '案由：'), createInput('case_reason', 'text', 'case_reason', true));
        addFormField(formFieldsDiv, createLabel('trial_authority', '审理机关：'), createInput('trial_authority', 'text', 'trial_authority', true));
        addFormField(formFieldsDiv, createLabel('trial_level', '审级：'), createInput('trial_level', 'text', 'trial_level', true));
        addFormField(formFieldsDiv, createLabel('dispute_object', '诉讼（仲裁）争议标的：'), createTextArea('dispute_object', 'dispute_object', 4, 50, true));
    } else if (templateChoice === 'power_of_attorney') {
        addFormField(formFieldsDiv, createLabel('client_unit', '委托单位：'), createInput('client_unit', 'text', 'client_unit', true));
        addFormField(formFieldsDiv, createLabel('case', '案件：'), createInput('case', 'text', 'case', true));
        addFormField(formFieldsDiv, createLabel('case_reason', '案件原因：'), createInput('case_reason', 'text', 'case_reason', true));
        addFormField(formFieldsDiv, createLabel('date', '日期：'), createInput('date', 'date', 'date', true));
        
    } else if (templateChoice === 'contract') {
        addFormField(formFieldsDiv, createLabel('client_name', '客户名称：'), createInput('client_name', 'text', 'client_name', true));
        addFormField(formFieldsDiv, createLabel('client_gender', '客户性别：'), createInput('client_gender', 'text', 'client_gender', true));
        addFormField(formFieldsDiv, createLabel('client_id', '客户身份证号：'), createInput('client_id', 'text', 'client_id', true));
        addFormField(formFieldsDiv, createLabel('client_phone', '客户电话：'), createInput('client_phone', 'tel', 'client_phone', true));
        addFormField(formFieldsDiv, createLabel('client_email', '客户电子邮件：'), createInput('client_email', 'email', 'client_email', true));
        addFormField(formFieldsDiv, createLabel('client_address', '客户地址：'), createInput('client_address', 'text', 'client_address', true));
        addFormField(formFieldsDiv, createLabel('opposing_party_name', '对方当事人名称：'), createInput('opposing_party_name', 'text', 'opposing_party_name', true));
        addFormField(formFieldsDiv, createLabel('case_reason', '案件原因：'), createInput('case_reason', 'text', 'case_reason', true));
        addFormField(formFieldsDiv, createLabel('judicial_body', '司法机关：'), createInput('judicial_body', 'text', 'judicial_body', true));
        addFormField(formFieldsDiv, createLabel('judicial_level', '司法级别：'), createInput('judicial_level', 'text', 'judicial_level', true));
        addFormField(formFieldsDiv, createLabel('lawyer_fee', '律师费：'), createInput('lawyer_fee', 'number', 'lawyer_fee', true));
        addFormField(formFieldsDiv, createLabel('signing_date', '签署日期：'), createInput('signing_date', 'date', 'signing_date', true));
    }



}
let historyRecords = [];

document.getElementById('pdfForm').addEventListener('submit', function (event) {
    event.preventDefault();
    // 显示加载动画
    document.getElementById('loading').style.display = 'block';

    const templateChoice = document.getElementById('template_choice').value;
    
    let formData = new FormData();
    
    if (templateChoice === 'default') {
        formData = {
            template_choice: 'default',
            party_a: document.getElementById('party_a').value,
            party_b: document.getElementById('party_b').value,
            agreement_content: document.getElementById('agreement_content').value,
            margin: '2cm', 
            linespread: '1.5',
            font_size: '12pt'
        };
        console.log("Default Template Data:", formData);

    } else if (templateChoice === 'authorization_letter') {
        formData = {
            template_choice: 'authorization_letter',
            client_name: document.getElementById('client_name').value,
            lawyer_name: document.getElementById('lawyer_name').value,
            opposite_party_name: document.getElementById('opposite_party_name').value,
            position: document.getElementById('position').value,
            phone: document.getElementById('phone').value,
            case_name: document.getElementById('case_name').value,
            case_type: document.getElementById('case_type').value,
            c_permission: document.getElementById('c_permission').value,
            margin: '1in', 
            linespread: '1.5',
            font_size: '12pt'
        };
        console.log("Authorization Letter Template Data:", formData);
    } else if (templateChoice === 'legal_rep_identity') {
        formData = {
            template_choice: 'legal_rep_identity',
            rep_name: document.getElementById('rep_name').value,
            position: document.getElementById('position').value,
            unit_name: document.getElementById('unit_name').value,
            date: document.getElementById('date').value,
            address: document.getElementById('address').value,
            phone: document.getElementById('phone').value,
                    
        };
        console.log("Legal Representative Identity Certificate Data:", formData);
    }if (templateChoice === 'lawyer_agency_contract') {
        formData = {
            template_choice: 'lawyer_agency_contract',
            client_address: document.getElementById('client_address').value,
            client_postcode: document.getElementById('client_postcode').value,
            client_phone: document.getElementById('client_phone').value,
            opponent_name: document.getElementById('opponent_name').value,
            case_reason: document.getElementById('case_reason').value,
            trial_authority: document.getElementById('trial_authority').value,
            trial_level: document.getElementById('trial_level').value,
            dispute_object: document.getElementById('dispute_object').value,
                    
        };
        console.log("Lawyer Agency Contract Data:", formData);
    }if (templateChoice === 'power_of_attorney') {
        formData = {
            template_choice: 'power_of_attorney',
            client_unit: document.getElementById('client_unit').value,
            case: document.getElementById('case').value,
            case_reason: document.getElementById('case_reason').value,
            date: document.getElementById('date').value,
                    
        };
        console.log("Power of Attorney Template Data:", formData);
        
    }else if (templateChoice === 'contract') {
        formData = {
            template_choice: 'contract',
            client_name: document.getElementById('client_name').value,
            client_gender: document.getElementById('client_gender').value,
            client_id: document.getElementById('client_id').value,
            client_phone: document.getElementById('client_phone').value,
            client_email: document.getElementById('client_email').value,
            client_address: document.getElementById('client_address').value,
            opposing_party_name: document.getElementById('opposing_party_name').value,
            case_reason: document.getElementById('case_reason').value,
            judicial_body: document.getElementById('judicial_body').value,
            judicial_level: document.getElementById('judicial_level').value,
            lawyer_fee: document.getElementById('lawyer_fee').value,
            signing_date: document.getElementById('signing_date').value,
        };
        console.log("Contract Template Data:", formData);
    }

    // 显示PDF查看器
    var pdfViewer = document.getElementById('pdfViewer');
    pdfViewer.hidden = false;

    fetch('http://localhost:5000/generate_pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const pdfViewer = document.getElementById('pdfViewer');
        const downloadLink = document.getElementById('downloadLink');
        const successNotification = document.getElementById('successNotification');

        pdfViewer.src = url;
        pdfViewer.hidden = false;
        downloadLink.href = url;

        // 显示弹窗
        successNotification.style.display = 'block';

        // 设置3秒后自动隐藏弹窗
        setTimeout(() => {
            successNotification.style.display = 'none';
        }, 3000);

        // 存储历史记录
        const timestamp = new Date().toLocaleString();
        const templateName = document.getElementById('template_choice').options[document.getElementById('template_choice').selectedIndex].text;
        historyRecords.push({ 
            formData: Object.fromEntries(new FormData(document.getElementById('pdfForm')).entries()), 
            pdfUrl: url,
            timestamp: timestamp,
            templateName: templateName
        });
        updateSidebar(); // 更新侧边栏

        
        
        let downloadButton = document.getElementById('downloadPdfButton');
        if (!downloadButton) {
            downloadButton = document.createElement('a');
            downloadButton.id = 'downloadPdfButton';
            downloadButton.className = 'download-button'; 
            downloadButton.textContent = 'Download PDF';
            document.getElementById('pdfForm').appendChild(downloadButton);
        }
        downloadButton.href = url;
        downloadButton.download = templateChoice === 'default' ? 'agreement.pdf' : 
            (templateChoice === 'authorization_letter' ? 'authorization_letter.pdf' :
            (templateChoice === 'legal_rep_identity' ? 'legal_rep_identity.pdf' :
            (templateChoice === 'lawyer_agency_contract' ? 'lawyer_agency_contract.pdf' :
            (templateChoice === 'power_of_attorney' ? 'power_of_attorney.pdf' : 'document.pdf'))));
        // 隐藏加载动画
        document.getElementById('loading').style.display = 'none';

    })
    .catch((error) => {
        console.error('Error:', error);
        // 隐藏加载动画
        document.getElementById('loading').style.display = 'none';

        // 显示错误通知
        const errorNotification = document.getElementById('errorNotification');
        errorNotification.style.display = 'block';

        // 设置3秒后自动隐藏错误通知
        setTimeout(() => {
            errorNotification.style.display = 'none';
        }, 3000);
    });
});
function updateSidebar() {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = ''; // 清除现有列表

    historyRecords.forEach((record, index) => {
        const listItem = document.createElement('li');
        listItem.textContent = `${record.timestamp} - ${record.templateName}`;
        listItem.onclick = () => loadHistoryRecord(record);
        historyList.appendChild(listItem);
    });
}

function loadHistoryRecord(record) {
    const templateChoiceElement = document.getElementById('template_choice');
    if (templateChoiceElement && record.formData['template_choice']) {
        templateChoiceElement.value = record.formData['template_choice'];
        updateFormFields(); 
    }

    
    for (const key in record.formData) {
        const element = document.getElementById(key);
        if (element) {
            element.value = record.formData[key];
        }
    }

    
    const pdfViewer = document.getElementById('pdfViewer');
    pdfViewer.src = record.pdfUrl;
    pdfViewer.hidden = false;
    // 更新下载链接
    let downloadButton = document.getElementById('downloadPdfButton');
    if (!downloadButton) {
        downloadButton = document.createElement('a');
        downloadButton.id = 'downloadPdfButton';
        downloadButton.className = 'download-button'; 
        downloadButton.textContent = 'Download PDF';
        document.getElementById('pdfForm').appendChild(downloadButton);
    }
    downloadButton.href = record.pdfUrl;
    downloadButton.download = record.formData['template_choice'] === 'default' ? 'agreement.pdf' : 
        (record.formData['template_choice'] === 'authorization_letter' ? 'authorization_letter.pdf' :
        (record.formData['template_choice'] === 'legal_rep_identity' ? 'legal_rep_identity.pdf' :
        (record.formData['template_choice'] === 'lawyer_agency_contract' ? 'lawyer_agency_contract.pdf' :
        (record.formData['template_choice'] === 'power_of_attorney' ? 'power_of_attorney.pdf' : 'document.pdf'))));

}


window.onload = function() {
    updateFormFields(); 
};

