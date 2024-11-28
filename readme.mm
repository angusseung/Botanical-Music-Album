<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Art and Music Project</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            padding: 0;
            background-color: #f9f9f9;
        }
        h1, h2, h3 {
            color: #333;
        }
        code {
            background-color: #eee;
            padding: 2px 4px;
            border-radius: 4px;
        }
        pre {
            background-color: #eee;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
    </style>
</head>
<body>

<h1>Overview</h1>
<p>This project offers an interactive platform for creating AI-generated art and music, blending creativity with advanced technology. Users can select from various art styles inspired by historical periods and artists, upload personal plant images, and generate unique visual and auditory content, making for a highly personalized creative experience.</p>

<h2>Setup Guide</h2>
<ol>
    <li><strong>Install ComfyUI</strong>: Ensure that ComfyUI is installed on your system.</li>
    <li><strong>Launch ComfyUI</strong>: Open ComfyUI, click the sidebar in the bottom right, and select <strong>Load</strong> to choose the <code>workflow_api.json</code> file.</li>
    <li><strong>Configure API</strong>: Set the Open Web UI top bar API to <code>http://127.0.0.1:8188/</code>.</li>
    <li><strong>Check Checkpoint Name</strong>: Ensure the <code>ckpt_name</code> in the Load Checkpoint node matches the <code>ckpt_name</code> in the <code>workflow_api.json</code> file.</li>
    <li><strong>Python Version</strong>: Run the application using Python <strong>3.11.9</strong>.</li>
    <li><strong>Change Directory</strong>: Enter <code>cd streamlit_web_UI</code> to navigate to the correct directory.</li>
    <li><strong>Install Requirements</strong>: Run <code>pip install -r requirements.txt</code> to install the necessary packages.</li>
    <li><strong>Start Streamlit</strong>: Execute <code>python -m streamlit run UI.py</code> to start the application.</li>
</ol>

<h2>Music Generate Flow</h2>
<ol>
    <li><strong>Select Art Style</strong>: Users can choose an art style from a diverse range inspired by various historical artists.</li>
    <li><strong>Import Plant Image</strong>: Upload a personal plant image or select from default images located in <code>Music-Album-Generator/streamlit_web_UI/image_chosen</code>.</li>
    <li><strong>Enter Textual Descriptions</strong>: Provide additional information such as your name, album name, or other descriptions. These details will be stored in the Album Gallery for personalization.</li>
    <li><strong>Wait for Processing</strong>: After submission, wait briefly as the system processes the data and generates content.</li>
    <li><strong>View & Hear Generated Content</strong>: Once processing is complete, users will be redirected to a new interface to view the generated image and listen to the accompanying music or sound.</li>
    <li><strong>Album Gallery</strong>: Access the Album Gallery to view content created by yourself and others, allowing exploration of previously generated works and new artistic possibilities.</li>
</ol>

<p>This platform seamlessly integrates art and music, encouraging creativity through user engagement and AI technology.</p>

</body>
</html>