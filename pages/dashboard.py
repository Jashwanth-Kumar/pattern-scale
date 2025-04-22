import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_manager import load_architecture_data
from utils.metrics_analyzer import get_pattern_scores, get_pattern_characteristics, get_pattern_description, get_pattern_sources, compare_before_after_scaling
from utils.visualization import create_radar_chart, create_before_after_chart

def show():
    """Show the Pattern Dashboard page"""
    st.title("Architecture Pattern Dashboard")
    
    # Load architecture data
    arch_data = load_architecture_data()
    pattern_names = list(arch_data.keys())
    
    # Select a pattern to view
    if 'selected_pattern' in st.session_state and st.session_state.selected_pattern:
        default_pattern = st.session_state.selected_pattern
    else:
        default_pattern = pattern_names[0]
    
    selected_pattern = st.selectbox("Select an architecture pattern:", 
                                    pattern_names, 
                                    index=pattern_names.index(default_pattern))
    
    # Store selected pattern in session state
    st.session_state.selected_pattern = selected_pattern
    
    # Display pattern information
    st.header(selected_pattern)
    
    # Description
    st.subheader("Description")
    st.write(get_pattern_description(selected_pattern, arch_data))
    
    # Key characteristics
    st.subheader("Key Characteristics")
    characteristics = get_pattern_characteristics(selected_pattern, arch_data)
    for char in characteristics:
        st.markdown(f"- {char}")
    
    # Display metrics
    st.subheader("Performance Metrics")
    
    # Create two columns for layout
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Radar chart
        fig = create_radar_chart(selected_pattern, arch_data)
        st.plotly_chart(fig)
    
    with col2:
        # Create a table of metrics
        metrics_table = []
        for metric_name, metric_data in arch_data[selected_pattern]["metrics"].items():
            metrics_table.append({
                "Metric": metric_name,
                "Value": f"{metric_data['value']} {metric_data['unit']}",
                "Description": metric_data["description"]
            })
        
        metrics_df = pd.DataFrame(metrics_table)
        st.dataframe(metrics_df, hide_index=True)
    
    # Before and After Scaling Comparison
    st.subheader("Before vs After Scaling")
    scaling_data = compare_before_after_scaling(selected_pattern, arch_data)
    
    if scaling_data and "before" in scaling_data and "after" in scaling_data:
        # Create before vs after chart
        fig = create_before_after_chart(scaling_data["before"], scaling_data["after"], selected_pattern)
        st.plotly_chart(fig)
        
        # Create a dataframe for comparison
        comparison_df = pd.DataFrame({
            "Metric": list(scaling_data["before"].keys()),
            "Before Scaling": list(scaling_data["before"].values()),
            "After Scaling": list(scaling_data["after"].values()),
            "Change (%)": [(after / before - 1) * 100 if before > 0 else 0 
                          for before, after in zip(scaling_data["before"].values(), scaling_data["after"].values())]
        })
        
        # Format the Change column
        comparison_df["Change (%)"] = comparison_df["Change (%)"].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(comparison_df, hide_index=True)
        
        # Add explanation
        st.markdown("""
        This comparison shows how the architecture pattern performs before and after scaling.
        For latency and error rate, lower values are better. For throughput, higher values are better.
        """)
    else:
        st.info("No scaling comparison data available for this pattern.")
    
    # Source citations
    st.subheader("Data Sources")
    sources = get_pattern_sources(selected_pattern, arch_data)
    for source in sources:
        st.markdown(f"- {source}")
    
    st.markdown("---")
    
    # Additional notes
    st.subheader("Notes on Metrics")
    st.markdown("""
    **Throughput**: The number of requests the system can handle per second.
    
    **Latency**: The time it takes for the system to respond to a request, measured in milliseconds.
    
    **Availability**: The percentage of time the system is operational.
    
    **Resource Utilization**: The percentage of CPU and memory resources used by the system.
    
    **Fault Tolerance**: The ability of the system to continue operating when components fail, rated on a scale of 1-5.
    
    **Elasticity**: The ability of the system to scale up or down based on load, rated on a scale of 1-5.
    
    **Cost Efficiency**: The cost of running the system relative to its performance, rated on a scale of 1-5.
    
    **Data Consistency**: The ability of the system to maintain data integrity across components, rated on a scale of 1-5.
    """)
