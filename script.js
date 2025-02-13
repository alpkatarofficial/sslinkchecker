let websites = [];

function addWebsite() {
    const urlInput = document.getElementById('urlInput');
    const url = urlInput.value.trim();
    if (url) {
        websites.push({ url, status: 'Pending', remainingTime: 'N/A' });
        updateTable();
        urlInput.value = '';
    }
}

function deleteWebsite(index) {
    websites.splice(index, 1);
    updateTable();
}

function checkCertificate(index) {
    const website = websites[index].url;
    fetch(`http://127.0.0.1:8000/check_ssl?url=${website}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const statusCell = document.getElementById(`status-${index}`);
            const remainingTimeCell = document.getElementById(`remaining-time-${index}`);
            if (data.renew) {
                statusCell.innerHTML = '<span class="status-renew">Renew SSL</span>';
            } else if (data.valid) {
                statusCell.innerHTML = '<span class="status-valid">Valid</span>';
            } else {
                statusCell.innerHTML = '<span class="status-invalid">Invalid</span>';
            }
            remainingTimeCell.innerHTML = data.remaining_time || 'N/A';
            websites[index].status = statusCell.innerHTML;
            websites[index].remainingTime = remainingTimeCell.innerHTML;
        })
        .catch(error => {
            console.error('Fetch error:', error);
            const statusCell = document.getElementById(`status-${index}`);
            statusCell.innerHTML = `<span class="status-invalid">Error: ${error.message}</span>`;
            websites[index].status = statusCell.innerHTML;
        });
}

function updateTable() {
    const tableBody = document.getElementById('websitesTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
    websites.forEach((website, index) => {
        const row = tableBody.insertRow();
        row.insertCell(0).innerHTML = `<a style="color:#ffffff;"href="https://${website.url}" target="_blank">${website.url}</a>`;
        row.insertCell(1).innerHTML = `<span id="status-${index}">${website.status}</span>`;
        row.insertCell(2).innerHTML = `<span id="remaining-time-${index}">${website.remainingTime}</span>`;
        row.insertCell(3).innerHTML = `
            <button onclick="checkCertificate(${index})">Check</button>
            <button onclick="deleteWebsite(${index})">Delete</button>
        `;
    });
}