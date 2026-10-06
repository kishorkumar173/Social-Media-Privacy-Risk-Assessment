/**
 * Privacy Hardening Simulator Controller
 * Evaluates real-time speculative score delta and updates Chart.js before/after comparisons.
 */

let baselineResponses = null;
let availableActions = {};
let comparisonChart = null;

document.addEventListener('DOMContentLoaded', async () => {
    await initSimulator();
    bindSimulatorEvents();
});

async function initSimulator() {
    // 1. Check for stored baseline from assessment page or fall back to high-risk demo
    const stored = sessionStorage.getItem('simulator_baseline_responses');
    if (stored) {
        try {
            baselineResponses = JSON.parse(stored);
        } catch (e) {
            baselineResponses = null;
        }
    }

    if (!baselineResponses) {
        const demo = await PrivacyAPI.getDemoProfile();
        baselineResponses = demo.responses;
    }

    // 2. Fetch available actions
    const actRes = await PrivacyAPI.getSimulationActions();
    if (actRes.success) {
        availableActions = actRes.actions;
        renderToggles();
        // Run initial simulation with default high-impact fixes preselected
        const defaultSelected = ["enable_mfa", "hide_phone", "stop_realtime_location", "enable_tag_review"];
        setSelectedToggles(defaultSelected);
        await runSimulation();
    }
}

function renderToggles() {
    const container = document.getElementById('simulatorTogglesList');
    container.innerHTML = '';

    Object.entries(availableActions).forEach(([key, act]) => {
        const item = document.createElement('div');
        item.className = 'simulator-toggle-item';
        item.id = `toggle-box-${key}`;

        item.innerHTML = `
            <label class="switch">
                <input type="checkbox" value="${key}" class="sim-checkbox">
                <span class="slider"></span>
            </label>
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #fff; font-size: 0.9rem;">${act.label}</div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">${act.description}</div>
            </div>
        `;

        item.addEventListener('click', (e) => {
            if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'SPAN') {
                const cb = item.querySelector('input[type="checkbox"]');
                cb.checked = !cb.checked;
                cb.dispatchEvent(new Event('change'));
            }
        });

        const cb = item.querySelector('.sim-checkbox');
        cb.addEventListener('change', async () => {
            if (cb.checked) {
                item.classList.add('checked');
            } else {
                item.classList.remove('checked');
            }
            await runSimulation();
        });

        container.appendChild(item);
    });
}

function setSelectedToggles(keys) {
    keys.forEach(k => {
        const cb = document.querySelector(`.sim-checkbox[value="${k}"]`);
        if (cb) {
            cb.checked = true;
            const box = document.getElementById(`toggle-box-${k}`);
            if (box) box.classList.add('checked');
        }
    });
}

function getSelectedToggles() {
    const cbs = document.querySelectorAll('.sim-checkbox:checked');
    return Array.from(cbs).map(cb => cb.value);
}

function bindSimulatorEvents() {
    document.getElementById('btnSelectAllToggles').addEventListener('click', async () => {
        document.querySelectorAll('.sim-checkbox').forEach(cb => {
            cb.checked = true;
            const box = document.getElementById(`toggle-box-${cb.value}`);
            if (box) box.classList.add('checked');
        });
        await runSimulation();
    });

    document.getElementById('btnClearToggles').addEventListener('click', async () => {
        document.querySelectorAll('.sim-checkbox').forEach(cb => {
            cb.checked = false;
            const box = document.getElementById(`toggle-box-${cb.value}`);
            if (box) box.classList.remove('checked');
        });
        await runSimulation();
    });
}

async function runSimulation() {
    const selected = getSelectedToggles();
    const res = await PrivacyAPI.simulateImprovement(baselineResponses, selected);

    if (res.success) {
        updateSimulationUI(res.data);
    }
}

function updateSimulationUI(data) {
    // 1. Baseline
    const bScore = data.baseline.overall_score;
    const bTier = data.baseline.risk_level;
    document.getElementById('simBaselineScore').textContent = bScore;
    const bTierEl = document.getElementById('simBaselineTier');
    bTierEl.textContent = bTier;
    bTierEl.className = `badge badge-${bTier === 'CRITICAL' ? 'crit' : (bTier === 'HIGH' ? 'high' : (bTier === 'MODERATE' ? 'mod' : 'low'))}`;

    // 2. Projected
    const pScore = data.simulated.overall_score;
    const pTier = data.simulated.risk_level;
    document.getElementById('simProjectedScore').textContent = pScore;
    const pTierEl = document.getElementById('simProjectedTier');
    pTierEl.textContent = pTier;
    pTierEl.className = `badge badge-${pTier === 'CRITICAL' ? 'crit' : (pTier === 'HIGH' ? 'high' : (pTier === 'MODERATE' ? 'mod' : 'low'))}`;

    // 3. Delta
    const delta = data.risk_reduction_points;
    const deltaPct = data.percentage_improvement;
    document.getElementById('simDeltaPoints').textContent = delta;
    document.getElementById('simDeltaPct').textContent = `${deltaPct}% RISK REDUCTION`;

    // 4. Comparison Chart
    renderComparisonChart(data.baseline.category_scores, data.simulated.category_scores);
}

function renderComparisonChart(baselineCats, simulatedCats) {
    const labels = Object.values(baselineCats).map(c => c.name);
    const baselineScores = Object.values(baselineCats).map(c => c.score);
    const simulatedScores = Object.values(simulatedCats).map(c => c.score);

    const ctx = document.getElementById('chartSimulatorComparison').getContext('2d');
    if (comparisonChart) comparisonChart.destroy();

    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Current Baseline',
                    data: baselineScores,
                    backgroundColor: 'rgba(239, 68, 68, 0.7)',
                    borderRadius: 4
                },
                {
                    label: 'Simulated Hardened',
                    data: simulatedScores,
                    backgroundColor: 'rgba(16, 185, 129, 0.85)',
                    borderRadius: 4
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    min: 0,
                    max: 100,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#cbd5e1', font: { size: 10 } }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: { color: '#cbd5e1', font: { size: 11 }, boxWidth: 12 }
                }
            }
        }
    });
}
