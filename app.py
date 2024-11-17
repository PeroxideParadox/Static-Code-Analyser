from flask import Flask, request, render_template, redirect, url_for, send_file
import os
from CodeAnalyzer import CodeAnalyzer

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
OPTIMIZED_FOLDER = 'optimized'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OPTIMIZED_FOLDER'] = OPTIMIZED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OPTIMIZED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    original_code = ""
    if request.method == "POST":
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.py'):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                # Analyze the code
                with open(file_path, 'r') as f:
                    original_code = f.read()

                analyzer = CodeAnalyzer(original_code)
                issues, optimized_code = analyzer.analyze()

                # Save the optimized code
                optimized_file_path = os.path.join(app.config['OPTIMIZED_FOLDER'], f"optimized_{file.filename}")
                with open(optimized_file_path, 'w') as f:
                    f.write(optimized_code)

                return render_template(
                    "index.html", 
                    original_code=original_code,
                    issues=issues, 
                    optimized_code=optimized_code, 
                    download_url=url_for('download_file', filename=f"optimized_{file.filename}")
                )

        # Handle text input
        elif 'code_input' in request.form:
            original_code = request.form['code_input']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], "input_code.py")

            with open(file_path, 'w') as f:
                f.write(original_code)

            analyzer = CodeAnalyzer(original_code)
            issues, optimized_code = analyzer.analyze()

            # Save the optimized code
            optimized_file_path = os.path.join(app.config['OPTIMIZED_FOLDER'], "optimized_input_code.py")
            with open(optimized_file_path, 'w') as f:
                f.write(optimized_code)

            return render_template(
                "index.html", 
                original_code=original_code,
                issues=issues, 
                optimized_code=optimized_code, 
                download_url=url_for('download_file', filename="optimized_input_code.py")
            )

    return render_template("index.html", original_code=original_code)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OPTIMIZED_FOLDER'], filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
