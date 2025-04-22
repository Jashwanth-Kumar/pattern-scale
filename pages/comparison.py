import streamlit as st
import pandas as pd
import numpy as np
from utils.data_manager import load_architecture_data, get_comparison_data
from utils.metrics_analyzer import calculate_overall_scores, get_best_pattern_for_metrics, get_pattern_scores
from utils.visualization import (
    create_comparison_radar_chart, 
    create_bar_chart_comparison, 
    create_latency_throughput_scatter,
    create_heat_map
)

def show():
    """Show the Comparison Tool page"""
    st.title("Architecture Pattern Comparison Tool")
    
    # Load architecture data
    arch_data = load_architecture_data()
    pattern_names = list(arch_data.keys())
    
    # Load comparison data as DataFrame
    comparison_df = get_comparison_data()
    
    st.markdown("""
    This tool helps you compare different architecture patterns based on performance metrics. 
    Use the options below to customize your comparison.
    """)
    
    # Select patterns to compare
    st.subheader("Select Patterns to Compare")
    selected_patterns = st.multiselect(
        "Choose architecture patterns:",
        pattern_names,
        default=pattern_names
    )
    
    if not selected_patterns:
        st.warning("Please select at least one architecture pattern to continue.")
        return
    
    # Select metrics to compare
    st.subheader("Select Metrics to Compare")
    
    # Get all available metrics
    metrics = list(arch_data[pattern_names[0]]["metrics"].keys())
    
    selected_metrics = st.multiselect(
        "Choose performance metrics:",
        metrics,
        default=metrics
    )
    
    if not selected_metrics:
        st.warning("Please select at least one metric to continue.")
        return
    
    # Filter comparison data based on selections
    filtered_df = comparison_df[comparison_df["Pattern"].isin(selected_patterns)]
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Radar Comparison", 
        "Metric Breakdown", 
        "Latency vs Throughput", 
        "Heat Map",
        "Overall Score"
    ])
    
    with tab1:
        st.subheader("Radar Chart Comparison")
        st.markdown("This chart compares selected patterns across all metrics on a normalized scale.")
        
        radar_fig = create_comparison_radar_chart(selected_patterns, selected_metrics, arch_data)
        st.plotly_chart(radar_fig)
    
    with tab2:
        st.subheader("Metric Breakdown")
        st.markdown("These charts show how each pattern performs for individual metrics.")
        
        # Create a metric selector
        selected_metric = st.selectbox("Select a metric to view:", selected_metrics)
        
        # Create bar chart for the selected metric
        bar_fig = create_bar_chart_comparison(filtered_df, selected_metric)
        st.plotly_chart(bar_fig)
        
        # Add explanation about the metric
        if selected_metric in arch_data[pattern_names[0]]["metrics"]:
            st.markdown(f"**{selected_metric}**: {arch_data[pattern_names[0]]['metrics'][selected_metric]['description']}")
            st.markdown(f"Unit: {arch_data[pattern_names[0]]['metrics'][selected_metric]['unit']}")
            
            # Add note about interpretation
            if selected_metric in ["Latency", "Resource Utilization"]:
                st.markdown("**Note**: For this metric, lower values are better.")
            else:
                st.markdown("**Note**: For this metric, higher values are better.")
    
    with tab3:
        st.subheader("Latency vs Throughput Analysis")
        st.markdown("This chart shows the relationship between latency and throughput for each pattern.")
        
        # Create scatter plot of latency vs throughput
        scatter_fig = create_latency_throughput_scatter(filtered_df)
        st.plotly_chart(scatter_fig)
        
        st.markdown("""
        **Interpretation**:
        - Patterns in the bottom-right quadrant (low latency, high throughput) have the best performance.
        - The size of each point represents availability (larger = higher availability).
        """)
    
    with tab4:
        st.subheader("Performance Heat Map")
        st.markdown("This heat map shows the normalized performance of each pattern across all metrics.")
        
        # Create heat map
        heat_map_fig = create_heat_map(filtered_df)
        st.plotly_chart(heat_map_fig)
        
        st.markdown("""
        **Interpretation**:
        - Higher (darker green) values indicate better performance.
        - For Latency and Resource Utilization, values are inverted so that lower raw values (better performance) appear as higher normalized scores.
        """)
    
    with tab5:
        st.subheader("Overall Pattern Scores")
        
        # Allow custom weighting of metrics
        st.markdown("Customize the importance of each metric to find the best pattern for your needs:")
        
        # Create sliders for setting weights
        weights = {}
        for metric in selected_metrics:
            weights[metric] = st.slider(f"{metric} importance:", 0, 10, 5, 1)
        
        # Calculate scores based on weights
        best_pattern, score = get_best_pattern_for_metrics(weights, arch_data)
        
        # Display the best pattern
        st.success(f"**Best Pattern Based on Your Priorities**: {best_pattern} (Score: {score:.2f})")
        
        # Calculate overall scores for all patterns
        scores = calculate_overall_scores(arch_data)
        
        # Filter scores to selected patterns
        filtered_scores = {pattern: score for pattern, score in scores.items() if pattern in selected_patterns}
        
        # Sort scores
        sorted_scores = dict(sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True))
        
        # Create dataframe for display
        scores_df = pd.DataFrame({
            "Pattern": list(sorted_scores.keys()),
            "Score": list(sorted_scores.values())
        })
        
        # Display bar chart of scores
        st.bar_chart(scores_df.set_index("Pattern"))
        
        # Display scores as table
        scores_df["Score"] = scores_df["Score"].apply(lambda x: f"{x:.2f}")
        st.dataframe(scores_df, hide_index=True)
    
    # Comparison table
    st.subheader("Detailed Comparison Table")
    
    # Create a detailed comparison table
    table_metrics = []
    for metric in selected_metrics:
        metric_values = {}
        metric_values["Metric"] = metric
        
        for pattern in selected_patterns:
            metric_values[pattern] = get_pattern_scores(pattern, metric, arch_data)
        
        table_metrics.append(metric_values)
    
    # Convert to DataFrame
    table_df = pd.DataFrame(table_metrics)
    
    # Display table
    st.dataframe(table_df, hide_index=True)
