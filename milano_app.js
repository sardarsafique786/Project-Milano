/**
 * Milano Tech Solutions - Core Application Architecture
 * High-end Classified JS: ES6 Classes, Web Components, Shadow DOM, Singleton Pattern
 */

// 1. Web Component: Encapsulated UI Element for Analytics Cards
class MilanoKpiCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    static get observedAttributes() {
        return ['title', 'value', 'trend'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        this.render();
    }

    render() {
        const title = this.getAttribute('title') || 'Metric';
        const value = this.getAttribute('value') || '0';
        const trend = this.getAttribute('trend') || '';
        const trendClass = trend.includes('+') ? 'positive' : (trend.includes('-') ? 'negative' : 'neutral');

        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    background: rgba(30, 41, 59, 0.65);
                    backdrop-filter: blur(12px);
                    border: 1px solid rgba(255,255,255,0.05);
                    border-radius: 16px;
                    padding: 1.5rem;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    transition: transform 0.3s ease, border-color 0.3s ease;
                }
                :host(:hover) {
                    transform: translateY(-5px);
                    border-color: rgba(59, 130, 246, 0.4);
                }
                .title { color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; margin: 0 0 0.5rem 0; letter-spacing: 1px; }
                .value { color: #f8fafc; font-size: 1.8rem; font-weight: 700; margin: 0; }
                .trend { font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600; }
                .positive { color: #10b981; }
                .negative { color: #ef4444; }
                .neutral { color: #94a3b8; }
            </style>
            <div class="kpi-content">
                <h3 class="title">${title}</h3>
                <p class="value">${value}</p>
                <div class="trend ${trendClass}">${trend}</div>
            </div>
        `;
    }
}
customElements.define('milano-kpi-card', MilanoKpiCard);

// 2. State Management: Singleton API Provider
class APIProvider {
    constructor(endpoint) {
        if (APIProvider.instance) return APIProvider.instance;
        this.endpoint = endpoint;
        APIProvider.instance = this;
    }

    async fetchDataset() {
        try {
            const response = await fetch(this.endpoint);
            if (!response.ok) throw new Error(`HTTP Error! Status: ${response.status}`);
            const payload = await response.json();
            return payload.data || [];
        } catch (err) {
            console.error("Milano Systems Error fetching dataset:", err);
            return [];
        }
    }
}

// 3. Dashboard Controller: Binds Data to the UI
class DashboardController {
    constructor(apiProvider) {
        this.provider = apiProvider;
        this.kpiContainer = document.getElementById('kpiContainer');
        this.init();
    }

    init() {
        document.getElementById('refreshBtn').addEventListener('click', () => this.syncUI());
        this.syncUI(); 
    }

    async syncUI() {
        this.kpiContainer.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; color: var(--text-secondary);">Connecting to Secure API...</p>';
        const tableContainer = document.getElementById('tableContainer');
        if (tableContainer) tableContainer.innerHTML = '';
        
        const data = await this.provider.fetchDataset();
        
        if (!data.length) {
            this.kpiContainer.innerHTML = `
                <div style="grid-column: 1 / -1; background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; padding: 2rem; border-radius: 12px; text-align: center;">
                    <h3 style="color: #ef4444; margin-top: 0;">Connection Error</h3>
                    <p>Unable to fetch data from the Milano API. Please ensure your Python backend server is running in the terminal:</p>
                    <code style="background: #000; padding: 0.5rem; border-radius: 6px; color: #60a5fa;">python3 milano_api.py</code>
                </div>`;
            return;
        }

        // Advanced Array Reductions to calculate live KPI stats
        const totalRev = data.reduce((acc, row) => acc + parseFloat(row.total_revenue || 0), 0);
        const totalExp = data.reduce((acc, row) => acc + parseFloat(row.total_expense || 0), 0);
        const totalProfit = data.reduce((acc, row) => acc + parseFloat(row.net_profit || 0), 0);
        
        // Dynamic Trends (Latest Year vs Previous Year)
        const years = [...new Set(data.map(d => parseInt(d.year)))].sort((a,b) => b - a);
        const latestYear = years[0];
        const prevYear = years[1] || latestYear;
        
        const latestRev = data.filter(d => parseInt(d.year) === latestYear).reduce((acc, row) => acc + parseFloat(row.total_revenue || 0), 0);
        const prevRev = data.filter(d => parseInt(d.year) === prevYear).reduce((acc, row) => acc + parseFloat(row.total_revenue || 0), 0);
        const revTrend = prevRev ? (((latestRev - prevRev) / prevRev) * 100).toFixed(1) : 0;

        const latestExp = data.filter(d => parseInt(d.year) === latestYear).reduce((acc, row) => acc + parseFloat(row.total_expense || 0), 0);
        const prevExp = data.filter(d => parseInt(d.year) === prevYear).reduce((acc, row) => acc + parseFloat(row.total_expense || 0), 0);
        const expTrend = prevExp ? (((latestExp - prevExp) / prevExp) * 100).toFixed(1) : 0;

        const formatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
        
        this.kpiContainer.innerHTML = ''; // Clear previous
        const metrics = [
            { t: "Global Revenue", v: formatter.format(totalRev), r: `${revTrend > 0 ? '+' : ''}${revTrend}% YoY` },
            { t: "Global Expenses", v: formatter.format(totalExp), r: `${expTrend > 0 ? '+' : ''}${expTrend}% YoY` },
            { t: "Net Profitability", v: formatter.format(totalProfit), r: totalProfit > 0 ? "Healthy" : "Critical Loss" }
        ];

        metrics.forEach(m => {
            const card = document.createElement('milano-kpi-card');
            card.setAttribute('title', m.t);
            card.setAttribute('value', m.v);
            card.setAttribute('trend', m.r);
            this.kpiContainer.appendChild(card);
        });

        // Render Interactive Graphs
        this.renderCharts(data, latestYear);

        // Render Data Table directly from CSV rows
        if (tableContainer) {
            let tableHTML = `
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; background: rgba(15, 23, 42, 0.65); backdrop-filter: blur(12px);">
                    <thead>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--text-secondary);">
                            <th style="padding: 1rem;">Date</th>
                            <th style="padding: 1rem;">Department</th>
                            <th style="padding: 1rem;">Total Revenue</th>
                            <th style="padding: 1rem;">Total Expense</th>
                            <th style="padding: 1rem;">Net Profit</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            // Show latest 10 rows from CSV
            const recentData = data.slice(-10).reverse();
            recentData.forEach(row => {
                tableHTML += `
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <td style="padding: 1rem;">${row.month}/${row.year}</td>
                        <td style="padding: 1rem;">${row.department}</td>
                        <td style="padding: 1rem; color: #10b981;">${formatter.format(row.total_revenue)}</td>
                        <td style="padding: 1rem; color: #ef4444;">${formatter.format(row.total_expense)}</td>
                        <td style="padding: 1rem;">${formatter.format(row.net_profit)}</td>
                    </tr>
                `;
            });
            
            tableHTML += `</tbody></table>`;
            tableContainer.innerHTML = tableHTML;
        }

        // Render the new Employee Insights section
        this.renderReviews();
    }

    renderCharts(data, latestYear) {
        // Destroy existing charts to prevent hover-glitches on re-sync
        if (this.revChart) this.revChart.destroy();
        if (this.pieChart) this.pieChart.destroy();

        // Graph 1: Monthly Revenue & Expense for Latest Year
        const latestYearData = data.filter(d => parseInt(d.year) === latestYear).sort((a,b) => parseInt(a.month) - parseInt(b.month));
        const monthlyData = {};
        for(let i = 1; i <= 12; i++) monthlyData[i] = { rev: 0, exp: 0 };
        
        latestYearData.forEach(row => {
            monthlyData[row.month].rev += parseFloat(row.total_revenue || 0);
            monthlyData[row.month].exp += parseFloat(row.total_expense || 0);
        });

        const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const revData = labels.map((_, i) => monthlyData[i+1].rev);
        const expData = labels.map((_, i) => monthlyData[i+1].exp);

        const ctxRev = document.getElementById('revenueExpenseChart');
        if (ctxRev) {
            this.revChart = new Chart(ctxRev, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        { label: 'Revenue ($)', data: revData, backgroundColor: 'rgba(59, 130, 246, 0.9)', borderRadius: 4 },
                        { label: 'Expenses ($)', data: expData, backgroundColor: 'rgba(239, 68, 68, 0.9)', borderRadius: 4 }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { labels: { color: '#f8fafc', font: { family: 'Inter' } } },
                        title: { display: true, text: `FY ${latestYear} Monthly Financials`, color: '#94a3b8', font: { size: 14 } }
                    },
                    scales: {
                        y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                        x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
                    }
                }
            });
        }

        // Graph 2: Global Revenue by Department (Pie Chart)
        const deptRev = {};
        data.forEach(row => {
            deptRev[row.department] = (deptRev[row.department] || 0) + parseFloat(row.total_revenue || 0);
        });

        const ctxPie = document.getElementById('deptPieChart');
        if (ctxPie) {
            this.pieChart = new Chart(ctxPie, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(deptRev),
                    datasets: [{
                        data: Object.values(deptRev),
                        backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#6366f1', '#ec4899', '#14b8a6'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'right', labels: { color: '#f8fafc', font: { size: 11 } } },
                        title: { display: true, text: 'Global Revenue by Department', color: '#94a3b8', font: { size: 14 } }
                    }
                }
            });
        }
    }

    renderReviews() {
        const reviewsContainer = document.getElementById('reviewsContainer');
        if (!reviewsContainer) return;
        
        const mockReviews = [
            { name: "Sarah Jenkins", role: "Data & AI Engineer", text: "Working at Milano gives me access to incredible data sets. The scale we operate at is mind-blowing!" },
            { name: "David Vasquez", role: "Operations Lead", text: "The cross-departmental collaboration here is unmatched. We smoothly manage million-dollar budgets." },
            { name: "Michael Graves", role: "Finance Director", text: "Our internal analytics tools make forecasting operating profits a breeze. Proud to be part of the leadership team." },
            { name: "Briana Flores", role: "Sales & Marketing", text: "Selling our tech solutions is easy when you're backed by a world-class engineering team like Milano's." }
        ];

        let html = '';
        mockReviews.forEach(r => {
            html += `
                <div class="review-card">
                    <div class="review-author">${r.name}</div>
                    <div class="review-role">${r.role}</div>
                    <div class="review-text">"${r.text}"</div>
                </div>
            `;
        });
        reviewsContainer.innerHTML = html;
    }
}

// 4. Milano Chatbot Logic
class MilanoBot {
    constructor() {
        this.launcher = document.getElementById('chatLauncher');
        this.panel = document.getElementById('chatPanel');
        this.closeBtn = document.getElementById('chatClose');
        this.form = document.getElementById('chatForm');
        this.input = document.getElementById('chatInput');
        this.messages = document.getElementById('chatMessages');

        this.responses = [
          { match: /\b(hi|hello|hey)\b/i, reply: "Hello! I'm the Milano Insights Bot. Ask me about our projects, departments, or revenue." },
          { match: /\b(project|projects)\b/i, reply: "We are currently running 5 major projects: apex, betex, conol, drivenX, and Balenciaga-RED." },
          { match: /\b(department|departments)\b/i, reply: "Milano Tech Solutions has multiple departments including Engineering, Sales & Marketing, Finance, HR, Product, Operations, Customer Support, and Data & AI." },
          { match: /\b(employee|employees|headcount)\b/i, reply: "We have an extensive global workforce of exactly 10,000 highly skilled professionals!" },
          { match: /\b(revenue|profit|financial|expense)\b/i, reply: "Our dashboards reflect live multi-million dollar revenues and operating profits derived directly from our corporate arrays." },
          { match: /\b(who are you|what are you)\b/i, reply: "I am an AI assistant integrated into the Milano Corporate Financial Data Engine." }
        ];

        if (this.launcher) this.init();
    }

    init() {
        this.launcher.addEventListener('click', () => this.toggle(true));
        this.closeBtn.addEventListener('click', () => this.toggle(false));
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    toggle(force) {
        this.panel.classList.toggle('open', force);
        this.panel.setAttribute('aria-hidden', !force);
        if (force) this.input.focus();
    }

    handleSubmit(e) {
        e.preventDefault();
        const text = this.input.value.trim();
        if (!text) return;
        
        this.addMessage(text, 'user');
        this.input.value = '';
        
        setTimeout(() => {
            const response = this.responses.find(r => r.match.test(text));
            this.addMessage(response ? response.reply : "I don't have that specific data on hand, but you can explore the dashboard above!", 'bot');
        }, 500);
    }

    addMessage(text, sender) {
        const msg = document.createElement('div');
        msg.className = `chat-message ${sender}`;
        msg.innerHTML = `<p>${text}</p>`;
        this.messages.appendChild(msg);
        this.messages.scrollTop = this.messages.scrollHeight;
    }
}

// 5. Authentication & Review Management
class AuthAndReviewManager {
    constructor() {
        this.isRegisterMode = false;
        
        // Bind Elements
        this.loginBtn = document.getElementById('loginBtn');
        this.logoutBtn = document.getElementById('logoutBtn');
        this.authModal = document.getElementById('authModal');
        this.authClose = document.getElementById('authClose');
        this.authForm = document.getElementById('authForm');
        this.authTitle = document.getElementById('authTitle');
        this.authName = document.getElementById('authName');
        this.toggleAuthMode = document.getElementById('toggleAuthMode');
        this.authToggleText = document.getElementById('authToggleText');
        
        this.leaveReviewBtn = document.getElementById('leaveReviewBtn');
        this.addReviewForm = document.getElementById('addReviewForm');
        
        this.aboutSection = document.getElementById('aboutSection');
        this.dashboardContent = document.getElementById('dashboardContent');
        this.refreshBtn = document.getElementById('refreshBtn');
        this.transitionOverlay = document.getElementById('transitionOverlay');
        
        this.init();
    }

    init() {
        if(this.loginBtn) this.loginBtn.addEventListener('click', () => this.authModal.classList.add('open'));
        if(this.logoutBtn) this.logoutBtn.addEventListener('click', () => this.handleLogout());
        if(this.authClose) this.authClose.addEventListener('click', () => this.authModal.classList.remove('open'));
        
        if(this.toggleAuthMode) this.toggleAuthMode.addEventListener('click', (e) => {
            e.preventDefault();
            this.isRegisterMode = !this.isRegisterMode;
            this.authTitle.innerText = this.isRegisterMode ? 'Create Account' : 'Sign In';
            this.authName.style.display = this.isRegisterMode ? 'block' : 'none';
            this.authName.required = this.isRegisterMode;
            this.toggleAuthMode.innerText = this.isRegisterMode ? 'Login here' : 'Register here';
            this.authToggleText.textContent = this.isRegisterMode ? 'Already have an account? ' : 'New user? ';
        });
        
        if(this.authForm) this.authForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('authEmail').value;
            const password = document.getElementById('authPassword').value;
            
            if (this.isRegisterMode) {
                const name = this.authName.value;
                this.authTitle.innerText = "Creating Account...";
                try {
                    const response = await fetch('http://localhost:8080/api/register', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name, email, password })
                    });
                    const result = await response.json();
                    
                    if (result.status === 'success') {
                        document.getElementById('revName').value = result.name;
                        this.authModal.classList.remove('open');
                        this.handleLogin(result.name);
                    } else {
                        alert(result.message);
                    }
                } catch (err) {
                    console.error("Register Error:", err);
                    alert("System Error: " + err.message + "\nMake sure your Python API is actively running in the terminal.");
                } finally {
                    this.authTitle.innerText = "Create Account";
                }
                return;
            }

            // Real Database Verification via API
            this.authTitle.innerText = "Verifying Identity...";
            try {
                const response = await fetch('http://localhost:8080/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    document.getElementById('revName').value = result.name;
                    this.authModal.classList.remove('open');
                    this.handleLogin(result.name);
                } else {
                    alert(result.message);
                }
            } catch (err) {
                console.error("Login Error:", err);
                alert("System Error: " + err.message + "\nMake sure your Python API is actively running.");
            } finally {
                this.authTitle.innerText = "Sign In";
            }
        });
        
        if(this.leaveReviewBtn) this.leaveReviewBtn.addEventListener('click', () => {
            this.addReviewForm.style.display = this.addReviewForm.style.display === 'none' ? 'flex' : 'none';
        });
        
        if(this.addReviewForm) this.addReviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const reviewsContainer = document.getElementById('reviewsContainer');
            const newReview = document.createElement('div');
            newReview.className = 'review-card';
            newReview.innerHTML = `<div class="review-author">${document.getElementById('revName').value}</div><div class="review-role">${document.getElementById('revRole').value}</div><div class="review-text">"${document.getElementById('revText').value}"</div>`;
            reviewsContainer.insertBefore(newReview, reviewsContainer.firstChild);
            this.addReviewForm.reset();
            this.addReviewForm.style.display = 'none';
        });
    }

    handleLogin(name) {
        // Trigger transition overlay
        this.transitionOverlay.classList.add('open');
        
        setTimeout(() => {
            this.transitionOverlay.classList.remove('open');
            this.loginBtn.style.display = 'none';
            this.logoutBtn.style.display = 'inline-block';
            this.logoutBtn.textContent = `Log Out (${name})`;
            if (this.refreshBtn) this.refreshBtn.style.display = 'inline-block';
            
            this.aboutSection.style.display = 'none';
            this.dashboardContent.style.display = 'block';
            
            // Small delay to ensure display: block applies before opacity transition
            setTimeout(() => this.dashboardContent.style.opacity = '1', 50);
        }, 1800); // 1.8 second loading transition simulating DB fetching
    }

    handleLogout() {
        this.dashboardContent.style.opacity = '0';
        setTimeout(() => {
            this.dashboardContent.style.display = 'none';
            this.aboutSection.style.display = 'block';
            this.loginBtn.style.display = 'inline-block';
            this.logoutBtn.style.display = 'none';
            if (this.refreshBtn) this.refreshBtn.style.display = 'none';
        }, 500);
    }
}

// 6. Application Bootstrapper
document.addEventListener('DOMContentLoaded', () => {
    const apiProvider = new APIProvider('http://localhost:8080/api/expenses');
    new DashboardController(apiProvider);
    new MilanoBot();
    new AuthAndReviewManager();
});