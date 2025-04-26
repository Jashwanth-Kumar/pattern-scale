import streamlit as st
import os
import sys
from utils.data_manager import load_architecture_data
from utils.metrics_analyzer import get_pattern_scores
import pandas as pd

# Add the current directory to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set page configuration
st.set_page_config(
    page_title="AI Architecture Pattern Evaluator",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'selected_pattern' not in st.session_state:
    st.session_state.selected_pattern = None
if 'test_results' not in st.session_state:
    st.session_state.test_results = None
if 'comparison_data' not in st.session_state:
    st.session_state.comparison_data = None
if 'before_after_data' not in st.session_state:
    st.session_state.before_after_data = None

# Main title and description
st.write("") 
st.title("🏛️ AI Architecture Pattern Evaluator")
st.markdown("""
This application helps you evaluate different software architecture patterns based on performance metrics. 
Compare and analyze patterns to determine the best approach for your application scaling needs.
""")

# Sidebar navigation

# Hide sidebar and toggle
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }

        .block-container {
            padding-top: 1rem;
        }

        /* Remove gaps between columns */
        .stButton > button {
            margin: 0px;
            border-radius: 0px;
        }

        div[data-testid="column"] {
            padding-left: 0.1rem;
            padding-right: 0.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Navigation with top bar
if 'page' not in st.session_state:
    st.session_state.page = "Home"

with st.container():
    nav_cols = st.columns(5)

    nav_labels = ["Home", "Pattern Dashboard", "Comparison Tool", "Custom Test Plan", "About & Citations"]
    
    for i, label in enumerate(nav_labels):
        with nav_cols[i]:
            if st.button(label):
                st.session_state.page = label

# Read page from session state
page = st.session_state.page

# Load architecture patterns data
arch_data = load_architecture_data()
pattern_names = list(arch_data.keys())

# Home page content
if page == "Home":
    st.header("Welcome to the AI Architecture Pattern Evaluator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### What this tool does
        
        The AI Architecture Pattern Evaluator helps you:
        
        - **Analyze** different software architecture patterns based on key performance metrics
        - **Compare** patterns side-by-side to identify strengths and weaknesses
        - **Visualize** performance data through interactive charts and graphs
        - **Test** your application against different architectural models
        - **Recommend** the best pattern for your specific scaling needs
        
        ### Available Architecture Patterns
        
        This tool evaluates the following architecture patterns:
        """)
        
        for pattern in pattern_names:
            st.markdown(f"- **{pattern}**")
                    
    with col2:
        st.markdown("""
        ### Key Metrics Tracked
        
        The evaluator measures and compares these critical performance metrics:
        
        - **Throughput**: Requests processed per second
        - **Latency**: Response time in milliseconds
        - **Availability**: System uptime percentage
        - **Resource Utilization**: CPU and memory usage
        - **Fault Tolerance**: Ability to handle failures
        - **Elasticity**: Scaling capabilities
        - **Cost Efficiency**: Resource usage vs. performance
        - **Data Consistency**: Data integrity across the system
        """)
    
    
    # Show sample metrics comparison
    st.header("Sample Metrics Comparison")
    
    # Create sample data for visualization
    sample_data = {
        'Pattern': pattern_names,
        'Throughput': [get_pattern_scores(pattern, 'Throughput', arch_data) for pattern in pattern_names],
        'Latency': [get_pattern_scores(pattern, 'Latency', arch_data) for pattern in pattern_names],
        'Resource Utilization': [get_pattern_scores(pattern, 'Resource Utilization', arch_data) for pattern in pattern_names]
    }
    
    sample_df = pd.DataFrame(sample_data)
    
    # Display sample data as a bar chart
    st.bar_chart(sample_df.set_index('Pattern'))
    
    st.caption("This is a sample visualization. For detailed analysis, navigate to the Comparison Tool.")

# Include other pages based on navigation
elif page == "Pattern Dashboard":
    import pages.dashboard
    pages.dashboard.show()
    
elif page == "Comparison Tool":
    import pages.comparison
    pages.comparison.show()
    
elif page == "Custom Test Plan":
    import pages.custom_test
    pages.custom_test.show()
    
elif page == "About & Citations":
    import pages.about
    pages.about.show()


