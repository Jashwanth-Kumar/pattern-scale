import pandas as pd
import numpy as np
from utils.data_manager import load_architecture_data

def get_pattern_scores(pattern_name, metric_name, arch_data=None):
    """
    Get the score for a specific pattern and metric
    
    Args:
        pattern_name (str): Name of the architecture pattern
        metric_name (str): Name of the metric
        arch_data (dict, optional): Architecture data. Defaults to None.
        
    Returns:
        float: The score value for the specified pattern and metric
    """
    if arch_data is None:
        arch_data = load_architecture_data()
        
    if pattern_name in arch_data and "metrics" in arch_data[pattern_name]:
        if metric_name in arch_data[pattern_name]["metrics"]:
            return arch_data[pattern_name]["metrics"][metric_name]["value"]
    
    return 0  # Default value if pattern or metric not found

def normalize_metric(values, metric_name):
    """
    Normalize metric values to a 0-1 scale
    
    Args:
        values (list): List of metric values
        metric_name (str): Name of the metric
        
    Returns:
        list: Normalized values
    """
    # For latency and resource utilization, lower is better
    if metric_name in ["Latency", "Resource Utilization"]:
        min_val = min(values)
        max_val = max(values)
        # Avoid division by zero
        if max_val == min_val:
            return [1.0] * len(values)
        return [1 - ((val - min_val) / (max_val - min_val)) for val in values]
    else:
        # For all other metrics, higher is better
        min_val = min(values)
        max_val = max(values)
        # Avoid division by zero
        if max_val == min_val:
            return [1.0] * len(values)
        return [(val - min_val) / (max_val - min_val) for val in values]

def calculate_overall_scores(arch_data=None):
    """
    Calculate overall scores for each architecture pattern
    
    Args:
        arch_data (dict, optional): Architecture data. Defaults to None.
        
    Returns:
        dict: Dictionary with pattern names as keys and overall scores as values
    """
    if arch_data is None:
        arch_data = load_architecture_data()
    
    # Define metric weights (custom weights based on importance)
    weights = {
        "Throughput": 0.15,
        "Latency": 0.15,
        "Availability": 0.15,
        "Resource Utilization": 0.1,
        "Fault Tolerance": 0.15,
        "Elasticity": 0.1,
        "Cost Efficiency": 0.1,
        "Data Consistency": 0.1
    }
    
    # Initialize data structures
    pattern_metrics = {}
    metric_values = {metric: [] for metric in weights.keys()}
    
    # Extract metric values for each pattern
    for pattern_name, pattern_data in arch_data.items():
        pattern_metrics[pattern_name] = {}
        for metric_name in weights.keys():
            value = get_pattern_scores(pattern_name, metric_name, arch_data)
            pattern_metrics[pattern_name][metric_name] = value
            metric_values[metric_name].append(value)
    
    # Normalize metrics
    normalized_metrics = {}
    for pattern_name in pattern_metrics.keys():
        normalized_metrics[pattern_name] = {}
    
    for metric_name in weights.keys():
        normalized = normalize_metric(metric_values[metric_name], metric_name)
        for i, pattern_name in enumerate(pattern_metrics.keys()):
            normalized_metrics[pattern_name][metric_name] = normalized[i]
    
    # Calculate weighted scores
    scores = {}
    for pattern_name in normalized_metrics.keys():
        weighted_sum = sum(normalized_metrics[pattern_name][metric] * weights[metric] for metric in weights.keys())
        scores[pattern_name] = weighted_sum
    
    return scores

def get_best_pattern_for_metrics(metrics_priority, arch_data=None):
    """
    Get the best architecture pattern based on specified metrics priority
    
    Args:
        metrics_priority (dict): Dictionary with metric names as keys and priority weights as values
        arch_data (dict, optional): Architecture data. Defaults to None.
        
    Returns:
        tuple: Best pattern name and its score
    """
    if arch_data is None:
        arch_data = load_architecture_data()
    
    # Normalize priority weights
    total_weight = sum(metrics_priority.values())
    normalized_weights = {metric: weight/total_weight for metric, weight in metrics_priority.items()}
    
    # Initialize data structures
    pattern_metrics = {}
    metric_values = {metric: [] for metric in metrics_priority.keys()}
    
    # Extract metric values for each pattern
    for pattern_name, pattern_data in arch_data.items():
        pattern_metrics[pattern_name] = {}
        for metric_name in metrics_priority.keys():
            value = get_pattern_scores(pattern_name, metric_name, arch_data)
            pattern_metrics[pattern_name][metric_name] = value
            metric_values[metric_name].append(value)
    
    # Normalize metrics
    normalized_metrics = {}
    for pattern_name in pattern_metrics.keys():
        normalized_metrics[pattern_name] = {}
    
    for metric_name in metrics_priority.keys():
        normalized = normalize_metric(metric_values[metric_name], metric_name)
        for i, pattern_name in enumerate(pattern_metrics.keys()):
            normalized_metrics[pattern_name][metric_name] = normalized[i]
    
    # Calculate weighted scores
    scores = {}
    for pattern_name in normalized_metrics.keys():
        weighted_sum = sum(normalized_metrics[pattern_name][metric] * normalized_weights[metric] for metric in normalized_weights.keys())
        scores[pattern_name] = weighted_sum
    
    # Find the best pattern
    best_pattern = max(scores.items(), key=lambda x: x[1])
    
    return best_pattern

def compare_before_after_scaling(pattern_name, arch_data=None):
    """
    Compare before and after scaling metrics for a specific pattern
    
    Args:
        pattern_name (str): Name of the architecture pattern
        arch_data (dict, optional): Architecture data. Defaults to None.
        
    Returns:
        dict: Dictionary with before and after metrics
    """
    if arch_data is None:
        arch_data = load_architecture_data()
    
    if pattern_name in arch_data and "scaling_comparison" in arch_data[pattern_name]:
        return arch_data[pattern_name]["scaling_comparison"]
    
    return {
        "before": {},
        "after": {}
    }

def get_pattern_characteristics(pattern_name, arch_data=None):
    """
    Get characteristics of a specific architecture pattern
    
    Args:
        pattern_name (str): Name of the architecture pattern
        arch_data (dict, optional): Architecture data. Defaults to None.
        
    Returns:
        list: List of characteristics
    """
    if arch_data is None:
        arch_data = load_architecture_data()
    
    if pattern_name in arch_data and "characteristics" in arch_data[pattern_name]:
        return arch_data[pattern_name]["characteristics"]
    
    return []

def get_pattern_description(pattern_name, arch_data=None):
    """
    Get description of a specific architecture pattern
    
    Args:
        pattern_name (str): Name of the architecture pattern
        arch_data (dict, optional): Architecture data. Defaults to None.
        
    Returns:
        str: Description of the pattern
    """
    if arch_data is None:
        arch_data = load_architecture_data()
    
    if pattern_name in arch_data and "description" in arch_data[pattern_name]:
        return arch_data[pattern_name]["description"]
    
    return ""

def get_pattern_sources(pattern_name, arch_data=None):
    """
    Get sources for a specific architecture pattern
    
    Args:
        pattern_name (str): Name of the architecture pattern
        arch_data (dict, optional): Architecture data. Defaults to None.
        
    Returns:
        list: List of sources
    """
    if arch_data is None:
        arch_data = load_architecture_data()
    
    if pattern_name in arch_data and "sources" in arch_data[pattern_name]:
        return arch_data[pattern_name]["sources"]
    
    return []
