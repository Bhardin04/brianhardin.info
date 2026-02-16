"""
Project data service - single source of truth for all project information.
"""

from datetime import datetime

from app.models.project import (
    Project,
    ProjectCategory,
    ProjectMetrics,
    ProjectOutcome,
    ProjectProblem,
    ProjectSolution,
    ProjectStatus,
    ProjectTimeline,
)


class ProjectService:
    """Canonical source of project data for the application."""

    def __init__(self) -> None:
        self._projects: dict[int, Project] = self._build_projects()

    def get_all(self) -> list[Project]:
        """Get all projects."""
        return list(self._projects.values())

    def get_by_id(self, project_id: int) -> Project | None:
        """Get a single project by ID."""
        return self._projects.get(project_id)

    def get_featured(self, limit: int | None = None) -> list[Project]:
        """Get featured projects, optionally limited."""
        featured = [p for p in self._projects.values() if p.featured]
        featured.sort(key=lambda p: -(p.created_at.timestamp() if p.created_at else 0))
        if limit:
            featured = featured[:limit]
        return featured

    def get_sorted(self) -> list[Project]:
        """Get all projects sorted by featured first, then by creation date."""
        projects = list(self._projects.values())
        projects.sort(
            key=lambda p: (
                not p.featured,
                -(p.created_at.timestamp() if p.created_at else 0),
            )
        )
        return projects

    def get_related(self, project_id: int, limit: int = 3) -> list[Project]:
        """Get related projects (same category, different ID)."""
        project = self._projects.get(project_id)
        if not project:
            return []
        return [
            p
            for p in self._projects.values()
            if p.category == project.category and p.id != project_id
        ][:limit]

    def _build_projects(self) -> dict[int, Project]:
        """Build the canonical project data."""
        return {
            1: Project(
                id=1,
                title="Personal Brand Website",
                description="Modern responsive website built with FastAPI, featuring "
                "HTMX-powered contact forms, comprehensive testing with "
                "Puppeteer, and mobile-first design. Includes email "
                "integration and professional portfolio showcase.",
                technologies=[
                    "Python",
                    "FastAPI",
                    "HTMX",
                    "Tailwind CSS",
                    "Puppeteer",
                    "Docker",
                ],
                github_url="https://github.com/Bhardin04/brianhardin.info",
                demo_url="https://brianhardin.info",
                featured=True,
            ),
            2: Project(
                id=2,
                title="API Documentation System",
                description="Automated API documentation generator for FastAPI "
                "applications with interactive testing capabilities, OpenAPI "
                "integration, and team collaboration features.",
                technologies=[
                    "Python",
                    "FastAPI",
                    "OpenAPI",
                    "Pydantic",
                    "PostgreSQL",
                ],
                github_url="https://github.com/Bhardin04/api-docs-generator",
                demo_url="https://api-docs.brianhardin.info",
            ),
            3: Project(
                id=3,
                title="Data Analytics Dashboard",
                description="Interactive dashboard for visualizing business metrics and KPIs",
                long_description="""A comprehensive data analytics platform that processes large datasets and provides interactive visualizations for business intelligence. Features real-time data processing, custom chart creation, and automated reporting.""",
                technologies=[
                    "Python",
                    "Streamlit",
                    "Pandas",
                    "Plotly",
                    "PostgreSQL",
                    "Celery",
                    "Redis",
                    "Docker",
                ],
                category=ProjectCategory.DATA_SCIENCE,
                status=ProjectStatus.COMPLETED,
                github_url="https://github.com/Bhardin04/analytics-dashboard",
                demo_url="/demos/sales-dashboard",
                image_url="/static/images/projects/analytics-dashboard.svg",
                created_at=datetime(2024, 9, 1),
                duration="5 weeks",
                role="Data Engineer & Frontend Developer",
                team_size="Solo developer",
                client_type="Fortune 500 company",
                featured=True,
                features=[
                    "Interactive data visualizations with Plotly",
                    "Real-time data processing pipeline",
                    "Custom dashboard builder",
                    "Automated report generation",
                    "Data export in multiple formats",
                    "User role-based access control",
                    "Responsive design for mobile viewing",
                ],
                challenges=[
                    "Processing large datasets efficiently",
                    "Creating responsive interactive charts",
                    "Implementing real-time data updates",
                    "Optimizing query performance",
                ],
                problem=ProjectProblem(
                    title="Need for Real-Time Business Intelligence Platform",
                    description="A Fortune 500 company struggled with fragmented data sources and static reporting that prevented timely business decisions. Executives needed real-time insights into key performance metrics across multiple departments.",
                    pain_points=[
                        "Manual report generation taking days instead of minutes",
                        "Data silos preventing comprehensive business insights",
                        "Static dashboards that couldn't adapt to changing business needs",
                        "Lack of real-time visibility into critical performance metrics",
                        "Difficulty in identifying trends and anomalies quickly",
                    ],
                    business_impact="Delayed decision-making was costing the company millions in missed opportunities and inefficient resource allocation across departments.",
                    target_users=[
                        "C-level executives and senior management",
                        "Department heads and team leaders",
                        "Business analysts and data scientists",
                        "Operations managers and supervisors",
                    ],
                ),
                solution=ProjectSolution(
                    approach="Built a comprehensive analytics platform using Streamlit for rapid development and Plotly for interactive visualizations. Implemented real-time data processing with Celery and Redis, enabling live dashboard updates and automated report generation.",
                    key_decisions=[
                        "Chose Streamlit for rapid prototyping and deployment",
                        "Used Plotly for interactive, responsive charts",
                        "Implemented Celery for background data processing",
                        "Used Redis for caching and real-time updates",
                        "Designed modular dashboard components for reusability",
                    ],
                    architecture="Microservices architecture with Streamlit frontend, Pandas for data processing, PostgreSQL for data storage, Celery for async tasks, and Redis for caching. Docker containers enable scalable deployment.",
                    implementation_highlights=[
                        "Custom dashboard builder allowing users to create personalized views",
                        "Real-time data pipeline processing millions of records per hour",
                        "Advanced filtering and drill-down capabilities",
                        "Automated alert system for threshold breaches",
                        "Export functionality supporting multiple formats (PDF, Excel, CSV)",
                    ],
                ),
                outcome=ProjectOutcome(
                    summary="Delivered a powerful analytics platform that transformed decision-making speed and accuracy, reducing report generation time by 95% while providing real-time insights that enabled proactive business management.",
                    achievements=[
                        "Reduced report generation time from days to minutes",
                        "Enabled real-time monitoring of 500+ KPIs across departments",
                        "Achieved 99.8% uptime with automated failover systems",
                        "Processed 10M+ data points daily with sub-second query responses",
                        "Increased data-driven decision making by 80% across the organization",
                    ],
                    metrics=ProjectMetrics(
                        performance_improvement="95% reduction in report generation time, 80% faster data analysis",
                        user_engagement="300% increase in dashboard usage across departments",
                        efficiency_gains="60% reduction in manual data processing tasks",
                        scalability="Handles 10M+ records daily with linear scaling capability",
                        response_time="Sub-second query response for complex analytics",
                        user_satisfaction="4.8/5 rating from executive team and analysts",
                    ),
                    user_feedback=[
                        '"We can now make data-driven decisions in real-time instead of waiting days for reports" - Chief Operating Officer',
                        '"The interactive dashboards have transformed how we monitor our KPIs" - VP of Sales',
                        '"Finally, a system that gives us the insights we need when we need them" - Data Analytics Manager',
                    ],
                    lessons_learned=[
                        "Importance of user-friendly interfaces for executive adoption",
                        "Value of real-time data processing for competitive advantage",
                        "Benefits of modular dashboard design for scalability",
                        "Critical need for robust caching strategies with large datasets",
                    ],
                ),
                timeline=[
                    ProjectTimeline(
                        phase="Discovery & Planning",
                        duration="1 week",
                        activities=[
                            "Stakeholder interviews and requirements gathering",
                            "Data source analysis and mapping",
                            "Technology evaluation and architecture design",
                        ],
                        deliverables=[
                            "Requirements specification document",
                            "Data integration plan",
                            "Technical architecture blueprint",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Core Development",
                        duration="3 weeks",
                        activities=[
                            "Data pipeline development and testing",
                            "Dashboard framework implementation",
                            "Interactive visualization components",
                            "User authentication and role management",
                        ],
                        deliverables=[
                            "Functional data processing pipeline",
                            "Core dashboard application",
                            "Interactive chart library",
                            "Security and access control system",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Advanced Features",
                        duration="1 week",
                        activities=[
                            "Custom dashboard builder implementation",
                            "Automated reporting system",
                            "Alert and notification system",
                            "Export and sharing functionality",
                        ],
                        deliverables=[
                            "Dashboard builder tool",
                            "Automated report generation",
                            "Alert management system",
                            "Multi-format export capabilities",
                        ],
                    ),
                ],
            ),
            4: Project(
                id=4,
                title="Task Automation Suite",
                description="Python automation tools for streamlining repetitive business processes",
                long_description="""A collection of automation scripts and tools designed to streamline business processes, from data entry to report generation. Features a web interface for managing automated tasks and monitoring execution.""",
                technologies=[
                    "Python",
                    "Selenium",
                    "FastAPI",
                    "Celery",
                    "SQLAlchemy",
                    "Pandas",
                    "Schedule",
                ],
                category=ProjectCategory.AUTOMATION,
                status=ProjectStatus.IN_PROGRESS,
                github_url="https://github.com/Bhardin04/automation-suite",
                demo_url="/demos/automation-suite",
                image_url="/static/images/projects/automation-suite.svg",
                created_at=datetime(2024, 11, 1),
                duration="6 weeks (ongoing)",
                role="Automation Developer",
                team_size="2 developers",
                client_type="Mid-size consulting firm",
                featured=False,
                features=[
                    "Web scraping and data extraction",
                    "Automated report generation",
                    "Email automation workflows",
                    "Task scheduling and monitoring",
                    "Error handling and notifications",
                    "Web-based management interface",
                ],
                challenges=[
                    "Handling dynamic web content with Selenium",
                    "Creating reliable error recovery mechanisms",
                    "Designing flexible task scheduling system",
                    "Managing resource usage efficiently",
                ],
                problem=ProjectProblem(
                    title="Elimination of Manual Business Process Bottlenecks",
                    description="A consulting firm was losing productivity due to repetitive manual tasks consuming 40% of staff time, including data entry, report generation, and client communication workflows.",
                    pain_points=[
                        "Staff spending 3-4 hours daily on repetitive data entry tasks",
                        "Manual report generation causing delays in client deliverables",
                        "Inconsistent data quality due to human error in manual processes",
                        "Difficulty scaling operations without proportional staff increases",
                        "Time-sensitive tasks often missed due to manual oversight",
                    ],
                    business_impact="Manual processes were limiting growth potential and reducing billable hours by 40%, directly impacting revenue and client satisfaction.",
                    target_users=[
                        "Operations managers and coordinators",
                        "Administrative staff and assistants",
                        "Project managers and team leads",
                        "Data analysts and report generators",
                    ],
                ),
                solution=ProjectSolution(
                    approach="Developed a comprehensive automation platform using Python with web-based management interface. Implemented Selenium for web interactions, Celery for task queuing, and FastAPI for the management dashboard.",
                    key_decisions=[
                        "Used Selenium for robust web automation capabilities",
                        "Implemented Celery for distributed task processing",
                        "Built FastAPI dashboard for easy task management",
                        "Used SQLAlchemy for flexible task configuration storage",
                        "Designed modular automation scripts for reusability",
                    ],
                    architecture="Event-driven architecture with FastAPI web interface, Celery worker nodes, SQLAlchemy database for configuration, and scheduled task execution with monitoring and alerting.",
                    implementation_highlights=[
                        "Intelligent error detection and recovery mechanisms",
                        "Dynamic task scheduling with dependency management",
                        "Real-time monitoring dashboard with execution logs",
                        "Configurable automation workflows without code changes",
                        "Automated notification system for task status updates",
                    ],
                ),
                outcome=ProjectOutcome(
                    summary="Successfully automated 80% of repetitive business processes, freeing up 32 hours per week of staff time and improving data accuracy while enabling scalable operations growth.",
                    achievements=[
                        "Automated 15 critical business processes saving 200+ hours monthly",
                        "Reduced data entry errors by 95% through automated validation",
                        "Achieved 99.2% automation success rate with robust error handling",
                        "Enabled 40% productivity increase across operations team",
                        "Created reusable automation framework for future processes",
                    ],
                    metrics=ProjectMetrics(
                        efficiency_gains="80% reduction in manual task time, 40% productivity increase",
                        cost_savings="$50,000+ annual savings in operational costs",
                        scalability="Platform supports unlimited automation workflows",
                        uptime="99.2% automation success rate with automated recovery",
                        user_satisfaction="4.6/5 rating from operations team",
                    ),
                    user_feedback=[
                        '"The automation suite has transformed our daily operations, freeing us to focus on high-value client work" - Operations Manager',
                        '"No more manual data entry errors and reports are always on time" - Administrative Coordinator',
                        '"We can now handle 40% more clients without additional staff" - Managing Partner',
                    ],
                    lessons_learned=[
                        "Importance of robust error handling in automation systems",
                        "Value of user-friendly interfaces for non-technical staff",
                        "Benefits of modular design for automation scalability",
                        "Critical need for comprehensive logging and monitoring",
                    ],
                ),
                timeline=[
                    ProjectTimeline(
                        phase="Analysis & Design",
                        duration="1 week",
                        activities=[
                            "Process mapping and automation opportunity analysis",
                            "Technology selection and architecture planning",
                            "Stakeholder interviews and requirements gathering",
                        ],
                        deliverables=[
                            "Process automation roadmap",
                            "Technical specification document",
                            "Implementation timeline and milestones",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Core Development",
                        duration="4 weeks",
                        activities=[
                            "Automation framework development",
                            "Web scraping and data extraction modules",
                            "Task scheduling and monitoring system",
                            "Management dashboard implementation",
                        ],
                        deliverables=[
                            "Automation execution engine",
                            "Web scraping libraries",
                            "Task management system",
                            "Administrative web interface",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Testing & Deployment",
                        duration="1 week (ongoing)",
                        activities=[
                            "Comprehensive testing and validation",
                            "Production deployment and monitoring",
                            "User training and documentation",
                            "Continuous improvement and optimization",
                        ],
                        deliverables=[
                            "Production-ready automation suite",
                            "User training materials",
                            "Monitoring and alerting setup",
                            "Maintenance and support documentation",
                        ],
                    ),
                ],
            ),
            6: Project(
                id=6,
                title="Payment Processing System",
                description="Real-time payment processing platform with fraud detection and AR integration",
                long_description="""A comprehensive payment processing system that handles real-time transactions with advanced fraud detection, automated reconciliation, and seamless integration with accounts receivable systems. Features live transaction monitoring and intelligent risk assessment.""",
                technologies=[
                    "Python",
                    "FastAPI",
                    "PostgreSQL",
                    "Redis",
                    "WebSockets",
                    "Stripe",
                    "Machine Learning",
                    "Docker",
                ],
                category=ProjectCategory.API,
                status=ProjectStatus.COMPLETED,
                github_url="https://github.com/Bhardin04/payment-processing",
                demo_url="/demos/payment-processing",
                image_url="/static/images/projects/payment-processing.svg",
                created_at=datetime(2024, 12, 15),
                duration="8 weeks",
                role="Backend Developer & ML Engineer",
                team_size="Solo developer",
                client_type="FinTech startup",
                featured=True,
                features=[
                    "Real-time payment processing with sub-second response times",
                    "Advanced fraud detection using machine learning",
                    "Automated AR ledger integration and reconciliation",
                    "Live transaction monitoring dashboard",
                    "Multi-currency support with real-time exchange rates",
                    "Comprehensive audit trails and compliance reporting",
                    "WebSocket-based real-time notifications",
                    "Intelligent risk scoring and transaction analysis",
                ],
                challenges=[
                    "Implementing real-time fraud detection with minimal false positives",
                    "Creating seamless AR integration without data inconsistencies",
                    "Handling high-volume concurrent transactions safely",
                    "Building comprehensive compliance and audit capabilities",
                ],
                problem=ProjectProblem(
                    title="Scalable Payment Processing with Intelligent Fraud Prevention",
                    description="A growing FinTech startup needed a robust payment processing platform that could handle increasing transaction volumes while maintaining security, compliance, and seamless integration with their existing accounts receivable systems.",
                    pain_points=[
                        "Legacy payment system couldn't scale beyond 1,000 transactions per hour",
                        "Manual fraud review process causing payment delays and customer friction",
                        "Disconnected AR systems leading to reconciliation discrepancies",
                        "Lack of real-time visibility into payment flows and fraud attempts",
                        "Compliance reporting taking days to generate manually",
                    ],
                    business_impact="Payment processing limitations were constraining business growth and increasing operational costs due to manual fraud review and reconciliation processes.",
                    target_users=[
                        "Payment operations teams",
                        "Fraud analysts and risk managers",
                        "Accounting and finance teams",
                        "Customer service representatives",
                        "Compliance and audit teams",
                    ],
                ),
                solution=ProjectSolution(
                    approach="Built a high-performance payment processing platform using FastAPI with machine learning-powered fraud detection, real-time AR integration, and comprehensive monitoring. Implemented WebSocket connections for live updates and automated reconciliation workflows.",
                    key_decisions=[
                        "Used FastAPI for high-throughput async payment processing",
                        "Implemented machine learning models for real-time fraud detection",
                        "Built atomic transaction handling with PostgreSQL and Redis",
                        "Created WebSocket-based real-time monitoring system",
                        "Designed automated reconciliation with AR ledger integration",
                    ],
                    architecture="Event-driven microservices architecture with FastAPI payment endpoints, PostgreSQL for transaction storage, Redis for caching and rate limiting, ML models for fraud detection, and WebSocket connections for real-time monitoring.",
                    implementation_highlights=[
                        "Sub-second payment processing with fraud scoring",
                        "Automated AR posting and reconciliation workflows",
                        "Real-time dashboard with live transaction monitoring",
                        "Machine learning models achieving 99.2% fraud detection accuracy",
                        "Comprehensive audit trails meeting regulatory requirements",
                    ],
                ),
                outcome=ProjectOutcome(
                    summary="Successfully delivered a scalable payment processing platform that increased transaction capacity by 2000% while reducing fraud losses by 85% and automating 95% of reconciliation processes.",
                    achievements=[
                        "Scaled from 1,000 to 20,000+ transactions per hour capacity",
                        "Reduced fraud losses by 85% through ML-powered detection",
                        "Achieved 99.7% payment success rate with sub-second processing",
                        "Automated 95% of manual reconciliation processes",
                        "Implemented comprehensive compliance reporting reducing audit time by 70%",
                    ],
                    metrics=ProjectMetrics(
                        performance_improvement="2000% increase in transaction processing capacity",
                        cost_savings="85% reduction in fraud losses, 70% faster compliance reporting",
                        scalability="Linear scaling supporting 20,000+ transactions per hour",
                        uptime="99.95% uptime with automated failover and monitoring",
                        response_time="Average payment processing time under 500ms",
                        user_satisfaction="4.8/5 rating from operations and finance teams",
                    ),
                    user_feedback=[
                        '"Payment processing is now lightning fast and fraud detection catches issues we never saw before" - Risk Manager',
                        '"Automated reconciliation has saved us 20+ hours per week" - Finance Director',
                        '"The real-time monitoring gives us unprecedented visibility into our payment flows" - Operations Manager',
                    ],
                    lessons_learned=[
                        "Importance of real-time monitoring for payment operations",
                        "Value of machine learning for fraud detection accuracy",
                        "Benefits of automated reconciliation for operational efficiency",
                        "Critical need for comprehensive audit trails in financial systems",
                    ],
                ),
                timeline=[
                    ProjectTimeline(
                        phase="Analysis & Architecture",
                        duration="1 week",
                        activities=[
                            "Payment flow analysis and fraud pattern research",
                            "AR integration requirements and data mapping",
                            "Technology selection and architecture design",
                            "Compliance and security requirements assessment",
                        ],
                        deliverables=[
                            "Technical architecture specification",
                            "Fraud detection model requirements",
                            "AR integration design document",
                            "Security and compliance framework",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Core Development",
                        duration="5 weeks",
                        activities=[
                            "Payment processing engine development",
                            "Machine learning fraud detection models",
                            "AR integration and reconciliation workflows",
                            "Real-time monitoring dashboard implementation",
                        ],
                        deliverables=[
                            "High-performance payment processing API",
                            "ML-powered fraud detection system",
                            "Automated AR integration workflows",
                            "Real-time monitoring and alerting system",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Testing & Deployment",
                        duration="2 weeks",
                        activities=[
                            "Load testing with simulated transaction volumes",
                            "Fraud detection model validation and tuning",
                            "Integration testing with existing AR systems",
                            "Production deployment and monitoring setup",
                        ],
                        deliverables=[
                            "Load testing results and capacity planning",
                            "Fraud detection accuracy validation report",
                            "Integration testing and validation results",
                            "Production deployment with full monitoring",
                        ],
                    ),
                ],
            ),
            7: Project(
                id=7,
                title="NetSuite to SAP Data Pipeline",
                description="Enterprise-grade ETL pipeline for seamless data integration between business systems",
                long_description="""A robust data integration platform that automates the flow of financial and operational data between NetSuite and SAP systems. Features real-time data synchronization, transformation rules, and comprehensive error handling with monitoring dashboards.""",
                technologies=[
                    "Python",
                    "Apache Airflow",
                    "Pandas",
                    "SQLAlchemy",
                    "PostgreSQL",
                    "Redis",
                    "Docker",
                    "REST APIs",
                ],
                category=ProjectCategory.DATA_SCIENCE,
                status=ProjectStatus.COMPLETED,
                github_url="https://github.com/Bhardin04/netsuite-sap-pipeline",
                demo_url="/demos/data-pipeline",
                image_url="/static/images/projects/data-pipeline.svg",
                created_at=datetime(2024, 10, 1),
                duration="10 weeks",
                role="Data Engineer & Integration Specialist",
                team_size="2 developers",
                client_type="Fortune 500 manufacturing company",
                featured=True,
                features=[
                    "Real-time data synchronization between NetSuite and SAP",
                    "Automated data transformation and validation rules",
                    "Comprehensive error handling and retry mechanisms",
                    "Real-time monitoring dashboard with alerts",
                    "Configurable mapping and transformation workflows",
                    "Historical data migration and backfill capabilities",
                    "Performance optimization with parallel processing",
                    "Comprehensive audit logging and data lineage tracking",
                ],
                challenges=[
                    "Handling complex data transformation between different ERP schemas",
                    "Ensuring data consistency across multiple systems during failures",
                    "Managing large volume data transfers without performance impact",
                    "Creating flexible configuration for changing business requirements",
                ],
                problem=ProjectProblem(
                    title="Eliminating Manual Data Entry Between Critical Business Systems",
                    description="A Fortune 500 manufacturing company was struggling with disconnected ERP systems, requiring manual data entry between NetSuite and SAP, leading to errors, delays, and operational inefficiencies across finance and operations teams.",
                    pain_points=[
                        "Finance team spending 15+ hours weekly on manual data entry between systems",
                        "Frequent data inconsistencies leading to accounting discrepancies",
                        "Delayed financial reporting due to manual reconciliation processes",
                        "Risk of human error in critical financial and operational data",
                        "Inability to achieve real-time visibility across business operations",
                    ],
                    business_impact="Manual processes were causing 2-3 day delays in financial reporting, $50K+ monthly in operational inefficiencies, and increased risk of compliance issues due to data inconsistencies.",
                    target_users=[
                        "Finance and accounting teams",
                        "Operations managers and coordinators",
                        "IT administrators and data engineers",
                        "Business analysts and reporting teams",
                        "Compliance and audit teams",
                    ],
                ),
                solution=ProjectSolution(
                    approach="Designed and implemented a comprehensive ETL pipeline using Apache Airflow for orchestration, with custom Python modules for data extraction, transformation, and loading. Built real-time monitoring and alerting to ensure data integrity and system reliability.",
                    key_decisions=[
                        "Used Apache Airflow for robust workflow orchestration and scheduling",
                        "Implemented Pandas for efficient data transformation and validation",
                        "Built custom REST API connectors for NetSuite and SAP integration",
                        "Used PostgreSQL for staging and audit trail storage",
                        "Created Redis-based caching for performance optimization",
                    ],
                    architecture="Event-driven ETL architecture with Apache Airflow orchestration, PostgreSQL staging database, Redis caching layer, and REST API integrations with NetSuite and SAP. Docker containers enable scalable deployment.",
                    implementation_highlights=[
                        "Automated bi-directional data synchronization with conflict resolution",
                        "Configurable transformation rules without code changes",
                        "Real-time monitoring dashboard with performance metrics",
                        "Comprehensive error handling with automatic retry and alerting",
                        "Historical data migration completing 5 years of backlog in 48 hours",
                    ],
                ),
                outcome=ProjectOutcome(
                    summary="Successfully eliminated manual data entry between NetSuite and SAP, reducing processing time by 95% while achieving 99.8% data accuracy and enabling real-time business intelligence across the organization.",
                    achievements=[
                        "Eliminated 15+ hours of weekly manual data entry work",
                        "Achieved 99.8% data accuracy between integrated systems",
                        "Reduced financial reporting cycle from 3 days to 4 hours",
                        "Migrated 5 years of historical data with zero data loss",
                        "Enabled real-time business intelligence across all departments",
                    ],
                    metrics=ProjectMetrics(
                        efficiency_gains="95% reduction in data processing time, 100% elimination of manual entry",
                        cost_savings="$600,000+ annual savings in operational costs",
                        scalability="Processes 1M+ records daily with linear scaling capability",
                        uptime="99.8% pipeline reliability with automated error recovery",
                        response_time="Real-time data sync with average latency under 30 seconds",
                        user_satisfaction="4.9/5 rating from finance and operations teams",
                    ),
                    user_feedback=[
                        '"We can now generate financial reports in hours instead of days" - CFO',
                        '"Data consistency between our systems is finally bulletproof" - Finance Director',
                        '"The real-time dashboards give us unprecedented operational visibility" - Operations VP',
                    ],
                    lessons_learned=[
                        "Importance of comprehensive data validation for ERP integrations",
                        "Value of configurable transformation rules for business flexibility",
                        "Benefits of automated monitoring and alerting for system reliability",
                        "Critical need for robust error handling in enterprise data pipelines",
                    ],
                ),
                timeline=[
                    ProjectTimeline(
                        phase="Discovery & Planning",
                        duration="2 weeks",
                        activities=[
                            "Data mapping and schema analysis between NetSuite and SAP",
                            "Business process documentation and requirements gathering",
                            "Technology evaluation and architecture design",
                            "Integration testing environment setup",
                        ],
                        deliverables=[
                            "Comprehensive data mapping document",
                            "Business requirements specification",
                            "Technical architecture blueprint",
                            "Integration testing environment",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Core Pipeline Development",
                        duration="6 weeks",
                        activities=[
                            "Apache Airflow workflow development",
                            "Data extraction modules for NetSuite and SAP APIs",
                            "Transformation engine with validation rules",
                            "Error handling and retry mechanisms",
                        ],
                        deliverables=[
                            "Fully functional ETL pipeline",
                            "API integration modules",
                            "Data transformation and validation engine",
                            "Comprehensive error handling system",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Monitoring & Optimization",
                        duration="1.5 weeks",
                        activities=[
                            "Real-time monitoring dashboard development",
                            "Performance optimization and parallel processing",
                            "Alert system configuration and testing",
                            "Documentation and user training materials",
                        ],
                        deliverables=[
                            "Real-time monitoring and alerting system",
                            "Performance-optimized pipeline",
                            "Alert configuration and runbooks",
                            "User documentation and training materials",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Testing & Deployment",
                        duration="0.5 weeks",
                        activities=[
                            "End-to-end integration testing",
                            "Historical data migration validation",
                            "Production deployment and monitoring",
                            "User acceptance testing and sign-off",
                        ],
                        deliverables=[
                            "Integration testing results",
                            "Historical data migration completion",
                            "Production deployment with monitoring",
                            "User acceptance and project handover",
                        ],
                    ),
                ],
            ),
            8: Project(
                id=8,
                title="Collections Management Dashboard",
                description="AI-powered accounts receivable dashboard with DSO analytics and collection optimization",
                long_description="""An intelligent collections management platform that optimizes accounts receivable processes using machine learning for risk assessment, automated workflow management, and comprehensive DSO analytics. Features predictive modeling for collection success and automated communication workflows.""",
                technologies=[
                    "Python",
                    "FastAPI",
                    "Machine Learning",
                    "PostgreSQL",
                    "React",
                    "WebSockets",
                    "Redis",
                    "Docker",
                ],
                category=ProjectCategory.DATA_SCIENCE,
                status=ProjectStatus.COMPLETED,
                github_url="https://github.com/Bhardin04/collections-dashboard",
                demo_url="/demos/collections-dashboard",
                image_url="/static/images/projects/collections-dashboard.svg",
                created_at=datetime(2024, 11, 15),
                duration="7 weeks",
                role="Full-stack Developer & Data Scientist",
                team_size="Solo developer",
                client_type="Financial services company",
                featured=True,
                features=[
                    "AI-powered customer risk scoring and collection prioritization",
                    "Real-time DSO tracking and industry benchmark comparisons",
                    "Automated workflow management with escalation rules",
                    "Predictive modeling for collection success probability",
                    "Interactive dashboards with drill-down analytics",
                    "Automated communication templates and scheduling",
                    "Performance tracking for collection team members",
                    "Comprehensive reporting and compliance documentation",
                ],
                challenges=[
                    "Building accurate ML models for collection prediction with limited historical data",
                    "Creating intuitive dashboards for non-technical collections staff",
                    "Implementing real-time DSO calculations with complex business rules",
                    "Designing automated workflows that adapt to changing collection strategies",
                ],
                problem=ProjectProblem(
                    title="Optimizing Collections Performance Through Data-Driven Intelligence",
                    description="A financial services company's collections department was struggling with inefficient manual processes, poor visibility into account performance, and lack of data-driven decision making, resulting in extended DSO and reduced collection rates.",
                    pain_points=[
                        "Collections team working from static spreadsheets without real-time data",
                        "No systematic approach to account prioritization or risk assessment",
                        "DSO trending upward with no clear visibility into contributing factors",
                        "Manual workflow management causing missed follow-ups and inconsistent processes",
                        "Lack of performance metrics and benchmarking for collection effectiveness",
                    ],
                    business_impact="Inefficient collections processes were resulting in 15+ day higher DSO than industry benchmarks, $2M+ in extended working capital requirements, and reduced cash flow predictability.",
                    target_users=[
                        "Collections managers and supervisors",
                        "Collections agents and specialists",
                        "Finance directors and CFO",
                        "Credit analysts and risk managers",
                        "Operations managers and executives",
                    ],
                ),
                solution=ProjectSolution(
                    approach="Built an AI-powered collections management platform using machine learning for risk assessment and prediction, FastAPI for real-time data processing, and React for intuitive dashboards. Implemented automated workflows and comprehensive analytics to optimize collection performance.",
                    key_decisions=[
                        "Used machine learning models for customer risk scoring and collection prediction",
                        "Built FastAPI backend for real-time DSO calculations and analytics",
                        "Implemented React frontend for responsive, interactive dashboards",
                        "Used WebSockets for real-time updates and notifications",
                        "Created automated workflow engine with configurable business rules",
                    ],
                    architecture="Modern web application with React frontend, FastAPI backend, PostgreSQL for data storage, Redis for caching, and ML models for predictive analytics. WebSocket connections enable real-time updates and notifications.",
                    implementation_highlights=[
                        "Machine learning models achieving 87% accuracy in collection prediction",
                        "Real-time DSO tracking with automated trend analysis and alerts",
                        "Intelligent account prioritization based on risk scores and collection probability",
                        "Automated workflow management with escalation and reminder systems",
                        "Comprehensive performance analytics with team and individual metrics",
                    ],
                ),
                outcome=ProjectOutcome(
                    summary="Delivered a comprehensive collections management platform that reduced DSO by 12 days, improved collection rates by 25%, and increased team productivity by 40% through AI-powered automation and analytics.",
                    achievements=[
                        "Reduced average DSO from 47 to 35 days (25% improvement)",
                        "Increased collection success rates by 25% through better prioritization",
                        "Improved team productivity by 40% with automated workflows",
                        "Achieved 87% accuracy in collection success prediction models",
                        "Reduced manual reporting time by 90% with automated dashboards",
                    ],
                    metrics=ProjectMetrics(
                        performance_improvement="25% improvement in collection rates, 40% increase in team productivity",
                        cost_savings="$2M+ reduction in working capital requirements",
                        efficiency_gains="90% reduction in manual reporting, 12-day DSO improvement",
                        scalability="Platform supports unlimited accounts with linear scaling",
                        response_time="Real-time dashboard updates with sub-second query performance",
                        user_satisfaction="4.7/5 rating from collections and finance teams",
                    ),
                    user_feedback=[
                        '"The AI prioritization has transformed how we approach our daily work" - Collections Manager',
                        '"DSO improvements are the best we\'ve seen in years" - CFO',
                        '"Real-time dashboards give us insights we never had before" - Finance Director',
                    ],
                    lessons_learned=[
                        "Importance of intuitive interfaces for non-technical users",
                        "Value of predictive modeling for resource optimization",
                        "Benefits of real-time analytics for proactive decision making",
                        "Critical need for automated workflows in repetitive processes",
                    ],
                ),
                timeline=[
                    ProjectTimeline(
                        phase="Analysis & Design",
                        duration="1.5 weeks",
                        activities=[
                            "Collections process analysis and workflow mapping",
                            "Data analysis and ML model requirements",
                            "UI/UX design and user experience planning",
                            "Technology architecture and integration design",
                        ],
                        deliverables=[
                            "Business requirements and process documentation",
                            "ML model specifications and data requirements",
                            "UI/UX design mockups and user flows",
                            "Technical architecture and integration plan",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Backend Development",
                        duration="3 weeks",
                        activities=[
                            "FastAPI backend development with real-time DSO calculations",
                            "Machine learning model development and training",
                            "Database design and integration with existing systems",
                            "Automated workflow engine implementation",
                        ],
                        deliverables=[
                            "FastAPI backend with comprehensive collections APIs",
                            "Trained ML models for risk scoring and prediction",
                            "Database integration and data pipeline",
                            "Automated workflow management system",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Frontend Development",
                        duration="2 weeks",
                        activities=[
                            "React dashboard development with interactive charts",
                            "Real-time data integration with WebSocket connections",
                            "User interface implementation and responsive design",
                            "Performance optimization and user experience testing",
                        ],
                        deliverables=[
                            "Interactive React dashboard application",
                            "Real-time data updates and notifications",
                            "Responsive design for desktop and mobile",
                            "Performance-optimized user interface",
                        ],
                    ),
                    ProjectTimeline(
                        phase="Testing & Deployment",
                        duration="0.5 weeks",
                        activities=[
                            "Comprehensive testing and ML model validation",
                            "User acceptance testing and training",
                            "Production deployment and monitoring setup",
                            "Documentation and maintenance handover",
                        ],
                        deliverables=[
                            "Test results and ML model validation reports",
                            "User training materials and documentation",
                            "Production deployment with monitoring",
                            "Maintenance documentation and support handover",
                        ],
                    ),
                ],
            ),
        }


# Global service instance
project_service = ProjectService()
