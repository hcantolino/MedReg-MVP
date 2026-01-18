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

# Custom CSS for the + upload box
st.markdown("""
<style>
.upload-box {
    width: 300px;
    height: 300px;
    border: 4px dashed #0693e3;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 100px;
    color: #0693e3;
    background-color: #f8f9fa;
    cursor: pointer;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)

# Main area logic
uploaded_file = st.file_uploader("", type=["csv", "xlsx"], key="hidden_uploader", label_visibility="collapsed")

if uploaded_file is None:
    # No file: Show centered + box (clickable)
    st.markdown("<h3 style='text-align: center; color: #555;'>Upload Medical Files to Begin Analysis</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<label for="visible_uploader"><div class="upload-box">+</div></label>', unsafe_allow_html=True)
        # This hidden uploader makes the + box clickable
        st.file_uploader("Upload CSV/Excel with 'time' and 'event' columns for custom analysis", 
                         type=["csv", "xlsx"], key="visible_uploader", label_visibility="collapsed")
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
                # Mock survival data (20 patients)
                times = np.array([5, 6, 6, 7, 9, 10, 12, 15, 17, 25, 30, 32, 33, 34, 40, 5, 8, 11, 13, 18])
                events = np.array([1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1])
            
            # Generate Kaplan-Meier curve
            sf = SurvfuncRight(times, events)
            fig, ax = plt.subplots(figsize=(12, 8))
            sf.plot(ax=ax, drawstyle='steps-post')  # Stepped line like standard KM plots
            ax.set_title("Overall Survival of Patients (Kaplan-Meier Estimate)", fontsize=16)
            ax.set_xlabel("Time (e.g., Months)", fontsize=14)
            ax.set_ylabel("Survival Probability", fontsize=14)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_ylim(0, 1.05)
            st.pyplot(fig)
            
            # Optional: Data preview below chart
            st.subheader("Uploaded Data Preview")
            st.dataframe(df.head(10))
        
        elif navigation == "Clinical Writing":
            st.header("Clinical Writing Report")
            st.write("Mock report generation based on uploaded data...")
            # (Keep/expand your old code here)
        
        elif navigation == "Medical Device Writing":
            st.header("Medical Device Writing")
            st.write("Mock device documentation...")
            # (Expand later)
        
        elif navigation == "Copywriting":
            st.header("Copywriting Assistance")
            st.write("Generated promotional text based on data...")
            # (Expand later)
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}. Check format/columns.")

# If no file and not Biostatistics, show welcome or placeholder
if uploaded_file is None and navigation != "Biostatistics":
    st.info(f"Select '{navigation}' and upload a file to see results.")