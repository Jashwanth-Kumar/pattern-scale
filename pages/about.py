import streamlit as st

def show():
    """Show the About & Citations page"""
    st.title("About & Citations")
    
    st.markdown("""
    <style>
        a {
            color: black !important;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
                
    # AI Architecture Pattern Evaluator
    
    This application helps you evaluate different software architecture patterns based on performance metrics.
    Compare and analyze patterns to determine the best approach for your application scaling needs.
    
    ## Purpose
    
    The AI Architecture Pattern Evaluator is designed to help developers, architects, and IT professionals
    make informed decisions about which software architecture pattern to use for their applications.
    By providing detailed performance metrics and comparison tools, the evaluator makes it easier to
    understand the tradeoffs between different architectural approaches.
    
    ## Metrics Definitions
    
    This application tracks and analyzes the following performance metrics:
    
    ### Throughput
    **Definition**: The number of requests the system can handle per second.  
    **Unit**: Requests per second (req/sec)  
    **Importance**: Higher throughput means the system can handle more traffic, which is critical for high-load applications.
    
    ### Latency
    **Definition**: The time it takes for the system to respond to a request.  
    **Unit**: Milliseconds (ms)  
    **Importance**: Lower latency means faster response times, which improves user experience.
    
    ### Availability
    **Definition**: The percentage of time the system is operational and accessible.  
    **Unit**: Percentage (%)  
    **Importance**: Higher availability means the system is more reliable and has less downtime.
    
    ### Resource Utilization
    **Definition**: The percentage of CPU and memory resources used by the system.  
    **Unit**: Percentage (%)  
    **Importance**: Lower resource utilization means the system is more efficient and can potentially handle more load.
    
    ### Fault Tolerance
    **Definition**: The ability of the system to continue operating when components fail.  
    **Unit**: 1-5 scale (higher is better)  
    **Importance**: Higher fault tolerance means the system is more resilient to failures.
    
    ### Elasticity
    **Definition**: The ability of the system to scale up or down based on load.  
    **Unit**: 1-5 scale (higher is better)  
    **Importance**: Higher elasticity means the system can handle varying loads more efficiently.
    
    ### Cost Efficiency
    **Definition**: The cost of running the system relative to its performance.  
    **Unit**: 1-5 scale (higher is better)  
    **Importance**: Higher cost efficiency means better performance per dollar spent.
    
    ### Data Consistency
    **Definition**: The ability of the system to maintain data integrity across components.  
    **Unit**: 1-5 scale (higher is better)  
    **Importance**: Higher data consistency means the system ensures data is accurate and up-to-date.
    
    ## Testing Methodology
    
    The evaluator uses a combination of simulated tests and industry benchmarks to generate performance metrics.
    
    For simulated tests:
    
    1. The application generates realistic performance data based on the characteristics of each architecture pattern
    2. The data is normalized to allow for fair comparison between patterns
    3. The results are displayed in various visualization formats for easy interpretation
    
    For URL tests (simulated in this environment):
    
    1. The application would perform HTTP requests to the specified URL
    2. It measures response times, throughput, and error rates
    3. The results are mapped to architecture pattern metrics for analysis
    
    ## Citations and Data Sources
    
    The performance metrics and architectural characteristics in this application are based on the following sources:
    
    ### Academic Sources
    
    - [Richards, M. (2015). *Software Architecture Patterns*. O'Reilly Media.](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/)      [E-Book](https://theswissbay.ch/pdf/Books/Computer%20science/O'Reilly/software-architecture-patterns.pdf)
    - [Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley.](https://martinfowler.com/books/eaa.html)      [E-Book](https://dl.ebooksworld.ir/motoman/Patterns%20of%20Enterprise%20Application%20Architecture.pdf)
    - [Newman, S. (2015). *Building Microservices*. O'Reilly Media.](https://www.oreilly.com/library/view/building-microservices/9781491950340/)        [E- Book](https://github.com/namhoangduc99/TargetOf2018/blob/master/Sam%20Newman-Building%20Microservices-O'Reilly%20Media%20(2015).pdf)
    - [Bass, L., Clements, P., & Kazman, R. (2012). *Software Architecture in Practice*. Addison-Wesley Professional.](https://www.oreilly.com/library/view/software-architecture-in/9780132942799/)        [E-Book](https://ptgmedia.pearsoncmg.com/images/9780321815736/samplepages/0321815734.pdf)
    
    ### Industry Reports and Documentation
    
    - [AWS Architecture Center: Best Practices for Serverless Applications](https://aws.amazon.com/blogs/compute/best-practices-for-organizing-larger-serverless-applications/).
    - [Microsoft Azure Architecture Center: Microservices Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/patterns).
    - [Netflix Technology Blog: Microservices at Netflix Scale](https://gotocon.com/dl/goto-amsterdam-2016/slides/RuslanMeshenberg_MicroservicesAtNetflixScaleFirstPrinciplesTradeoffsLessonsLearned.pdf)
    - [Google Cloud Architecture Framework: Best Practices for Cloud-Native Applications](https://cloud.google.com/architecture/framework).
    - [Kubernetes Documentation: Best Practices for Large Clusters](https://kubernetes.io/docs/setup/best-practices/cluster-large/)
    
    ### Benchmarking Studies
    
    - [TechEmpower Web Framework Benchmarks](https://www.techempower.com/benchmarks/#section=data-r23&test=json)
    - [SPEC Cloud IaaS 2018 Benchmark](https://www.spec.org/cloud_iaas2018/results/cloud_iaas2018/)
                
    ### Case Studies
    
    - [Netflix's migration from monolithic to microservices architecture](https://roshancloudarchitect.me/understanding-netflixs-microservices-architecture-a-cloud-architect-s-perspective-5c345f0a70af#:~:text=From%20Monolithic%20to%20Microservices%3A&text=By%202008%2C%20Netflix%20shifted%20to,without%20affecting%20the%20whole%20system.)
    - [Amazon's event-driven architecture for high-throughput systems](https://aws.amazon.com/event-driven-architecture/)
    - [Google's approach to distributed systems and scaling](https://cloud.google.com/architecture/scalable-and-resilient-apps#scalability_adjusting_capacity_to_meet_demand)
    """,unsafe_allow_html=True)

