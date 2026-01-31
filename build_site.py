import os

# Define the structure
folders = [
    "content/services",
    "layouts/_default",
    "layouts/partials",
    "assets/css",
    "static",
    ".github/workflows"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# 1. Config File (Primary settings)
config = """
baseURL = 'https://fieldsolutions.us'
languageCode = 'en-us'
title = 'Field Solutions'
theme = [] # We are using a custom layout

[params]
    description = "Expert Industrial, Marine, and Mechanical Consulting"
    stripe_payment_link = "#" # REPLACE WITH YOUR STRIPE LINK
    stripe_portal_link = "#"  # REPLACE WITH YOUR STRIPE PORTAL LINK
"""

# 2. The Custom CSS (Red, White, Blue Theme)
css = """
body { font-family: 'Segoe UI', sans-serif; margin: 0; color: #333; line-height: 1.6; }
header { background: #002868; color: white; padding: 2rem; text-align: center; border-bottom: 5px solid #BF0A30; }
.hero { padding: 4rem 2rem; text-align: center; background: #f4f4f4; }
.btn { background: #BF0A30; color: white; padding: 1rem 2rem; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; margin-top: 10px;}
.container { max-width: 1000px; margin: auto; padding: 2rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
.card { border: 1px solid #ddd; padding: 1.5rem; border-radius: 8px; background: white; border-top: 4px solid #002868; }
.card h3 { color: #002868; margin-top: 0; }
footer { background: #333; color: white; text-align: center; padding: 2rem; margin-top: 40px; }
.logo { max-width: 150px; margin-bottom: 10px; }
"""

# 3. The Logo (Diamond SVG)
logo_svg = """
<svg width="150" height="90" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
  <path d="M100 5 L195 60 L100 115 L5 60 Z" fill="white" stroke="white" stroke-width="2"/>
  <path d="M100 12 L185 60 L100 108 L15 60 Z" fill="none" stroke="white" stroke-width="1.5"/>
  <text x="50%" y="65%" font-family="Arial Black, sans-serif" font-size="50" fill="#BF0A30" text-anchor="middle" dominant-baseline="middle">FS</text>
</svg>
"""

# 4. The HTML Layouts
base_html = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ .Title }} | Field Solutions</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <header>
        <div class="logo-container">""" + logo_svg + """</div>
        <h1>FIELD SOLUTIONS</h1>
        <p>Expert Consulting for Mechanical, Marine, & Millwright Systems</p>
    </header>
    {{ block "main" . }}{{ end }}
    <footer>
        <p>&copy; {{ now.Format "2006" }} Field Solutions. Patriotic Service, American Expertise.</p>
        <a href="{{ .Site.Params.stripe_portal_link }}" style="color:white;">Client Account Portal</a>
    </footer>
</body>
</html>
"""

index_html = """
{{ define "main" }}
<div class="hero">
    <h2>The Jack-of-all-Trades for Modern Industry</h2>
    <p>Providing precision solutions for whatever moves, floats, or stands.</p>
    <a href="{{ .Site.Params.stripe_payment_link }}" class="btn">Pay an Invoice</a>
</div>

<div class="container">
    <div class="grid">
        <div class="card">
            <h3>Millwright & Industrial</h3>
            <p>Precision machinery installation, laser alignment, and complex system troubleshooting.</p>
        </div>
        <div class="card">
            <h3>Marine Services</h3>
            <p>Specialized marine mechanics, diesel systems, and structural consulting for vessels.</p>
        </div>
        <div class="card">
            <h3>Mechanical & Fleet</h3>
            <p>From heavy equipment to automotive fleets, we keep the gears turning.</p>
        </div>
        <div class="card">
            <h3>Construction & Facilities</h3>
            <p>Facility maintenance consulting, building systems, and structural equipment installs.</p>
        </div>
    </div>
</div>
{{ end }}
"""

# 5. GitHub Actions Workflow (The "Magic" that deploys it)
github_action = """
name: deploy-to-gh-pages
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
          fetch-depth: 0
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          extended: true
      - name: Build
        run: hugo --minify
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
"""

# Writing files
files = {
    "hugo.toml": config,
    "assets/css/style.css": css,
    "layouts/_default/baseof.html": base_html,
    "layouts/index.html": index_html,
    "layouts/_default/single.html": '{{ define "main" }}<div class="container">{{ .Content }}</div>{{ end }}',
    "layouts/_default/list.html": '{{ define "main" }}<div class="container">{{ .Content }}</div>{{ end }}',
    "content/_index.md": "---\\ntitle: 'Home'\\n---",
    ".github/workflows/hugo.yml": github_action
}

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content.strip())

print("Stack Generated Successfully! Push to GitHub to go live.")