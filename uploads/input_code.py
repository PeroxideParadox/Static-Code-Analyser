<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Code Analyzer</title>
    <style>
        :root {
            --primary-color: #F3F3E0;
            --secondary-color: #133E87;
            --tertiary-color: #608BC1;
            --light-blue: #CBDCEB;
            --accent-color: #E0F7FA;
            --button-gradient: linear-gradient(135deg, #608BC1, #133E87);
            --soft-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        * {
            box-sizing: border-box;
            transition: all 0.3s ease;
        }

        body {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            background-color: var(--primary-color);
            color: var(--secondary-color);
            margin: 0;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            line-height: 1.6;
        }

        h1 {
            color: var(--secondary-color);
            font-size: 2.75rem;
            text-align: center;
            margin-bottom: 30px;
            letter-spacing: -0.5px;
        }

        textarea {
            width: 100%;
            height: 300px;
            padding: 15px;
            border: 2px solid var(--tertiary-color);
            border-radius: 12px;
            background-color: var(--accent-color);
            color: var(--secondary-color);
            font-size: 1rem;
            margin-bottom: 20px;
            resize: vertical;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            line-height: 1.5;
        }

        form {
            background-color: var(--light-blue);
            box-shadow: var(--soft-shadow);
            border-radius: 20px;
            padding: 35px;
            margin: 15px 0;
            width: 100%;
            max-width: 650px;
            transform-origin: center;
        }

        form input[type="file"] {
            margin-bottom: 20px;
            display: block;
        }

        form:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        }

        .emissions-section {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            width: 100%;
            max-width: 1200px;
            margin: 30px 0;
            justify-content: center;
        }

        .emissions-card {
            flex: 1;
            min-width: 300px;
            background-color: var(--light-blue);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: var(--soft-shadow);
        }

        .emissions-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }

        .emissions-value {
            font-size: 2rem;
            font-weight: bold;
            color: var(--secondary-color);
            margin: 15px 0;
        }

        .reduction-card {
            width: 100%;
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            margin-top: 20px;
        }

        .reduction-value {
            font-size: 2.5rem;
            font-weight: bold;
            margin: 15px 0;
        }

        .progress-container {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin: 15px 0;
        }

        .progress-bar {
            background: white;
            height: 100%;
            border-radius: 10px;
            transition: width 1s ease-in-out;
        }

        .card {
            background-color: var(--accent-color);
            border: 2px solid var(--light-blue);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: var(--soft-shadow);
            width: 100%;
            max-width: 650px;
        }

        .code-container {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 30px;
            width: 100%;
            max-width: 1300px;
            margin: 40px auto;
            align-items: start;
        }

        .code-box {
            background-color: var(--accent-color);
            border: 2px solid var(--light-blue);
            padding: 25px;
            border-radius: 15px;
            box-shadow: var(--soft-shadow);
            height: 100%;
            min-height: 400px;
            overflow: auto;
        }

        .code-box pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .download-btn {
            background: var(--button-gradient);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: bold;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
            text-decoration: none;
            display: inline-block;
            width: auto;
            min-width: 200px;
            text-align: center;
            margin: 20px 0;
        }

        button {
            background: var(--button-gradient);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            font-weight: bold;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
        }

        button:hover, .download-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .floating-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--button-gradient);
            border-radius: 50%;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
            z-index: 1000;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        .floating-btn:hover {
            transform: scale(1.1);
        }

        @media (max-width: 768px) {
            .code-container {
                grid-template-columns: 1fr;
            }
            
            .code-box {
                min-height: 300px;
            }
        }
    </style>
</head>
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>

<body>
    <h1>Python Code Analyzer</h1>
    
    <dotlottie-player src="https://lottie.host/172cfcaa-9141-4684-a107-840e08fc5f8a/B1T7agoBSJ.json" background="transparent" speed="1" style="width: 300px; height: 300px;" loop autoplay></dotlottie-player>

    <form action="/" method="POST" enctype="multipart/form-data">
        <h3>Upload a Python File:</h3>
        <input type="file" name="file" accept=".py">
        <button type="submit">Analyze File</button>
    </form>

    <form action="/" method="POST">
        <h3>Paste Python Code:</h3>
        <textarea name="code_input" placeholder="Paste your Python code here..."></textarea>
        <button type="submit">Analyze Code</button>
    </form>

    <dotlottie-player src="https://lottie.host/b81f2a21-e40a-4110-a745-c3009fc2e9d0/3axHqyQTlB.json" background="transparent" speed="1" style="width: 300px; height: 300px;" loop autoplay></dotlottie-player>

    {% if issues %}
    <h2>Detected Issues</h2>
    {% for issue in issues %}
    <div class="card">
        <strong>Line {{ issue.line }}:</strong> {{ issue.issue }}<br>
        <b>Recommendation:</b> {{ issue.recommendation }}
    </div>
    {% endfor %}
    {% endif %}

    {% if original_emissions is defined and optimized_emissions is defined %}
    <div class="emissions-section">
        <div class="emissions-card">
            <h3>Original Code Emissions</h3>
            <div class="emissions-value">{{ "%.6f"|format(original_emissions) }} kg CO₂</div>
        </div>
        
        <div class="emissions-card">
            <h3>Optimized Code Emissions</h3>
            <div class="emissions-value">{{ "%.6f"|format(optimized_emissions) }} kg CO₂</div>
        </div>

        {% if improvement is defined %}
        <div class="reduction-card">
            <h3>Carbon Footprint Reduction</h3>
            <div class="reduction-value">{{ "%.2f"|format(improvement) }}%</div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {{ "%.2f"|format(improvement) }}%"></div>
            </div>
            <p>Total Carbon Emissions Reduced</p>
        </div>
        {% endif %}
    </div>

    {% if graph_url %}
    <div class="card emissions-graph">
        <h3>Carbon Emissions Comparison</h3>
        <img src="{{ graph_url }}" alt="Emissions Comparison Graph" style="width: 100%; border-radius: 12px;">
    </div>
    {% endif %}
    {% endif %}

    <div class="code-container">
        <div class="code-box">
            <h2>Original Code:</h2>
            <pre id="original-code" class="language-python">{{ original_code }}</pre>
        </div>
        
        <dotlottie-player src="https://lottie.host/d0340c3b-8c07-40e4-bb12-2c9614da70af/os818t5d0g.json" background="transparent" speed="1" style="width: 300px; height: 300px;" loop autoplay></dotlottie-player>
        
        <div class="code-box">
            <h2>Optimized Code:</h2>
            <pre id="optimized-code" class="language-python">{{ optimized_code }}</pre>
        </div>
    </div>

    <div style="text-align: center;">
        <a href="{{ download_url }}" class="download-btn">Download Optimized Code</a>
    </div>

    <div class="floating-btn" onclick="copyToClipboard()">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="white">
            <path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1s-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm7 16H5V5h2v2h10V5h2v14z"/>
        </svg>
    </div>

    <script>
        function copyToClipboard() {
            const codeElement = document.getElementById('optimized-code');
            const codeText = codeElement.innerText;
            navigator.clipboard.writeText(codeText).then(() => {
                alert('Code copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy text: ', err);
            });
        }
    </script>
</body>
</html>