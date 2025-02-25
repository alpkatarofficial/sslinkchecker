let websites = [
    { url: 'linkdijital.com.tr', status: 'Pending', remainingTime: 'N/A' },
    { url: 'apro.com.tr', status: 'Pending', remainingTime: 'N/A' },
    { url: 'istpaz.com.tr', status: 'Pending', remainingTime: 'N/A' }, 
    { url: 'agiglobal.com.tr', status: 'Pending', remainingTime: 'N/A' }, 
    { url: 'rapoo-tr.com', status: 'Pending', remainingTime: 'N/A' }, 
    { url: 'ngtech.com.tr', status: 'Pending', remainingTime: 'N/A' }, 
    { url: 'secreto.com.tr', status: 'Pending', remainingTime: 'N/A' }, 
    { url: 'agaranti.com.tr', status: 'Pending', remainingTime: 'N/A' }, 
    { url: 'sinerjibt.com', status: 'Pending', remainingTime: 'N/A' }, 
    { url: 'jforce.com.tr', status: 'Pending', remainingTime: 'N/A' }
];

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

function requestNotificationPermission() {
    if (Notification.permission !== 'granted') {
        Notification.requestPermission().then(permission => {
            if (permission !== 'granted') {
                console.warn('Notification permission not granted');
            }
        });
    }
}

function showNotification(title, message) {
    if (Notification.permission === 'granted') {
        new Notification(title, { body: message });
    }
}

function checkCertificate(index) {
    const website = websites[index].url;
    fetch(`/check_ssl?url=${encodeURIComponent(website)}`)
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
                showNotification('SSL Certificate Alert', `The SSL certificate for ${website} needs to be renewed.`);
            } else if (data.valid) {
                statusCell.innerHTML = '<span class="status-valid">Valid</span>';
            } else {
                statusCell.innerHTML = '<span class="status-invalid">Invalid</span>';
                showNotification('SSL Certificate Alert', `The SSL certificate for ${website} is invalid.`);
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
        row.insertCell(0).innerHTML = `<a style="color:#ffffff;" href="https://${website.url}" target="_blank">${website.url}</a>`;
        row.insertCell(1).innerHTML = `<span id="status-${index}">${website.status}</span>`;
        row.insertCell(2).innerHTML = `<span id="remaining-time-${index}">${website.remainingTime}</span>`;
        row.insertCell(3).innerHTML = `
            <button onclick="checkCertificate(${index})">Check</button>
            <button onclick="deleteWebsite(${index})">Delete</button>
        `;
    });
}

window.onload = function() {
    requestNotificationPermission();
    updateTable();
    websites.forEach((_, index) => checkCertificate(index));
};
