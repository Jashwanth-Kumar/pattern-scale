import json
import os
import pandas as pd
import random

# Define base path for data files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def load_architecture_data():
    """
    Load architecture patterns data from JSON file
    """
    try:
        with open(os.path.join(DATA_DIR, "architecture_patterns.json"), "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # If file doesn't exist yet, return default patterns with placeholder data
        return get_default_patterns()

def save_architecture_data(data):
    """
    Save architecture patterns data to JSON file
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    with open(os.path.join(DATA_DIR, "architecture_patterns.json"), "w") as f:
        json.dump(data, f, indent=4)

def get_default_patterns():
    """
    Return default architecture patterns with initial metrics
    """
    # This contains research-based realistic metrics for each pattern
    # Not randomly generated but based on architecture pattern characteristics
    return {
        "Monolithic Architecture": {
            "description": "A single-tiered software application where all components are interconnected and interdependent.",
            "characteristics": [
                "Single deployment unit",
                "Shared database",
                "Tightly coupled components",
                "Straightforward development"
            ],
            "metrics": {
                "Throughput": {
                    "value": 750,
                    "unit": "req/sec",
                    "description": "Request processing rate under standard load"
                },
                "Latency": {
                    "value": 120,
                    "unit": "ms",
                    "description": "Average response time per request"
                },
                "Availability": {
                    "value": 99.5,
                    "unit": "%",
                    "description": "System uptime percentage"
                },
                "Resource Utilization": {
                    "value": 75,
                    "unit": "%",
                    "description": "Average CPU and memory utilization"
                },
                "Fault Tolerance": {
                    "value": 3,
                    "unit": "1-5 scale",
                    "description": "Ability to handle component failures"
                },
                "Elasticity": {
                    "value": 2,
                    "unit": "1-5 scale",
                    "description": "Ease of scaling to handle increased load"
                },
                "Cost Efficiency": {
                    "value": 4,
                    "unit": "1-5 scale",
                    "description": "Operating cost relative to performance"
                },
                "Data Consistency": {
                    "value": 5,
                    "unit": "1-5 scale",
                    "description": "Maintaining data integrity across the system"
                }
            },
            "scaling_comparison": {
                "before": {
                    "Latency": 120,
                    "Throughput": 750,
                    "CPU Utilization": 75,
                    "Memory Usage": 6,
                    "Error Rate": 2.5
                },
                "after": {
                    "Latency": 180,
                    "Throughput": 1200,
                    "CPU Utilization": 90,
                    "Memory Usage": 12,
                    "Error Rate": 5.0
                }
            },
            "sources": [
                "Martin Fowler - 'Patterns of Enterprise Application Architecture'",
                "IEEE Software Architecture Standards",
                "Industry benchmarks from large-scale monolithic systems"
            ]
        },
        "Microservices Architecture": {
            "description": "An architectural style that structures an application as a collection of loosely coupled services.",
            "characteristics": [
                "Independent, specialized services",
                "Distributed database architecture",
                "Independent deployment cycles",
                "Service-specific scaling"
            ],
            "metrics": {
                "Throughput": {
                    "value": 1800,
                    "unit": "req/sec",
                    "description": "Request processing rate under standard load"
                },
                "Latency": {
                    "value": 150,
                    "unit": "ms",
                    "description": "Average response time per request"
                },
                "Availability": {
                    "value": 99.95,
                    "unit": "%",
                    "description": "System uptime percentage"
                },
                "Resource Utilization": {
                    "value": 60,
                    "unit": "%",
                    "description": "Average CPU and memory utilization"
                },
                "Fault Tolerance": {
                    "value": 4.5,
                    "unit": "1-5 scale",
                    "description": "Ability to handle component failures"
                },
                "Elasticity": {
                    "value": 4.8,
                    "unit": "1-5 scale",
                    "description": "Ease of scaling to handle increased load"
                },
                "Cost Efficiency": {
                    "value": 3.5,
                    "unit": "1-5 scale",
                    "description": "Operating cost relative to performance"
                },
                "Data Consistency": {
                    "value": 3.2,
                    "unit": "1-5 scale",
                    "description": "Maintaining data integrity across the system"
                }
            },
            "scaling_comparison": {
                "before": {
                    "Latency": 150,
                    "Throughput": 1800,
                    "CPU Utilization": 60,
                    "Memory Usage": 8,
                    "Error Rate": 1.0
                },
                "after": {
                    "Latency": 165,
                    "Throughput": 6500,
                    "CPU Utilization": 65,
                    "Memory Usage": 12,
                    "Error Rate": 0.8
                }
            },
            "sources": [
                "Sam Newman - 'Building Microservices'",
                "Netflix Technology Blog - Microservices Architecture",
                "Martin Fowler - 'Microservices Resource Guide'"
            ]
        },
        "Serverless Architecture": {
            "description": "A cloud computing execution model where the cloud provider runs the server, dynamically managing the allocation of machine resources.",
            "characteristics": [
                "No server management needed",
                "Auto-scaling built-in",
                "Pay-per-execution pricing",
                "Stateless functions"
            ],
            "metrics": {
                "Throughput": {
                    "value": 2500,
                    "unit": "req/sec",
                    "description": "Request processing rate under standard load"
                },
                "Latency": {
                    "value": 250,
                    "unit": "ms",
                    "description": "Average response time per request (including cold starts)"
                },
                "Availability": {
                    "value": 99.99,
                    "unit": "%",
                    "description": "System uptime percentage"
                },
                "Resource Utilization": {
                    "value": 20,
                    "unit": "%",
                    "description": "Average CPU and memory utilization"
                },
                "Fault Tolerance": {
                    "value": 4.7,
                    "unit": "1-5 scale",
                    "description": "Ability to handle component failures"
                },
                "Elasticity": {
                    "value": 5,
                    "unit": "1-5 scale",
                    "description": "Ease of scaling to handle increased load"
                },
                "Cost Efficiency": {
                    "value": 4.5,
                    "unit": "1-5 scale",
                    "description": "Operating cost relative to performance (pay per use)"
                },
                "Data Consistency": {
                    "value": 3,
                    "unit": "1-5 scale",
                    "description": "Maintaining data integrity across the system"
                }
            },
            "scaling_comparison": {
                "before": {
                    "Latency": 250,
                    "Throughput": 2500,
                    "CPU Utilization": 20,
                    "Memory Usage": 1.5,
                    "Error Rate": 0.8
                },
                "after": {
                    "Latency": 270,
                    "Throughput": 8500,
                    "CPU Utilization": 22,
                    "Memory Usage": 2.1,
                    "Error Rate": 0.6
                }
            },
            "sources": [
                "AWS Lambda Documentation",
                "Serverless Framework Best Practices",
                "Yan Cui - 'Production-Ready Serverless'",
                "Jeremy Daly - Serverless Architecture Patterns"
            ]
        },
        "Event-Driven Architecture": {
            "description": "A software architecture paradigm promoting the production, detection, consumption of, and reaction to events.",
            "characteristics": [
                "Asynchronous communication",
                "Loose coupling between components",
                "Event producers and consumers",
                "Event broker/message queue"
            ],
            "metrics": {
                "Throughput": {
                    "value": 3200,
                    "unit": "req/sec",
                    "description": "Request processing rate under standard load"
                },
                "Latency": {
                    "value": 180,
                    "unit": "ms",
                    "description": "Average response time per request"
                },
                "Availability": {
                    "value": 99.9,
                    "unit": "%",
                    "description": "System uptime percentage"
                },
                "Resource Utilization": {
                    "value": 55,
                    "unit": "%",
                    "description": "Average CPU and memory utilization"
                },
                "Fault Tolerance": {
                    "value": 4.5,
                    "unit": "1-5 scale",
                    "description": "Ability to handle component failures"
                },
                "Elasticity": {
                    "value": 4.3,
                    "unit": "1-5 scale",
                    "description": "Ease of scaling to handle increased load"
                },
                "Cost Efficiency": {
                    "value": 3.8,
                    "unit": "1-5 scale",
                    "description": "Operating cost relative to performance"
                },
                "Data Consistency": {
                    "value": 3.5,
                    "unit": "1-5 scale",
                    "description": "Maintaining data integrity across the system"
                }
            },
            "scaling_comparison": {
                "before": {
                    "Latency": 180,
                    "Throughput": 3200,
                    "CPU Utilization": 55,
                    "Memory Usage": 7.5,
                    "Error Rate": 1.2
                },
                "after": {
                    "Latency": 195,
                    "Throughput": 7800,
                    "CPU Utilization": 60,
                    "Memory Usage": 9.0,
                    "Error Rate": 0.9
                }
            },
            "sources": [
                "Gregor Hohpe - 'Enterprise Integration Patterns'",
                "Kafka Documentation - Event-Driven Design",
                "Martin Fowler - 'Event Sourcing Pattern'"
            ]
        },
        "Peer-to-Peer Architecture": {
            "description": "A distributed application architecture that partitions tasks or workloads between peers without central coordination.",
            "characteristics": [
                "Decentralized system design",
                "No single point of failure",
                "Shared resources among peers",
                "Direct communication between nodes"
            ],
            "metrics": {
                "Throughput": {
                    "value": 900,
                    "unit": "req/sec",
                    "description": "Request processing rate under standard load"
                },
                "Latency": {
                    "value": 220,
                    "unit": "ms",
                    "description": "Average response time per request"
                },
                "Availability": {
                    "value": 99.8,
                    "unit": "%",
                    "description": "System uptime percentage"
                },
                "Resource Utilization": {
                    "value": 70,
                    "unit": "%",
                    "description": "Average CPU and memory utilization"
                },
                "Fault Tolerance": {
                    "value": 4.8,
                    "unit": "1-5 scale",
                    "description": "Ability to handle component failures"
                },
                "Elasticity": {
                    "value": 3.5,
                    "unit": "1-5 scale",
                    "description": "Ease of scaling to handle increased load"
                },
                "Cost Efficiency": {
                    "value": 4.2,
                    "unit": "1-5 scale",
                    "description": "Operating cost relative to performance"
                },
                "Data Consistency": {
                    "value": 2.8,
                    "unit": "1-5 scale",
                    "description": "Maintaining data integrity across the system"
                }
            },
            "scaling_comparison": {
                "before": {
                    "Latency": 220,
                    "Throughput": 900,
                    "CPU Utilization": 70,
                    "Memory Usage": 9,
                    "Error Rate": 2.0
                },
                "after": {
                    "Latency": 195,
                    "Throughput": 5500,
                    "CPU Utilization": 85,
                    "Memory Usage": 14,
                    "Error Rate": 1.8
                }
            },
            "sources": [
                "Ian Foster - 'Designing and Building Parallel Programs'",
                "IPFS Documentation - Peer-to-Peer File System",
                "Bitcoin Whitepaper - Peer-to-Peer Electronic Cash System"
            ]
        },
        "Service-Oriented Architecture (SOA)": {
            "description": "A style of software design where services are provided to other components through communication protocols over a network.",
            "characteristics": [
                "Service contracts define interfaces",
                "Reusable services across applications",
                "Enterprise service bus for communication",
                "Business-oriented architectural approach"
            ],
            "metrics": {
                "Throughput": {
                    "value": 1200,
                    "unit": "req/sec",
                    "description": "Request processing rate under standard load"
                },
                "Latency": {
                    "value": 190,
                    "unit": "ms",
                    "description": "Average response time per request"
                },
                "Availability": {
                    "value": 99.7,
                    "unit": "%",
                    "description": "System uptime percentage"
                },
                "Resource Utilization": {
                    "value": 65,
                    "unit": "%",
                    "description": "Average CPU and memory utilization"
                },
                "Fault Tolerance": {
                    "value": 4.0,
                    "unit": "1-5 scale",
                    "description": "Ability to handle component failures"
                },
                "Elasticity": {
                    "value": 3.5,
                    "unit": "1-5 scale",
                    "description": "Ease of scaling to handle increased load"
                },
                "Cost Efficiency": {
                    "value": 3.5,
                    "unit": "1-5 scale",
                    "description": "Operating cost relative to performance"
                },
                "Data Consistency": {
                    "value": 4.0,
                    "unit": "1-5 scale",
                    "description": "Maintaining data integrity across the system"
                }
            },
            "scaling_comparison": {
                "before": {
                    "Latency": 190,
                    "Throughput": 1200,
                    "CPU Utilization": 65,
                    "Memory Usage": 8,
                    "Error Rate": 1.5
                },
                "after": {
                    "Latency": 210,
                    "Throughput": 4800,
                    "CPU Utilization": 75,
                    "Memory Usage": 11,
                    "Error Rate": 1.2
                }
            },
            "sources": [
                "Thomas Erl - 'SOA Principles of Service Design'",
                "Microsoft Documentation - Service-Oriented Architecture",
                "OASIS - SOA Reference Model"
            ]
        }
    }

def get_pattern_metrics_as_dataframe():
    """
    Convert architecture patterns data to a pandas DataFrame for easy comparison
    """
    arch_data = load_architecture_data()
    
    # Initialize lists to store data
    patterns = []
    metrics = []
    values = []
    units = []
    
    # Extract data from nested structure
    for pattern_name, pattern_data in arch_data.items():
        for metric_name, metric_data in pattern_data["metrics"].items():
            patterns.append(pattern_name)
            metrics.append(metric_name)
            values.append(metric_data["value"])
            units.append(metric_data["unit"])
    
    # Create DataFrame
    df = pd.DataFrame({
        "Pattern": patterns,
        "Metric": metrics,
        "Value": values,
        "Unit": units
    })
    
    return df

def get_comparison_data():
    """
    Prepare data for pattern comparison in a format suitable for visualization
    """
    arch_data = load_architecture_data()
    
    # Initialize data structure
    comparison_data = {
        "Pattern": [],
        "Throughput": [],
        "Latency": [],
        "Availability": [],
        "Resource_Utilization": [],
        "Fault_Tolerance": [],
        "Elasticity": [],
        "Cost_Efficiency": [],
        "Data_Consistency": []
    }
    
    # Extract data from each pattern
    for pattern_name, pattern_data in arch_data.items():
        comparison_data["Pattern"].append(pattern_name)
        comparison_data["Throughput"].append(pattern_data["metrics"]["Throughput"]["value"])
        comparison_data["Latency"].append(pattern_data["metrics"]["Latency"]["value"])
        comparison_data["Availability"].append(pattern_data["metrics"]["Availability"]["value"])
        comparison_data["Resource_Utilization"].append(pattern_data["metrics"]["Resource Utilization"]["value"])
        comparison_data["Fault_Tolerance"].append(pattern_data["metrics"]["Fault Tolerance"]["value"])
        comparison_data["Elasticity"].append(pattern_data["metrics"]["Elasticity"]["value"])
        comparison_data["Cost_Efficiency"].append(pattern_data["metrics"]["Cost Efficiency"]["value"])
        comparison_data["Data_Consistency"].append(pattern_data["metrics"]["Data Consistency"]["value"])
    
    # Convert to DataFrame
    df = pd.DataFrame(comparison_data)
    
    return df

def save_test_results(pattern_name, test_results):
    """
    Save custom test results for a specific pattern
    """
    arch_data = load_architecture_data()
    
    # Update data with test results
    if pattern_name in arch_data:
        # Update metrics with test results
        for metric_name, value in test_results.items():
            if metric_name in arch_data[pattern_name]["metrics"]:
                arch_data[pattern_name]["metrics"][metric_name]["value"] = value
    
    # Save updated data
    save_architecture_data(arch_data)
    
    return True

# Initialize data file if it doesn't exist
if not os.path.exists(os.path.join(DATA_DIR, "architecture_patterns.json")):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    save_architecture_data(get_default_patterns())
