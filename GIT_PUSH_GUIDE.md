# How to Push This Project to GitHub

## Step 1 — Create a GitHub Repository
1. Go to https://github.com
2. Click **New Repository**
3. Name it: `shopmax-returns-analysis`
4. Set to **Public**
5. Do NOT initialize with README (we already have one)
6. Click **Create Repository**

## Step 2 — Copy Your .pbix File
Copy your saved Power BI file into the powerbi folder:
```
shopmax-returns-analysis/powerbi/ShopMax_Returns_Dashboard.pbix
```

## Step 3 — Take a Dashboard Screenshot
1. Take a screenshot of your Power BI dashboard
2. Save it as `dashboard_screenshot.png`
3. Place it in the `assets/` folder

## Step 4 — Open VS Code Terminal
1. Open VS Code
2. Press Ctrl + ` (backtick) to open terminal
3. Navigate to your project folder:
```bash
cd path/to/shopmax-returns-analysis
```

## Step 5 — Push to GitHub
Run these commands one by one:

```bash
git init
git add .
git commit -m "Initial commit - ShopMax Returns & Refund Loss Recovery Project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shopmax-returns-analysis.git
git push -u origin main
```

Replace YOUR_USERNAME with your actual GitHub username.

## Step 6 — Verify on GitHub
Go to your GitHub profile and confirm all files are uploaded:
- README.md shows with full formatting
- sql/ folder has all 3 scripts
- powerbi/ folder has .pbix and guide
- assets/ has dashboard screenshot

Done! Your project is live on GitHub.
