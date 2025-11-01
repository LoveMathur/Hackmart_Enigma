// auth.js
class AuthManager {
    constructor(apiBaseUrl) {
        this.apiBaseUrl = apiBaseUrl;
        this.sessionToken = null;
    }
    
    async login(voterId, dob, email) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    voter_id: voterId,
                    dob: dob,
                    email: email
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Authentication failed');
            }
            
            this.sessionToken = data.session_token;
            sessionStorage.setItem('voting_session', this.sessionToken);
            
            return {
                success: true,
                voterInfo: data.voter_info
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    getSessionToken() {
        return this.sessionToken || sessionStorage.getItem('voting_session');
    }
    
    logout() {
        this.sessionToken = null;
        sessionStorage.removeItem('voting_session');
    }
}

// Form handling
document.addEventListener('DOMContentLoaded', () => {
    const authManager = new AuthManager('http://localhost:5000');
    const loginForm = document.getElementById('loginForm');
    const errorDiv = document.getElementById('error-message');
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const voterId = document.getElementById('voterId').value;
        const dob = document.getElementById('dob').value;
        const email = document.getElementById('email').value;
        
        errorDiv.classList.add('hidden');
        
        const result = await authManager.login(voterId, dob, email);
        
        if (result.success) {
            window.location.href = 'voting.html';
        } else {
            errorDiv.textContent = result.error;
            errorDiv.classList.remove('hidden');
        }
    });
});