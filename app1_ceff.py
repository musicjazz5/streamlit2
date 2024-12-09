import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import app2  # Import App 2
# Manage session state for app selection and chat
if "selected_app" not in st.session_state:
    st.session_state.selected_app = "App 2: Another Application"
if "ceff_change" not in st.session_state:
    st.session_state.ceff_change = 0  # Initialize \(C_{eff}\) slider value
if "messages" not in st.session_state:
    st.session_state.messages = []

# Manage session state for cover page


# Function to switch to main app
def start_analysis():
    st.session_state.start_app = True

# Function to switch to cover page
def back_to_cover():
    st.session_state.start_app = False

# Function to switch between apps
def select_app(selected_app):
    st.session_state.selected_app = selected_app

# Cover Page
if "start_app" not in st.session_state:
    st.session_state.start_app = False

if not st.session_state.start_app:
    st.title("Welcome to the Multi-App Platform")
    st.image("image", caption="Technical Application Suite", use_column_width=True)
    st.markdown("""
    Select an app to proceed from the dropdown below.  
    Use the chat box to interact with the app or type "start" to begin.
    """)

    # App selection dropdown
  #  app_options = ["Frequency Sensitivity Analysis Tool", "App 2: Another Application"]
  #  selected_app = st.selectbox("Choose an application:", app_options, index=0, on_change=select_app, args=(st.session_state.selected_app,))

    # App selection dropdown
    app_options = ["Frequency Sensitivity Analysis Tool", "App 2: Another Application"]
    selected_app = st.selectbox("Choose an application:", app_options, index=app_options.index(st.session_state.selected_app))
    st.session_state.selected_app = selected_app  # Update session state based on dropdown selection


    # Chat and Start Button
    st.button("Start Selected App", on_click=lambda: st.session_state.update({"start_app": True}))

    # Chat Input
    chat_message = st.chat_input("Type 'start' to begin or interact with the app.")
    if chat_message:
        st.session_state.messages.append({"role": "user", "content": chat_message})
        if chat_message.lower() == "start":
            st.session_state.start_app = True
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Selected App: {st.session_state.selected_app}. Use the dropdown to switch apps or type 'start' to proceed."
            })

    # Display Chat History
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])


# Main Apps
elif st.session_state.selected_app == "Frequency Sensitivity Analysis Tool":
    st.title("Frequency Sensitivity to Ceff Changes at Selected Vdd Levels")
    st.markdown("""
    This tool evaluates the **frequency sensitivity (\(\%\Delta f\))** and the **frequency offset (\(\%\Delta f\))** 
    relative to \(C_{eff}\) change = 0 for selected \(V_{dd}\) values. Adjust the \(C_{eff}\) percentage change via the slider or chat input.
    """)

    # Add "Back to Cover Page" button
    st.button("Back to Cover Page", on_click=back_to_cover)

    # Sidebar Inputs
    st.sidebar.header("Input Parameters")
    ceff_base = 100
    freq_base = 100
    vdd_base = 0.75  # Fixed base voltage

    # Dropdown for Vdd selection
    vdd_values = st.sidebar.multiselect(
        "Select Vdd Levels (V)", [0.5, 0.75, 1.0, 1.5, 2.0, 3.0], default=[0.5, 0.75, 1.0]
    )

    # Slider for Ceff percentage change, synced with chat input
    ceff_change = st.sidebar.slider("Ceff Percentage Change (%)", -20, 20, st.session_state.ceff_change)

    # Frequency model: Frequency inversely proportional to Ceff and linearly dependent on Vdd
    def calculate_frequency(vdd, ceff_ratio, base_frequency, base_ceff, base_vdd):
        adjusted_ceff = (1 + ceff_ratio / 100)  # Adjust Ceff by percentage
        return base_frequency * (vdd / base_vdd) / adjusted_ceff

    # Calculate baseline frequencies (Ceff change = 0)
    baseline_frequencies = {
        vdd: calculate_frequency(vdd, 0, freq_base, ceff_base, vdd_base) for vdd in vdd_values
    }

    # Calculate frequency sensitivity and offset for the selected Vdd values
    results = []
    for vdd in vdd_values:
        freq = calculate_frequency(vdd, ceff_change, freq_base, ceff_base, vdd_base)
        baseline_freq = baseline_frequencies[vdd]
        freq_sensitivity = ((freq - freq_base) / freq_base) * 100  # % Sensitivity
        freq_offset = ((freq - baseline_freq) / baseline_freq) * 100  # % Offset relative to baseline
        results.append({
            "Vdd (V)": vdd,
            "Frequency Sensitivity (%)": freq_sensitivity,
            "Frequency Offset (%)": freq_offset
        })

    # Display metrics
    st.subheader("Frequency Sensitivity and Offset Metrics")
    cols = st.columns(len(vdd_values))
    for i, vdd in enumerate(vdd_values):
        freq_sensitivity = next(item["Frequency Sensitivity (%)"] for item in results if item["Vdd (V)"] == vdd)
        freq_offset = next(item["Frequency Offset (%)"] for item in results if item["Vdd (V)"] == vdd)
        cols[i].metric(label=f"Sensitivity @ Vdd={vdd}V", value=f"{freq_sensitivity:.2f} %", delta=f"{freq_offset:.2f} %")

    # Use columns for the chart and table
    col1, col2 = st.columns([0.5, 0.5])

    # Chart: Frequency Offset vs Vdd
    with col1:
        st.subheader("Frequency Offset Chart")
        plt.figure(figsize=(4, 3))
        vdd_list = [result["Vdd (V)"] for result in results]
        freq_offsets = [result["Frequency Offset (%)"] for result in results]
        plt.plot(vdd_list, freq_offsets, marker='o', linestyle='-', color='b', label="Frequency Offset (%)")
        plt.xlabel("Vdd (V)")
        plt.ylabel("Frequency Offset (%)")
        plt.title("Frequency Offset vs Vdd")
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)

    # Data Table
    with col2:
        st.subheader("Detailed Frequency Sensitivity and Offset Data")
        df = pd.DataFrame(results)
        st.dataframe(df)

elif st.session_state.selected_app == "App 2: Another Application":
    st.title("App 2: Another Application")
    st.markdown("This is a placeholder for another application. Customize it as needed.")
    app2.app()  # Call the `app()` function from `app2.py`
    # Add "Back to Cover Page" button
    #st.button("Back to Cover Page", on_click=back_to_cover)
