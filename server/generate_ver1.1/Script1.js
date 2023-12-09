
function createLabel(inputId, text) {
    var label = document.createElement('label');
    label.setAttribute('for', inputId);
    label.textContent = text;
    return label;
}

function createInput(inputId, inputType, name, required, placeholder = '') {
    var input = document.createElement('input');
    input.setAttribute('type', inputType);
    input.setAttribute('id', inputId);
    input.setAttribute('name', name);
    if (required) input.required = true;
    if (placeholder && inputType === 'date') input.setAttribute('placeholder', '年/月/日'); 
    return input;
}



function createTextArea(inputId, name, rows, cols, required) {
    var textarea = document.createElement('textarea');
    textarea.setAttribute('id', inputId);
    textarea.setAttribute('name', name);
    textarea.setAttribute('rows', rows);
    textarea.setAttribute('cols', cols);
    if (required) textarea.required = true;
    return textarea;
}


function updateFormFields() {
    var templateChoice = document.getElementById('template_choice').value;
    var formFieldsDiv = document.getElementById('formFields');
            
            
    while (formFieldsDiv.firstChild) {
        formFieldsDiv.removeChild(formFieldsDiv.firstChild);
    }

    
    if (templateChoice === 'default') {
                
        formFieldsDiv.appendChild(createLabel('party_a', 'Party A:'));
        formFieldsDiv.appendChild(createInput('party_a', 'text', 'party_a', true));

        formFieldsDiv.appendChild(createLabel('party_b', 'Party B:'));
        formFieldsDiv.appendChild(createInput('party_b', 'text', 'party_b', true));

        formFieldsDiv.appendChild(createLabel('agreement_content', 'Agreement Content:'));
        formFieldsDiv.appendChild(createTextArea('agreement_content', 'agreement_content', 4, 50, true));

                
    } else if (templateChoice === 'authorization_letter') {
                
        formFieldsDiv.appendChild(createLabel('client_name', '委托人：'));
        formFieldsDiv.appendChild(createInput('client_name', 'text', 'client_name', true));

                
        formFieldsDiv.appendChild(createLabel('attorney_name', '受委托人姓名：'));
        formFieldsDiv.appendChild(createInput('attorney_name', 'text', 'attorney_name', true));

        formFieldsDiv.appendChild(createLabel('work_unit', '工作单位：'));
        formFieldsDiv.appendChild(createInput('work_unit', 'text', 'work_unit', false));

        formFieldsDiv.appendChild(createLabel('position', '职务：'));
        formFieldsDiv.appendChild(createInput('position', 'text', 'position', false));

        formFieldsDiv.appendChild(createLabel('phone', '电话：'));
        formFieldsDiv.appendChild(createInput('phone', 'tel', 'phone', false));

                
        formFieldsDiv.appendChild(createLabel('case_name', '案件：'));
        formFieldsDiv.appendChild(createInput('case_name', 'text', 'case_name', true));

                
        formFieldsDiv.appendChild(createLabel('case_reason', '案件原因：'));
        formFieldsDiv.appendChild(createInput('case_reason', 'text', 'case_reason', true));

                
        formFieldsDiv.appendChild(createLabel('agent_power', '代理权限：'));
        formFieldsDiv.appendChild(createTextArea('agent_power', 'agent_power', 4, 50, true));
    }else if (templateChoice === 'legal_rep_identity') {
        formFieldsDiv.appendChild(createLabel('rep_name', '代表人姓名：'));
        formFieldsDiv.appendChild(createInput('rep_name', 'text', 'rep_name', true));

        formFieldsDiv.appendChild(createLabel('position', '职务：'));
        formFieldsDiv.appendChild(createInput('position', 'text', 'position', true));

        formFieldsDiv.appendChild(createLabel('unit_name', '单位全称：'));
        formFieldsDiv.appendChild(createInput('unit_name', 'text', 'unit_name', true));

        formFieldsDiv.appendChild(createLabel('date', '日期：'));
        formFieldsDiv.appendChild(createInput('date', 'date', 'date', true));

        formFieldsDiv.appendChild(createLabel('address', '地址：'));
        formFieldsDiv.appendChild(createInput('address', 'text', 'address', true));

        formFieldsDiv.appendChild(createLabel('phone', '电话：'));
        formFieldsDiv.appendChild(createInput('phone', 'tel', 'phone', true));
    }if (templateChoice === 'lawyer_agency_contract') {
        formFieldsDiv.appendChild(createLabel('client_address', '甲方地址：'));
        formFieldsDiv.appendChild(createInput('client_address', 'text', 'client_address', true));

        formFieldsDiv.appendChild(createLabel('client_postcode', '邮政编码：'));
        formFieldsDiv.appendChild(createInput('client_postcode', 'text', 'client_postcode', true));

        formFieldsDiv.appendChild(createLabel('client_phone', '电话：'));
        formFieldsDiv.appendChild(createInput('client_phone', 'tel', 'client_phone', true));

        formFieldsDiv.appendChild(createLabel('opponent_name', '对方当事人名称或者姓名：'));
        formFieldsDiv.appendChild(createInput('opponent_name', 'text', 'opponent_name', true));

        formFieldsDiv.appendChild(createLabel('case_reason', '案由：'));
        formFieldsDiv.appendChild(createInput('case_reason', 'text', 'case_reason', true));

        formFieldsDiv.appendChild(createLabel('trial_authority', '审理机关：'));
        formFieldsDiv.appendChild(createInput('trial_authority', 'text', 'trial_authority', true));

        formFieldsDiv.appendChild(createLabel('trial_level', '审级：'));
        formFieldsDiv.appendChild(createInput('trial_level', 'text', 'trial_level', true));

        formFieldsDiv.appendChild(createLabel('dispute_object', '诉讼（仲裁）争议标的：'));
        formFieldsDiv.appendChild(createTextArea('dispute_object', 'dispute_object', 4, 50, true));
    }if (templateChoice === 'power_of_attorney') {
                
        formFieldsDiv.appendChild(createLabel('client_unit', '委托单位：'));
        formFieldsDiv.appendChild(createInput('client_unit', 'text', 'client_unit', true));

        formFieldsDiv.appendChild(createLabel('case', '案件：'));
        formFieldsDiv.appendChild(createInput('case', 'text', 'case', true));

        formFieldsDiv.appendChild(createLabel('case_reason', '案件原因：'));
        formFieldsDiv.appendChild(createInput('case_reason', 'text', 'case_reason', true));

        formFieldsDiv.appendChild(createLabel('date', '日期：'));
        formFieldsDiv.appendChild(createInput('date', 'date', 'date', true));
    }


}
let historyRecords = [];

document.getElementById('pdfForm').addEventListener('submit', function (event) {
    event.preventDefault();
    
    const templateChoice = document.getElementById('template_choice').value;
    let formData = {};

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
            attorney_name: document.getElementById('attorney_name').value,
            work_unit: document.getElementById('work_unit').value,
            position: document.getElementById('position').value,
            phone: document.getElementById('phone').value,
            case_name: document.getElementById('case_name').value,
            case_reason: document.getElementById('case_reason').value,
            agent_power: document.getElementById('agent_power').value,
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
        
    }


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
        pdfViewer.src = url;
        pdfViewer.hidden = false;
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
    })
    .catch((error) => {
        console.error('Error:', error);
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

