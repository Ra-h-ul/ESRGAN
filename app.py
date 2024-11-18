import streamlit as st
import os
import subprocess
import sys

# Set fixed parameters
UPLOAD_DIR = "LR"
VENV_DIR = "myenv"  # Virtual environment directory

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Streamlit app title
st.title("Run CycleGAN Command from Streamlit")

# File uploader widget
uploaded_file = st.file_uploader("Upload a file", type=None, accept_multiple_files=False)

# Handle file upload
if uploaded_file is not None:
    # Define the file save path
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    
    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' has been saved to '{UPLOAD_DIR}'.")

# Button to run the CycleGAN command
if st.button("Run CycleGAN"):
    try:
        # Step 1: Check if Python 3.8 is installed
        if sys.version_info < (3, 8):
            st.error("Python 3.8 or higher is required for this environment.")
           
        
        # Step 2: Create the virtual environment (if it doesn't exist)
        if not os.path.exists(VENV_DIR):
            st.info("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", VENV_DIR])
            st.success("Virtual environment created successfully.")
        
        # Step 3: Activate the virtual environment and install dependencies
        activate_command = f"source {VENV_DIR}/bin/activate"
        subprocess.run(activate_command, shell=True)
        
        # Step 4: Install dependencies (like torch, tensorflow, etc.)
        st.info("Installing dependencies...")
        subprocess.run([f"{VENV_DIR}/bin/pip", "install", "-r", "requirements.txt"])
        st.success("Dependencies installed successfully.")
        
        # Step 5: Construct the command to run CycleGAN
        command = [
            "python",
            "test.py",
        ]
        
        # Step 6: Run the CycleGAN command
        st.info("Running CycleGAN...")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Display the output
        st.subheader("Command Output")
        st.text(result.stdout)
        
        #process completed
        st.subheader("process completed")
        # Display any errors
        if result.stderr:
            st.subheader("Errors")
            st.text(result.stderr)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")