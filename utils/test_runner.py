import time
import random
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import os

def run_latency_test(url, num_requests=100, concurrency=10):
    """
    Run a latency test against a URL
    
    Args:
        url (str): URL to test
        num_requests (int): Number of requests to make
        concurrency (int): Number of concurrent requests
        
    Returns:
        dict: Dictionary with test results
    """
    # Initialize results
    results = {
        "latency": [],
        "status_codes": [],
        "errors": 0
    }
    
    def make_request(i):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            return {
                "latency": (end_time - start_time) * 1000,  # Convert to ms
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "latency": None,
                "status_code": 0,
                "error": str(e)
            }
    
    # Use ThreadPoolExecutor to make concurrent requests
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        responses = list(executor.map(make_request, range(num_requests)))
    
    # Process responses
    for response in responses:
        if response.get("latency") is not None:
            results["latency"].append(response["latency"])
            results["status_codes"].append(response["status_code"])
        else:
            results["errors"] += 1
    
    # Calculate results
    if results["latency"]:
        avg_latency = sum(results["latency"]) / len(results["latency"])
        min_latency = min(results["latency"])
        max_latency = max(results["latency"])
        p95_latency = np.percentile(results["latency"], 95)
        successful_requests = len([code for code in results["status_codes"] if 200 <= code < 300])
        error_rate = (results["errors"] + len(results["status_codes"]) - successful_requests) / num_requests * 100
    else:
        avg_latency = 0
        min_latency = 0
        max_latency = 0
        p95_latency = 0
        successful_requests = 0
        error_rate = 100
    
    return {
        "avg_latency": avg_latency,
        "min_latency": min_latency,
        "max_latency": max_latency,
        "p95_latency": p95_latency,
        "successful_requests": successful_requests,
        "error_rate": error_rate,
        "total_requests": num_requests,
        "errors": results["errors"]
    }

def run_throughput_test(url, duration=10, concurrency=50):
    """
    Run a throughput test against a URL
    
    Args:
        url (str): URL to test
        duration (int): Duration of the test in seconds
        concurrency (int): Number of concurrent requests
        
    Returns:
        dict: Dictionary with test results
    """
    # Initialize results
    results = {
        "requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "latencies": []
    }
    
    def worker():
        start_time = time.time()
        end_time = start_time + duration
        local_results = {
            "requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "latencies": []
        }
        
        while time.time() < end_time:
            try:
                req_start = time.time()
                response = requests.get(url, timeout=5)
                req_end = time.time()
                
                local_results["requests"] += 1
                if 200 <= response.status_code < 300:
                    local_results["successful_requests"] += 1
                else:
                    local_results["failed_requests"] += 1
                
                local_results["latencies"].append((req_end - req_start) * 1000)  # Convert to ms
            except Exception:
                local_results["requests"] += 1
                local_results["failed_requests"] += 1
        
        return local_results
    
    # Use ThreadPoolExecutor to run workers
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        worker_results = list(executor.map(lambda _: worker(), range(concurrency)))
    
    # Aggregate results
    for result in worker_results:
        results["requests"] += result["requests"]
        results["successful_requests"] += result["successful_requests"]
        results["failed_requests"] += result["failed_requests"]
        results["latencies"].extend(result["latencies"])
    
    # Calculate throughput and other metrics
    throughput = results["requests"] / duration
    successful_throughput = results["successful_requests"] / duration
    error_rate = results["failed_requests"] / results["requests"] * 100 if results["requests"] > 0 else 0
    
    if results["latencies"]:
        avg_latency = sum(results["latencies"]) / len(results["latencies"])
        p95_latency = np.percentile(results["latencies"], 95)
    else:
        avg_latency = 0
        p95_latency = 0
    
    return {
        "throughput": throughput,
        "successful_throughput": successful_throughput,
        "error_rate": error_rate,
        "total_requests": results["requests"],
        "successful_requests": results["successful_requests"],
        "failed_requests": results["failed_requests"],
        "avg_latency": avg_latency,
        "p95_latency": p95_latency,
        "duration": duration
    }

def simulate_test_results(pattern_name):
    """
    Simulate test results for a pattern
    
    This function is used when a real test can't be run against a URL.
    It generates realistic but simulated results based on the characteristics
    of different architecture patterns.
    
    Args:
        pattern_name (str): Name of the architecture pattern
        
    Returns:
        dict: Dictionary with simulated test results
    """
    # Base values for different metrics
    base_metrics = {
        "Monolithic Architecture": {
            "Throughput": 750,
            "Latency": 120,
            "Availability": 99.5,
            "Resource Utilization": 75,
            "Fault Tolerance": 3,
            "Elasticity": 2,
            "Cost Efficiency": 4,
            "Data Consistency": 5
        },
        "Microservices Architecture": {
            "Throughput": 1800,
            "Latency": 150,
            "Availability": 99.95,
            "Resource Utilization": 60,
            "Fault Tolerance": 4.5,
            "Elasticity": 4.8,
            "Cost Efficiency": 3.5,
            "Data Consistency": 3.2
        },
        "Serverless Architecture": {
            "Throughput": 2500,
            "Latency": 250,
            "Availability": 99.99,
            "Resource Utilization": 20,
            "Fault Tolerance": 4.7,
            "Elasticity": 5,
            "Cost Efficiency": 4.5,
            "Data Consistency": 3
        },
        "Event-Driven Architecture": {
            "Throughput": 3200,
            "Latency": 180,
            "Availability": 99.9,
            "Resource Utilization": 55,
            "Fault Tolerance": 4.5,
            "Elasticity": 4.3,
            "Cost Efficiency": 3.8,
            "Data Consistency": 3.5
        },
        "Peer-to-Peer Architecture": {
            "Throughput": 900,
            "Latency": 220,
            "Availability": 99.8,
            "Resource Utilization": 70,
            "Fault Tolerance": 4.8,
            "Elasticity": 3.5,
            "Cost Efficiency": 4.2,
            "Data Consistency": 2.8
        },
        "Service-Oriented Architecture (SOA)": {
            "Throughput": 1200,
            "Latency": 190,
            "Availability": 99.7,
            "Resource Utilization": 65,
            "Fault Tolerance": 4.0,
            "Elasticity": 3.5,
            "Cost Efficiency": 3.5,
            "Data Consistency": 4.0
        }
    }
    
    # Add some randomness to the simulated results (±10%)
    if pattern_name in base_metrics:
        variation = 0.1  # 10% variation
        
        results = {}
        for metric, value in base_metrics[pattern_name].items():
            # Add random variation
            random_factor = 1 + (random.random() * 2 - 1) * variation
            results[metric] = value * random_factor
            
            # Round to appropriate precision
            if metric in ["Fault Tolerance", "Elasticity", "Cost Efficiency", "Data Consistency"]:
                results[metric] = round(results[metric], 1)
            elif metric == "Availability":
                results[metric] = round(results[metric], 2)
            else:
                results[metric] = round(results[metric])
        
        return results
    else:
        # Default values if pattern not found
        return {
            "Throughput": 1000,
            "Latency": 200,
            "Availability": 99.5,
            "Resource Utilization": 60,
            "Fault Tolerance": 3.0,
            "Elasticity": 3.0,
            "Cost Efficiency": 3.0,
            "Data Consistency": 3.0
        }

def simulate_scaling_comparison(pattern_name):
    """
    Simulate before and after scaling comparison for a pattern
    
    Args:
        pattern_name (str): Name of the architecture pattern
        
    Returns:
        dict: Dictionary with before and after scaling metrics
    """
    # Define scaling factors for different metrics for each pattern
    scaling_factors = {
        "Monolithic Architecture": {
            "Latency": 1.5,  # Latency increases (worse)
            "Throughput": 1.8,  # Throughput increases but not linearly
            "CPU Utilization": 1.2,  # CPU utilization increases
            "Memory Usage": 2.0,  # Memory usage doubles
            "Error Rate": 2.0  # Error rate doubles
        },
        "Microservices Architecture": {
            "Latency": 1.1,  # Slight latency increase
            "Throughput": 3.6,  # Good throughput scaling
            "CPU Utilization": 1.08,  # Small CPU increase
            "Memory Usage": 1.5,  # Memory increases
            "Error Rate": 0.8  # Error rate decreases
        },
        "Serverless Architecture": {
            "Latency": 1.08,  # Minimal latency increase
            "Throughput": 3.4,  # Excellent throughput scaling
            "CPU Utilization": 1.1,  # Small CPU increase
            "Memory Usage": 1.4,  # Memory increases
            "Error Rate": 0.75  # Error rate decreases
        },
        "Event-Driven Architecture": {
            "Latency": 1.08,  # Minimal latency increase
            "Throughput": 2.4,  # Good throughput scaling
            "CPU Utilization": 1.1,  # Small CPU increase
            "Memory Usage": 1.2,  # Memory increases slightly
            "Error Rate": 0.75  # Error rate decreases
        },
        "Peer-to-Peer Architecture": {
            "Latency": 0.9,  # Latency can improve with more peers
            "Throughput": 6.1,  # Throughput scales well with peers
            "CPU Utilization": 1.2,  # CPU increases
            "Memory Usage": 1.55,  # Memory increases
            "Error Rate": 0.9  # Error rate slightly decreases
        },
        "Service-Oriented Architecture (SOA)": {
            "Latency": 1.1,  # Slight latency increase
            "Throughput": 4.0,  # Good throughput scaling
            "CPU Utilization": 1.15,  # CPU increases
            "Memory Usage": 1.4,  # Memory increases
            "Error Rate": 0.8  # Error rate decreases
        }
    }
    
    # Base metrics before scaling
    before_metrics = {
        "Latency": 150,  # ms
        "Throughput": 1000,  # req/sec
        "CPU Utilization": 60,  # %
        "Memory Usage": 8,  # GB
        "Error Rate": 2.0  # %
    }
    
    # Apply pattern-specific factors or default factors
    factors = scaling_factors.get(pattern_name, {
        "Latency": 1.2,
        "Throughput": 2.0,
        "CPU Utilization": 1.2,
        "Memory Usage": 1.5,
        "Error Rate": 1.2
    })
    
    # Calculate after metrics
    after_metrics = {}
    for metric, value in before_metrics.items():
        factor = factors.get(metric, 1.0)
        after_metrics[metric] = round(value * factor, 1)
    
    return {
        "before": before_metrics,
        "after": after_metrics
    }

def run_custom_test_plan(url=None, pattern=None):
    """
    Run a custom test plan against a URL or simulate results for a pattern
    
    Args:
        url (str, optional): URL to test. Defaults to None.
        pattern (str, optional): Pattern to simulate. Defaults to None.
        
    Returns:
        dict: Dictionary with test results
    """
    if url and os.environ.get("ENABLE_REAL_TESTS", "false").lower() == "true":
        # Run real tests against URL
        latency_results = run_latency_test(url)
        throughput_results = run_throughput_test(url)
        
        # Map results to pattern metrics
        return {
            "Throughput": throughput_results["throughput"],
            "Latency": latency_results["avg_latency"],
            "Availability": (1 - (latency_results["error_rate"] / 100)) * 100,
            "Resource Utilization": 60,  # Placeholder, can't measure directly
            "Fault Tolerance": 3.0,  # Placeholder, can't measure directly
            "Elasticity": 3.0,  # Placeholder, can't measure directly
            "Cost Efficiency": 3.0,  # Placeholder, can't measure directly
            "Data Consistency": 3.0  # Placeholder, can't measure directly
        }
    elif pattern:
        # Simulate test results for pattern
        return simulate_test_results(pattern)
    else:
        # Default results if neither URL nor pattern provided
        return {
            "Throughput": 1000,
            "Latency": 200,
            "Availability": 99.5,
            "Resource Utilization": 60,
            "Fault Tolerance": 3.0,
            "Elasticity": 3.0,
            "Cost Efficiency": 3.0,
            "Data Consistency": 3.0
        }
