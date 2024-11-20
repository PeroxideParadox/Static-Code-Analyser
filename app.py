import os
import io
import base64
import matplotlib
# Set the backend before importing pyplot
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

from flask import Flask, request, render_template, redirect, url_for, send_file
from CodeAnalyzer import CodeAnalyzer, run_code_with_tracking, calculate_emission_reduction

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
OPTIMIZED_FOLDER = 'optimized'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OPTIMIZED_FOLDER'] = OPTIMIZED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OPTIMIZED_FOLDER, exist_ok=True)

def generate_emissions_graph(original_emissions, optimized_emissions):
    """Generate a bar graph comparing carbon emissions"""
    plt.figure(figsize=(8, 5))
    labels = ['Original Code', 'Optimized Code']
    values = [original_emissions, optimized_emissions]
    
    bars = plt.bar(labels, values, color=['red', 'green'], alpha=0.8)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height:.6f}', 
                ha='center', va='bottom', fontsize=10)

    plt.xlabel('Code Version', fontsize=12)
    plt.ylabel('Emissions (kg CO2)', fontsize=12)
    plt.title('Comparison of Carbon Emissions', fontsize=14)
    plt.tight_layout()
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    # Encode the image to base64
    graph_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{graph_url}'

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

                issues = sorted(issues, key=lambda x: x['line'])

                # Save the optimized code
                optimized_file_path = os.path.join(app.config['OPTIMIZED_FOLDER'], f"optimized_{file.filename}")
                with open(optimized_file_path, 'w') as f:
                    f.write(optimized_code)

                # Calculate emissions
                original_emissions = run_code_with_tracking(file_path, is_optimized=False)
                optimized_emissions = run_code_with_tracking(optimized_file_path, is_optimized=True)
                improvement = calculate_emission_reduction(original_emissions, optimized_emissions)

                # Generate emissions graph
                graph_url = generate_emissions_graph(original_emissions, optimized_emissions)

                return render_template(
                    "index.html", 
                    original_code=original_code,
                    issues=issues, 
                    optimized_code=optimized_code, 
                    download_url=url_for('download_file', filename=f"optimized_{file.filename}"),
                    original_emissions=original_emissions,
                    optimized_emissions=optimized_emissions,
                    improvement=improvement,
                    graph_url=graph_url
                )

        # Handle text input
        elif 'code_input' in request.form:
            original_code = request.form['code_input']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], "input_code.py")

            with open(file_path, 'w') as f:
                f.write(original_code)

            analyzer = CodeAnalyzer(original_code)
            issues, optimized_code = analyzer.analyze()

            issues = sorted(issues, key=lambda x: x['line'])

            # Save the optimized code
            optimized_file_path = os.path.join(app.config['OPTIMIZED_FOLDER'], "optimized_input_code.py")
            with open(optimized_file_path, 'w') as f:
                f.write(optimized_code)

            # Calculate emissions
            original_emissions = run_code_with_tracking(file_path, is_optimized=False)
            optimized_emissions = run_code_with_tracking(optimized_file_path, is_optimized=True)
            improvement = calculate_emission_reduction(original_emissions, optimized_emissions)

            # Generate emissions graph
            graph_url = generate_emissions_graph(original_emissions, optimized_emissions)

            return render_template(
                "index.html", 
                original_code=original_code,
                issues=issues, 
                optimized_code=optimized_code, 
                download_url=url_for('download_file', filename="optimized_input_code.py"),
                original_emissions=original_emissions,
                optimized_emissions=optimized_emissions,
                improvement=improvement,
                graph_url=graph_url
            )

    return render_template("index.html", original_code=original_code)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OPTIMIZED_FOLDER'], filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)