# 🗳️ Vote Vault — Decentralized Digital Voting Platform

**Vote Vault** is a blockchain-powered digital voting platform that ensures secure, transparent, and tamper-proof elections.  
It leverages **KYC verification**, **OTP-based authentication**, **blockchain-backed vote recording**, and **real-time monitoring** to prevent unauthorized or duplicate votes.

---

## 🚀 Features

- **Decentralized Voting Ledger**  
  Each vote is stored on a blockchain-like structure using cryptographic hashing to ensure integrity and traceability.

- **Secure Voter Authentication**
  - Online **KYC verification** (with encrypted KYC image hash).
  - **OTP-based login** for verified voters.
  - Validation against an existing voter database.

- **Fraud Prevention**
  - Denies duplicate or unauthorized votes.
  - Captures voter's **IP address**, **geolocation**, and **timestamp**.
  - Captures a random **camera snapshot** during voting to ensure no coercion or multiple-person voting.

- **End-to-End Transparency**
  - Votes are stored with candidate choice hashes (not plain text) for privacy.
  - All interactions are timestamped and traceable on the blockchain ledger.

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Python (Flask/FastAPI) |
| Frontend | HTML, CSS, JavaScript |
| Blockchain | Custom lightweight blockchain (`blockchain_lite.py`) |
| Database | Excel-based registry (`voter_registry.xlsx`, `vote_records.xlsx`) |
| Security | OTP verification, KYC hash verification, anti-replay protection |
| Deployment | Local / Cloud (prototype stage) |

---

## 📁 Project Structure

| File / Folder | Description |
|---------------------------|---------------------------------------------|
| `app.py` | Main backend entry point |
| `blockchain_lite.py` | Custom blockchain implementation |
| `vote_service.py` | Core voting logic and verification |
| `kyc_service.py` | KYC verification and image hashing |
| `otp_service.py` | OTP generation and validation |
| `auth_service.py` | User authentication logic |
| `check_data.py` | Data validation and cleanup scripts |
| `create_voter_registry.py` | Scripts to create / manage voter registry |
| `excel_manager.py` | Helpers for Excel read/write operations |
| `/kyc_storage/` | Encrypted KYC image storage |
| `/templates/` | HTML front-end (login, vote, verification) |
| `/static/` | CSS and JavaScript files |
| `requirements.txt` | Python dependencies |
| `vote_chain.json` | Prototype blockchain ledger |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/vote-vault.git
cd vote-vault/Hackmart_Enigma
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the app
```bash
python app.py
```

Your local server will start — open it in your browser (e.g., http://localhost:5000).

---

## 🔒 Security & Privacy

- All KYC data is hashed and encrypted before being stored.

- Blockchain ensures immutability and tamper resistance.

- Random camera capture prevents coercion and proxy voting.

- OTP and KYC prevent replay attacks and vote duplication.

## 🧠 Future Enhancements

- Multi-factor authentication and face verification

- Scalable backend (PostgreSQL + FastAPI + containerization)

## 📜 License

This project is released under the MIT License.
Feel free to modify and use it for educational or development purposes.

## 🏗️ Current Status

**🚧 Prototype Stage** <br />
The system currently runs as a functional prototype for testing and demonstration.
Blockchain, KYC, and OTP modules are operational, but production-level deployment and distributed node integration are in progress.

## 📬 Contact

Author: Love Mathur <br />
Project: Vote Vault <br />
Email: love.mathur@outlook.com <br />
GitHub: https://github.com/L0veMathur
