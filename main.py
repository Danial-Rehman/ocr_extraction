import streamlit as st
import requests
import pandas as pd
import csv
import os

base_url = "https://danial123.pythonanywhere.com/api/payments/"

def send_folder_id(folder_id):
    payload = {'folder_id': folder_id}
    try:
        response = requests.post(base_url, json=payload)
        if response.status_code == 200:
            st.success("Payment saved successfully!")
        else:
            st.error(f"Failed to save payment. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def download_payments():
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            payments = response.json()

            csv_file = "data.csv"
            if os.path.exists(csv_file):
                os.remove(csv_file)

            with open(csv_file, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=payments[0].keys())
                writer.writeheader()
                for payment in payments:
                    writer.writerow(payment)
            
            df = pd.read_csv(csv_file)
            st.download_button(label="Download Payments CSV", data=df.to_csv(index=False), file_name="payments.csv", mime="text/csv")
        else:
            st.error(f"Failed to fetch payments. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.title("Payments Management App")

st.subheader("Submit Payment")
folder_id = st.text_input("Enter Folder ID")
if st.button("Send Folder ID"):
    send_folder_id(folder_id)

st.subheader("Download Payments")
if st.button("Download Payments CSV"):
    download_payments()
