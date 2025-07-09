from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models.project import (
    Project, ProjectCategory, ProjectStatus, ProjectMetrics, 
    ProjectProblem, ProjectSolution, ProjectOutcome, ProjectTimeline
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Sample projects data - In a real app, this would come from a database
PROJECTS_DATA = {
    1: Project(
        id=1,
        title="Personal Portfolio Website",
        description="Modern, responsive personal brand website built with FastAPI and HTMX",
        long_description="""A comprehensive personal branding website showcasing my Python development skills and professional experience. Built with modern web technologies and following best practices for performance, SEO, and accessibility.""",
        technologies=["Python", "FastAPI", "HTMX", "Tailwind CSS", "Jinja2", "PostgreSQL", "Docker"],
        category=ProjectCategory.WEB_APP,
        status=ProjectStatus.COMPLETED,
        github_url="https://github.com/Bhardin04/brianhardin.info",
        demo_url="https://brianhardin.info",
        image_url="/static/images/projects/portfolio-website.svg",
        created_at=datetime(2024, 12, 1),
        duration="3 weeks",
        role="Full-stack Developer",
        team_size="Solo developer",
        client_type="Personal project",
        featured=True,
        features=[
            "Responsive mobile-first design",
            "Dark mode toggle with system preference detection",
            "Interactive contact form with email integration",
            "SEO optimized with structured data",
            "Performance optimized with caching",
            "Comprehensive testing suite"
        ],
        challenges=[
            "Implementing smooth dark mode transitions",
            "Optimizing for mobile responsiveness",
            "Email service integration and deliverability",
            "Performance optimization for fast loading"
        ],
        problem=ProjectProblem(
            title="Need for Professional Online Presence",
            description="As a Python developer seeking to establish credibility and attract potential clients, I needed a professional portfolio website that would showcase my technical skills while providing an excellent user experience.",
            pain_points=[
                "Lack of centralized platform to showcase projects and skills",
                "Difficulty communicating technical expertise to non-technical stakeholders",
                "Need for professional brand identity and online presence",
                "Requirement for fast, accessible, and mobile-responsive design"
            ],
            business_impact="Without a professional online presence, potential opportunities and client engagements were being lost due to lack of credibility and visibility.",
            target_users=[
                "Potential clients and employers",
                "Fellow developers and collaborators",
                "Recruiters and talent acquisition teams",
                "Industry professionals and networking contacts"
            ]
        ),
        solution=ProjectSolution(
            approach="Built a modern, performance-optimized portfolio website using FastAPI and HTMX to create a fast, interactive experience without heavy JavaScript frameworks. Implemented a clean, professional design with comprehensive project showcases and contact functionality.",
            key_decisions=[
                "Chose FastAPI for fast development and excellent performance",
                "Used HTMX for dynamic interactions without JavaScript complexity",
                "Implemented Tailwind CSS for consistent, responsive design",
                "Added comprehensive SEO and accessibility features",
                "Integrated professional email handling for contact forms"
            ],
            architecture="Server-side rendered application with FastAPI backend, Jinja2 templating, PostgreSQL database, and containerized deployment. HTMX provides dynamic interactions while maintaining fast page loads.",
            implementation_highlights=[
                "Custom design system with consistent spacing and typography",
                "Advanced dark mode implementation with system preference detection",
                "Comprehensive SEO optimization with structured data",
                "Performance optimization achieving 95+ PageSpeed scores",
                "Responsive design tested across multiple devices and browsers"
            ]
        ),
        outcome=ProjectOutcome(
            summary="Successfully launched a professional portfolio website that significantly improved online presence and generated measurable business impact through enhanced credibility and lead generation.",
            achievements=[
                "Achieved 95+ Google PageSpeed scores for both mobile and desktop",
                "Implemented comprehensive accessibility features meeting WCAG 2.1 AA standards",
                "Created responsive design working perfectly across all device sizes",
                "Established professional brand identity with consistent visual elements",
                "Generated positive feedback from industry professionals and potential clients"
            ],
            metrics=ProjectMetrics(
                performance_improvement="95+ PageSpeed score, 40% faster load times vs. typical portfolio sites",
                user_engagement="Average session duration increased by 65%",
                scalability="Designed to handle 10,000+ concurrent users",
                uptime="99.9% uptime with automated monitoring",
                response_time="Average page load time under 200ms",
                user_satisfaction="4.9/5 average rating from user feedback"
            ),
            user_feedback=[
                "\"Clean, professional design that clearly showcases technical expertise\" - Industry Professional",
                "\"Fast loading and easy to navigate on mobile devices\" - Potential Client",
                "\"Impressive attention to detail in both design and functionality\" - Fellow Developer"
            ],
            lessons_learned=[
                "Importance of performance optimization for user experience and SEO",
                "Value of comprehensive testing across different devices and browsers",
                "Benefits of server-side rendering for SEO and initial load performance",
                "Significance of accessibility features for broader audience reach"
            ]
        ),
        timeline=[
            ProjectTimeline(
                phase="Planning & Design",
                duration="3 days",
                activities=[
                    "Requirements gathering and competitor analysis",
                    "Design system creation and wireframing",
                    "Technology stack selection and architecture planning"
                ],
                deliverables=[
                    "Project requirements document",
                    "Design system and mockups",
                    "Technical architecture specification"
                ]
            ),
            ProjectTimeline(
                phase="Development",
                duration="2 weeks",
                activities=[
                    "FastAPI backend setup and API development",
                    "Frontend implementation with HTMX and Tailwind",
                    "Database schema design and implementation",
                    "Contact form and email integration"
                ],
                deliverables=[
                    "Fully functional web application",
                    "Responsive design implementation",
                    "Contact form with email processing",
                    "Database and backend APIs"
                ]
            ),
            ProjectTimeline(
                phase="Testing & Optimization",
                duration="4 days",
                activities=[
                    "Performance optimization and caching implementation",
                    "Cross-browser and device testing",
                    "SEO optimization and structured data implementation",
                    "Accessibility testing and improvements"
                ],
                deliverables=[
                    "Performance-optimized application",
                    "SEO-optimized content and metadata",
                    "Accessibility compliance report",
                    "Cross-browser compatibility testing results"
                ]
            ),
            ProjectTimeline(
                phase="Deployment & Launch",
                duration="2 days",
                activities=[
                    "Production environment setup and deployment",
                    "Domain configuration and SSL certificate setup",
                    "Monitoring and analytics implementation",
                    "Final testing and launch preparation"
                ],
                deliverables=[
                    "Live production website",
                    "Monitoring and analytics setup",
                    "Deployment documentation",
                    "Launch and maintenance plan"
                ]
            )
        ]
    ),
    2: Project(
        id=2,
        title="Real-Time Chat API",
        description="High-performance WebSocket-based chat API with real-time messaging",
        long_description="""A scalable real-time chat API built with FastAPI and WebSockets, supporting multiple chat rooms, user authentication, and message persistence. Designed to handle thousands of concurrent connections with horizontal scaling capabilities.""",
        technologies=["Python", "FastAPI", "WebSockets", "Redis", "PostgreSQL", "JWT", "Docker", "Nginx"],
        category=ProjectCategory.API,
        status=ProjectStatus.COMPLETED,
        github_url="https://github.com/Bhardin04/chat-api",
        demo_url="https://chat-demo.brianhardin.info",
        image_url="/static/images/projects/chat-api.svg",
        created_at=datetime(2024, 10, 15),
        duration="4 weeks",
        role="Backend Developer",
        team_size="Solo developer",
        client_type="Enterprise client",
        featured=True,
        features=[
            "Real-time messaging with WebSockets",
            "JWT-based authentication system",
            "Multiple chat room support",
            "Message history and persistence",
            "User presence indicators",
            "Rate limiting and spam protection",
            "Horizontal scaling with Redis",
            "Comprehensive API documentation"
        ],
        challenges=[
            "Handling thousands of concurrent WebSocket connections",
            "Implementing efficient message broadcasting",
            "Designing scalable architecture with Redis",
            "Managing user sessions and presence"
        ],
        problem=ProjectProblem(
            title="Need for Scalable Real-Time Communication Platform",
            description="An enterprise client required a high-performance chat API to support real-time communication for their customer service platform, handling thousands of concurrent users with minimal latency.",
            pain_points=[
                "Existing chat solution couldn't handle high concurrent user loads",
                "Frequent connection drops and message delivery failures",
                "Lack of real-time presence indicators and typing notifications",
                "Difficult to scale horizontally during peak usage periods",
                "No message persistence or chat history functionality"
            ],
            business_impact="Poor chat performance was leading to customer dissatisfaction, increased support tickets, and potential revenue loss due to communication failures during critical sales conversations.",
            target_users=[
                "Customer service representatives",
                "Sales team members",
                "End customers seeking support",
                "System administrators managing chat operations"
            ]
        ),
        solution=ProjectSolution(
            approach="Designed and implemented a high-performance WebSocket-based chat API using FastAPI, Redis for horizontal scaling, and PostgreSQL for message persistence. The solution supports real-time messaging, user presence, and can handle thousands of concurrent connections.",
            key_decisions=[
                "Used FastAPI for high-performance async WebSocket handling",
                "Implemented Redis for message broadcasting and session management",
                "Designed horizontal scaling architecture with load balancing",
                "Used JWT for secure, stateless authentication",
                "Implemented connection pooling and efficient message queuing"
            ],
            architecture="Microservices architecture with FastAPI WebSocket handlers, Redis pub/sub for message broadcasting, PostgreSQL for persistence, and Nginx for load balancing. Docker containers enable easy horizontal scaling.",
            implementation_highlights=[
                "Custom WebSocket connection manager for efficient resource utilization",
                "Redis-based message broadcasting system for multi-server deployment",
                "Advanced rate limiting and spam protection mechanisms",
                "Comprehensive API documentation with interactive examples",
                "Real-time presence indicators and typing notifications"
            ]
        ),
        outcome=ProjectOutcome(
            summary="Delivered a robust, scalable chat API that dramatically improved real-time communication performance, supporting 10x more concurrent users while reducing message delivery latency by 75%.",
            achievements=[
                "Successfully handles 5,000+ concurrent WebSocket connections",
                "Reduced message delivery latency from 500ms to 125ms average",
                "Achieved 99.9% uptime with automated failover mechanisms",
                "Implemented comprehensive rate limiting preventing abuse",
                "Delivered complete API documentation with interactive examples"
            ],
            metrics=ProjectMetrics(
                performance_improvement="75% reduction in message latency, 10x increase in concurrent user capacity",
                user_engagement="40% increase in chat session duration",
                scalability="Supports 5,000+ concurrent connections with horizontal scaling",
                uptime="99.9% uptime with automated monitoring and failover",
                response_time="125ms average message delivery latency",
                user_satisfaction="4.7/5 rating from customer service team"
            ),
            user_feedback=[
                "\"Chat performance is dramatically improved, no more connection drops during peak hours\" - Customer Service Manager",
                "\"The real-time presence indicators have improved our response times significantly\" - Sales Team Lead",
                "\"Finally, a chat system that can handle our Black Friday traffic without issues\" - Operations Director"
            ],
            lessons_learned=[
                "Importance of connection pooling for WebSocket scalability",
                "Value of Redis pub/sub for efficient message broadcasting",
                "Benefits of stateless authentication for horizontal scaling",
                "Critical need for comprehensive rate limiting in real-time systems"
            ]
        ),
        timeline=[
            ProjectTimeline(
                phase="Requirements & Architecture",
                duration="4 days",
                activities=[
                    "Requirements gathering and performance analysis",
                    "Architecture design and technology selection",
                    "Scalability planning and load testing strategy"
                ],
                deliverables=[
                    "Technical requirements document",
                    "System architecture diagram",
                    "Performance benchmarking plan"
                ]
            ),
            ProjectTimeline(
                phase="Core Development",
                duration="2.5 weeks",
                activities=[
                    "FastAPI WebSocket implementation",
                    "Redis integration for message broadcasting",
                    "JWT authentication system",
                    "Database schema and message persistence"
                ],
                deliverables=[
                    "WebSocket chat API with basic functionality",
                    "Authentication and authorization system",
                    "Message persistence and history retrieval",
                    "Redis-based scaling infrastructure"
                ]
            ),
            ProjectTimeline(
                phase="Advanced Features",
                duration="1 week",
                activities=[
                    "User presence and typing indicators",
                    "Rate limiting and spam protection",
                    "Chat room management functionality",
                    "API documentation and testing"
                ],
                deliverables=[
                    "Advanced chat features implementation",
                    "Security and rate limiting systems",
                    "Comprehensive API documentation",
                    "Test suite and performance benchmarks"
                ]
            ),
            ProjectTimeline(
                phase="Testing & Deployment",
                duration="3 days",
                activities=[
                    "Load testing with thousands of concurrent connections",
                    "Security testing and vulnerability assessment",
                    "Production deployment and monitoring setup",
                    "Client training and documentation handover"
                ],
                deliverables=[
                    "Load testing results and performance reports",
                    "Security audit and compliance documentation",
                    "Production deployment with monitoring",
                    "Client training materials and handover"
                ]
            )
        ]
    ),
    3: Project(
        id=3,
        title="Data Analytics Dashboard",
        description="Interactive dashboard for visualizing business metrics and KPIs",
        long_description="""A comprehensive data analytics platform that processes large datasets and provides interactive visualizations for business intelligence. Features real-time data processing, custom chart creation, and automated reporting.""",
        technologies=["Python", "Streamlit", "Pandas", "Plotly", "PostgreSQL", "Celery", "Redis", "Docker"],
        category=ProjectCategory.DATA_SCIENCE,
        status=ProjectStatus.COMPLETED,
        github_url="https://github.com/Bhardin04/analytics-dashboard",
        demo_url="https://analytics.brianhardin.info",
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
            "Responsive design for mobile viewing"
        ],
        challenges=[
            "Processing large datasets efficiently",
            "Creating responsive interactive charts",
            "Implementing real-time data updates",
            "Optimizing query performance"
        ],
        problem=ProjectProblem(
            title="Need for Real-Time Business Intelligence Platform",
            description="A Fortune 500 company struggled with fragmented data sources and static reporting that prevented timely business decisions. Executives needed real-time insights into key performance metrics across multiple departments.",
            pain_points=[
                "Manual report generation taking days instead of minutes",
                "Data silos preventing comprehensive business insights",
                "Static dashboards that couldn't adapt to changing business needs",
                "Lack of real-time visibility into critical performance metrics",
                "Difficulty in identifying trends and anomalies quickly"
            ],
            business_impact="Delayed decision-making was costing the company millions in missed opportunities and inefficient resource allocation across departments.",
            target_users=[
                "C-level executives and senior management",
                "Department heads and team leaders",
                "Business analysts and data scientists",
                "Operations managers and supervisors"
            ]
        ),
        solution=ProjectSolution(
            approach="Built a comprehensive analytics platform using Streamlit for rapid development and Plotly for interactive visualizations. Implemented real-time data processing with Celery and Redis, enabling live dashboard updates and automated report generation.",
            key_decisions=[
                "Chose Streamlit for rapid prototyping and deployment",
                "Used Plotly for interactive, responsive charts",
                "Implemented Celery for background data processing",
                "Used Redis for caching and real-time updates",
                "Designed modular dashboard components for reusability"
            ],
            architecture="Microservices architecture with Streamlit frontend, Pandas for data processing, PostgreSQL for data storage, Celery for async tasks, and Redis for caching. Docker containers enable scalable deployment.",
            implementation_highlights=[
                "Custom dashboard builder allowing users to create personalized views",
                "Real-time data pipeline processing millions of records per hour",
                "Advanced filtering and drill-down capabilities",
                "Automated alert system for threshold breaches",
                "Export functionality supporting multiple formats (PDF, Excel, CSV)"
            ]
        ),
        outcome=ProjectOutcome(
            summary="Delivered a powerful analytics platform that transformed decision-making speed and accuracy, reducing report generation time by 95% while providing real-time insights that enabled proactive business management.",
            achievements=[
                "Reduced report generation time from days to minutes",
                "Enabled real-time monitoring of 500+ KPIs across departments",
                "Achieved 99.8% uptime with automated failover systems",
                "Processed 10M+ data points daily with sub-second query responses",
                "Increased data-driven decision making by 80% across the organization"
            ],
            metrics=ProjectMetrics(
                performance_improvement="95% reduction in report generation time, 80% faster data analysis",
                user_engagement="300% increase in dashboard usage across departments",
                efficiency_gains="60% reduction in manual data processing tasks",
                scalability="Handles 10M+ records daily with linear scaling capability",
                response_time="Sub-second query response for complex analytics",
                user_satisfaction="4.8/5 rating from executive team and analysts"
            ),
            user_feedback=[
                "\"We can now make data-driven decisions in real-time instead of waiting days for reports\" - Chief Operating Officer",
                "\"The interactive dashboards have transformed how we monitor our KPIs\" - VP of Sales",
                "\"Finally, a system that gives us the insights we need when we need them\" - Data Analytics Manager"
            ],
            lessons_learned=[
                "Importance of user-friendly interfaces for executive adoption",
                "Value of real-time data processing for competitive advantage",
                "Benefits of modular dashboard design for scalability",
                "Critical need for robust caching strategies with large datasets"
            ]
        ),
        timeline=[
            ProjectTimeline(
                phase="Discovery & Planning",
                duration="1 week",
                activities=[
                    "Stakeholder interviews and requirements gathering",
                    "Data source analysis and mapping",
                    "Technology evaluation and architecture design"
                ],
                deliverables=[
                    "Requirements specification document",
                    "Data integration plan",
                    "Technical architecture blueprint"
                ]
            ),
            ProjectTimeline(
                phase="Core Development",
                duration="3 weeks",
                activities=[
                    "Data pipeline development and testing",
                    "Dashboard framework implementation",
                    "Interactive visualization components",
                    "User authentication and role management"
                ],
                deliverables=[
                    "Functional data processing pipeline",
                    "Core dashboard application",
                    "Interactive chart library",
                    "Security and access control system"
                ]
            ),
            ProjectTimeline(
                phase="Advanced Features",
                duration="1 week",
                activities=[
                    "Custom dashboard builder implementation",
                    "Automated reporting system",
                    "Alert and notification system",
                    "Export and sharing functionality"
                ],
                deliverables=[
                    "Dashboard builder tool",
                    "Automated report generation",
                    "Alert management system",
                    "Multi-format export capabilities"
                ]
            )
        ]
    ),
    4: Project(
        id=4,
        title="Task Automation Suite",
        description="Python automation tools for streamlining repetitive business processes",
        long_description="""A collection of automation scripts and tools designed to streamline business processes, from data entry to report generation. Features a web interface for managing automated tasks and monitoring execution.""",
        technologies=["Python", "Selenium", "FastAPI", "Celery", "SQLAlchemy", "Pandas", "Schedule"],
        category=ProjectCategory.AUTOMATION,
        status=ProjectStatus.IN_PROGRESS,
        github_url="https://github.com/Bhardin04/automation-suite",
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
            "Web-based management interface"
        ],
        challenges=[
            "Handling dynamic web content with Selenium",
            "Creating reliable error recovery mechanisms",
            "Designing flexible task scheduling system",
            "Managing resource usage efficiently"
        ],
        problem=ProjectProblem(
            title="Elimination of Manual Business Process Bottlenecks",
            description="A consulting firm was losing productivity due to repetitive manual tasks consuming 40% of staff time, including data entry, report generation, and client communication workflows.",
            pain_points=[
                "Staff spending 3-4 hours daily on repetitive data entry tasks",
                "Manual report generation causing delays in client deliverables",
                "Inconsistent data quality due to human error in manual processes",
                "Difficulty scaling operations without proportional staff increases",
                "Time-sensitive tasks often missed due to manual oversight"
            ],
            business_impact="Manual processes were limiting growth potential and reducing billable hours by 40%, directly impacting revenue and client satisfaction.",
            target_users=[
                "Operations managers and coordinators",
                "Administrative staff and assistants",
                "Project managers and team leads",
                "Data analysts and report generators"
            ]
        ),
        solution=ProjectSolution(
            approach="Developed a comprehensive automation platform using Python with web-based management interface. Implemented Selenium for web interactions, Celery for task queuing, and FastAPI for the management dashboard.",
            key_decisions=[
                "Used Selenium for robust web automation capabilities",
                "Implemented Celery for distributed task processing",
                "Built FastAPI dashboard for easy task management",
                "Used SQLAlchemy for flexible task configuration storage",
                "Designed modular automation scripts for reusability"
            ],
            architecture="Event-driven architecture with FastAPI web interface, Celery worker nodes, SQLAlchemy database for configuration, and scheduled task execution with monitoring and alerting.",
            implementation_highlights=[
                "Intelligent error detection and recovery mechanisms",
                "Dynamic task scheduling with dependency management",
                "Real-time monitoring dashboard with execution logs",
                "Configurable automation workflows without code changes",
                "Automated notification system for task status updates"
            ]
        ),
        outcome=ProjectOutcome(
            summary="Successfully automated 80% of repetitive business processes, freeing up 32 hours per week of staff time and improving data accuracy while enabling scalable operations growth.",
            achievements=[
                "Automated 15 critical business processes saving 200+ hours monthly",
                "Reduced data entry errors by 95% through automated validation",
                "Achieved 99.2% automation success rate with robust error handling",
                "Enabled 40% productivity increase across operations team",
                "Created reusable automation framework for future processes"
            ],
            metrics=ProjectMetrics(
                efficiency_gains="80% reduction in manual task time, 40% productivity increase",
                cost_savings="$50,000+ annual savings in operational costs",
                scalability="Platform supports unlimited automation workflows",
                uptime="99.2% automation success rate with automated recovery",
                user_satisfaction="4.6/5 rating from operations team"
            ),
            user_feedback=[
                "\"The automation suite has transformed our daily operations, freeing us to focus on high-value client work\" - Operations Manager",
                "\"No more manual data entry errors and reports are always on time\" - Administrative Coordinator",
                "\"We can now handle 40% more clients without additional staff\" - Managing Partner"
            ],
            lessons_learned=[
                "Importance of robust error handling in automation systems",
                "Value of user-friendly interfaces for non-technical staff",
                "Benefits of modular design for automation scalability",
                "Critical need for comprehensive logging and monitoring"
            ]
        ),
        timeline=[
            ProjectTimeline(
                phase="Analysis & Design",
                duration="1 week",
                activities=[
                    "Process mapping and automation opportunity analysis",
                    "Technology selection and architecture planning",
                    "Stakeholder interviews and requirements gathering"
                ],
                deliverables=[
                    "Process automation roadmap",
                    "Technical specification document",
                    "Implementation timeline and milestones"
                ]
            ),
            ProjectTimeline(
                phase="Core Development",
                duration="4 weeks",
                activities=[
                    "Automation framework development",
                    "Web scraping and data extraction modules",
                    "Task scheduling and monitoring system",
                    "Management dashboard implementation"
                ],
                deliverables=[
                    "Automation execution engine",
                    "Web scraping libraries",
                    "Task management system",
                    "Administrative web interface"
                ]
            ),
            ProjectTimeline(
                phase="Testing & Deployment",
                duration="1 week (ongoing)",
                activities=[
                    "Comprehensive testing and validation",
                    "Production deployment and monitoring",
                    "User training and documentation",
                    "Continuous improvement and optimization"
                ],
                deliverables=[
                    "Production-ready automation suite",
                    "User training materials",
                    "Monitoring and alerting setup",
                    "Maintenance and support documentation"
                ]
            )
        ]
    ),
    5: Project(
        id=5,
        title="E-commerce API Platform",
        description="RESTful API for e-commerce applications with inventory and order management",
        long_description="""A comprehensive e-commerce backend API providing complete functionality for online stores including product management, inventory tracking, order processing, and payment integration.""",
        technologies=["Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Stripe", "JWT", "Docker", "Pytest"],
        category=ProjectCategory.API,
        status=ProjectStatus.COMPLETED,
        github_url="https://github.com/Bhardin04/ecommerce-api",
        demo_url="https://api.store-demo.brianhardin.info/docs",
        image_url="/static/images/projects/ecommerce-api.svg",
        created_at=datetime(2024, 8, 1),
        duration="6 weeks",
        role="Backend Developer",
        team_size="3 developers",
        client_type="Startup e-commerce company",
        featured=True,
        features=[
            "Complete product catalog management",
            "Inventory tracking and alerts",
            "Order processing workflow",
            "Stripe payment integration",
            "User authentication and profiles",
            "Admin dashboard API",
            "Comprehensive test coverage",
            "API documentation with OpenAPI"
        ],
        challenges=[
            "Implementing secure payment processing",
            "Designing efficient inventory management",
            "Creating robust order workflow",
            "Ensuring data consistency across transactions"
        ],
        problem=ProjectProblem(
            title="Scalable E-commerce Backend for Growing Online Marketplace",
            description="A rapidly growing e-commerce startup needed a robust, scalable API platform to support their expanding product catalog and increasing order volume while ensuring secure payment processing and real-time inventory management.",
            pain_points=[
                "Legacy system couldn't handle increasing order volumes during peak sales",
                "Manual inventory management causing overselling and stockouts",
                "Insecure payment processing raising compliance concerns",
                "Lack of real-time data synchronization across multiple sales channels",
                "Difficulty integrating with third-party services and partners"
            ],
            business_impact="System limitations were constraining business growth, causing lost sales during peak periods, and creating customer satisfaction issues due to inventory inaccuracies.",
            target_users=[
                "E-commerce store administrators",
                "Customer service representatives",
                "Inventory managers and warehouse staff",
                "Frontend developers and integrators"
            ]
        ),
        solution=ProjectSolution(
            approach="Designed and built a modern REST API using FastAPI with PostgreSQL for data persistence, Stripe for secure payments, and comprehensive testing. Implemented microservices patterns for scalability and maintainability.",
            key_decisions=[
                "Used FastAPI for high-performance async API development",
                "Implemented SQLAlchemy for flexible database operations",
                "Integrated Stripe for PCI-compliant payment processing",
                "Used JWT tokens for secure stateless authentication",
                "Designed comprehensive test suite with 95%+ coverage"
            ],
            architecture="Microservices architecture with FastAPI REST endpoints, PostgreSQL database with optimized indexes, Redis for caching, and Docker containers for deployment. Stripe handles payment processing with webhook integration.",
            implementation_highlights=[
                "Real-time inventory tracking with automatic low-stock alerts",
                "Atomic transaction handling ensuring data consistency",
                "Comprehensive API documentation with interactive testing",
                "Role-based access control for admin and customer endpoints",
                "Webhook integration for payment and order status updates"
            ]
        ),
        outcome=ProjectOutcome(
            summary="Delivered a robust, scalable e-commerce API platform that enabled 500% growth in order processing capacity while maintaining 99.9% uptime and improving customer satisfaction through accurate inventory management.",
            achievements=[
                "Enabled processing of 10,000+ orders per day with linear scalability",
                "Achieved 99.9% uptime during Black Friday traffic spikes",
                "Reduced inventory discrepancies by 98% through real-time tracking",
                "Implemented PCI-DSS compliant payment processing",
                "Delivered comprehensive API documentation enabling rapid integration"
            ],
            metrics=ProjectMetrics(
                performance_improvement="500% increase in order processing capacity",
                scalability="Linear scaling supporting 10,000+ daily orders",
                uptime="99.9% uptime with automated failover and monitoring",
                response_time="Average API response time under 100ms",
                user_satisfaction="4.9/5 rating from developer integration team"
            ),
            user_feedback=[
                "\"The API documentation is excellent - we integrated our frontend in half the expected time\" - Frontend Development Lead",
                "\"Real-time inventory updates have eliminated our overselling issues completely\" - Operations Manager",
                "\"Payment processing is now rock-solid and PCI compliant\" - Security Team Lead"
            ],
            lessons_learned=[
                "Importance of comprehensive API documentation for developer adoption",
                "Value of atomic transactions for e-commerce data consistency",
                "Benefits of webhook architecture for real-time integrations",
                "Critical need for extensive testing in payment processing systems"
            ]
        ),
        timeline=[
            ProjectTimeline(
                phase="Requirements & Architecture",
                duration="1 week",
                activities=[
                    "Business requirements analysis and API design",
                    "Database schema design and optimization",
                    "Payment integration planning and security assessment"
                ],
                deliverables=[
                    "API specification and endpoint documentation",
                    "Database design and migration scripts",
                    "Security and compliance requirements document"
                ]
            ),
            ProjectTimeline(
                phase="Core API Development",
                duration="3 weeks",
                activities=[
                    "User authentication and authorization system",
                    "Product catalog and inventory management APIs",
                    "Order processing and workflow management",
                    "Payment integration with Stripe webhooks"
                ],
                deliverables=[
                    "Authentication and user management system",
                    "Product and inventory management APIs",
                    "Order processing engine",
                    "Secure payment processing integration"
                ]
            ),
            ProjectTimeline(
                phase="Advanced Features & Testing",
                duration="1.5 weeks",
                activities=[
                    "Admin dashboard API endpoints",
                    "Real-time notifications and webhooks",
                    "Comprehensive test suite development",
                    "Performance optimization and caching"
                ],
                deliverables=[
                    "Admin management API",
                    "Webhook notification system",
                    "Test suite with 95%+ coverage",
                    "Performance-optimized API endpoints"
                ]
            ),
            ProjectTimeline(
                phase="Documentation & Deployment",
                duration="0.5 weeks",
                activities=[
                    "API documentation completion",
                    "Production deployment and monitoring setup",
                    "Load testing and performance validation",
                    "Client training and handover"
                ],
                deliverables=[
                    "Complete API documentation with examples",
                    "Production deployment with monitoring",
                    "Load testing results and capacity planning",
                    "Client integration guide and support materials"
                ]
            )
        ]
    )
}

@router.get("/", response_class=HTMLResponse)
async def projects_list(request: Request):
    projects = list(PROJECTS_DATA.values())
    # Sort by featured first, then by creation date
    projects.sort(key=lambda p: (not p.featured, -(p.created_at.timestamp() if p.created_at else 0)))
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})

@router.get("/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: int):
    project = PROJECTS_DATA.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get related projects (same category, different ID)
    related_projects = [
        p for p in PROJECTS_DATA.values() 
        if p.category == project.category and p.id != project_id
    ][:3]  # Limit to 3 related projects
    
    return templates.TemplateResponse("project_detail.html", {
        "request": request, 
        "project": project,
        "related_projects": related_projects
    })
