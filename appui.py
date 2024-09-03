import streamlit as st
import requests
import json
from io import BytesIO
import pandas as pd
import plotly.express as px

# Streamlit app title and icon
st.set_page_config(page_title="ExpenAI", page_icon="💸")
st.title("💸 ExpenAI")

# Initialize session state for wallet balance and transactions
if 'wallet_balance' not in st.session_state:
    st.session_state.wallet_balance = 0
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# Ask the user to enter their wallet balance
wallet_balance = st.number_input("Enter your wallet balance:", min_value=0, value=st.session_state.wallet_balance)
st.session_state.wallet_balance = wallet_balance

# Backend API endpoints
BACKEND_URL = "http://0.0.0.0:8000"  # Adjust this URL based on where your FastAPI app is running
UPLOAD_IMAGE_ENDPOINT = f"{BACKEND_URL}/upload-image/"
UPLOAD_AUDIO_ENDPOINT = f"{BACKEND_URL}/upload_audio/"
TEXT_PROMPT_ENDPOINT = f"{BACKEND_URL}/text_prompt/"

# Functions to interact with FastAPI backend
def process_image(file):
    files = {"file": (file.name, file, file.type)}
    response = requests.post(UPLOAD_IMAGE_ENDPOINT, files=files)
    return response.json()

def process_audio(file):
    files = {"file": (file.name, file, file.type)}
    response = requests.post(UPLOAD_AUDIO_ENDPOINT, files=files)
    return response.json()

def process_text(text):
    try:
        # Send the text as a query parameter
        response = requests.post(f"{TEXT_PROMPT_ENDPOINT}?invoice_text={text}")
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error occurred: {e}")
        st.write(response.text if response else "No response")  # More verbose error message
        return {}



# User options
st.header("Add Expenses")
col1, col2, col3 = st.columns(3)

# Option 1: Scan Bill
with col1:
    st.subheader("Scan Bill")
    uploaded_image = st.file_uploader("Upload an image file", type=['png', 'jpg', 'jpeg'])
    if st.button("Process Image") and uploaded_image is not None:
        with st.spinner("Processing..."):
            result = process_image(uploaded_image)
            if "response" in result:
                st.success("Expense processed!")
                st.session_state.transactions.append(result["response"])
            else:
                st.error("Failed to process the image")

# Option 2: Voice Input
with col2:
    st.subheader("Voice Input")
    uploaded_audio = st.file_uploader("Record or upload a .wav file", type=['wav'])
    if st.button("Process Audio") and uploaded_audio is not None:
        with st.spinner("Processing..."):
            result = process_audio(uploaded_audio)
            if "response" in result:
                st.success("Expense processed!")
                st.session_state.transactions.append(result["response"])
            else:
                st.error("Failed to process the audio")

# Option 3: Text Input
with col3:
    st.subheader("Text Input")
    text_input = st.text_area("Enter your expense description:")
    if st.button("Process Text") and text_input:
        with st.spinner("Processing..."):
            result = process_text(text_input)
            if "response" in result:
                st.success("Expense processed!")
                st.session_state.transactions.append(result["response"])
            else:
                st.error("Failed to process the text")

# Display Transactions
if st.session_state.transactions:
    st.header("Transaction Dashboard")
    
    # Prepare data for table and plots
    transactions_df = pd.DataFrame(st.session_state.transactions)
    transactions_df['S. No'] = transactions_df.index + 1
    transactions_df = transactions_df[['S. No', 'category', 'amount']]

    # Display the transactions in a table
    st.subheader("Transactions Table")
    st.dataframe(transactions_df)

    # Create a pie chart for categories
    st.subheader("Expenses by Category")
    pie_chart = px.pie(transactions_df, names='category', values='amount', title="Expenses by Category")
    st.plotly_chart(pie_chart, use_container_width=True)

    # Create a graph for wallet balance deductions
    st.subheader("Wallet Balance Over Time")
    wallet_df = transactions_df.copy()
    wallet_df['remaining_balance'] = wallet_balance - wallet_df['amount'].cumsum()
    wallet_line_chart = px.line(wallet_df, x='S. No', y='remaining_balance', title="Remaining Wallet Balance Over Time")
    st.plotly_chart(wallet_line_chart, use_container_width=True)

    # Update the wallet balance in the session state
    st.session_state.wallet_balance = wallet_df['remaining_balance'].iloc[-1]

# Footer
st.markdown("---")
st.write("ExpenAI: Your Personal Expense Tracker")

