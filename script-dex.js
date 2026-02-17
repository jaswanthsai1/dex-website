// ===== EAT TOKEN SEARCH =====
const eatTokenForm = document.getElementById('eatTokenForm');
const eatTokenInput = document.getElementById('eatTokenInput');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const resultsContent = document.getElementById('resultsContent');
const errorMessage = document.getElementById('errorMessage');

if (eatTokenForm) {
    eatTokenForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const eatToken = eatTokenInput.value.trim();
        if (!eatToken) {
            showError('Please enter an EAT token');
            return;
        }

        // Show loading, hide results and errors
        loadingIndicator.style.display = 'block';
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';

        try {
            const response = await fetch(`/Eat?eat_token=${encodeURIComponent(eatToken)}`);
            const data = await response.json();

            loadingIndicator.style.display = 'none';

            if (data.error || !response.ok) {
                showError(data.error || data.details || 'Failed to retrieve account information');
            } else {
                showResults(data);
            }
        } catch (error) {
            loadingIndicator.style.display = 'none';
            showError('Network error. Please check your connection and try again.');
            console.error('Error:', error);
        }
    });
}

function showResults(data) {
    let html = '';

    if (data.account_id) {
        html += `<div class="result-item">
            <span class="result-label">Account ID</span>
            <span class="result-value">${data.account_id}</span>
        </div>`;
    }

    if (data.account_nickname) {
        html += `<div class="result-item">
            <span class="result-label">Nickname</span>
            <span class="result-value">${data.account_nickname}</span>
        </div>`;
    }

    if (data.open_id) {
        html += `<div class="result-item">
            <span class="result-label">Open ID</span>
            <span class="result-value">${data.open_id}</span>
        </div>`;
    }

    if (data.access_token) {
        html += `<div class="result-item">
            <span class="result-label">Access Token</span>
            <span class="result-value">${data.access_token}</span>
        </div>`;
    }

    if (data.region) {
        html += `<div class="result-item">
            <span class="result-label">Region</span>
            <span class="result-value">${data.region}</span>
        </div>`;
    }

    if (data.credit) {
        html += `<div class="result-item">
            <span class="result-label">Credit</span>
            <span class="result-value">${data.credit}</span>
        </div>`;
    }

    if (data.Instagram) {
        html += `<div class="result-item">
            <span class="result-label">Instagram</span>
            <span class="result-value">${data.Instagram}</span>
        </div>`;
    }

    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ===== NAVIGATION =====
const navbar = document.querySelector('.navbar');
const navLinks = document.querySelectorAll('.nav-link');
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

// Navbar scroll effect
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Smooth scrolling for nav links
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);

        if (targetSection) {
            targetSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }

        // Update active link
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});

// ===== PARTICLES ANIMATION =====
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');

        // Random size between 2-6px
        const size = Math.random() * 4 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;

        // Random horizontal position
        particle.style.left = `${Math.random() * 100}%`;

        // Random animation duration between 10-20s
        const duration = Math.random() * 10 + 10;
        particle.style.animationDuration = `${duration}s`;

        // Random delay
        const delay = Math.random() * 5;
        particle.style.animationDelay = `${delay}s`;

        particlesContainer.appendChild(particle);
    }
}

// Initialize particles on load
createParticles();

// ===== COUNTER ANIMATION =====
function animateCounter(element, target, duration = 2000) {
    let current = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Intersection Observer for counters
const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px'
};

const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const target = parseInt(entry.target.dataset.target);
            animateCounter(entry.target, target);
            counterObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all stat numbers
document.querySelectorAll('.stat-number').forEach(stat => {
    counterObserver.observe(stat);
});

// ===== SCROLL ANIMATIONS =====
const animateOnScroll = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

// Add scroll animation to sections
const animatedElements = document.querySelectorAll('.service-card, .feature-item');
animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    animateOnScroll.observe(el);
});




// Form now submits directly to FormSubmit.co via HTML form action


// ===== BUTTON INTERACTIONS =====
const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .submit-btn');
buttons.forEach(button => {
    button.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-3px)';
    });

    button.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0)';
    });
});

// ===== CARD TILT EFFECT - DISABLED =====
// Disabled to prevent cards from moving
/*
const serviceCards = document.querySelectorAll('.service-card');
serviceCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
    });
});
*/

// ===== DYNAMIC BACKGROUND GLOW =====
document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth) * 100;
    const y = (e.clientY / window.innerHeight) * 100;

    const heroBg = document.querySelector('.hero-bg-animation');
    if (heroBg) {
        heroBg.style.background = `
            radial-gradient(circle at ${x}% ${y}%, rgba(255, 107, 53, 0.2) 0%, transparent 50%),
            radial-gradient(circle at ${100 - x}% ${100 - y}%, rgba(0, 217, 255, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%)
        `;
    }
});

// ===== SECTION ACTIVE STATE =====
const sections = document.querySelectorAll('section[id]');
const navObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${id}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}, { threshold: 0.5 });

sections.forEach(section => {
    navObserver.observe(section);
});

// ===== MOBILE MENU TOGGLE =====
if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// ===== PAGE LOAD ANIMATION =====
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 100);
});

console.log('🔥 DEX RECOVER SOLUTIONS - Website Loaded Successfully');

// ===== ADVANCED TOOLS HANDLERS =====

// JWT Generator
const jwtForm = document.getElementById('jwtForm');
const jwtResults = document.getElementById('jwtResults');

if (jwtForm) {
    jwtForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const eatToken = this.querySelector('input[name="eat_token"]').value.trim();

        if (!eatToken) {
            alert('Please enter a valid Access Token');
            return;
        }

        jwtResults.classList.remove('active');
        jwtResults.innerHTML = '<div class="success-message">⏳ Generating JWT...</div>';
        jwtResults.classList.add('active');

        try {
            const response = await fetch(`/generate-jwt?eat_token=${encodeURIComponent(eatToken)}`);
            const data = await response.json();

            if (data.error || !response.ok) {
                let msg = data.error || data.details || 'Failed to generate JWT';
                jwtResults.innerHTML = `<div class="error-message">❌ ${msg}</div>`;
            } else if (data.access_token) {
                let html = '<div class="success-message">✅ JWT Generated!</div>';
                html += '<div style="margin-top: 1rem;">';
                html += '<p style="font-size: 0.85rem; color: #aaa; margin-bottom: 0.5rem;">Copy this token for Bio Update:</p>';
                html += `<textarea id="access-token-display" readonly style="width: 100%; height: 100px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,107,53,0.3); color: #fff; border-radius: 5px; padding: 10px; font-family: monospace; font-size: 0.8rem;">${data.access_token}</textarea>`;

                if (data.region) {
                    html += `<div class="result-item" style="margin-top: 10px;"><span class="result-label">Region:</span><span class="result-value">${data.region}</span></div>`;
                }

                html += '</div>';
                jwtResults.innerHTML = html;
            } else {
                jwtResults.innerHTML = `<div class="error-message">❌ No JWT found in response</div>`;
            }
        } catch (error) {
            jwtResults.innerHTML = `<div class="error-message">❌ Network Error: ${error.message}</div>`;
        }
    });
}

// UID Lookup
const uidForm = document.getElementById('uidForm');
const uidResults = document.getElementById('uidResults');

if (uidForm) {
    uidForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const uid = this.querySelector('input[name="uid"]').value.trim();

        uidResults.classList.remove('active');
        uidResults.innerHTML = '<div class="success-message">⏳ Looking up player...</div>';
        uidResults.classList.add('active');

        try {
            const response = await fetch(`/uid-lookup?uid=${encodeURIComponent(uid)}`);
            const data = await response.json();

            if (data.error) {
                uidResults.innerHTML = `<div class="error-message">❌ ${data.error}</div>`;
            } else if (data.success) {
                let html = '<div class="success-message">ℹ️ ' + data.message + '</div>';
                html += '<div style="margin-top: 1rem;">';
                html += '<div class="result-item"><span class="result-label">UID:</span><span class="result-value">' + data.uid + '</span></div>';
                if (data.demo_structure) {
                    Object.keys(data.demo_structure).forEach(key => {
                        html += '<div class="result-item"><span class="result-label">' + key + ':</span><span class="result-value">' + data.demo_structure[key] + '</span></div>';
                    });
                }
                html += '</div>';
                uidResults.innerHTML = html;
            }
        } catch (error) {
            uidResults.innerHTML = `<div class="error-message">❌ Error: ${error.message}</div>`;
        }
    });
}

// Account Info Display
const accountForm = document.getElementById('accountForm');
const accountResults = document.getElementById('accountResults');

if (accountForm) {
    accountForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const uid = this.querySelector('input[name="uid"]').value.trim();

        accountResults.classList.remove('active');
        accountResults.innerHTML = '<div class="success-message">⏳ Fetching account info...</div>';
        accountResults.classList.add('active');

        try {
            const response = await fetch(`/account-info?uid=${encodeURIComponent(uid)}`);
            const data = await response.json();

            if (data.error) {
                accountResults.innerHTML = `<div class="error-message">❌ ${data.error}</div>`;
            } else if (data.success) {
                let html = '<div class="success-message">ℹ️ ' + data.message + '</div>';
                html += '<div style="margin-top: 1rem;">';
                html += '<div class="result-item"><span class="result-label">UID:</span><span class="result-value">' + data.uid + '</span></div>';

                if (data.raw_data) {
                    html += '<div style="margin-top: 1rem; color: var(--primary-orange); font-weight: 600;">Full Account Data:</div>';
                    html += '<div class="json-container" style="max-height: 400px; overflow-y: auto; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px;">';
                    html += formatJSON(data.raw_data);
                    html += '</div>';
                } else if (data.available_data) {
                    html += '<div style="margin-top: 1rem; color: var(--primary-orange); font-weight: 600;">Available Data Types:</div>';
                    data.available_data.forEach(item => {
                        html += '<div class="result-item">• ' + item + '</div>';
                    });
                }

                if (data.note) {
                    html += '<div style="margin-top: 1rem; padding: 0.5rem; background: rgba(255, 107, 53, 0.1); border-radius: 5px; font-size: 0.85rem;">';
                    html += '💡 ' + data.note;
                    html += '</div>';
                }
                html += '</div>';
                accountResults.innerHTML = html;
            }
        } catch (error) {
            accountResults.innerHTML = `<div class="error-message">❌ Error: ${error.message}</div>`;
        }
    });
}

// Bio Update Tool
const bioForm = document.getElementById('bioForm');
const bioResults = document.getElementById('bioResults');

if (bioForm) {
    bioForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const token = this.querySelector('textarea[name="token"]').value.trim();
        const bioText = this.querySelector('input[name="bio_text"]').value.trim();

        if (!token) {
            alert('Please enter a valid access token');
            return;
        }

        bioResults.classList.remove('active');
        bioResults.innerHTML = '<div class="success-message">⏳ Updating signature...</div>';
        bioResults.classList.add('active');

        try {
            const response = await fetch('/update-bio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token: token,
                    bio_text: bioText
                })
            });

            const data = await response.json();

            if (data.success) {
                let html = '<div class="success-message">✅ ' + data.message + '</div>';
                html += '<div style="margin-top: 1rem;">';
                html += `<div class="result-item"><span class="result-label">Region:</span><span class="result-value">${data.region}</span></div>`;
                html += `<div class="result-item"><span class="result-label">New Bio:</span><span class="result-value" style="color: var(--primary-orange);">${data.new_bio}</span></div>`;
                html += '</div>';
                bioResults.innerHTML = html;
            } else {
                let msg = data.message || data.detail || 'Unknown error occurred';
                let errorHtml = `<div class="error-message">❌ ${msg}</div>`;
                if (data.details) {
                    errorHtml += `<div style="font-size: 0.8rem; margin-top: 0.5rem; color: #ff6b6b; opacity: 0.8; word-break: break-all;">Details: ${data.details}</div>`;
                }
                bioResults.innerHTML = errorHtml;
            }
        } catch (error) {
            bioResults.innerHTML = `<div class="error-message">❌ Network Error: ${error.message}</div>`;
        }
    });
}

// Helper function to format JSON data
function formatJSON(obj, indent = 0) {
    let html = '';
    const indentStr = '&nbsp;&nbsp;&nbsp;&nbsp;'.repeat(indent);

    for (const [key, value] of Object.entries(obj)) {
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
            html += `<div class="result-item">${indentStr}<span class="result-label">${key}:</span></div>`;
            html += formatJSON(value, indent + 1);
        } else if (Array.isArray(value)) {
            html += `<div class="result-item">${indentStr}<span class="result-label">${key}:</span> [${value.join(', ')}]</div>`;
        } else {
            html += `<div class="result-item">${indentStr}<span class="result-label">${key}:</span><span class="result-value"> ${value}</span></div>`;
        }
    }
    return html;
}

// ===== END ADVANCED TOOLS =====

// Ban Status Checker Handler
const banForm = document.getElementById('banForm');
const banResults = document.getElementById('banResults');

if (banForm) {
    banForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const uid = this.querySelector('input[name="uid"]').value.trim();

        if (!uid) {
            alert('Please enter a valid UID');
            return;
        }

        banResults.classList.remove('active');
        banResults.innerHTML = '<div class="success-message">⏳ Checking ban status...</div>';
        banResults.classList.add('active');

        try {
            const response = await fetch(`/check-ban-uid?uid=${encodeURIComponent(uid)}`);
            const data = await response.json();

            if (data.error) {
                banResults.innerHTML = `<div class="error-message">❌ ${data.error}</div>`;
            } else if (data.success) {
                let html = `<div class="success-message">ℹ️ Status Check Complete</div>`;
                html += '<div style="margin-top: 1rem;">';
                html += `<div class="result-item"><span class="result-label">Nickname:</span><span class="result-value">${data.nickname}</span></div>`;

                const statusColor = data.is_restricted ? '#ff4d4d' : '#00ff00';
                html += `<div class="result-item"><span class="result-label">Status:</span><span class="result-value" style="color: ${statusColor}; font-weight: bold;">${data.status}</span></div>`;

                html += `<div class="result-item"><span class="result-label">Details:</span><span class="result-value">${data.details}</span></div>`;
                html += `<div class="result-item"><span class="result-label">CS Rank Ban:</span><span class="result-value">${data.cs_ban ? '❌ Yes' : '✅ No'}</span></div>`;
                html += `<div class="result-item"><span class="result-label">Credit Score:</span><span class="result-value">${data.credit_score}</span></div>`;
                html += '</div>';
                banResults.innerHTML = html;
            }
        } catch (error) {
            banResults.innerHTML = `<div class="error-message">❌ Error: ${error.message}</div>`;
        }
    });
}

// Update Bio Shortcut Handler
const updateBioBtn = document.getElementById('updateBioBtn');
if (updateBioBtn) {
    updateBioBtn.addEventListener('click', () => {
        const bioForm = document.getElementById('bioForm');
        if (bioForm) {
            bioForm.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Auto-fill token if available
            const tokenToken = document.getElementById('access-token-display');
            const bioTokenInput = bioForm.querySelector('textarea[name="token"]');
            if (tokenToken && bioTokenInput && tokenToken.value) {
                bioTokenInput.value = tokenToken.value;
            }
        }
    });
}
