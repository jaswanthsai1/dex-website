# FREE FIRE ACCOUNT INFO

🔥 Free Fire Account Information Decoder 🔥

Owned by: JASWANTH SAI

## Overview

This web application allows users to decode Garena EAT (Encrypted Access Token) to retrieve Free Fire account information including account ID, nickname, and other details.

## Features

- Clean, responsive user interface
- Real-time token decoding
- Secure token processing
- Detailed account information display
- Mobile-friendly design

## Local Development

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```
5. Open your browser and go to `http://localhost:8000`

## Deployment to Vercel

This application is configured for deployment on Vercel.

### Steps to Deploy:

1. Fork this repository to your GitHub account
2. Sign up or log in to [Vercel](https://vercel.com)
3. Click "New Project" and select "Import from Git"
4. Select your forked repository
5. Vercel will automatically detect it's a Python project and use the configuration in `vercel.json`
6. Click "Deploy" and wait for the build to complete
7. Your application will be live at the provided URL

### GitHub Integration

Alternatively, you can connect your GitHub account to Vercel and deploy directly from GitHub:
1. Connect your GitHub account to Vercel
2. Import your repository
3. Vercel will automatically deploy on pushes to main branch

## How to Use

1. Enter a valid Garena EAT token in the input field
2. Click "Decode Token"
3. View the decoded account information
4. Information displayed includes:
   - Account ID
   - Nickname
   - Open ID
   - Access Token
   - Region
   - Credits

## Security Notice

⚠️ This application handles sensitive account information. Only use with tokens you own or have permission to access.

## Files Structure

- `index.html` - Main HTML interface
- `styles.css` - Styling and layout
- `script.js` - Frontend JavaScript logic
- `api.py` - Backend API and server
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel deployment configuration

## Contributing

Feel free to fork this repository and submit pull requests for improvements.

## License

This project is for educational purposes only.