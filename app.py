from flask import Flask, render_template_string, request, redirect, url_for, session
import os
import pandas as pd 
from preprocess import preprocess_data  
from load_model import loaded_models  # Assuming this is the correct import path for your models

app = Flask(__name__)

app.secret_key = 'sdh swhcaskc askcoasclaksc '  # use a strong, random string

# Dummy credentials
USERNAME = 'nagesh'
PASSWORD = 'churn'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

login_template = '''
<!DOCTYPE html> 
<html>
<head>
    <title>Admin Login</title>
    <style>
        body {
            background-color: #121212;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            margin-bottom: 40px;
            font-size: 28px;
            color: #00bcd4;
        }
        form {
            background-color: #1e1e1e;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0, 188, 212, 0.3);
        }
        input {
            padding: 10px;
            margin: 10px 0;
            width: 250px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
        }
        input[type="submit"] {
            background-color: #00bcd4;
            color: white;
            cursor: pointer;
            font-weight: bold;
            margin-left: 10px;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Integrated Decision Support Tool for Churn Analysis</h1>
    <form method="POST">
        <div><input type="text" name="username" placeholder="Username" required></div>
        <div><input type="password" name="password" placeholder="Password" required></div>
        <div><input type="submit" value="Login"></div>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True 
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
    return render_template_string(login_template, error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/data')
def data_page():
    if not session.get('logged_in'):
        return redirect('/')
    
    try:
        train_df = pd.read_csv('cleaned_train.csv')
        test_df = pd.read_csv('cleaned_test.csv')
    except Exception as e:
        return f"<h2 style='color: red;'>Error loading CSV files: {e}</h2>"

    train_html = train_df.head(10).to_html(classes='data-table', index=False)
    test_html = test_df.head(10).to_html(classes='data-table', index=False)

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Data View</title>
        <style>
            body {{
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background-color: #121212;
                color: white;
                display: flex;
            }}
            .sidebar {{
                width: 220px;
                background-color: #1f1f1f;
                padding: 20px;
            }}
            .sidebar h2 {{
                color: #00bcd4;
            }}
            .sidebar a {{
                display: block;
                color: white;
                text-decoration: none;
                padding: 10px 0;
                border-bottom: 1px solid #333;
            }}
            .sidebar a:hover {{
                background-color: #00bcd4;
                color: black;
                border-radius: 4px;
                padding-left: 10px;
            }}
            .main-content {{
                flex: 1;
                padding: 20px;
                overflow-x: auto;
            }}
            .data-table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 40px;
                color: white;
            }}
            .data-table th, .data-table td {{
                border: 1px solid #444;
                padding: 8px;
                text-align: left;
            }}
            .data-table th {{
                background-color: #00bcd4;
                color: black;
            }}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Navigation</h2>
            <a href="/dashboard">Dashboard</a>
            <a href="/data">Data</a>
            <a href="/models">Models</a>
            <a href="/Test">Test</a>
            <a href="/">Logout</a>
        </div>
        <div class="main-content">
            <h2>Train Data (first 10 rows)</h2>
            {train_html}
            <h2>Test Data (first 10 rows)</h2>
            {test_html}
        </div>
    </body>
    </html>
    '''


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background-color: #121212;
                color: white;
                display: flex;
            }
            .sidebar {
                width: 220px;
                height: 100vh;
                background-color: #1f1f1f;
                padding: 20px;
                box-shadow: 2px 0 5px rgba(0,0,0,0.5);
            }
            .sidebar h2 {
                color: #00bcd4;
                margin-bottom: 20px;
            }
            .sidebar a {
                display: block;
                color: white;
                text-decoration: none;
                padding: 10px 0;
                margin: 5px 0;
                border-bottom: 1px solid #333;
                transition: background 0.3s;
            }
            .sidebar a:hover {
                background-color: #00bcd4;
                color: black;
                border-radius: 4px;
                padding-left: 10px;
            }
            .main-content {
                flex: 1;
                padding: 20px;
            }
            iframe {
                width: 100%;
                height: 85vh;
                border: none;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 188, 212, 0.3);
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Navigation</h2>
            <a href="/dashboard">Dashboard</a>
            <a href="/data">Data</a>
            <a href="/models">Models</a>
            <a href="/Test">Test</a>
            <a href="/">Logout</a>
        </div>
        <div class="main-content">
            <h2>Power BI Dashboard</h2>
            <iframe title="codivy dashboard" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=88f21ee6-0be6-4823-a852-74bb1a5a3afa&autoAuth=true&ctid=474565c1-bca4-4295-a2f5-b0c7dbf2591c" frameborder="0" allowFullScreen="true">
            </iframe>
        </div>
    </body>
    </html>
    '''

@app.route('/models')
def models_page():
    if not session.get('logged_in'):
        return redirect('/')

    model_data = {
        'Model': ['Decision Tree', 'Gradient Boosting', 'Random Forest', 'Logistic Regression', 'KNN', 'Naive Bayes'],
        'Accuracy': [1.00000, 0.99995, 0.99815, 0.86915, 0.66700, 0.66125],
        'Precision': [1.0, 1.0, 0.997444, 0.874546, 0.654557, 0.617757],
        'Recall': [1.0, 0.999884, 0.998256, 0.812209, 0.477674, 0.556628],
        'F1 Score': [1.0, 0.999942, 0.997850, 0.842226, 0.552299, 0.585602],
        'ROC AUC': [1.0, 1.0, 0.999982, 0.933140, 0.702908, 0.697425]
    }
    df = pd.DataFrame(model_data)
    table_html = df.to_html(classes='data-table', index=False)

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Models</title>
        <style>
            body {{
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background-color: #121212;
                color: white;
                display: flex;
            }}
            .sidebar {{
                width: 220px;
                background-color: #1f1f1f;
                padding: 20px;

            }}
            .sidebar h2 {{
                color: #00bcd4;
            }}
            .sidebar a {{
                display: block;
                color: white;
                text-decoration: none;
                padding: 10px 0;
                border-bottom: 1px solid #333;
            }}
            .sidebar a:hover {{
                background-color: #00bcd4;
                color: black;
                border-radius: 4px;
                padding-left: 10px;
            }}
            .main-content {{
                flex: 1;
                padding: 20px;
                overflow-x: auto;
            }}
            .data-table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 40px;
                color: white;
            }}
            .data-table th, .data-table td {{
                border: 1px solid #444;
                padding: 8px;
                text-align: left;
            }}
            .data-table th {{
                background-color: #00bcd4;
                color: black;
            }}
            img {{
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 188, 212, 0.3);
            }}
            img {{
                max-width: 600px;  /* max width */
                height: auto;      /* keep aspect ratio */
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 188, 212, 0.3);
            }}

        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Navigation</h2>
            <a href="/dashboard">Dashboard</a>
            <a href="/data">Data</a>
            <a href="/models">Models</a>
            <a href="/Test">Test</a>
            <a href="/">Logout</a>
        </div>
        <div class="main-content">
            <h2>Model Performance Summary</h2>
            {table_html}
            <h2>Top 20 Features (Feature Importance)</h2>
            <img src="/static/image.png" alt="Feature Importance">
        </div>
    </body>
    </html>
    '''

uploaded_filename = None  # store file name globally or in session

@app.route('/Test', methods=['GET', 'POST'])
def test_page():
    global uploaded_filename,processed_df
    if not session.get('logged_in'):
        return redirect('/')

    message = ''
    preview_table = ''
    processed_table = ''

    if request.method == 'POST':
        if 'file' in request.files:
            # Handle file upload
            file = request.files.get('file')
            if file and file.filename.endswith('.csv'):
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                uploaded_filename = file.filename
                df = pd.read_csv(filepath)
                preview_table = df.iloc[:6,:3].to_html(classes='data-table', index=False)
                message = f"✅ File '{file.filename}' uploaded successfully!"
            else:
                message = "❌ Please upload a valid CSV file."

        elif 'preprocess' in request.form and uploaded_filename:
            # Handle preprocessing
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_filename)
            try:
                df = pd.read_csv(filepath)
                processed_df, error = preprocess_data(df)
                if error:
                    message = f"⚠️ Error during preprocessing: {error}"
                else:
                    processed_table = processed_df.iloc[:6,:3].to_html(classes='data-table', index=False)
                    message = f"✅ Preprocessing completed successfully!"
            except Exception as e:
                message = f"⚠️ Could not process file: {e}"

        elif 'selected_model' in request.form:
            model_name = request.form.get('selected_model')
            model = loaded_models.get(model_name)

            if processed_df is not None:
                predictions = model.predict(processed_df)
                result_html = pd.DataFrame(predictions, columns=['Prediction']).head(10).to_html(classes='data-table', index=False)
                message = f"✅ Predictions using {model_name} completed!"
            else:
                message = "❌ Please preprocess the data first."


    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Data Upload & Preprocessing</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background-color: #121212;
                color: white;
                display: flex;
            }
            .sidebar {
                width: 220px;
                min-height: 100vh;
                background-color: #1f1f1f;
                padding: 20px;
                position: sticky;
                top: 0;
                align-self: flex-start;
            }
            .sidebar h2 {
                color: #00bcd4;
            }
            .sidebar a {
                display: block;
                color: white;
                text-decoration: none;
                padding: 10px 0;
                border-bottom: 1px solid #333;
            }
            .sidebar a:hover {
                background-color: #00bcd4;
                color: black;
                border-radius: 4px;
                padding-left: 10px;
            }
            .main-content {
                flex: 1;
                padding: 40px;
            }
            .upload-box {
                background-color: #1f1f1f;
                padding: 30px;
                border-radius: 10px;
                width: 600px;
                margin: auto;
                box-shadow: 0 0 10px rgba(0,188,212,0.3);
                text-align: center;
            }
            input[type="file"], input[type="submit"] {
                margin: 15px 5px;
                padding: 10px;
                font-size: 16px;
            }
            .message {
                margin-top: 20px;
                color: #00ff90;
            }
            .data-table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 30px;
                color: white;
            }
            .data-table th, .data-table td {
                border: 1px solid #444;
                padding: 8px;
                text-align: left;
            }
            .data-table th {
                background-color: #00bcd4;
                color: black;
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Navigation</h2>
            <a href="/dashboard">Dashboard</a>
            <a href="/data">Data</a>
            <a href="/models">Models</a>
            <a href="/Test">Test</a>
            <a href="/logout">Logout</a>
        </div>
        <div class="main-content">
            <div class="upload-box">
                <h2>Upload & Preprocess Test CSV</h2>
                <form method="POST" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <input type="submit" value="Upload">
                </form>
                {% if uploaded_filename %}
                <form method="POST">
                    <input type="hidden" name="preprocess" value="true">
                    <input type="submit" value="Preprocess">
                </form>
                <form method="POST">
                    <label for="selected_model">Choose a model:</label><br>
                    <select name="selected_model" required>
                        <option value="Logistic Regression">Logistic Regression</option>
                        <option value="Decision Tree">Decision Tree</option>
                        <option value="Random Forest">Random Forest</option>
                        <option value="KNN">KNN</option>
                        <option value="Naive Bayes">Naive Bayes</option>
                        <option value="Gradient Boosting">Gradient Boosting</option>
                    </select><br><br>
                    <input type="submit" value="Predict">
                </form>
                {% endif %}
                {% if message %}
                    <div class="message">{{ message }}</div>
                {% endif %}
                {{ preview_table|safe }}
                {{ processed_table|safe }}
            </div>
        </div>
    </body>
    </html>
    ''', message=message, preview_table=preview_table, processed_table=processed_table, uploaded_filename=uploaded_filename)
