"""
Curated Career Roadmap Curriculum derived directly from the official developer roadmaps
(Frontend, Backend, Full Stack, React, Node.js, Python, TypeScript, Java, Spring Boot,
SQL, PostgreSQL, System Design, AI & Data Science, DevOps, Mobile, QA, Cyber Security).

Used to enforce that all student guidance, next courses of action, and paths forward
are strictly grounded in this curriculum.
"""

from typing import Dict, List, Any


ROADMAP_TRACKS: Dict[str, Dict[str, Any]] = {
    "Frontend": {
        "title": "Frontend Developer Roadmap",
        "reference": "https://roadmap.sh/frontend (Page 31 of Roadmap Guide)",
        "checkpoints": [
            {
                "checkpoint": "Checkpoint 1: Web & Language Fundamentals",
                "topics": ["Internet Basics (HTTP, DNS, Browsers)", "Semantic HTML5, Forms, Accessibility & SEO", "CSS3 Layouts, Flexbox, Responsive Design", "JavaScript ES6+ (DOM Manipulation, Fetch API, Async/Await, Closures)"],
                "action": "Build 2 semantic, mobile-responsive web pages and implement dynamic DOM manipulation with vanilla JavaScript."
            },
            {
                "checkpoint": "Checkpoint 2: Version Control & Modern Package Management",
                "topics": ["Git & GitHub Workflows (Branching, PRs)", "Package Managers (npm, pnpm, yarn)", "Build Tools (Vite, npm scripts)"],
                "action": "Set up a structured repository on GitHub with Vite build bundling and clean git commit history."
            },
            {
                "checkpoint": "Checkpoint 3: Component-Driven Framework & Styling",
                "topics": ["React (Functional Components, Hooks: useState, useEffect, Custom Hooks)", "Component State Management (Context, Zustand)", "Modern CSS (Tailwind CSS, CSS Modules)"],
                "action": "Develop a multi-component interactive application utilizing React Hooks and responsive Tailwind CSS layout."
            },
            {
                "checkpoint": "Checkpoint 4: State, Routing, APIs & Web Security",
                "topics": ["Client Routing (React Router)", "API Calls (REST APIs, Axios / React Query)", "Web Security Basics (CORS, HTTPS, OWASP Security Risks)"],
                "action": "Integrate asynchronous backend REST endpoints with caching and robust error boundary handling."
            },
            {
                "checkpoint": "Checkpoint 5: Testing, SSR & Production Optimization",
                "topics": ["Testing Frameworks (Jest, React Testing Library, Vitest)", "Server-Side Rendering (Next.js)", "Performance (Lighthouse, Core Web Vitals)"],
                "action": "Add unit tests for core interactive logic and audit with Lighthouse for score > 90."
            }
        ]
    },
    "Backend": {
        "title": "Backend Developer Roadmap",
        "reference": "https://roadmap.sh/backend (Page 30 of Roadmap Guide)",
        "checkpoints": [
            {
                "checkpoint": "Checkpoint 1: Core Language & OS Foundations",
                "topics": ["Backend Language (Python, Node.js, Java, or Go)", "POSIX Basics, Terminal Usage, Linux Commands", "Threads, Concurrency & Process Management"],
                "action": "Write modular backend scripts and automate command-line data processing in a Linux/terminal environment."
            },
            {
                "checkpoint": "Checkpoint 2: Relational & Document Databases",
                "topics": ["PostgreSQL / MySQL (ACID, Normalization, Indexes, Joins)", "MongoDB / Redis (Key-Value & Document caching)", "Database Constraints & Query Optimization"],
                "action": "Design normalized database schemas in PostgreSQL with indexes and execute complex analytical JOIN queries."
            },
            {
                "checkpoint": "Checkpoint 3: RESTful & Structured APIs",
                "topics": ["RESTful Design & HTTP Methods", "JSON APIs, OpenAPI / Swagger Specs", "Authentication (JWT, OAuth2, Session Auth)"],
                "action": "Build a secure RESTful API service featuring JWT authentication, input validation, and auto-generated API documentation."
            },
            {
                "checkpoint": "Checkpoint 4: Caching, Message Queues & Microservices",
                "topics": ["Caching Strategies (Redis, Cache-Aside)", "Message Brokers (RabbitMQ, Apache Kafka)", "Architectural Patterns (Microservices, Monolith to Distributed)"],
                "action": "Implement a Redis caching layer and asynchronous task processing using background queues."
            },
            {
                "checkpoint": "Checkpoint 5: Testing, CI/CD & Observability",
                "topics": ["Unit & Integration Testing (PyTest, Jest, JUnit)", "CI/CD Pipelines (GitHub Actions)", "Observability (Structured Logging, Metrics, Monitoring)"],
                "action": "Configure GitHub Actions CI/CD to run automated test suites on every pull request."
            }
        ]
    },
    "Full Stack": {
        "title": "Full Stack Developer Roadmap",
        "reference": "https://roadmap.sh/full-stack (Page 28 of Roadmap Guide)",
        "checkpoints": [
            {
                "checkpoint": "Checkpoint 1: Static Webpages & Interactivity",
                "topics": ["HTML5 & CSS3 Essentials", "JavaScript Fundamentals & DOM Interactivity", "npm Package Management"],
                "action": "Construct a clean, responsive static web interface with interactive DOM components."
            },
            {
                "checkpoint": "Checkpoint 2: Collaborative Work & Frontend Frameworks",
                "topics": ["Git & GitHub Workflows", "React & Tailwind CSS Component Architecture", "Client State Management"],
                "action": "Build a modular Single Page Application in React with Tailwind CSS and host on GitHub."
            },
            {
                "checkpoint": "Checkpoint 3: Backend Development & Database CRUD",
                "topics": ["Node.js / Express or Python / FastAPI", "PostgreSQL Relational Schema & ORM", "CRUD Endpoints & Error Handling"],
                "action": "Implement complete CRUD server endpoints wired directly to a PostgreSQL database."
            },
            {
                "checkpoint": "Checkpoint 4: Complete App Integration & Security",
                "topics": ["JWT Authentication & Authorization", "RESTful API Integration between React & Backend", "Redis Caching"],
                "action": "Unify frontend and backend into an authenticated end-to-end full stack application."
            },
            {
                "checkpoint": "Checkpoint 5: Deployment, CI/CD & Cloud Basics",
                "topics": ["Linux Basics & Basic AWS (EC2, S3)", "Docker Containerization", "GitHub Actions CI/CD & Monitoring"],
                "action": "Containerize the full stack app using Docker and deploy with automated CI/CD pipeline."
            }
        ]
    },
    "Python": {
        "title": "Python Developer Roadmap",
        "reference": "https://roadmap.sh/python (Page 6 of Roadmap Guide)",
        "checkpoints": [
            {
                "checkpoint": "Checkpoint 1: Python Fundamentals & Data Structures",
                "topics": ["Syntax, Variables, Conditionals, Loops", "Lists, Tuples, Sets, Dictionaries", "Built-in Functions, Type Casting & Exception Handling"],
                "action": "Master Python core collections and implement robust exception handling across data scripts."
            },
            {
                "checkpoint": "Checkpoint 2: Data Structures, Algorithms & OOP",
                "topics": ["Arrays, Linked Lists, Hash Tables, Binary Search Trees", "Classes, Inheritance, Dunder Methods", "Decorators, Iterators, Generators, RegEx"],
                "action": "Write object-oriented Python classes and apply custom decorators and generator expressions."
            },
            {
                "checkpoint": "Checkpoint 3: Backend Web Frameworks",
                "topics": ["FastAPI (Asynchronous, Pydantic Type Validation)", "Django / Flask (MVC/MTV, ORM)", "Package Management (pip, Poetry, virtualenv)"],
                "action": "Build a high-performance REST API with FastAPI utilizing Pydantic data schemas."
            },
            {
                "checkpoint": "Checkpoint 4: Testing & Code Quality",
                "topics": ["Unit Testing with pytest & unittest", "Mocking & Fixtures", "Type Hinting & Static Checking (mypy)"],
                "action": "Implement pytest test coverage with test fixtures and enforce mypy type safety."
            }
        ]
    },
    "React": {
        "title": "React Developer Roadmap",
        "reference": "https://roadmap.sh/react (Page 13 of Roadmap Guide)",
        "checkpoints": [
            {
                "checkpoint": "Checkpoint 1: React Fundamentals & JSX",
                "topics": ["Functional Components, JSX, Props vs State", "Conditional Rendering, Lists & Keys", "Component Lifecycle & Rendering Mechanics"],
                "action": "Develop clean functional components strictly utilizing declarative JSX and proper key props."
            },
            {
                "checkpoint": "Checkpoint 2: Hooks & Custom Hooks",
                "topics": ["useState, useEffect", "useCallback, useMemo, useRef", "Writing Custom Reusable Hooks"],
                "action": "Encapsulate business logic into reusable custom React hooks with optimized render performance."
            },
            {
                "checkpoint": "Checkpoint 3: Routing, State Management & Forms",
                "topics": ["React Router", "State Management (Context API, Zustand, Redux Toolkit)", "React Hook Form"],
                "action": "Implement client-side multi-page routing with global state management and validated forms."
            },
            {
                "checkpoint": "Checkpoint 4: Testing, Next.js & Production Architecture",
                "topics": ["Jest, React Testing Library, Vitest", "Next.js SSR/SSG Framework", "Component Libraries (Tailwind, Radix UI)"],
                "action": "Write component interaction tests using React Testing Library and explore Next.js Server Components."
            }
        ]
    },
    "Data & AI": {
        "title": "AI & Data Scientist Roadmap",
        "reference": "https://roadmap.sh/ai-data-scientist (Page 25 of Roadmap Guide)",
        "checkpoints": [
            {
                "checkpoint": "Checkpoint 1: Mathematics & Statistics",
                "topics": ["Linear Algebra & Calculus for ML", "Probability Distributions & Hypothesis Testing", "A/B Testing & Statistical Inference"],
                "action": "Apply statistical hypothesis testing and matrix mathematics to dataset verification."
            },
            {
                "checkpoint": "Checkpoint 2: Python Data Engineering & EDA",
                "topics": ["Python Programming, Data Structures & Algorithms", "SQL Querying & Aggregations", "Pandas, NumPy & Visualization (Seaborn, Matplotlib)"],
                "action": "Perform thorough Exploratory Data Analysis (EDA) on real-world datasets with Pandas and Seaborn."
            },
            {
                "checkpoint": "Checkpoint 3: Classical Machine Learning",
                "topics": ["Supervised Learning (Regression, Classification, Decision Trees)", "Unsupervised Learning (Clustering, PCA)", "Scikit-Learn, Model Evaluation & Cross-Validation"],
                "action": "Train, tune, and evaluate machine learning models using Scikit-Learn pipelines."
            },
            {
                "checkpoint": "Checkpoint 4: Deep Learning & MLOps",
                "topics": ["Neural Networks, CNNs, Transformers (Attention Is All You Need)", "PyTorch / TensorFlow", "MLOps, Model Deployment & CI/CD"],
                "action": "Fine-tune a neural model in PyTorch and package it into a deployable inference API."
            }
        ]
    },
    "SQL & Databases": {
        "title": "SQL & Relational Database Roadmap",
        "reference": "https://roadmap.sh/sql (Page 5 & Page 27 of Roadmap Guide)",
        "checkpoints": [
            {
                "checkpoint": "Checkpoint 1: Basic SQL Syntax & DDL/DML",
                "topics": ["Data Types, Operators", "CREATE, ALTER, DROP, TRUNCATE (DDL)", "SELECT, INSERT, UPDATE, DELETE (DML)"],
                "action": "Set up relational schemas with primary and foreign key data constraints."
            },
            {
                "checkpoint": "Checkpoint 2: Aggregate Queries & JOINs",
                "topics": ["GROUP BY, HAVING, COUNT, SUM, AVG", "INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN", "Subqueries & Correlated Subqueries"],
                "action": "Write multi-table relational queries combining JOINs, aggregate filters, and grouping."
            },
            {
                "checkpoint": "Checkpoint 3: Advanced SQL Functions & Indexing",
                "topics": ["Window Functions (ROW_NUMBER, RANK, DENSE_RANK)", "CTEs (Common Table Expressions)", "Indexes (B-Tree, Query Optimization, EXPLAIN)"],
                "action": "Optimize query execution plans using B-Tree indexing and analytical Window Functions."
            },
            {
                "checkpoint": "Checkpoint 4: Transactions & Data Integrity",
                "topics": ["ACID Principles", "Transactions (BEGIN, COMMIT, ROLLBACK)", "Stored Procedures, Triggers & Security"],
                "action": "Implement transactional safety ensuring ACID guarantees across concurrent updates."
            }
        ]
    },
    "System Design": {
        "title": "System Design & Architecture Roadmap",
        "reference": "https://roadmap.sh/system-design (Page 4 of Roadmap Guide)",
        "checkpoints": [
            {
                "checkpoint": "Checkpoint 1: Core System Design Principles",
                "topics": ["Performance vs Scalability", "Latency vs Throughput", "CAP Theorem (Consistency vs Availability)"],
                "action": "Analyze trade-offs between consistency and partition tolerance for high-scale apps."
            },
            {
                "checkpoint": "Checkpoint 2: Load Balancing, Networking & Caching",
                "topics": ["Load Balancers (Layer 4 vs Layer 7)", "CDN & Reverse Proxies", "Caching Strategies (Cache-Aside, Write-Through, Redis)"],
                "action": "Design multi-tier caching architectures to alleviate database read pressure."
            },
            {
                "checkpoint": "Checkpoint 3: Database Scaling & Asynchronism",
                "topics": ["Database Sharding, Replication, Federation", "Message Queues (Kafka, RabbitMQ)", "Asynchronous Decoupling & Backpressure"],
                "action": "Architect an event-driven decoupled architecture using distributed message brokers."
            }
        ]
    },
    "DevOps": {
        "title": "DevOps Engineer Roadmap",
        "reference": "https://roadmap.sh/devops (Page 29 of Roadmap Guide)",
        "checkpoints": [
            {
                "checkpoint": "Checkpoint 1: Linux & Networking Foundations",
                "topics": ["Terminal Mastery (Bash, SSH, Permissions)", "Networking Protocols (HTTP, DNS, SSL/TLS, OSI Model)", "Git Version Control"],
                "action": "Configure a secure remote Linux server with SSH keys, firewall, and reverse proxy."
            },
            {
                "checkpoint": "Checkpoint 2: Containers & Orchestration",
                "topics": ["Docker (Images, Containers, Multi-Stage Builds, Docker Compose)", "Kubernetes Fundamentals (Pods, Deployments, Services)"],
                "action": "Containerize microservices with Docker and deploy them via Kubernetes manifests."
            },
            {
                "checkpoint": "Checkpoint 3: CI/CD & Infrastructure as Code",
                "topics": ["GitHub Actions / GitLab CI Pipelines", "Terraform (IaC, State Management, Cloud Provisioning)", "AWS / Cloud Providers"],
                "action": "Automate cloud infrastructure provisioning with Terraform and deploy with GitHub Actions."
            }
        ]
    }
}


def get_curriculum_track_for_role(category_str: str, keywords_text: str = "") -> Dict[str, Any]:
    """
    Selects the best matching roadmap track from the PDF based on role category and text keywords.
    """
    text = (category_str + " " + keywords_text).lower()

    if "front" in text or "react" in text or "ui" in text:
        return ROADMAP_TRACKS["Frontend"]
    elif "data" in text or "machine learning" in text or "ai" in text:
        return ROADMAP_TRACKS["Data & AI"]
    elif "python" in text:
        return ROADMAP_TRACKS["Python"]
    elif "sql" in text or "database" in text or "postgres" in text:
        return ROADMAP_TRACKS["SQL & Databases"]
    elif "devops" in text or "cloud" in text:
        return ROADMAP_TRACKS["DevOps"]
    elif "full" in text:
        return ROADMAP_TRACKS["Full Stack"]
    elif "system" in text or "architect" in text:
        return ROADMAP_TRACKS["System Design"]
    else:
        return ROADMAP_TRACKS["Backend"]
