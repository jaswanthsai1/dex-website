console.log("🔥 DEX SCRIPT RELOADED v2");
// alert("DEX Script Loaded - Popups should work!"); // Debug alert
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

        jwtResults.innerHTML = '<div class="loading-text">Generating...</div>';
        jwtResults.classList.add('active');

        try {
            const response = await fetch(`/generate-jwt?eat_token=${encodeURIComponent(eatToken)}`);
            const data = await response.json();

            if (data.error || !response.ok) {
                let msg = data.error || data.details || 'Failed to generate JWT';
                jwtResults.innerHTML = `<div class="error-message">❌ ${msg}</div>`;
            } else if (data.access_token) {
                let html = '<div class="success-message">✅ Generated Successfully!</div>';
                html += '<div style="margin-top: 5px;">';
                html += `<div class="result-item"><span class="result-label">Region:</span> <span class="result-value">${data.region || 'Unknown'}</span></div>`;
                html += '<div style="display:flex; justify-content:space-between; align-items:center; margin: 5px 0;">';
                html += '<p style="font-size: 0.85rem; color: #aaa; margin: 0;">Token:</p>';
                html += `<button onclick="navigator.clipboard.writeText(document.getElementById('access-token-display').value).then(() => { this.innerText = 'Copied!'; setTimeout(() => this.innerText = 'Copy', 2000); })" style="background:var(--primary-orange); border:none; color:white; padding:2px 8px; border-radius:3px; cursor:pointer; font-size:0.75rem;">Copy</button>`;
                html += '</div>';
                html += `<textarea id="access-token-display" readonly style="width: 100%; height: 80px; background: rgba(0,0,0,0.5); border: 1px solid #444; color: #0f0; border-radius: 4px; font-family: monospace; font-size: 0.8rem;">${data.access_token}</textarea>`;
                html += '</div>';
                jwtResults.innerHTML = html;
            } else {
                jwtResults.innerHTML = '<div class="error-message">❌ No JWT found in response</div>';
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

        uidResults.innerHTML = '<div class="loading-text">Searching...</div>';
        uidResults.classList.add('active');

        try {
            const response = await fetch(`/uid-lookup?uid=${encodeURIComponent(uid)}`);
            const data = await response.json();

            if (data.error) {
                uidResults.innerHTML = `<div class="error-message">❌ ${data.error}</div>`;
            } else if (data.success) {
                if (data.player_data) {
                    const pd = data.player_data;
                    const guild = pd.guild || {};
                    let html = `
                        <div class="result-card">
                            <div class="result-header">
                                <strong>${pd.nickname}</strong>
                                <span class="badge badge-orange">${pd.region}</span>
                            </div>
                            <div class="result-body">
                                <div class="result-row">
                                    <span class="result-label">UID:</span>
                                    <span class="result-value">${data.uid}</span>
                                </div>
                                <div class="result-row">
                                    <span class="result-label">Level:</span>
                                    <span class="result-value">${pd.level}</span>
                                </div>
                                <div class="result-row">
                                    <span class="result-label">Rank:</span>
                                    <span class="result-value">${pd.rank}</span>
                                </div>
                                <div class="result-row">
                                    <span class="result-label">Likes:</span>
                                    <span class="result-value">${pd.likes}</span>
                                </div>
                                <div class="result-row">
                                    <span class="result-label">Guild:</span>
                                    <span class="result-value">${guild.name ? guild.name + ' (Lv.' + guild.level + ')' : 'None'}</span>
                                </div>
                                <div class="result-row">
                                    <span class="result-label">Last Login:</span>
                                    <span class="result-value" style="font-size: 0.8em;">${pd.last_login}</span>
                                </div>
                                
                                <div style="margin-top: 5px; color: #ffd700; font-style: italic; font-size: 0.8rem; text-align: center;">
                                    "${pd.bio || 'No Signature'}"
                                </div>
                            </div>
                        </div>
                    `;
                    uidResults.innerHTML = html;
                } else {
                    let html = `
                         <div class="result-card">
                            <div class="result-header">
                                <strong>${data.message}</strong>
                                <span class="badge badge-orange">Found</span>
                            </div>
                             <div class="result-body">
                                <div class="result-row">
                                    <span class="result-label">UID:</span>
                                    <span class="result-value">${data.uid}</span>
                                </div>
                                ${data.player_data || data.demo_structure ? Object.entries(data.player_data || data.demo_structure).filter(([_, v]) => typeof v !== 'object').map(([k, v]) => `
                                    <div class="result-row">
                                        <span class="result-label">${k}:</span>
                                        <span class="result-value">${v}</span>
                                    </div>
                                `).join('') : ''}
                             </div>
                         </div>
                    `;
                    uidResults.innerHTML = html;
                }
            }
        } catch (error) {
            uidResults.innerHTML = `<div class="error-message">❌ Error: ${error.message}</div>`;
        }
    });
}

// Global function for Add Friend Button
// Global function for Add Friend Button
window.sendFriendRequest = async function () {
    const input = document.getElementById('friend-uid-input');
    const uid = input.value.trim();
    const actionSelect = document.getElementById('friend-action-select');
    const action = actionSelect.value; // 'add' or 'remove'

    const friendResult = document.getElementById('friend-result');

    if (!uid) {
        friendResult.style.display = 'block';
        friendResult.innerHTML = '<div class="error-message">❌ Please enter a Target UID.</div>';
        return;
    }

    const actionText = action === 'remove' ? 'Removing' : 'Adding';

    friendResult.style.display = 'block';
    friendResult.innerHTML = `<div class="loading-text">🔥 Spamming ${actionText} Friend x20 to ${uid}...<br><small>This takes ~6 seconds</small></div>`;

    try {
        let url = `/add-friend?uid=${encodeURIComponent(uid)}&action=${encodeURIComponent(action)}&count=20`;

        const response = await fetch(url, {
            method: 'POST'
        });
        const data = await response.json();

        if (data.success) {
            const d = data.details || {};
            friendResult.innerHTML = `<div class="success-message">${data.message}<br><small>✅ ${d.success || 0} sent | ❌ ${d.failed || 0} failed</small></div>`;
        } else {
            friendResult.innerHTML = `<div class="error-message">${data.message}</div>`;
        }
    } catch (error) {
        friendResult.innerHTML = `<div class="error-message">❌ Network Error: ${error.message}</div>`;
    }
};

// === Team Spammer Logic ===

window.toggleTeamInput = function (mode) {
    const inviteGroup = document.getElementById('team-invite-input-group');
    const joinGroup = document.getElementById('team-join-input-group');
    const roomInviteGroup = document.getElementById('room-invite-input-group');
    const roomJoinGroup = document.getElementById('room-join-input-group');

    // Reset all
    inviteGroup.style.display = 'none';
    joinGroup.style.display = 'none';
    if (roomInviteGroup) roomInviteGroup.style.display = 'none';
    if (roomJoinGroup) roomJoinGroup.style.display = 'none';

    if (mode === 'invite') {
        inviteGroup.style.display = 'block';
        document.getElementById('team-target-uid').focus();
    } else if (mode === 'join') {
        joinGroup.style.display = 'block';
        document.getElementById('team-target-code').focus();
    } else if (mode === 'room_invite') {
        roomInviteGroup.style.display = 'block';
        document.getElementById('room-target-uid').focus();
    } else if (mode === 'room_join') {
        roomJoinGroup.style.display = 'block';
        document.getElementById('room-target-id').focus();
    }
};

window.sendTeamAction = async function () {
    // Get value from select instead of radio
    const mode = document.getElementById('team-action-select').value;

    const teamResult = document.getElementById('team-result');
    teamResult.style.display = 'block';
    teamResult.innerHTML = '<div class="loading-text">Processing...</div>';

    try {
        let response;
        if (mode === 'invite') {
            const uid = document.getElementById('team-target-uid').value.trim();
            if (!uid) { teamResult.innerHTML = '<div class="error-message">❌ Please enter a UID</div>'; return; }
            response = await fetch(`/team-invite?uid=${encodeURIComponent(uid)}`, { method: 'POST' });
        } else if (mode === 'join') {
            const code = document.getElementById('team-target-code').value.trim();
            if (!code) { teamResult.innerHTML = '<div class="error-message">❌ Please enter a Team Code</div>'; return; }
            response = await fetch(`/team-join?code=${encodeURIComponent(code)}`, { method: 'POST' });
        } else if (mode === 'room_invite') {
            const uid = document.getElementById('room-target-uid').value.trim();
            const roomId = document.getElementById('room-target-id-inv').value.trim();
            if (!uid || !roomId) { teamResult.innerHTML = '<div class="error-message">❌ Enter UID and Room ID</div>'; return; }
            response = await fetch(`/room-invite?uid=${encodeURIComponent(uid)}&room_id=${encodeURIComponent(roomId)}`, { method: 'POST' });
        } else if (mode === 'room_join') {
            const roomId = document.getElementById('room-target-id').value.trim();
            if (!roomId) { teamResult.innerHTML = '<div class="error-message">❌ Please enter a Room ID</div>'; return; }
            response = await fetch(`/room-join?room_id=${encodeURIComponent(roomId)}`, { method: 'POST' });
        }

        const data = await response.json();

        if (data.success) {
            teamResult.innerHTML = `<div class="success-message">✅ ${data.message}</div>`;
        } else {
            teamResult.innerHTML = `<div class="error-message">❌ ${data.message}</div>`;
        }
    } catch (error) {
        console.error(error);
        teamResult.innerHTML = `<div class="error-message">❌ Network Error: ${error.message}</div>`;
    }
};

// Account Info Display
const accountForm = document.getElementById('accountForm');
const accountResults = document.getElementById('accountResults');

if (accountForm) {
    accountForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const uid = this.querySelector('input[name="uid"]').value.trim();

        accountResults.innerHTML = '<div class="loading-text">Fetching account info...</div>';
        accountResults.classList.add('active');

        try {
            const response = await fetch(`/account-info?uid=${encodeURIComponent(uid)}`);
            const data = await response.json();

            if (data.error) {
                accountResults.innerHTML = `<div class="error-message">❌ ${data.error}</div>`;
            } else if (data.success) {
                let html = `
                    <div class="result-card">
                        <div class="result-header">
                            <strong>Account Info</strong>
                            <span class="badge badge-orange">UID: ${data.uid}</span>
                        </div>
                        <div class="json-container">
                            ${data.raw_data ? formatJSON(data.raw_data) : (data.available_data ? data.available_data.map(i => `<div>• ${i}</div>`).join('') : 'No details')}
                        </div>
                        ${data.note ? `<div class="footer-note">💡 ${data.note}</div>` : ''}
                    </div>
                `;
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

        bioResults.innerHTML = '<div class="loading-text">Updating signature...</div>';
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
                bioResults.innerHTML = `<div class="error-message">❌ ${msg}</div>`;
                if (data.details) {
                    bioResults.innerHTML += `<div class="error-message" style="margin-top:5px;">Details: ${data.details}</div>`;
                }
            }
        } catch (error) {
            bioResults.innerHTML = `<div class="error-message">❌ Network Error: ${error.message}</div>`;
        }
    });
}

// Helper function to format JSON data
// Helper function to format JSON data with cleaner styling
function formatJSON(obj, indent = 0) {
    let html = '';
    const paddingLeft = indent * 15; // px

    for (const [key, value] of Object.entries(obj)) {
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
            html += `<div style="padding-left: ${paddingLeft}px; margin-top: 4px; color: var(--primary-orange); font-weight: 600; font-size: 0.85rem;">${key}:</div>`;
            html += formatJSON(value, indent + 1);
        } else if (Array.isArray(value)) {
            html += `<div style="padding-left: ${paddingLeft}px; margin-top: 2px;">
                        <span style="color: #aaa;">${key}:</span> 
                        <span style="color: #ddd;">[${value.join(', ')}]</span>
                     </div>`;
        } else {
            html += `<div style="padding-left: ${paddingLeft}px; display: flex; justify-content: space-between; border-bottom: 1px dashed rgba(255,255,255,0.05); padding-top: 2px; padding-bottom: 2px;">
                        <span style="color: #bbb;">${key}</span>
                        <span style="color: #fff; font-weight: 600; text-align: right;">${value}</span>
                     </div>`;
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

        banResults.innerHTML = '<div class="loading-text">Checking ban status...</div>';
        banResults.classList.add('active');

        try {
            const response = await fetch(`/check-ban-uid?uid=${encodeURIComponent(uid)}`);
            const data = await response.json();

            if (data.error) {
                banResults.innerHTML = `<div class="error-message">❌ ${data.error}</div>`;
            } else if (data.success) {
                const statusClass = data.is_restricted ? 'badge-red' : 'badge-green';
                const statusIcon = data.is_restricted ? '🛑' : '✅';

                let html = `
                    <div class="result-card">
                        <div class="result-header">
                            <strong>${data.nickname || 'Unknown'}</strong>
                            <span class="badge ${statusClass}">${data.status}</span>
                        </div>
                        <div class="result-body">
                             <div class="result-row">
                                <span class="result-label">UID:</span>
                                <span class="result-value">${uid}</span>
                            </div>
                            <div class="result-row">
                                <span class="result-label">CS Rank Ban:</span>
                                <span class="result-value" style="color: ${data.cs_ban ? '#ff4d4d' : '#00ff88'}">${data.cs_ban ? 'YES' : 'NO'}</span>
                            </div>
                             <div class="result-row">
                                <span class="result-label">Credit Score:</span>
                                <span class="result-value">${data.credit_score}</span>
                            </div>
                        </div>
                        <div class="footer-note" style="color: #aaa; font-style: normal;">
                            ${statusIcon} ${data.details}
                        </div>
                    </div>
                `;
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

// Token Extractor Logic
function extractTokenFromUrl() {
    const urlInput = document.getElementById('kiosgamer-url');
    const resultDiv = document.getElementById('extractor-result');

    if (!urlInput || !resultDiv) return;

    const url = urlInput.value.trim();

    if (!url) {
        alert('Please paste a URL first.');
        return;
    }

    // Pattern to find 'eat=' followed by the token until '&'
    const match = url.match(/eat=([^&]+)/);

    if (match && match[1]) {
        const token = match[1];
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="success-message">✅ Token Extracted!</div>
            <div style="margin-top: 10px;">
                 <p style="font-size: 0.85rem; color: #aaa; margin: 0;">Access Token:</p>
                 <div style="display:flex; gap: 5px;">
                     <textarea id="extracted-token" readonly style="width: 100%; height: 60px; background: rgba(0,0,0,0.5); border: 1px solid #444; color: #0f0; border-radius: 4px; font-family: monospace; font-size: 0.8rem;">${token}</textarea>
                 </div>
                 <button onclick="navigator.clipboard.writeText(document.getElementById('extracted-token').value).then(() => { this.innerText = 'Copied!'; setTimeout(() => this.innerText = 'Copy Token', 2000); })" style="width: 100%; margin-top: 5px; background:var(--primary-orange); border:none; color:white; padding:8px; border-radius:4px; cursor:pointer; font-weight: bold;">Copy Token</button>
            </div>
        `;
    } else {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `<div class="error-message">❌ Could not find 'eat=' token in URL. Make sure it's a valid Kiosgamer link.</div>`;
    }
}

// ===== LEGACY SUPPORT =====
// No-op stubs in case any code calls these
window.openModal = function () { };
window.closeModal = function () { };
