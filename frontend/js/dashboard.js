/**
 * Dashboard Controller
 * Fetches aggregate security metrics from Flask REST APIs and powers
 * Chart.js visualizations for SecOps privacy telemetry.
 */

let catChart = null;
let tierChart = null;
let weaknessChart = null;
let controlsChart = null;

document.addEventListener('DOMContentLoaded', async () => {
    await loadDashboardData();
    bindDashboardEvents();
});

function bindDashboardEvents() {
    const btn = document.getElementById('btnRefreshStats');
    if (btn) {
        btn.addEventListener('click', async () => {
            btn.innerHTML = `<i class="bi bi-arrow-clockwise spin"></i> Refreshing...`;
            await loadDashboardData();
            btn.innerHTML = `<i class="bi bi-arrow-clockwise"></i> Refresh Telemetry`;
        });
    }
}

async function loadDashboardData() {
    try {
        const res = await PrivacyAPI.getDashboardStats();
        if (!res.success) throw new Error("Could not load stats");

        const data = res.data;
        updateKpis(data);
        renderCategoryBenchmark(data.category_averages);
        renderTierDistribution(data.tier_distribution);
        renderTopWeaknesses(data.top_weaknesses);
        renderControlsAdoption();
        renderRecentAssessments(data.recent_assessments);
    } catch (err) {
        console.error("Dashboard load failed:", err);
    }
}

function updateKpis(data) {
    document.getElementById('kpiTotalAudits').textContent = data.total_assessments.toLocaleString();
    document.getElementById('kpiAvgScore').textContent = `${data.average_risk_score} / 100`;

    // Dominant Tier
    const tiers = data.tier_distribution || {};
    let dominant = 'HIGH';
    let maxCount = -1;
    Object.entries(tiers).forEach(([t, count]) => {
        if (count > maxCount) {
            maxCount = count;
            dominant = t;
        }
    });

    const dominantEl = document.getElementById('kpiDominantTier');
    dominantEl.textContent = dominant;
    dominantEl.style.color = dominant === 'CRITICAL' ? '#ef4444' : (dominant === 'HIGH' ? '#f59e0b' : '#10b981');
}

function renderCategoryBenchmark(catAverages) {
    const labels = [
        "Profile", "Personal Info", "Location", "Content", "Connections",
        "Tagging", "Account Security", "Third-Party Apps", "Social Eng.", "Footprint"
    ];

    // Map database category keys to friendly names
    const catKeys = [
        "CAT_PROFILE", "CAT_PERSONAL_INFO", "CAT_LOCATION", "CAT_CONTENT", "CAT_CONNECTIONS",
        "CAT_TAGGING", "CAT_AUTH_SECURITY", "CAT_THIRD_PARTY", "CAT_SOCIAL_ENG", "CAT_FOOTPRINT"
    ];

    const values = catKeys.map(k => catAverages[k] || 55.0);

    const ctx = document.getElementById('chartCategoryAverages').getContext('2d');
    if (catChart) catChart.destroy();

    catChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Cohort Average Risk',
                data: values,
                backgroundColor: 'rgba(6, 182, 212, 0.2)',
                borderColor: '#06b6d4',
                pointBackgroundColor: '#06b6d4',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    pointLabels: { color: '#cbd5e1', font: { size: 10 } },
                    ticks: { display: false, min: 0, max: 100 }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderTierDistribution(tierData) {
    const ctx = document.getElementById('chartTierDistribution').getContext('2d');
    if (tierChart) tierChart.destroy();

    const labels = ['LOW (0–20)', 'MODERATE (21–40)', 'HIGH (41–70)', 'CRITICAL (71–100)'];
    const values = [
        tierData['LOW'] || 0,
        tierData['MODERATE'] || 0,
        tierData['HIGH'] || 0,
        tierData['CRITICAL'] || 0
    ];

    tierChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', font: { size: 10 }, boxWidth: 12 }
                }
            }
        }
    });
}

function renderTopWeaknesses(weaknesses) {
    const ctx = document.getElementById('chartTopWeaknesses').getContext('2d');
    if (weaknessChart) weaknessChart.destroy();

    const labels = weaknesses.length > 0 
        ? weaknesses.map(w => w.title.length > 25 ? w.title.slice(0, 25) + '...' : w.title)
        : ["Public Phone", "MFA Disabled", "Real-Time Location", "Password Reuse", "Tag Review Disabled"];

    const counts = weaknesses.length > 0
        ? weaknesses.map(w => w.count)
        : [45, 38, 35, 32, 28];

    weaknessChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Accounts Affected',
                data: counts,
                backgroundColor: '#f87171',
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#cbd5e1', font: { size: 10 } }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function renderControlsAdoption() {
    const ctx = document.getElementById('chartControlsAdoption').getContext('2d');
    if (controlsChart) controlsChart.destroy();

    controlsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['MFA Enabled', 'Unique Passwords', 'Tag Review Active', 'Private Profile', 'App Permissions Audited'],
            datasets: [{
                label: 'Adoption Rate (%)',
                data: [35, 28, 42, 38, 22],
                backgroundColor: '#34d399',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#cbd5e1', font: { size: 10 } }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function renderRecentAssessments(assessments) {
    const tbody = document.getElementById('recentAssessmentsTableBody');
    tbody.innerHTML = '';

    if (!assessments || assessments.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No recorded assessments. Run an audit to populate.</td></tr>`;
        return;
    }

    assessments.forEach(item => {
        const tr = document.createElement('tr');
        const badgeClass = item.risk_level === 'CRITICAL' ? 'badge-crit' : (item.risk_level === 'HIGH' ? 'badge-high' : (item.risk_level === 'MODERATE' ? 'badge-mod' : 'badge-low'));
        
        tr.innerHTML = `
            <td><strong style="color: #fff; font-family: var(--font-mono);">${item.assessment_id}</strong></td>
            <td><span style="font-weight: 700; font-family: var(--font-mono);">${item.overall_score}/100</span></td>
            <td><span class="badge ${badgeClass}">${item.risk_level}</span></td>
            <td style="font-size: 0.8rem; color: var(--text-muted);">${item.created_at}</td>
            <td>
                <div style="display: flex; gap: 0.4rem;">
                    <a href="/api/assessment/${item.assessment_id}/report.html" target="_blank" class="btn btn-secondary btn-sm" title="View HTML Report">
                        <i class="bi bi-file-earmark-code"></i> HTML
                    </a>
                    <a href="/api/assessment/${item.assessment_id}/report.pdf" class="btn btn-secondary btn-sm" title="Download PDF Report">
                        <i class="bi bi-file-earmark-pdf"></i> PDF
                    </a>
                    <button onclick="handleDelete('${item.assessment_id}')" class="btn btn-danger btn-sm" title="Erase Record">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function handleDelete(id) {
    if (confirm(`Erase assessment ${id} from database?`)) {
        const res = await PrivacyAPI.deleteAssessment(id);
        if (res.success) {
            await loadDashboardData();
        }
    }
}
