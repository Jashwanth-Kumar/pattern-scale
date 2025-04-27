import streamlit as st
import pandas as pd
import time
from utils.data_manager import load_architecture_data, save_test_results
from utils.test_runner import run_custom_test_plan, simulate_scaling_comparison
from utils.visualization import create_radar_chart, create_before_after_chart

def show():
    """Show the Custom Test Plan page"""
    st.title("Custom Test Plan")
    
    # Load architecture data
    arch_data = load_architecture_data()
    pattern_names = list(arch_data.keys())
    
    st.markdown("""
    This tool allows you to test and evaluate different architecture patterns. You can:
    
    1. Run a simulated test for a specific pattern to generate performance metrics
    2. Compare all patterns with one click
    3. Analyze before and after scaling metrics
    """)
    
    # Create tabs for different test options
    tab1, tab2, tab3 = st.tabs(["Test a Pattern", "Compare All Patterns", "Scaling Test"])
    
    with tab1:
        st.subheader("Test a Specific Pattern")
        
        # Select a pattern to test
        test_pattern = st.selectbox(
            "Select an architecture pattern to test:",
            pattern_names
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("### Test Options")
            
            test_type = st.radio(
                "Select test type:",
                ["Simulated Test", "URL Test"],
                index=0
            )
            
            if test_type == "URL Test":
                test_url = st.text_input("Enter URL to test:", "https://example.com")
                st.caption("Note: URL tests will be simulated in this environment.")
            else:
                test_url = None
            
            st.info("The test will generate performance metrics for the selected pattern.")
            
            # Run test button
            if st.button("Run Test", key="run_single_test"):
                with st.spinner("Running test..."):
                    # Add a small delay for UX
                    time.sleep(2)
                    
                    # Run the test
                    if test_url:
                        test_results = run_custom_test_plan(url=test_url, pattern=test_pattern)
                    else:
                        test_results = run_custom_test_plan(pattern=test_pattern)
                    
                    # Store results in session state
                    st.session_state.test_results = test_results
                    
                    # Save results to data
                    save_test_results(test_pattern, test_results)
                
                st.success("Test completed! Results are displayed below.")
        
        with col2:
            st.markdown("### Test Results")
            
            if 'test_results' in st.session_state and st.session_state.test_results:
                results = st.session_state.test_results
                
                # Create a table of results
                results_table = []
                for metric, value in results.items():
                    if metric in arch_data[test_pattern]["metrics"]:
                        unit = arch_data[test_pattern]["metrics"][metric]["unit"]
                        results_table.append({
                            "Metric": metric,
                            "Value": value,
                            "Unit": unit
                        })
                
                results_df = pd.DataFrame(results_table)
                st.dataframe(results_df, hide_index=True)
                
                # Update the architecture data with test results
                updated_arch_data = load_architecture_data()  # Reload to get updated data
                
                # Create radar chart with updated data
                radar_fig = create_radar_chart(test_pattern, updated_arch_data)
                st.plotly_chart(radar_fig)
            else:
                st.info("Run a test to see results here.")
    
    with tab2:
        st.subheader("Compare All Patterns")
        
        st.markdown("""
        This tool will run simulated tests for all architecture patterns and compare their performance metrics.
        The results will be displayed in a table for easy comparison.
        """)
        
        if st.button("Run Comparison Test", key="run_comparison_test"):
            with st.spinner("Running tests for all patterns..."):
                # Add a small delay for UX
                time.sleep(3)
                
                # Run tests for all patterns
                all_results = {}
                for pattern in pattern_names:
                    results = run_custom_test_plan(pattern=pattern)
                    all_results[pattern] = results
                    
                    # Save results to data
                    save_test_results(pattern, results)
                
                # Store results in session state
                st.session_state.comparison_data = all_results
            
            st.success("All tests completed! Results are displayed below.")
        
        if 'comparison_data' in st.session_state and st.session_state.comparison_data:
            # Create comparison table
            comparison_table = []
            metrics = list(st.session_state.comparison_data[pattern_names[0]].keys())
            
            # Create a row for each metric
            for metric in metrics:
                row = {"Metric": metric}
                
                for pattern in pattern_names:
                    if pattern in st.session_state.comparison_data:
                        row[pattern] = st.session_state.comparison_data[pattern][metric]
                
                comparison_table.append(row)
            
            comparison_df = pd.DataFrame(comparison_table)
            
            st.dataframe(comparison_df, hide_index=True)
            
            # Add a download button for the comparison data
            csv = comparison_df.to_csv(index=False)
            st.download_button(
                label="Download Comparison Data as CSV",
                data=csv,
                file_name="architecture_pattern_comparison.csv",
                mime="text/csv"
            )
            
            # Highlight best pattern for each metric
            st.subheader("Best Pattern for Each Metric")
            
            best_patterns = []
            for metric in metrics:
                best_pattern = None
                best_value = None
                
                for pattern in pattern_names:
                    if pattern in st.session_state.comparison_data:
                        value = st.session_state.comparison_data[pattern][metric]
                        
                        # For latency and resource utilization, lower is better
                        if metric in ["Latency", "Resource Utilization"]:
                            if best_value is None or value < best_value:
                                best_value = value
                                best_pattern = pattern
                        else:
                            # For all other metrics, higher is better
                            if best_value is None or value > best_value:
                                best_value = value
                                best_pattern = pattern
                
                best_patterns.append({
                    "Metric": metric,
                    "Best Pattern": best_pattern,
                    "Value": best_value
                })
            
            best_patterns_df = pd.DataFrame(best_patterns)
            st.dataframe(best_patterns_df, hide_index=True)
        else:
            st.info("Run a comparison test to see results here.")
    
    with tab3:
        st.subheader("Scaling Test")
        
        st.markdown("""
        This test simulates how different architecture patterns perform before and after scaling.
        It will show metrics like latency, throughput, and resource utilization to help you 
        understand how each pattern handles increased load.
        """)
        
        # Select a pattern for scaling test
        scaling_pattern = st.selectbox(
            "Select an architecture pattern for scaling test:",
            pattern_names,
            key="scaling_pattern"
        )
        
        if st.button("Run Scaling Test"):
            with st.spinner("Running scaling test..."):
                # Add a small delay for UX
                time.sleep(2)
                
                # Run the scaling test
                scaling_results = simulate_scaling_comparison(scaling_pattern)
                
                # Store results in session state
                st.session_state.before_after_data = scaling_results
            
            st.success("Scaling test completed! Results are displayed below.")
        
        if 'before_after_data' in st.session_state and st.session_state.before_after_data:
            # Display before and after data
            before_data = st.session_state.before_after_data["before"]
            after_data = st.session_state.before_after_data["after"]
            
            # Create before vs after chart
            fig = create_before_after_chart(before_data, after_data, scaling_pattern)
            st.plotly_chart(fig)
            
            # Create a dataframe for comparison
            comparison_df = pd.DataFrame({
                "Metric": list(before_data.keys()),
                "Before Scaling": list(before_data.values()),
                "After Scaling": list(after_data.values()),
                "Change (%)": [(after / before - 1) * 100 if before > 0 else 0 
                                for before, after in zip(before_data.values(), after_data.values())]
            })
            
            # Format the Change column
            comparison_df["Change (%)"] = comparison_df["Change (%)"].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(comparison_df, hide_index=True)
            
            # Add interpretation
            st.subheader("Scaling Interpretation")
            
            # Get throughput change
            throughput_before = before_data.get("Throughput", 0)
            throughput_after = after_data.get("Throughput", 0)
            throughput_change = (throughput_after / throughput_before - 1) * 100 if throughput_before > 0 else 0
            
            # Get latency change
            latency_before = before_data.get("Latency", 0)
            latency_after = after_data.get("Latency", 0)
            latency_change = (latency_after / latency_before - 1) * 100 if latency_before > 0 else 0
            
            # Scaling efficiency interpretation
            scaling_efficiency = "Excellent"
            if throughput_change < 50:
                scaling_efficiency = "Poor"
            elif throughput_change < 100:
                scaling_efficiency = "Moderate"
            elif throughput_change < 200:
                scaling_efficiency = "Good"
            
            # Latency impact interpretation
            latency_impact = "Low"
            if latency_change > 50:
                latency_impact = "High"
            elif latency_change > 20:
                latency_impact = "Moderate"
            
            st.markdown(f"""
            ### Scaling Efficiency: **{scaling_efficiency}**
            
            - **Throughput Increase**: {throughput_change:.1f}%
            - **Latency Impact**: {latency_impact} ({latency_change:.1f}% change)
            
            Based on the scaling test, {scaling_pattern} shows **{scaling_efficiency.lower()}** scaling characteristics.
            The throughput increased by {throughput_change:.1f}% while the latency changed by {latency_change:.1f}%.
            """)
            
            # Add recommendations
            st.subheader("Recommendations")
            
            if scaling_efficiency == "Excellent" and latency_impact == "Low":
                st.success(f"{scaling_pattern} is an excellent choice for applications that need to scale efficiently.")
            elif scaling_efficiency == "Good" and latency_impact == "Low":
                st.success(f"{scaling_pattern} is a good choice for applications that need to scale efficiently.")
            elif scaling_efficiency == "Moderate":
                st.warning(f"{scaling_pattern} may not be ideal for applications that need to scale significantly.")
            else:
                st.error(f"{scaling_pattern} is not recommended for applications that need to scale significantly.")
        else:
            st.info("Run a scaling test to see results here.")
    
    # Additional information
    st.markdown("---")
    st.subheader("About the Tests")
    
    st.markdown("""
    ### Test Methodology
    
    The tests evaluate architecture patterns based on the following metrics:
    
    - **Throughput**: The number of requests per second the system can handle
    - **Latency**: The average response time for a request
    - **Availability**: The percentage of time the system is operational
    - **Resource Utilization**: The percentage of CPU and memory resources used
    - **Fault Tolerance**: The ability to handle component failures (rated 1-5)
    - **Elasticity**: The ease of scaling to handle increased load (rated 1-5)
    - **Cost Efficiency**: Operating cost relative to performance (rated 1-5)
    - **Data Consistency**: The ability to maintain data integrity (rated 1-5)
    
    ### Data Sources
    
    The test data is based on industry benchmarks, academic research, and real-world case studies.
    The simulated tests generate realistic performance metrics based on the characteristics of each
    architecture pattern.
    
    ### Ethical Considerations
    
    The AI analysis in this tool is based on established metrics and benchmarks, not personal data.
    It is designed to provide objective comparisons of different architecture patterns without bias.
    """)
