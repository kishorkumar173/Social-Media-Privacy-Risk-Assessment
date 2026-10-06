/**
 * API Client Module
 * Communicates with the Flask REST Backend for Privacy Assessments.
 */

const API_BASE = '/api';

const PrivacyAPI = {
    // 1. Fetch questionnaire metadata
    async getQuestions() {
        const res = await fetch(`${API_BASE}/questions`);
        return await res.json();
    },

    // 2. Fetch preloaded high-risk fictional demo profile
    async getDemoProfile() {
        const res = await fetch(`${API_BASE}/demo-profile`);
        return await res.json();
    },

    // 3. Submit assessment answers
    async submitAssessment(responses, customWeights = null) {
        const res = await fetch(`${API_BASE}/assessment`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ responses, custom_weights: customWeights })
        });
        return await res.json();
    },

    // 4. Retrieve assessment by ID
    async getAssessment(id) {
        const res = await fetch(`${API_BASE}/assessment/${id}`);
        return await res.json();
    },

    // 5. Delete assessment (Right to Erasure)
    async deleteAssessment(id) {
        const res = await fetch(`${API_BASE}/assessment/${id}`, {
            method: 'DELETE'
        });
        return await res.json();
    },

    // 6. Dashboard metrics
    async getDashboardStats() {
        const res = await fetch(`${API_BASE}/dashboard/stats`);
        return await res.json();
    },

    // 7. Recent assessments
    async getRecentAssessments() {
        const res = await fetch(`${API_BASE}/dashboard/recent`);
        return await res.json();
    },

    // 8. Privacy simulator
    async simulateImprovement(responses, actions) {
        const res = await fetch(`${API_BASE}/assessment/simulate-improvement`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ responses, actions })
        });
        return await res.json();
    },

    // 9. Simulation actions catalog
    async getSimulationActions() {
        const res = await fetch(`${API_BASE}/simulation-actions`);
        return await res.json();
    },

    // 10. Privacy checklist
    async getPrivacyChecklist() {
        const res = await fetch(`${API_BASE}/privacy-checklist`);
        return await res.json();
    },

    // 11. Image metadata inspector
    async inspectImageMetadata(formData) {
        const res = await fetch(`${API_BASE}/metadata/inspect`, {
            method: 'POST',
            body: formData
        });
        return await res.json();
    }
};

window.PrivacyAPI = PrivacyAPI;
