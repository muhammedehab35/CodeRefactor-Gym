"""
Simple web interface for CodeRefactor Gym Space.
This provides a basic HTML page to show the environment is running.
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Display environment info page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CodeRefactor Gym - OpenEnv Hackathon</title>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            }
            h1 { font-size: 2.5em; margin-bottom: 10px; }
            h2 { color: #ffd700; margin-top: 30px; }
            code {
                background: rgba(0, 0, 0, 0.3);
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            pre {
                background: rgba(0, 0, 0, 0.5);
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
            }
            .status {
                display: inline-block;
                background: #00ff00;
                color: #000;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
            }
            a {
                color: #ffd700;
                text-decoration: none;
            }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏋️ CodeRefactor Gym</h1>
            <p><span class="status">✓ RUNNING</span></p>

            <p>
                Un environnement OpenEnv qui apprend aux agents RL à refactoriser
                du code legacy en code moderne et maintenable.
            </p>

            <h2>📊 Caractéristiques</h2>
            <ul>
                <li>5 types de code legacy différents</li>
                <li>Métriques de qualité objectives (complexité, type hints, etc.)</li>
                <li>Rewards: -10 à +18 selon amélioration</li>
                <li>Validation syntaxe AST Python</li>
            </ul>

            <h2>🔗 Endpoints API</h2>
            <ul>
                <li><code>GET /health</code> - Health check</li>
                <li><code>POST /reset</code> - Reset environment</li>
                <li><code>POST /step</code> - Execute action</li>
                <li><code>GET /state</code> - Get current state</li>
                <li><code>GET /docs</code> - API documentation (OpenAPI)</li>
            </ul>

            <h2>💻 Exemple d'utilisation</h2>
            <pre><code>from openenv.client import Client
from models import CodeRefactorGymAction

# Connecter
client = Client(base_url="https://mo35-code-refactor-gym.hf.space")

# Reset
obs = client.reset()
print(f"Legacy code: {obs.legacy_code}")

# Refactoriser
action = CodeRefactorGymAction(
    refactored_code="...",
    reasoning="Added type hints and docstrings"
)
result = client.step(action)
print(f"Reward: {result.reward}")
print(f"Improvement: {result.improvement_score}/100")</code></pre>

            <h2>📚 Documentation</h2>
            <ul>
                <li><a href="/docs">API Documentation (Swagger UI)</a></li>
                <li><a href="https://github.com/meta-pytorch/OpenEnv">OpenEnv Framework</a></li>
            </ul>

            <h2>🏆 OpenEnv Hackathon 2025</h2>
            <p>
                Créé par <strong>mo35</strong> pour l'OpenEnv Hackathon.<br>
                Framework: OpenEnv + TRL (GRPO) + Unsloth<br>
                GPU: Northflank H100 80GB
            </p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
