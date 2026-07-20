// Main JavaScript for AI IT Technician Assistant

document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeTheme();
});

function initializeEventListeners() {
    // Menu toggle
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Language selector
    const langBtns = document.querySelectorAll('.lang-btn');
    langBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            langBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            setLanguage(this.dataset.lang);
        });
    });

    // Close sidebar when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.sidebar') && !e.target.closest('.menu-toggle')) {
            if (sidebar && window.innerWidth <= 768) {
                sidebar.classList.remove('show');
            }
        }
    });
}

function initializeTheme() {
    // Check for saved theme preference or default to light mode
    const theme = localStorage.getItem('theme') || 'light';
    setTheme(theme);
}

function setTheme(theme) {
    localStorage.setItem('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
}

function setLanguage(lang) {
    localStorage.setItem('language', lang);
    // This can be extended to translate the UI
    console.log('Language changed to:', lang);
}

// Get saved language
function getLanguage() {
    return localStorage.getItem('language') || 'th';
}

// Format date
function formatDate(date) {
    return new Intl.DateTimeFormat('th-TH', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('คัดลอกสำเร็จ', 'success');
    }).catch(() => {
        showToast('เกิดข้อผิดพลาด', 'error');
    });
}

// API Helper
class APIClient {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'API Error');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    chat(question, language = 'th', context = '') {
        return this.request('/chat', {
            method: 'POST',
            body: JSON.stringify({ question, language, context })
        });
    }

    analyzeLog(logContent, language = 'th') {
        return this.request('/analyze-log', {
            method: 'POST',
            body: JSON.stringify({ log_content: logContent, language })
        });
    }

    generateScript(description, scriptLanguage = 'powershell', language = 'th') {
        return this.request('/generate-script', {
            method: 'POST',
            body: JSON.stringify({ 
                description, 
                script_language: scriptLanguage, 
                language 
            })
        });
    }

    searchKnowledgeBase(query, category = null) {
        let endpoint = `/knowledge-base/search?query=${encodeURIComponent(query)}`;
        if (category) {
            endpoint += `&category=${encodeURIComponent(category)}`;
        }
        return this.request(endpoint);
    }

    getKBCategories() {
        return this.request('/knowledge-base/categories');
    }

    addKBArticle(category, title, content, tags = [], language = 'th') {
        return this.request('/knowledge-base/add', {
            method: 'POST',
            body: JSON.stringify({ category, title, content, tags, language })
        });
    }
}

// Create global API client
window.api = new APIClient();

// Toast styles (add to CSS if not already present)
const style = document.createElement('style');
style.textContent = `
.toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 15px 20px;
    border-radius: 8px;
    color: white;
    font-size: 14px;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 9999;
}

.toast.show {
    opacity: 1;
}

.toast-info {
    background-color: #2563eb;
}

.toast-success {
    background-color: #10b981;
}

.toast-warning {
    background-color: #f59e0b;
}

.toast-error {
    background-color: #ef4444;
}
`;
document.head.appendChild(style);
