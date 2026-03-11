# Firebase Project Setup Instructions

## AUTONOMOUS ACTION REQUIRED

1. **Create Firebase Project:**
   - Visit: https://console.firebase.google.com/
   - Click "Create Project"
   - Name: "Project-Chrysalis"
   - Disable Google Analytics (for minimalism)
   - Click "Create Project"

2. **Enable Firestore Database:**
   - In Firebase Console, go to "Firestore Database"
   - Click "Create Database"
   - Choose "Start in production mode"
   - Location: Select closest region (e.g., europe-west1)
   - Click "Enable"

3. **Create Service Account:**
   - Go to Project Settings → Service Accounts
   - Click "Generate New Private Key"
   - Confirm "Generate Key"
   - Save JSON file as `firebase-credentials.json`
   - Move to project root directory

4. **Configure Firestore Collections:**
   - Run the initialization script:
     ```bash
     python chrysalis/init_firestore.py
     ```
   This will create the required collections and security rules.

## SECURITY NOTES:
- NEVER commit firebase-credentials.json to version control
- Add firebase-credentials.json to .gitignore
- Restrict database access via Firestore security rules (provided in init script)