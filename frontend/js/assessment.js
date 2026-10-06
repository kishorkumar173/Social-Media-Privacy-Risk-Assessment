/**
 * Assessment Page Controller
 * Handles interactive questionnaire rendering, dynamic validation, demo loading,
 * API submission, Chart.js radar & bar visualizations, and results reporting.
 */

let allQuestions = [];
let allCategories = {};
let radarChartInstance = null;
let barChartInstance = null;
let currentAssessmentId = null;
let lastSubmittedResponses = {};

document.addEventListener('DOMContentLoaded', async () => {
    await initQuestionnaire();
    bindEvents();
});

async function initQuestionnaire() {
    try {
        const meta = await PrivacyAPI.getQuestions();
        if (!meta.success) throw new Error("Could not fetch questions.");

        allQuestions = meta.questions;
        allCategories = meta.categories;

        renderCategoryNavigation();
        renderQuestions();
        updateProgress();
    } catch (err) {
        document.getElementById('questionsContainer').innerHTML = `
            <div class="card" style="border-color: #ef4444; color: #f87171;">
                <i class="bi bi-exclamation-triangle-fill"></i> Error initializing questionnaire: ${err.message}
            </div>
        `;
    }
}

function renderCategoryNavigation() {
    const navContainer = document.getElementById('categoryNavList');
    navContainer.innerHTML = '';

    Object.values(allCategories).forEach(cat => {
        const item = document.createElement('div');
        item.className = 'cat-nav-item';
        item.dataset.catId = cat.id;
        item.innerHTML = `
            <span><i class="bi ${cat.icon || 'bi-shield'}"></i> ${cat.name}</span>
            <span style="font-size: 0.7rem; color: var(--text-muted); font-weight: 600;">${Math.round(cat.weight * 100)}%</span>
        `;
        item.addEventListener('click', () => {
            const targetEl = document.getElementById(`section-${cat.id}`);
            if (targetEl) {
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
        navContainer.appendChild(item);
    });
}

function renderQuestions() {
    const container = document.getElementById('questionsContainer');
    container.innerHTML = '';

    // Group questions by category
    const grouped = {};
    Object.keys(allCategories).forEach(cid => grouped[cid] = []);
    allQuestions.forEach(q => {
        if (!grouped[q.category]) grouped[q.category] = [];
        grouped[q.category].push(q);
    });

    Object.keys(grouped).forEach(catId => {
        const catMeta = allCategories[catId];
        const section = document.createElement('div');
        section.id = `section-${catId}`;
        section.style.marginBottom = '2.5rem';

        // Section header
        section.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
                <i class="bi ${catMeta.icon || 'bi-shield'}" style="font-size: 1.3rem; color: var(--accent-cyan);"></i>
                <div>
                    <h3 style="font-size: 1.15rem; color: #fff; font-weight: 700;">${catMeta.name}</h3>
                    <p style="font-size: 0.8rem; color: var(--text-muted);">${catMeta.description} (Weight: ${Math.round(catMeta.weight * 100)}%)</p>
                </div>
            </div>
        `;

        grouped[catId].forEach((q, idx) => {
            const card = document.createElement('div');
            card.className = 'question-card';
            card.id = `card-${q.id}`;

            let optionsHtml = '';
            q.options.forEach(opt => {
                optionsHtml += `
                    <label class="option-label" id="label-${q.id}-${opt.value}">
                        <input type="radio" name="${q.id}" value="${opt.value}" required>
                        <span>${opt.label}</span>
                    </label>
                `;
            });

            card.innerHTML = `
                <div class="question-header">
                    <div class="question-text">${q.id.toUpperCase()}. ${q.text}</div>
                    <span class="question-tag">${catMeta.name}</span>
                </div>
                <div class="options-group">
                    ${optionsHtml}
                </div>
                <div class="question-tip">
                    <i class="bi bi-lightbulb-fill" style="color: var(--accent-cyan);"></i>
                    <span><strong>Security Rationale:</strong> ${q.tip}</span>
                </div>
            `;

            section.appendChild(card);
        });

        container.appendChild(section);
    });

    // Add radio change listener to update styles and progress
    container.addEventListener('change', (e) => {
        if (e.target.type === 'radio') {
            const qid = e.target.name;
            const labels = document.querySelectorAll(`[id^="label-${qid}-"]`);
            labels.forEach(lbl => lbl.classList.remove('selected'));
            const selectedLabel = document.getElementById(`label-${qid}-${e.target.value}`);
            if (selectedLabel) selectedLabel.classList.add('selected');
            updateProgress();
        }
    });
}

function updateProgress() {
    const answeredCount = document.querySelectorAll('#assessmentForm input[type="radio"]:checked').length;
    const totalCount = allQuestions.length;
    const pct = Math.round((answeredCount / (totalCount || 1)) * 100);

    const bar = document.getElementById('progressBar');
    const txt = document.getElementById('progressText');
    if (bar) bar.style.width = `${pct}%`;
    if (txt) txt.textContent = `${answeredCount} / ${totalCount} Answered (${pct}%)`;
}

function bindEvents() {
    // 1. Submit Form
    const form = document.getElementById('assessmentForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleSubmit();
    });

    // 2. Load High Risk Demo Profile
    document.getElementById('btnLoadHighRisk').addEventListener('click', async () => {
        const demo = await PrivacyAPI.getDemoProfile();
        if (demo.success) {
            populateResponses(demo.responses);
        }
    });

    // 3. Load Hardened Profile
    document.getElementById('btnLoadSecure').addEventListener('click', () => {
        const secureResponses = {};
        allQuestions.forEach(q => {
            const best = q.options.reduce((prev, curr) => (prev.risk_points < curr.risk_points) ? prev : curr);
            secureResponses[q.id] = best.value;
        });
        populateResponses(secureResponses);
    });

    // 4. Reset Form
    document.getElementById('btnResetForm').addEventListener('click', () => {
        form.reset();
        document.querySelectorAll('.option-label').forEach(lbl => lbl.classList.remove('selected'));
        updateProgress();
        document.getElementById('resultsContainer').style.display = 'none';
    });

    // 5. Launch Simulator with this Data
    document.getElementById('btnLaunchSimulatorWithData').addEventListener('click', () => {
        sessionStorage.setItem('simulator_baseline_responses', JSON.stringify(lastSubmittedResponses));
        window.location.href = '/simulator';
    });

    // 6. Delete Assessment (Right to Erasure)
    document.getElementById('btnDeleteAssessment').addEventListener('click', async () => {
        if (!currentAssessmentId) return;
        if (confirm(`Permanently erase assessment ${currentAssessmentId} from the database? This cannot be undone.`)) {
            const res = await PrivacyAPI.deleteAssessment(currentAssessmentId);
            if (res.success) {
                alert(`Assessment ${currentAssessmentId} successfully deleted.`);
                document.getElementById('resultsContainer').style.display = 'none';
                currentAssessmentId = null;
            }
        }
    });
}

function populateResponses(responses) {
    Object.entries(responses).forEach(([qid, val]) => {
        const input = document.querySelector(`input[name="${qid}"][value="${val}"]`);
        if (input) {
            input.checked = true;
            const labels = document.querySelectorAll(`[id^="label-${qid}-"]`);
            labels.forEach(lbl => lbl.classList.remove('selected'));
            const selectedLabel = document.getElementById(`label-${qid}-${val}`);
            if (selectedLabel) selectedLabel.classList.add('selected');
        }
    });
    updateProgress();
}

async function handleSubmit() {
    const formData = new FormData(document.getElementById('assessmentForm'));
    const responses = {};
    for (let [key, val] of formData.entries()) {
        responses[key] = val;
    }

    lastSubmittedResponses = responses;

    const btn = document.getElementById('btnSubmitAssessment');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<i class="bi bi-arrow-repeat spin"></i> Evaluating Privacy Risks...`;
    btn.disabled = true;

    try {
        const result = await PrivacyAPI.submitAssessment(responses);
        if (!result.success) throw new Error(result.errors ? result.errors.join(", ") : "Assessment failed.");

        currentAssessmentId = result.assessment_id;
        displayResults(result.data, result.assessment_id);
    } catch (err) {
        alert("Evaluation Error: " + err.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function displayResults(data, assessmentId) {
    const container = document.getElementById('resultsContainer');
    container.style.display = 'block';

    // 1. Score and Tier
    const scoreValEl = document.getElementById('resScoreValue');
    const meterEl = document.getElementById('resScoreMeter');
    const badgeEl = document.getElementById('resRiskTierBadge');
    const descEl = document.getElementById('resRiskTierDesc');

    const score = data.overall_score;
    const tier = data.risk_level;
    const color = data.color || '#ef4444';

    scoreValEl.textContent = score;
    scoreValEl.style.color = color;
    meterEl.style.width = `${score}%`;
    meterEl.style.background = color;

    badgeEl.textContent = tier;
    badgeEl.className = `badge badge-${tier === 'CRITICAL' ? 'crit' : (tier === 'HIGH' ? 'high' : (tier === 'MODERATE' ? 'mod' : 'low'))}`;
    descEl.textContent = data.description;

    // Report Links
    document.getElementById('btnViewHtmlReport').href = `/api/assessment/${assessmentId}/report.html`;
    document.getElementById('btnDownloadPdfReport').href = `/api/assessment/${assessmentId}/report.pdf`;

    // 2. Charts
    renderCategoryCharts(data.category_scores);

    // 3. Findings
    renderFindings(data.findings);

    // 4. Recommendations
    renderRecommendations(data.recommendations);

    // Scroll smoothly to results
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderCategoryCharts(catScores) {
    const labels = Object.values(catScores).map(c => c.name);
    const scores = Object.values(catScores).map(c => c.score);
    const colors = Object.values(catScores).map(c => c.color || '#3b82f6');

    // Radar Chart
    const radarCtx = document.getElementById('categoryRadarChart').getContext('2d');
    if (radarChartInstance) radarChartInstance.destroy();

    radarChartInstance = new Chart(radarCtx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Category Risk (0-100)',
                data: scores,
                backgroundColor: 'rgba(239, 68, 68, 0.2)',
                borderColor: '#ef4444',
                pointBackgroundColor: '#ef4444',
                pointBorderColor: '#fff',
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
                    pointLabels: { color: '#94a3b8', font: { size: 10 } },
                    ticks: { display: false, min: 0, max: 100 }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    // Bar Chart
    const barCtx = document.getElementById('categoryBarChart').getContext('2d');
    if (barChartInstance) barChartInstance.destroy();

    barChartInstance = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Risk Score',
                data: scores,
                backgroundColor: colors,
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    min: 0,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.08)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#cbd5e1', font: { size: 11 } }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderFindings(findings) {
    const list = document.getElementById('findingsList');
    list.innerHTML = '';

    if (!findings || findings.length === 0) {
        list.innerHTML = `<div style="color: #10b981; font-size: 0.9rem;"><i class="bi bi-shield-check"></i> No critical vulnerabilities detected.</div>`;
        return;
    }

    findings.forEach(f => {
        const item = document.createElement('div');
        const badgeClass = f.severity === 'CRITICAL' ? 'badge-crit' : (f.severity === 'HIGH' ? 'badge-high' : 'badge-mod');
        item.style.padding = '0.85rem';
        item.style.background = 'var(--bg-secondary)';
        item.style.border = '1px solid var(--border-color)';
        item.style.borderRadius = '6px';

        item.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                <strong style="color: #fff; font-size: 0.9rem;">${f.title}</strong>
                <span class="badge ${badgeClass}">${f.severity}</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.35rem;">${f.description}</p>
            <div style="font-size: 0.75rem; color: var(--text-muted);"><i class="bi bi-arrow-right-short text-cyan"></i> <strong>Impact:</strong> ${f.risk_impact}</div>
        `;
        list.appendChild(item);
    });
}

function renderRecommendations(recommendations) {
    const list = document.getElementById('recommendationsList');
    list.innerHTML = '';

    if (!recommendations || recommendations.length === 0) {
        list.innerHTML = `<div style="color: #10b981; font-size: 0.9rem;"><i class="bi bi-check-all"></i> Account meets established privacy best practices.</div>`;
        return;
    }

    recommendations.forEach(r => {
        const item = document.createElement('div');
        const badgeClass = r.priority === 'IMMEDIATE' ? 'badge-crit' : (r.priority === 'IMPORTANT' ? 'badge-high' : 'badge-mod');
        const stepsHtml = r.steps.map(s => `<li>${s}</li>`).join('');

        item.style.padding = '0.85rem';
        item.style.background = 'var(--bg-secondary)';
        item.style.border = '1px solid var(--border-color)';
        item.style.borderRadius = '6px';

        item.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                <strong style="color: #60a5fa; font-size: 0.9rem;">${r.action}</strong>
                <span class="badge ${badgeClass}">${r.priority}</span>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.5rem;">${r.rationale}</p>
            <ol style="padding-left: 1.25rem; font-size: 0.775rem; color: var(--text-muted);">
                ${stepsHtml}
            </ol>
        `;
        list.appendChild(item);
    });
}
