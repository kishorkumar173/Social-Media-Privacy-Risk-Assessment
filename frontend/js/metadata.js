/**
 * Metadata Inspector Controller
 * Facilitates safe, local EXIF inspection and metadata stripping.
 */

let selectedFile = null;

document.addEventListener('DOMContentLoaded', () => {
    bindMetadataEvents();
});

function bindMetadataEvents() {
    const dropZone = document.getElementById('dropZone');
    const imageInput = document.getElementById('imageInput');
    const btnInspect = document.getElementById('btnInspect');
    const btnStrip = document.getElementById('btnStrip');

    dropZone.addEventListener('click', () => imageInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--accent-cyan)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'var(--border-color)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border-color)';
        if (e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    imageInput.addEventListener('change', () => {
        if (imageInput.files.length > 0) {
            handleFileSelection(imageInput.files[0]);
        }
    });

    btnInspect.addEventListener('click', async () => {
        await executeInspection();
    });

    btnStrip.addEventListener('click', async () => {
        await executeStripping();
    });
}

function handleFileSelection(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file (JPEG, PNG, WEBP).');
        return;
    }

    selectedFile = file;
    document.getElementById('fileInfoBox').style.display = 'block';
    document.getElementById('selectedFileName').textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
    document.getElementById('btnInspect').disabled = false;
    document.getElementById('btnStrip').disabled = false;
}

async function executeInspection() {
    if (!selectedFile) return;

    const btn = document.getElementById('btnInspect');
    btn.innerHTML = `<i class="bi bi-arrow-repeat spin"></i> Inspecting...`;
    btn.disabled = true;

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
        const res = await PrivacyAPI.inspectImageMetadata(formData);
        if (!res.success) throw new Error(res.error || "Inspection failed.");

        renderInspectionResults(res.results);
    } catch (err) {
        alert("Metadata Inspection Error: " + err.message);
    } finally {
        btn.innerHTML = `<i class="bi bi-search"></i> Inspect Metadata`;
        btn.disabled = false;
    }
}

function renderInspectionResults(results) {
    const badge = document.getElementById('exifStatusBadge');
    const alertsBox = document.getElementById('leakAlertsContainer');
    const gpsBox = document.getElementById('gpsDataBox');
    const tbody = document.getElementById('metadataTableBody');

    // 1. Status badge
    if (results.has_exif) {
        badge.textContent = 'EXIF DETECTED';
        badge.className = 'badge badge-crit';
    } else {
        badge.textContent = 'CLEAN / NO EXIF';
        badge.className = 'badge badge-low';
    }

    // 2. Leak Alerts
    alertsBox.innerHTML = '';
    if (results.privacy_leak_warnings && results.privacy_leak_warnings.length > 0) {
        alertsBox.style.display = 'block';
        results.privacy_leak_warnings.forEach(w => {
            const alertEl = document.createElement('div');
            alertEl.style.padding = '0.75rem';
            alertEl.style.background = 'rgba(239, 68, 68, 0.15)';
            alertEl.style.border = '1px solid rgba(239, 68, 68, 0.4)';
            alertEl.style.borderRadius = '6px';
            alertEl.style.fontSize = '0.8rem';
            alertEl.style.color = '#fca5a5';
            alertEl.style.marginBottom = '0.5rem';
            alertEl.innerHTML = `<i class="bi bi-exclamation-triangle-fill" style="color: #ef4444;"></i> ${w}`;
            alertsBox.appendChild(alertEl);
        });
    } else {
        alertsBox.style.display = 'none';
    }

    // 3. GPS Display
    if (results.gps_data) {
        gpsBox.style.display = 'block';
        document.getElementById('gpsCoordsText').textContent = 
            `Latitude: ${results.gps_data.latitude}, Longitude: ${results.gps_data.longitude}`;
    } else {
        gpsBox.style.display = 'none';
    }

    // 4. Metadata Table
    tbody.innerHTML = '';
    const entries = Object.entries(results.metadata || {});
    if (entries.length === 0) {
        tbody.innerHTML = `<tr><td colspan="2" style="text-align: center; color: #10b981; padding: 2rem;">No EXIF metadata tags found in this file.</td></tr>`;
        return;
    }

    entries.forEach(([key, val]) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong style="color: #cbd5e1; font-family: var(--font-mono); font-size: 0.8rem;">${key}</strong></td>
            <td style="color: var(--text-secondary); word-break: break-all; font-size: 0.8rem;">${val}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function executeStripping() {
    if (!selectedFile) return;

    const btn = document.getElementById('btnStrip');
    btn.innerHTML = `<i class="bi bi-arrow-repeat spin"></i> Sanitizing...`;
    btn.disabled = true;

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('format', 'PNG');

    try {
        const res = await fetch('/api/metadata/strip', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) throw new Error("Stripping failed on server.");

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sanitized_${selectedFile.name.split('.')[0]}.png`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();

        alert("Metadata successfully stripped! Sanitized image downloaded.");
    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        btn.innerHTML = `<i class="bi bi-shield-x"></i> Strip & Download`;
        btn.disabled = false;
    }
}
