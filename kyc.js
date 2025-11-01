// kyc.js
class KYCCapture {
    constructor() {
        this.stream = null;
        this.capturedImageBlob = null;
        this.kycImageHash = null;
    }
    
    async initWebcam() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                }
            });
            
            const videoElement = document.getElementById('webcam');
            videoElement.srcObject = this.stream;
            
            return true;
        } catch (error) {
            console.error('Webcam access denied:', error);
            alert('Camera access required for identity verification');
            return false;
        }
    }
    
    capturePhoto() {
        const video = document.getElementById('webcam');
        const canvas = document.getElementById('snapshot');
        const context = canvas.getContext('2d');
        
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0);
        
        // Convert to blob for upload
        canvas.toBlob((blob) => {
            this.capturedImageBlob = blob;
            
            // Show preview
            const preview = document.getElementById('capturedImage');
            preview.src = URL.createObjectURL(blob);
            
            // Hide camera, show preview
            document.getElementById('cameraContainer').style.display = 'none';
            document.getElementById('previewContainer').classList.remove('hidden');
            document.getElementById('captureBtn').classList.add('hidden');
        }, 'image/jpeg', 0.85);
    }
    
    async uploadKYCImage(sessionToken) {
        if (!this.capturedImageBlob) {
            throw new Error('No image captured');
        }
        
        const formData = new FormData();
        formData.append('kyc_image', this.capturedImageBlob, 'kyc_photo.jpg');
        formData.append('timestamp', new Date().toISOString());
        
        try {
            const response = await fetch('http://localhost:5000/api/kyc/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${sessionToken}`
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Upload failed');
            }
            
            this.kycImageHash = data.image_hash;
            
            return {
                success: true,
                imageHash: data.image_hash,
                encryptedRef: data.encrypted_reference
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    stopWebcam() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
    }
}

// Initialize KYC on page load
let kycCapture;
let sessionToken;

document.addEventListener('DOMContentLoaded', async () => {
    // Get session token from storage
    sessionToken = sessionStorage.getItem('voting_session');
    
    if (!sessionToken) {
        alert('Session expired. Please login again.');
        window.location.href = 'login.html';
        return;
    }
    
    // Initialize webcam
    kycCapture = new KYCCapture();
    const webcamStarted = await kycCapture.initWebcam();
    
    if (!webcamStarted) {
        document.getElementById('error-message').textContent = 'Unable to access camera. Please grant camera permissions.';
        document.getElementById('error-message').classList.remove('hidden');
        return;
    }
    
    // Capture button event
    document.getElementById('captureBtn').addEventListener('click', () => {
        kycCapture.capturePhoto();
    });
    
    // Retake button event
    document.getElementById('retakeBtn').addEventListener('click', () => {
        document.getElementById('cameraContainer').style.display = 'block';
        document.getElementById('previewContainer').classList.add('hidden');
        document.getElementById('captureBtn').classList.remove('hidden');
    });
    
    // Confirm photo button event
    document.getElementById('confirmPhotoBtn').addEventListener('click', async () => {
        const errorDiv = document.getElementById('error-message');
        errorDiv.classList.add('hidden');
        
        // Upload KYC image
        const uploadResult = await kycCapture.uploadKYCImage(sessionToken);
        
        if (uploadResult.success) {
            // Stop webcam
            kycCapture.stopWebcam();
            
            // Hide KYC section, show voting section
            document.getElementById('kycSection').classList.add('hidden');
            document.getElementById('voteSection').classList.remove('hidden');
        } else {
            errorDiv.textContent = 'Failed to upload photo: ' + uploadResult.error;
            errorDiv.classList.remove('hidden');
        }
    });
    
    // Vote form submission
    document.getElementById('voteForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const selectedCandidate = document.querySelector('input[name="candidate"]:checked');
        if (!selectedCandidate) {
            alert('Please select a candidate');
            return;
        }
        
        const voteData = {
            vote_choice: selectedCandidate.value,
            kyc_image_hash: kycCapture.kycImageHash,
            timestamp: new Date().toISOString()
        };
        
        try {
            const response = await fetch('http://localhost:5000/api/vote/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${sessionToken}`
                },
                body: JSON.stringify(voteData)
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                const messageDiv = document.getElementById('voteMessage');
                messageDiv.className = 'success';
                messageDiv.textContent = 'Vote submitted successfully! Your vote has been recorded securely.';
                messageDiv.classList.remove('hidden');
                
                // Disable form
                document.getElementById('voteForm').style.display = 'none';
                
                // Clear session after 3 seconds
                setTimeout(() => {
                    sessionStorage.removeItem('voting_session');
                    alert('Thank you for voting! You will be redirected to the login page.');
                    window.location.href = 'login.html';
                }, 3000);
            } else {
                const errorDiv = document.getElementById('error-message');
                errorDiv.textContent = 'Failed to submit vote: ' + (data.error || 'Unknown error');
                errorDiv.classList.remove('hidden');
            }
        } catch (error) {
            const errorDiv = document.getElementById('error-message');
            errorDiv.textContent = 'Network error: ' + error.message;
            errorDiv.classList.remove('hidden');
        }
    });
});
