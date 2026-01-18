import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.duration.survfunc import SurvfuncRight  # For Kaplan-Meier

# App title
st.title("MedReg MVP: Medical Regulatory Platform")

# Sidebar navigation only (no uploader here)
navigation = st.sidebar.radio(
    "Select Service",
    ["Biostatistics", "Clinical Writing", "Medical Device Writing", "Copywriting"]
)

# Custom CSS for large centered + box and hide default uploader text/button
st.markdown("""
<style>
.upload-box {
    width: 400px;
    height: 400px;
    border: 5px dashed #0693e3;
    border-radius: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 150px;
    color: #0693e3;
    background-color: #f8f9fa;
    cursor: pointer;
    margin: 50px auto;
}
 /* Hide default uploader text, button, and drag area */
 .stFileUploader > div > div > div > span {
    display: none !important;
 }
 .stFileUploader > div > div > div > button {
    display: none !important;
 }
 .stFileUploader > div > div > div > div:first-child {
    display: none !important;
 }
</style>
""", unsafe_allow_html=True)

# The main uploader (label empty to hide default text)
uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

if uploaded_file is None:
    # No file: Show centered + box (click the whole box to upload)
    st.markdown("<h3 style='text-align: center; color: #555;'>Upload Medical Files to Begin Analysis</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="upload-box">+</div>', unsafe_allow_html=True)
else:
    # File uploaded: Process and show section content
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        if navigation == "Biostatistics":
            st.header("Biostatistics Analysis")
            
            # Prepare data for Kaplan-Meier
            if 'time' in df.columns and 'event' in df.columns:
                times = df['time'].astype(float).dropna().values
                events = df['event'].astype(int).dropna().values
                st.success("Using uploaded data for survival analysis.")
            else:
                st.warning("Columns 'time' (duration) and 'event' (1=death/event, 0=censored) not found. Using mock data.")
                times = np.array([5, 6, 6, 7, 9, 10, 12, 15, 17, 25, 30, 32, 33, 34, 40, 5, 8, 11, 13, 18])
                events = np.array([1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1])
            
            # Fit Kaplan-Meier
            sf = SurvfuncRight(times, events)
            
            # Generate Kaplan-Meier curve (manual step plot - no CI or censor marks to avoid errors)
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.step(sf.surv_times, sf.surv_prob, where='post', color='blue', linewidth=2)
            ax.set_title("Overall Survival of Patients (Kaplan-Meier Estimate)", fontsize=16)
            ax.set_xlabel("Time (e.g., Months)", fontsize=14)
            ax.set_ylabel("Survival Probability", fontsize=14)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_ylim(0, 1.05)
            ax.set_xlim(0, sf.surv_times.max() * 1.05)
            st.pyplot(fig, use_container_width=True)  # Centered and responsive
            
            # Data preview below chart
            st.subheader("Uploaded Data Preview")
            st.dataframe(df.head(10))
        
        elif navigation == "Clinical Writing":
            st.header("Clinical Writing Report")
            st.write("Mock report generation based on uploaded data...")
        
        elif navigation == "Medical Device Writing":
            st.header("Medical Device Writing")
            st.write("Mock device documentation...")
        
        elif navigation == "Copywriting":
            st.header("Copywriting Assistance")
            st.write("Generated promotional text based on data...")
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}. Check format/columns.")

if uploaded_file is None:
    st.info("Click the + box to upload a file and begin.")