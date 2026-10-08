# ft_transcendence

> **Tactyx: TFT statistics, analytics and social platform**

*This project has been created as part of the 42 curriculum by sservant, nbodin, antbonin and julcleme.*

## Overview

**Tactyx** is a full-stack web application dedicated to **Teamfight Tactics (TFT)**.

The application provides players with a centralized platform to explore TFT statistics, analyze game data, search for players and game content, communicate with other users, and interact with an AI-powered assistant capable of answering questions about TFT.

The project combines a modern frontend and backend architecture with persistent data storage, OAuth authentication, real-time communication, advanced analytics, 3D visualization, internationalization, data import/export, and a Retrieval-Augmented Generation (RAG) system.

The goal was not only to build a functional TFT statistics viewer, but also to demonstrate the ability to design and integrate a complete web application covering frontend development, backend architecture, databases, authentication, observability, data processing, and user interaction.

---

# Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [TFT Statistics](#tft-statistics)
- [User Features](#user-features)
- [Search](#search)
- [Analytics Dashboard](#analytics-dashboard)
- [AI / RAG Assistant](#ai--rag-assistant)
- [3D Visualization](#3d-visualization)
- [Real-Time Features](#real-time-features)
- [Internationalization](#internationalization)
- [Data Import and Export](#data-import-and-export)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Database](#database)
- [Monitoring and Observability](#monitoring-and-observability)
- [42 Modules](#42-modules)
- [Project Management](#project-management)
- [Team](#team)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Security](#security)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [AI Usage](#ai-usage)
- [Resources](#resources)
- [Credits](#credits)

---

# Key Features

## TFT Statistics

The core of the application is a comprehensive TFT statistics viewer inspired by platforms such as MetaTFT.

Users can explore statistics for:

- Units / champions
- Items
- Augments
- Traits
- Players
- Other TFT-related game data

Depending on the selected data, users can access information such as:

- Win rate
- Pick / play rate
- Average placement
- Cost
- Usage statistics
- Ranking information
- Other aggregated statistics

The application is designed to transform raw TFT data into information that is easy to explore and understand.

---

## User Features

The application provides a complete user system including:

- Account creation
- Authentication
- OAuth 2.0 authentication
- User profiles
- Avatar upload
- Default avatars
- Online/offline status
- Friends
- Friend management
- User search
- User activity statistics
- Real-time chat

Each user has a dedicated profile page containing their publicly available information and relevant activity/statistical data.

---

## Search

The application provides an advanced search system covering both users and TFT content.

Users can search for:

- Players
- Units
- Items
- Augments
- Traits
- Other indexed TFT data

The search system supports:

- Filtering
- Sorting
- Pagination
- Multiple search criteria

This allows users to quickly find the information they are looking for even when working with a large dataset.

---

## Analytics Dashboard

One of the main features of the project is an advanced statistics and analytics dashboard.

The dashboard provides interactive data visualizations including:

- Line charts
- Statistical summaries
- Comparative visualizations

Users can customize the displayed data through:

- Date ranges
- Filters
- Search criteria
- Other configurable parameters

The dashboard also supports **real-time data updates**, allowing statistics to change without requiring a complete page reload.

### Data Export

Analytics can be exported for further analysis or external use.
User can export `units`, `items`, `traits` and `augments` and their stats.

Supported formats include:

- JSON

---

### Team Builder

Team Builder can be used to help craft teams and view their statistics in realtime. 
Teams can be also imported and exported through the upper buttons.

Supported formats include:

- XML
- JSON

---

# AI / RAG Assistant

The application includes a complete **Retrieval-Augmented Generation (RAG)** system designed around TFT-related information.

Users can interact with the assistant through the application's chat interface.

The chatbot can be invoked using the `/` prefix before a question.

For example:

```
/What are the strongest traits this patch?
```


The RAG pipeline works by:

1. Receiving the user's question.
2. Processing and understanding the query.
3. Searching the relevant TFT dataset.
4. Retrieving the most relevant contextual information.
5. Providing the retrieved context to the language model.
6. Generating an answer based on the retrieved information.

This approach allows the assistant to answer questions using the project's TFT dataset rather than relying exclusively on the model's general knowledge.

The system is particularly useful for questions involving:

- Units
- Traits
- Items
- Augments
- Statistics
- Gameplay information
- Comparative questions

---

# 3D Visualization

The application includes an interactive 3D environment built using a dedicated 3D graphics library.

The 3D interface provides:

- An immersive environment
- Interactive elements
- Advanced rendering
- Camera interaction
- User-controlled navigation
- Performance-oriented rendering

The 3D component demonstrates how complex graphical interfaces can be integrated into a statistics-oriented web application without compromising the rest of the user experience.

---

# Real-Time Features

Several parts of the application rely on real-time communication.

Real-time functionality is used for:

- Chat messages
- Online/offline status
- Analytics updates
- User activity
- Other live application events

This allows the application to provide a more dynamic experience without requiring users to manually refresh the page.

---

# Internationalization

The application supports multiple languages through an internationalization system.

At least three complete languages are supported.

The interface includes a language switcher allowing users to change the application language.

All user-facing text is designed to be translatable, including:

- Navigation
- Buttons
- Forms
- Error messages
- Notifications
- Dashboard labels
- Chat interface
- User management pages
- Search interface

This ensures that adding or maintaining translations does not require modifying application logic.

---

# Data Import and Export

The application provides tools for importing and exporting application data.

## Export

Data can be exported in multiple formats, including:

- JSON
- CSV
- XML

depending on the type of data being exported.

## Import

Imported data is validated before being inserted into the application.

The import system handles:

- Data validation
- Invalid entries
- Formatting errors
- Duplicate or conflicting data
- Bulk operations

Bulk operations allow large amounts of data to be processed efficiently instead of requiring individual operations for every record.

---

# Technology Stack

## Frontend

The frontend is implemented using:

- **[Frontend Framework]**
- **[Frontend Language]**
- **[CSS / UI technology]**
- **[Charting library]**
- **[3D library]**
- **[Internationalization library]**

The frontend is responsible for:

- Rendering the user interface
- User authentication flows
- TFT statistics visualization
- Search
- User profiles
- Friends
- Chat
- Analytics dashboards
- Data import/export interfaces
- 3D visualization
- Internationalization
- API communication

The interface is built around reusable components following a custom design system.

---

## Backend

The backend is implemented using:

- **[Backend Framework]**
- **[Backend Language]**
- **[ORM]**
- **[WebSocket technology]**
- **[Authentication libraries]**

The backend is responsible for:

- REST/API endpoints
- Authentication
- OAuth 2.0
- Authorization
- User management
- Friend management
- Chat
- TFT data processing
- Statistics
- Search
- Data import/export
- RAG services
- Database access
- Validation
- Error handling
- Metrics

---

## Database

The application uses:

**PostgreSQL**

An ORM is used to interact with the database, providing:

- Type-safe database access
- Model definitions
- Relationships
- Migrations
- Query abstraction
- Validation at the application layer

---

## Infrastructure and Monitoring

The project uses:

- Docker
- Docker Compose
- Prometheus
- Grafana

Prometheus collects application metrics while Grafana provides monitoring dashboards and alerting.

---

# Architecture

The application follows a modular full-stack architecture.


┌──────────────────────┐ │ Web Client │ │ Frontend │ └──────────┬───────────┘ │ HTTP / WebSocket │ ▼ ┌──────────────────────┐ │ Backend │ │ API / Services │ └───────┬───────┬──────┘ │ │ ┌────────────┘ └─────────────┐ ▼ ▼ ┌────────────────┐ ┌────────────────┐ │ PostgreSQL │ │ RAG / AI │ │ Database │ │ System │ └────────────────┘ └────────────────┘ │ │ Metrics ▼ ┌────────────────┐ │ Prometheus │ └───────┬────────┘ │ ▼ ┌────────────────┐ │ Grafana │ └────────────────┘



---

# Database

The database uses a relational structure designed around users, TFT data, statistics, and social functionality.

## Main Entities

Depending on the current implementation, the main entities include:

- Users
- Profiles
- Friends / friendships
- Messages
- Units
- Items
- Augments
- Traits
- TFT statistics
- Player statistics
- Activity records
- Imported data
- Other application-specific entities

## User Relationships

Users can:

- Have a profile
- Upload an avatar
- Add other users as friends
- Remove friends
- View their friends
- View online status
- Exchange messages
- Generate activity data

## TFT Relationships

TFT entities are related to their corresponding statistics and gameplay information.

For example:


┌──────────────┐ │ Unit │ └──────┬───────┘ │ ▼ ┌──────────────┐ │ Statistics │ └──────┬───────┘ │ ┌──────────┴──────────┐ ▼ ▼ Win Rate Play Rate



The actual schema should be generated from the project's ORM models and migrations.

---

# Monitoring and Observability

The application includes a complete monitoring stack using **Prometheus and Grafana**.

## Prometheus

Prometheus collects application metrics such as:

- Request metrics
- Application performance
- System metrics
- Database-related metrics
- Custom application metrics

Exporters and integrations are configured where appropriate to expose additional metrics.

## Grafana

Custom Grafana dashboards provide visual monitoring of the application.

The dashboards allow developers to monitor:

- Application health
- Request rates
- Errors
- Response times
- Resource usage
- Other relevant metrics

## Alerting

Alerting rules are configured to detect important application or infrastructure problems.

Examples include:

- High error rates
- Service failures
- Abnormal resource usage
- Performance degradation

Grafana access is secured to prevent unauthorized access to monitoring information.

---

# 42 Modules

The project implements a large number of optional modules from the **ft_transcendence** subject.

## Major Modules

### 1. Full-Stack Framework — 2 points

The project uses a modern framework on both the frontend and backend.

The frontend framework is responsible for building the interactive TFT interface, while the backend framework handles API endpoints, business logic, authentication, database operations, and other server-side functionality.

**Implemented:**

- Frontend framework
- Backend framework
- Framework-based application architecture

**Why we chose it:**

Using frameworks allowed us to structure a large application into reusable modules while providing established solutions for routing, state management, validation, API handling, and application lifecycle management.

---

### 2. Advanced Analytics Dashboard — 2 points

The application provides an advanced analytics dashboard dedicated to TFT statistics.

**Implemented:**

- Interactive charts and graphs
- Line charts
- Bar charts
- Pie charts
- Real-time data updates
- Data export
- Custom date ranges
- Filters

The dashboard transforms large amounts of TFT data into interactive visualizations that help users understand trends and compare statistics.

---

### 3. Monitoring System with Prometheus and Grafana — 2 points

The project includes a complete monitoring infrastructure.

**Implemented:**

- Prometheus metrics collection
- Exporters and integrations
- Custom Grafana dashboards
- Alerting rules
- Secured Grafana access

This allows the team to monitor the application's health and performance rather than relying exclusively on application logs.

---

### 4. User Interaction System — 2 points

Users can interact with one another through a complete social system.

**Implemented:**

- User profiles
- Friends
- Add/remove friends
- Friends list
- Online status
- Real-time chat

This module turns the application from a simple statistics viewer into a social platform for TFT players.

---

### 5. Advanced 3D Graphics — 2 points

The application contains an interactive 3D environment using a dedicated 3D graphics library.

**Implemented:**

- Immersive 3D environment
- Advanced rendering
- User interaction
- Camera controls
- Performance optimization

The 3D environment provides an additional interactive dimension to the application.

---

### 6. Complete RAG System — 2 points

A complete Retrieval-Augmented Generation pipeline is integrated into the application.

**Implemented:**

- Large TFT information dataset
- User questions
- Context retrieval
- Relevant information selection
- Context-aware response generation
- Integration with the application's chat interface

The RAG system enables users to ask natural-language questions about TFT and receive answers grounded in the project's data.

---

## Minor Modules

### 7. ORM — 1 point

An ORM is used for application database interactions.

It provides:

- Database models
- Relationships
- Queries
- Migrations
- Type-safe database access

---

### 8. OAuth 2.0 Authentication — 1 point

The application supports remote authentication using OAuth 2.0.

Users can authenticate through:

- Email/password authentication
- **42 OAuth**

The OAuth flow securely delegates authentication to the remote identity provider and associates the authenticated account with a local user profile.

---

### 9. Data Import and Export — 1 point

The application supports data import and export.

**Implemented:**

- JSON export
- CSV export
- XML export
- Validated imports
- Bulk operations

This functionality is particularly useful for managing the large datasets used by the TFT statistics system.

---

### 10. Multi-Language Support — 1 point

The application supports at least three languages.

**Implemented:**

- i18n system
- Three complete translations
- Language switcher
- Translatable user-facing content

---

### 11. Standard User Management — 2 points

The project implements a complete user management system.

**Implemented:**

- User profiles
- Avatar upload
- Default avatar
- Friends
- Online status
- Profile pages

Users can view their own profile and other users' public information.

> **Remaining improvement:** profile information editing can be added/completed if required by the final evaluation.

---

### 12. Advanced Search — 1 point

The application provides an advanced search system.

**Implemented:**

- Filters
- Sorting
- Pagination
- Search across players and TFT content

This is especially important because the application operates on a large dataset.

---

### 13. User Activity Analytics — 1 point

The application provides analytics about user activity.

The dashboard can be used to visualize relevant activity and usage information, helping users understand their interaction with the platform.

---

### 14. Custom Design System — 1 point

A custom-made design system was developed for the application.

It includes:

- Custom color palette
- Typography
- Icons
- Reusable UI components
- Consistent spacing
- Consistent interaction patterns
- Responsive layouts

The project contains more than the required **10 reusable components**.

---

# Module Point Calculation


| Module | Type | Points |
| --- | --- | --- |
| Full-stack framework | Major | +2 |
| Advanced analytics dashboard | Major | +2 |
| Prometheus + Grafana monitoring | Major | +2 |
| User interaction / social system | Major | +2 |
| Advanced 3D graphics | Major | +2 |
| Complete RAG system | Major | +2 |
| ORM | Minor | +1 |
| OAuth 2.0 | Minor | +1 |
| Data import/export | Minor | +1 |
| Multi-language support | Minor | +1 |
| User management | Major | +2 |
| Advanced search | Minor | +1 |
| User activity analytics | Minor | +1 |
| Custom design system | Minor | +1 |
| **Total** |  | **23** |

> The final score should be adjusted according to the exact modules accepted by the 42 evaluation and the exact implementation present in the final repository.

---

# Project Management

## Work Organization

Development was divided into several areas:

- Frontend development
- Backend development
- Database design
- TFT data processing
- Authentication
- OAuth
- Real-time communication
- Analytics
- RAG / AI
- 3D graphics
- Monitoring
- Internationalization
- Testing
- Deployment
- Documentation

Tasks were distributed between team members according to their responsibilities and technical interests.

---

## Development Workflow

Our development workflow consisted of:

1. Creating an issue describing the task.
2. Assigning the issue to one or more team members.
3. Creating a dedicated Git branch.
4. Implementing the feature.
5. Testing the implementation.
6. Opening a pull request.
7. Reviewing the changes.
8. Fixing review feedback.
9. Merging the completed work.

---

## Project Management Tools

- **Git** — version control.
- **GitHub** — repository hosting and collaboration.
- **GitHub Issues** — task tracking and bug reports.
- **GitHub Projects / Trello** — project planning.
- **Discord / Slack** — team communication.
- **Docker** — reproducible development and deployment environments.

---

# Team

The project was developed collaboratively by four students.

| Member | Login | Role |
| --- | --- | --- |
| Sacha Servanton | `sservant` | Project Manager / Developer |
| Nathan Bodin | `nbodin` | Product Owner / Developer |
| Antoine Bonin | `antbonin` | Tech Lead / Developer |
| Jules Clement Massonnat | `julcleme` | Developer |

## Product Owner

The Product Owner was responsible for:

- Defining functional requirements
- Prioritizing features
- Maintaining the product vision
- Ensuring that development remained aligned with project objectives

## Project Manager

The Project Manager was responsible for:

- Coordinating the team
- Organizing work
- Tracking progress
- Managing deadlines
- Identifying blockers
- Facilitating communication

## Tech Lead

The Tech Lead was responsible for:

- Technical architecture
- Major technical decisions
- Code organization
- Technical consistency
- Integration between application components

## Developers

All developers contributed to:

- Feature implementation
- Bug fixing
- Testing
- Code reviews
- Integration
- Documentation

---

# Installation

## Prerequisites

Make sure the following tools are installed:

- Git
- Docker
- Docker Compose
- Node.js — if required by the project
- npm / pnpm / yarn — depending on the project
- [Other required runtime]
- [Other required dependency]

Check your installation:


git --version
docker --version
docker compose version
node --version
npm --version


---

## Clone the Repository


git clone <repository-url>
cd <repository-directory>


---

## Environment Configuration

Create the environment file:


cp .env.example .env


Configure the required variables.

Example:


DATABASE_URL=
JWT_SECRET=
OAUTH_CLIENT_ID=
OAUTH_CLIENT_SECRET=
OAUTH_CALLBACK_URL=

# RAG / AI configuration
AI_API_KEY=

# Monitoring
GRAFANA_USER=
GRAFANA_PASSWORD=


The exact variables depend on the final project configuration.

**Never commit secrets or production credentials to the repository.**

---

# Running with Docker

Build and start the application:


docker compose up --build


To run in detached mode:


docker compose up -d --build


To stop the application:


docker compose down


---

# Running Without Docker

If local execution is supported:

### Backend


cd backend
[installation command]
[start command]


### Frontend


cd frontend
[installation command]
[start command]


The application will then be available at:


Frontend: http://localhost:[PORT]
Backend:  http://localhost:[PORT]


---

# Usage

1. Open the application in your browser.
2. Create an account or authenticate using OAuth.
3. Complete your profile.
4. Browse TFT statistics.
5. Search for players, units, items, augments or traits.
6. Use filters, sorting and pagination to refine results.
7. Open the analytics dashboard.
8. Select a date range and statistics filters.
9. Explore interactive charts.
10. Export data when needed.
11. Add other users as friends.
12. Chat with other users in real time.
13. Use `/` in chat to ask the TFT assistant a question.
14. Explore the interactive 3D environment.
15. Change the application language using the language switcher.

---

# Testing

Testing was performed throughout development.

Testing included:

- Unit testing
- Integration testing
- API testing
- Authentication testing
- OAuth testing
- Database testing
- WebSocket testing
- Search testing
- Import/export validation
- RAG testing
- Analytics testing
- Manual browser testing
- Responsive interface testing

Run the test suite with:


[test command]


---

# Security

Security was considered throughout the development of the application.

Implemented security measures include:

- Password hashing
- Authentication
- OAuth 2.0
- Authorization
- Input validation
- Server-side validation
- Environment-based secret management
- Protected API endpoints
- Database access controls
- Secured monitoring access
- Validation of imported data

Sensitive credentials such as API keys, OAuth secrets and database credentials are stored outside of the source code.

---

# Known Limitations

The current version may have limitations depending on the final deployment and dataset.

Potential limitations include:

- TFT data depends on the availability and freshness of the underlying data source.
- Some statistics may be limited by the available historical data.
- AI-generated answers depend on the quality and coverage of the retrieved context.
- Large datasets can increase processing and storage requirements.
- 3D rendering performance depends on the user's hardware and browser.
- Some user profile fields may not yet be editable.

---

# Future Improvements

Possible future improvements include:

- More TFT statistics
- More historical data
- Patch-to-patch comparison
- More advanced player analytics
- Team composition analysis
- Composition recommendations
- Improved AI recommendations
- More RAG sources
- Improved RAG retrieval
- More detailed player profiles
- Additional social features
- Notifications
- More advanced 3D visualizations
- Improved mobile experience
- Performance optimization
- More automated tests
- Improved monitoring and alerting

---

# AI Usage

AI tools were used as development aids during the project.

AI was used for:

- Explaining unfamiliar technical concepts.
- Understanding framework and library documentation.
- Investigating technical problems.
- Suggesting possible debugging approaches.
- Reviewing code and identifying potential bugs.
- Helping understand error messages.
- Improving documentation.
- Structuring the README.
- Exploring possible implementations.

AI-generated suggestions were reviewed, tested, and adapted by the team before being integrated into the project.

The team remained responsible for understanding, validating, implementing, and maintaining the final code.

AI was not used as a replacement for understanding the project or independently completing the required work.

---

# Resources

## Documentation

Relevant documentation includes:

- The official `ft_transcendence` subject.
- 42 intra documentation.
- Documentation for the selected frontend framework.
- Documentation for the selected backend framework.
- PostgreSQL documentation.
- ORM documentation.
- Docker documentation.
- Prometheus documentation.
- Grafana documentation.
- WebSocket documentation.
- OAuth 2.0 documentation.
- Three.js / selected 3D library documentation.
- RAG / LLM documentation.
- i18n documentation.

## Articles and Tutorials

During development, the team consulted technical resources covering:

- Full-stack web application architecture
- REST APIs
- WebSockets
- OAuth 2.0
- PostgreSQL
- ORM usage
- Data visualization
- Three.js / 3D rendering
- RAG architectures
- Vector / semantic search
- Prometheus
- Grafana
- Internationalization
- Docker

---

# Credits

Developed by:

- **Sacha Servanton** — `sservant`
- **Nathan Bodin** — `nbodin`
- **Antoine Bonin** — `antbonin`
- **Jules Clement Massonnat** — `julcleme`

As part of the **42 curriculum**.

Special thanks to **42 School** for the `ft_transcendence` project and its requirements.

---

# License

This project was created as part of the 42 curriculum and is primarily intended for educational purposes.

[Add the project's license here if applicable.]



