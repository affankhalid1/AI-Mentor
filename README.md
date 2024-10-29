# AI Mentor
This repository features an AI-powered mentoring chatbot designed to assist users in learning AI topics, including Machine Learning (ML), Deep Learning (DL), and Generative AI. With personalized guidance and interactive Q&amp;A, it aims to enhance understanding and empower users to achieve their educational goals in artificial intelligence.

## Steps to run the AI Mentor locally:

1: **Set up API Key:**

   - Create a `.streamlit` folder in the root directory.
   - Inside the folder, create a file named secrets.toml with the following content:
     
     ```toml
     HUGGING_FACE_API_KEY = "<Enter_your_HuggingFace_Api_key>"
     ```
         
2: **Create a Conda Environment and Install Dependencies:**

   - Run the following command to install the required packages:
     
     ```cmd 
     pip install -r requirements.txt

3: **Run the App on Localhost:**

   - Start the application by running:
     
     ```cmd 
     streamlit run streamlit_app.py
