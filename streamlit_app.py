from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
from huggingface_hub import InferenceClient

api_key = st.secrets["HUGGING_FACE_API_KEY"]

# Set streamlit page configuration
st.set_page_config(page_title="AI Agent", page_icon="img.svg")
st.title("AI Mentor")

# Initialize the variables in session state
if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = "" # stores the latest user Input
    
if 'generated' not in st.session_state:
    st.session_state['generated'] = [] # store AI generated responses 
    
if 'past' not in st.session_state:
    st.session_state['past'] = []  # store past user input

# define function to submit user input
def submit():
    # set entered_prompt to the current value of the prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # clear prompt_input
    st.session_state.prompt_input = ""

# Initialize Hugging Face Inference Client for Meta Llama Model 
client = InferenceClient(api_key= api_key) # Initialize Hugging Face Inference client

# Build Message List 
def build_message_list():
    """
    Build List of Messages including system , human_msg, and AI Message
    """
    
    zipped_messages = [
        {
            "role": "system",
            "content":"""Your name is AI Mentor. You are an AI Expert specializing in Machine Learning, Deep Learning, Neural Networks and LLMs And Artificial Intelligence
            Your sole task is to assist users in understanding AI/ML based Topics and Neural Networks and Deep Learning . You will generate the detailed explanation on the topics they provide, following the structure below. You donot generate any other type of content.
            1. Greet the user politely, ask their name, inquire the topic they want to Understand.
            2. Also use Headings and Sub Headings for better clarification.
            4. If a user discuss any sensitive topic, political topic politely respond with:
            - "I only assist you to expalin AI/ML based topics. Please provide me only an AI/ML related topic."
            3. Help users to understand the topic and use the following structure to generate the detailed explanation.
               - Short Introduction of the topic.
               - Main Point of the topic.
               - where it is used.
               - How it is used.
               - which time it is used.
               - Real World Use Cases.
               - 2 Real World Examples.
               - short conclusion.
            3. Give the tone a human touch.
            4. If the user discuss or ask anything else other than AI related topics , politely respond with:
            - "I only assist you to expalin AI/ML based topics. Please provide me only an AI/ML related topic."
            5. Be professional like a teacher , polite and encouraging at all times. But strictly limit responses to AI/ML based topics.   """
        }
    ]
    
    # Zip together the past and generated messages
    for human_msg, Ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append({"role":"user", "content":human_msg})
        if Ai_msg is not None:
            zipped_messages.append({"role":"assistant", "content":Ai_msg})
    return zipped_messages

def generate_response():
        """
        Generate AI response using Meta LLaMA Model.
        """
        # Build List of messages
        messages = build_message_list()
        # Generate response using the Meta Llama Model through Hugging face
        response = ""
        for message in client.chat_completion(
            model= "meta-llama/Llama-3.2-3B-Instruct",
            messages= messages,
            max_tokens=800, # Adjusted max tokens according to Hugging Face API.
            stream=True,  #Stream responses to handle in real time
            temperature=0.5,
            top_p= 0.60
        ):
            if "choices" in message and len(message.choices) > 0:
                response += message.choices[0].delta.get("content", "")
        return response
    
# Create a text Input for user 
st.text_input('YOU: ', key='prompt_input', on_change=submit)
   
if st.session_state.entered_prompt != "":
    # get user query
    user_query = st.session_state.entered_prompt
        
    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Genrete Response 
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)

    # Display the chat History
if st.session_state['generated']:
    for i in range(len(st.session_state["generated"])-1, -1, -1):
        # Display AI Response 
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],  is_user=True, key=str(i) + "_user")
