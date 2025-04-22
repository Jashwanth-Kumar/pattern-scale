import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_manager import load_architecture_data, get_comparison_data
from utils.metrics_analyzer import normalize_metric, get_pattern_scores

def create_radar_chart(pattern_name, arch_data=None):
    """
    Create a radar chart for a specific pattern
    
    Args:
        pattern_name (str): Name of the architecture pattern
        arch_data (dict, optional): Architecture data. Defaults to None.
        
    Returns:
        plotly.graph_objects.Figure: Radar chart figure
    """
    if arch_data is None:
        arch_data = load_architecture_data()
        
    # Extract metrics for the pattern
    metrics = list(arch_data[pattern_name]["metrics"].keys())
    values = [arch_data[pattern_name]["metrics"][metric]["value"] for metric in metrics]
    
    # Normalize values to 0-5 scale for radar chart
    # For latency and resource utilization, lower is better, so invert the scale
    normalized_values = []
    for i, metric in enumerate(metrics):
        if metric in ["Latency", "Resource Utilization"]:
            # Invert scale: higher is worse, so normalize and then invert
            if metric == "Latency":
                # Normalize Latency to 0-5 scale (lower is better)
                normalized_value = 5 - (values[i] / 100)  # Assuming latency is in ms
                normalized_value = max(0, min(5, normalized_value))  # Clamp to 0-5
            else:
                # Normalize Resource Utilization (lower is better)
                normalized_value = 5 - (values[i] / 100 * 5)  # Assuming percentage
                normalized_value = max(0, min(5, normalized_value))  # Clamp to 0-5
            normalized_values.append(normalized_value)
        elif metric == "Availability":
            # Normalize Availability (higher is better)
            # Map 99-100% to 0-5 scale
            normalized_value = (values[i] - 99) * 5
            normalized_value = max(0, min(5, normalized_value))  # Clamp to 0-5
            normalized_values.append(normalized_value)
        elif metric == "Throughput":
            # Normalize Throughput (higher is better)
            # Assuming throughput ranges from 0-5000 req/sec, map to 0-5 scale
            normalized_value = values[i] / 1000
            normalized_value = max(0, min(5, normalized_value))  # Clamp to 0-5
            normalized_values.append(normalized_value)
        else:
            # These metrics are already on a 1-5 scale
            normalized_values.append(values[i])
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=metrics,
        fill='toself',
        name=pattern_name
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=False,
        title=f"{pattern_name} Performance Metrics"
    )
    
    return fig

def create_comparison_radar_chart(patterns, metrics, arch_data=None):
    """
    Create a radar chart comparing multiple patterns
    
    Args:
        patterns (list): List of pattern names to compare
        metrics (list): List of metrics to compare
        arch_data (dict, optional): Architecture data. Defaults to None.
        
    Returns:
        plotly.graph_objects.Figure: Radar chart figure
    """
    if arch_data is None:
        arch_data = load_architecture_data()
    
    fig = go.Figure()
    
    # Get values for all patterns and metrics for normalization
    all_values = {}
    for metric in metrics:
        all_values[metric] = []
        for pattern in patterns:
            value = get_pattern_scores(pattern, metric, arch_data)
            all_values[metric].append(value)
    
    # Create a trace for each pattern
    for pattern in patterns:
        # Extract metrics for the pattern
        values = []
        for metric in metrics:
            value = get_pattern_scores(pattern, metric, arch_data)
            # Normalized value based on all patterns
            if metric in ["Latency", "Resource Utilization"]:
                # Lower is better for these metrics, so invert the normalization
                norm_value = normalize_metric(all_values[metric], metric)[all_values[metric].index(value)] * 5
            else:
                # Higher is better for these metrics
                norm_value = normalize_metric(all_values[metric], "")[all_values[metric].index(value)] * 5
            values.append(norm_value)
        
        # Add trace to the figure
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics,
            fill='toself',
            name=pattern
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        title="Architecture Pattern Comparison"
    )
    
    return fig

def create_bar_chart_comparison(comparison_df, metric_name):
    """
    Create a bar chart comparing patterns for a specific metric
    
    Args:
        comparison_df (pandas.DataFrame): DataFrame with comparison data
        metric_name (str): Name of the metric to compare
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    # Handle special case for the metric name in the dataframe
    df_metric_name = metric_name.replace(" ", "_") if " " in metric_name else metric_name
    
    # Sort dataframe by the metric value
    sorted_df = comparison_df.sort_values(by=df_metric_name, ascending=False)
    
    fig = px.bar(
        sorted_df, 
        x="Pattern", 
        y=df_metric_name, 
        title=f"Comparison of {metric_name} Across Patterns",
        labels={df_metric_name: metric_name, "Pattern": "Architecture Pattern"},
        color="Pattern",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    return fig

def create_before_after_chart(before_data, after_data, pattern_name):
    """
    Create a bar chart comparing before and after scaling metrics
    
    Args:
        before_data (dict): Dictionary with before scaling metrics
        after_data (dict): Dictionary with after scaling metrics
        pattern_name (str): Name of the architecture pattern
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    # Extract common metrics
    metrics = list(set(before_data.keys()) & set(after_data.keys()))
    before_values = [before_data[metric] for metric in metrics]
    after_values = [after_data[metric] for metric in metrics]
    
    # Create dataframe
    df = pd.DataFrame({
        "Metric": metrics + metrics,
        "Value": before_values + after_values,
        "Stage": ["Before Scaling"] * len(metrics) + ["After Scaling"] * len(metrics)
    })
    
    fig = px.bar(
        df, 
        x="Metric", 
        y="Value", 
        color="Stage",
        barmode="group",
        title=f"Before vs After Scaling: {pattern_name}",
        labels={"Value": "Metric Value", "Metric": "Performance Metric"},
        color_discrete_sequence=["#636EFA", "#EF553B"]
    )
    
    return fig

def create_latency_throughput_scatter(comparison_df):
    """
    Create a scatter plot of latency vs throughput for all patterns
    
    Args:
        comparison_df (pandas.DataFrame): DataFrame with comparison data
        
    Returns:
        plotly.graph_objects.Figure: Scatter plot figure
    """
    # Ensure we have finite values to avoid infinite extent warnings
    df = comparison_df.copy()
    # Replace any potential infinite values with NaN
    df.replace([float('inf'), float('-inf')], np.nan, inplace=True)
    # Drop rows with NaN values to avoid scale binding issues
    df.dropna(subset=["Throughput", "Latency"], inplace=True)
    
    if df.empty:
        # Create an empty figure with a message if no valid data
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            text="No valid data available for scatter plot",
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(
            title="Latency vs Throughput Comparison",
            xaxis=dict(title="Throughput (req/sec)"),
            yaxis=dict(title="Latency (ms)")
        )
        return fig
    
    # Calculate max values safely
    max_throughput = df["Throughput"].max() * 1.1 if not df.empty else 100
    max_latency = df["Latency"].max() * 1.1 if not df.empty else 100
    
    # Check if Availability is in the dataframe
    size_column = "Availability" if "Availability" in df.columns else None
    
    fig = px.scatter(
        df, 
        x="Throughput", 
        y="Latency", 
        text="Pattern",
        title="Latency vs Throughput Comparison",
        labels={"Throughput": "Throughput (req/sec)", "Latency": "Latency (ms)"},
        color="Pattern",
        size=size_column,
    )
    
    # Add annotations for each point
    fig.update_traces(textposition='top center')
    
    # Add a line to indicate the optimal direction
    fig.add_annotation(
        x=max_throughput * 0.9,
        y=max_latency * 0.1,
        text="Better Performance →",
        showarrow=True,
        arrowhead=1,
        ax=-40,
        ay=0
    )
    
    return fig

def create_heat_map(comparison_df):
    """
    Create a heat map of all metrics for all patterns
    
    Args:
        comparison_df (pandas.DataFrame): DataFrame with comparison data
        
    Returns:
        plotly.graph_objects.Figure: Heat map figure
    """
    # Melt the dataframe to get it in the right format for the heat map
    metrics = [col for col in comparison_df.columns if col != "Pattern"]
    df_melted = pd.melt(comparison_df, id_vars=["Pattern"], value_vars=metrics, var_name="Metric", value_name="Value")
    
    # Create a pivot table
    df_pivot = df_melted.pivot(index="Pattern", columns="Metric", values="Value")
    
    # Handle any potential NaN values
    df_pivot = df_pivot.fillna(0)
    
    # Normalize each column (metric) to 0-1
    for col in df_pivot.columns:
        min_val = df_pivot[col].min()
        max_val = df_pivot[col].max()
        
        # Handle case when min and max are equal to avoid division by zero
        if max_val == min_val:
            df_pivot[col] = 0.5  # Set to middle value if all values are the same
        else:
            if col in ["Latency", "Resource_Utilization"]:
                # For these metrics, lower is better
                df_pivot[col] = (max_val - df_pivot[col]) / (max_val - min_val)
            else:
                # For all other metrics, higher is better
                df_pivot[col] = (df_pivot[col] - min_val) / (max_val - min_val)
    
    # Create heat map
    fig = px.imshow(
        df_pivot,
        labels=dict(x="Metric", y="Pattern", color="Normalized Score"),
        x=df_pivot.columns,
        y=df_pivot.index,
        color_continuous_scale='Viridis',
        title="Architecture Pattern Performance Heat Map"
    )
    
    # Add text annotations
    for i, pattern in enumerate(df_pivot.index):
        for j, metric in enumerate(df_pivot.columns):
            fig.add_annotation(
                x=j,
                y=i,
                text=f"{df_pivot.iloc[i, j]:.2f}",
                showarrow=False,
                font=dict(color="white" if df_pivot.iloc[i, j] < 0.5 else "black")
            )
    
    return fig
