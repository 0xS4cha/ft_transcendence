*This project has been created as part of the 42 curriculum by sservant, nbodin, antbonin, julcleme.*

# Tactyx — TFT Statistics, Analytics & Social Platform

> **Tactyx** is a modern full-stack web application designed for **Teamfight Tactics (TFT)** players. It combines comprehensive game statistics exploration, interactive team composition building, real-time social interaction, 3D character visualization, local AI-powered assistance via Retrieval-Augmented Generation (RAG), and a production-grade monitoring infrastructure.

---

## Table of Contents

- [Description](#description)
- [Instructions](#instructions)
  - [Prerequisites](#prerequisites)
  - [Environment Configuration](#environment-configuration)
  - [Running the Project with Docker](#running-the-project-with-docker)
  - [Running Without Docker (Local Development)](#running-without-docker-local-development)
  - [Services and Port Mapping](#services-and-port-mapping)
  - [Makefile Commands](#makefile-commands)
  - [Testing and Linting](#testing-and-linting)
- [Team Information](#team-information)
- [Project Management](#project-management)
- [Technical Stack](#technical-stack)
- [Database Schema](#database-schema)
- [Features List](#features-list)
- [42 Modules](#42-modules)
  - [Module Point Calculation](#module-point-calculation)
  - [Major Modules (2 Points Each)](#major-modules-2-points-each)
  - [Minor Modules (1 Point Each)](#minor-modules-1-point-each)
- [Individual Contributions](#individual-contributions)
- [Security](#security)
- [Resources](#resources)
  - [Official Documentation](#official-documentation)
  - [Articles and References](#articles-and-references)
  - [AI Usage](#ai-usage)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Credits](#credits)

---

## Description

**Tactyx** is an end-to-end web platform inspired by competitive analytical tools such as MetaTFT, built specifically for the Teamfight Tactics gaming community.

### Goal and Overview

The primary goal of Tactyx is to give TFT players a centralized, high-performance platform to:
1. **Analyze Game Meta & Performance**: Explore granular statistical metrics (win rate, pick rate, average placement, item popularity) for units, items, traits, and augments.
2. **Experiment with Compositions**: Build and optimize team compositions with a drag-and-drop interactive Team Builder featuring real-time trait synergy calculations.
3. **Connect and Communicate**: Discover players, inspect summoner profiles directly via the Riot Games API, manage friendships, monitor live presence, and chat in real time.
4. **Get Instant Game Guidance**: Consult an embedded, local AI assistant capable of answering questions about TFT mechanics and meta strategies using Retrieval-Augmented Generation (RAG).
5. **Inspect 3D Game Assets**: View fully interactive 3D champion models directly in the statistics interface using WebGL and hardware acceleration.

Beyond gaming analytics, this project demonstrates the design and integration of a robust, microservice-inspired architecture featuring asynchronous backend APIs, full-duplex WebSocket communication backed by Redis Pub/Sub, relational ACID persistence with PostgreSQL, automated migrations with Alembic, OAuth 2.0 authentication, GDPR compliance, and a complete observability pipeline with Prometheus, Alertmanager, and Grafana.

---

## Instructions

### Prerequisites

Ensure the following tools are installed on your host system:

| Software | Required Version | Purpose |
| --- | --- | --- |
| **Git** | `>= 2.30` | Version control |
| **Docker** | `>= 24.0` | Container runtime |
| **Docker Compose** | `>= v2.20` | Multi-container orchestration |
| **Make** | Any standard GNU Make | Build automation |
| **Ollama** | Latest | Local LLM server for the RAG chatbot |
| **Node.js** *(optional, non-docker)* | `>= 20.0` | Frontend runtime |
| **Python** *(optional, non-docker)* | `>= 3.12` | Backend runtime |
| **uv** *(optional, non-docker)* | `>= 0.12` | Python package and project manager |

> [!IMPORTANT]
> The AI Chatbot relies on **Ollama** running on the host machine. You must pull the model before launching the RAG service:
> ```bash
> ollama pull qwen3:0.6b
> ```
> *(Or ensure your preferred local model is specified in the chatbot configuration).*

---

### Environment Configuration

Create a local environment file at the root of the repository:

```bash
cp .env.example .env
```

Edit `.env` to configure your credentials and application keys:

```ini
# PostgreSQL Database Configuration
POSTGRES_USER=DummyUser
POSTGRES_PASSWORD=DummyPassword
POSTGRES_DB=DummyDB
DATABASE_URL="postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_DB"

# Authentication Secrets
SECRET_JWT_KEY=GenerateAStrongSecretKeyHere

# 42 Intra OAuth 2.0 Credentials
FORTYTWO_CLIENT_ID=your_42_api_uid
FORTYTWO_CLIENT_SECRET=your_42_api_secret
FORTYTWO_REDIRECT_URI=https://localhost:8443/api/auth/login_with_42/callback

# Riot Games API (for live player summoner lookups)
RIOT_API_KEY=RGAPI-your-riot-api-key

# Monitoring & Observability Credentials
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin42
PROMETHEUS_ADMIN_USER=admin
PROMETHEUS_ADMIN_PASSWORD=admin42

# Application Settings
DEBUG=0
```

#### Detailed Breakdown of Environment Variables

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: Credentials used by the PostgreSQL container and backend connection strings.
- `DATABASE_URL`: Full PostgreSQL asynchronous connection URI used by SQLAlchemy and Alembic (`postgresql+asyncpg://...`).
- `SECRET_JWT_KEY`: Cryptographic key used to sign and verify HS256 JSON Web Tokens.
- `FORTYTWO_CLIENT_ID`, `FORTYTWO_CLIENT_SECRET`, `FORTYTWO_REDIRECT_URI`: OAuth 2.0 client credentials registered on the 42 Intra application portal.
- `RIOT_API_KEY`: Official Riot Games API key used to query live summoner ranks, match history, and icons.
- `GRAFANA_ADMIN_USER`, `GRAFANA_ADMIN_PASSWORD`: Administrator login credentials for Grafana.
- `PROMETHEUS_ADMIN_USER`, `PROMETHEUS_ADMIN_PASSWORD`: HTTP Basic Authentication credentials protecting `/prometheus/` on the reverse proxy.
- `DEBUG`: Controls OpenAPI documentation exposure (`/docs`, `/redoc`) and verbose application logging.

---

### Running the Project with Docker

The easiest and recommended way to start the entire Tactyx stack is using the provided `Makefile`:

1. **Start the application and Ollama server:**
   ```bash
   make
   # or
   make up
   ```
   *This automatically detects your local host IP, builds the containers, starts them in detached mode, and launches `ollama serve`.*

2. **Access the application in your browser:**
   - **Tactyx Web Application**: [https://localhost:8443](https://localhost:8443) *(Accept the self-signed SSL certificate in your browser)*
   - **HTTP to HTTPS Redirect**: [http://localhost:8080](http://localhost:8080)
   - **Grafana Monitoring Dashboard**: [https://localhost:8443/grafana/](https://localhost:8443/grafana/)
   - **Prometheus Metrics**: [https://localhost:8443/prometheus/](https://localhost:8443/prometheus/)
   - **FastAPI OpenAPI Documentation**: [http://localhost:3000/docs](http://localhost:3000/docs) *(When `DEBUG=1`)*

3. **Stop the application:**
   ```bash
   make down
   ```

---

### Running Without Docker (Local Development)

If you prefer running services directly on your host machine for development:

#### 1. Start External Dependencies
Start PostgreSQL and Redis locally:
```bash
# Redis on localhost:6379
redis-server

# PostgreSQL on localhost:5432
# Ensure a database matching your .env is created
```

#### 2. Start the Backend API
```bash
cd backend/app

# Synchronize dependencies with uv
uv sync

# Run database migrations
uv run alembic upgrade head

# Start the FastAPI server
uv run fastapi dev src/backend_app/main.py --host 0.0.0.0 --port 3000
```

#### 3. Start the Frontend
```bash
cd web

# Install node dependencies
npm install

# Run the Vite development server
npm run dev
```

The frontend will be available at `http://localhost:5173`, proxying API requests to `http://localhost:3000`.

---

### Services and Port Mapping

| Service | Container Name | Internal Port | Host / Proxy Port | Description |
| --- | --- | --- | --- | --- |
| **Proxy** | `transcendence-proxy` | `80`, `443` | `8080`, `8443` | Nginx SSL reverse proxy, rate limiting, and Basic Auth |
| **Web** | `transcendence-web` | `80` | Internal | React 19 production static server |
| **Backend** | `transcendence-backend` | `3000` | `3000` *(dev)* | FastAPI asynchronous REST & WebSocket server |
| **Database** | `transcendence-pg-db` | `5432` | `5432` | PostgreSQL 15 relational database |
| **Redis** | `transcendence-redis` | `6379` | `6378` | Redis 7 cache, rate limiter & WebSocket Pub/Sub broker |
| **Game Data** | `transcendence-game-data` | N/A | Background task | Automated 3D models downloader (`load_3d_models.py`) |
| **Prometheus** | `transcendence-prometheus` | `9090` | Via proxy (`/prometheus/`) | Metrics collection engine & time-series database |
| **Alertmanager** | `transcendence-alertmanager` | `9093` | Internal | Alert management and routing |
| **Grafana** | `transcendence-grafana` | `3000` | Via proxy (`/grafana/`) | Metrics visualization dashboards |
| **Node Exporter** | `transcendence-node-exporter` | `9100` | Internal | Host hardware and OS metrics exporter |
| **cAdvisor** | `transcendence-cadvisor` | `8080` | Internal | Container resource usage exporter |
| **Postgres Exporter** | `transcendence-postgres-exporter` | `9187` | Internal | PostgreSQL database performance metrics exporter |

---

### Makefile Commands

| Target | Command | Purpose |
| --- | --- | --- |
| `make` / `make all` | `make up` | Build and start the full project stack |
| `make build` | `docker compose build` | Build all container images |
| `make up` | `docker compose up -d` | Start all services in the background and start Ollama |
| `make down` | `docker compose down` | Stop and remove active containers |
| `make stop` | `docker compose stop` | Stop running containers without removing them |
| `make start` | `docker compose start` | Start stopped containers |
| `make re` | `make down && make build && make up` | Rebuild and restart the complete application |
| `make boom` | `docker compose down -v --rmi all` | Stop containers, remove volumes and delete images |
| `make nuke` | `make boom && docker system prune -af` | Complete Docker system purge |
| `make status` | `docker ps` | Display live container status |
| `make logs` | `docker compose logs -f` | Follow live container log streams |

---

### Testing and Linting

- **Backend Linting (Ruff)**:
  ```bash
  cd backend/app && uv run ruff check .
  ```
- **Backend Type & Unit Tests**:
  ```bash
  cd backend/app && uv run pytest
  ```
- **Frontend Linting (ESLint)**:
  ```bash
  cd web && npm run lint
  ```
- **Frontend Type Checking & Build Verification**:
  ```bash
  cd web && npm run build
  ```
- **Continuous Integration (CI)**:
  GitHub Actions workflow (`.github/workflows/cy.yml`) runs on every push and pull request to enforce `make build` and repository-wide `ruff check .`.

---

## Team Information

| Member | 42 Login | Assigned Role(s) | Primary Responsibilities |
| --- | --- | --- | --- |
| **Nathan Bodin** | `nbodin` | **Project Manager** / Developer | Supervised overall software architecture, system integration, Designed the css style of the site and technology choices. Architected backend models, Alembic migrations, user authentication (Argon2, JWT), 42 OAuth 2.0 integration, user profiles, friends system, Redis rate limiters, and code styling enforcement. |
| **Sacha Servanton** | `sservant` | **Tech Lead** / Developer | Coordinated sprint milestones, task assignments, and delivery schedules. Designed the frontend architecture with React 19, Vite, and Tailwind CSS v4. Implemented custom design system, theme switching, interactive data tables with multi-format export (JSON/XML), internationalization (i18n), Prometheus/Grafana integration, and frontend 42 OAuth/chat flows. |
| **Antoine Bonin** | `antbonin` | **Product Owner** / Developer | Defined product, feature priorities, user requirements, and acceptance criteria.  Designed and implemented the complete interactive Team Builder with `@dnd-kit` drag-and-drop, trait calculations, and composition import/export. Built the application navigation sidebar, patch notes page, ranking tables, and responsive theme polish. |
| **Jules Clement Massonnat** | `julcleme` | **Tech Lead**/ Developer | Developed the AI RAG Assistant pipeline (BM25s retrieval, LangChain chunking, Ollama Qwen integration, TFT knowledge base). Built the real-time WebSocket connection manager with Redis Pub/Sub, live chat backend, game data scrapers, 3D model automated downloader, multi-entity search with Riot API, home analytics, and Nginx reverse proxy SSL configuration. |

---

## Project Management

### Work Organization

The team adopted an **Agile / Scrum-inspired workflow** organized around iterative feature milestones:
1. **Requirements & Backlog Definition**: The Product Owner (`nbodin`) drafted user stories and feature specifications based on the 42 subject modules and TFT analytical platforms.
2. **Sprint Planning & Task Distribution**: The Project Manager (`sservant`) organized tasks, assigned issues to team members based on technical specialization, and tracked progress.
3. **Architecture Guidance**: The Tech Lead (`antbonin`) reviewed design choices, ensured consistency between frontend interfaces and backend APIs, and managed component contracts.
4. **Regular Sync Meetings**: Daily stand-ups (in-person at 42 Lyon and over voice calls) to identify blockers, synchronize interface contracts, and align sprint goals.

### Project Management Tools

- **Version Control**: Git hosted on GitHub.
- **Task Tracking & Milestones**: GitHub Issues and GitHub Projects board to track tasks across `Todo`, `In Progress`, `Review`, and `Done`.
- **Branching Strategy**: Strict feature-branch workflow (`feat/...`, `fix/...`) requiring pull requests and peer review before merging into `main`.
- **Continuous Integration (CI)**: GitHub Actions workflow checking automated build execution (`make build`) and Python code formatting with Ruff (`astral-sh/ruff-action`).

### Communication Channels

- **Discord**: Dedicated team server with channels for general discussion, frontend development, backend development, deployment/DevOps, pull request alerts, and voice channels for pair programming and stand-ups.
- **In-Person Syncs**: Regular collaboration sessions at 42 Lyon campus clusters.

---

## Technical Stack

### Frontend Technologies and Frameworks

- **Core Framework**: [React 19](https://react.dev/) (`19.2.8`) — Modern component architecture leveraging concurrent rendering and modern hook patterns.
- **Build Tool**: [Vite](https://vite.dev/) (`8.2.0`) — Ultra-fast HMR and optimized asset bundling.
- **Language**: [TypeScript](https://www.typescriptlang.org/) (`~6.0.2`) — Strict type safety across components, API contracts, and models.
- **Styling & CSS**: [Tailwind CSS v4](https://tailwindcss.com/) (`^4.3.3`) — Utility-first CSS engine with modern CSS variables.
- **Component Primitives**: [shadcn/ui](https://ui.shadcn.com/) (`^4.16.2`) & `@base-ui/react` — Accessible, headless UI component architecture.
- **Animations & Transitions**: [Framer Motion](https://motion.dev/) (`^13.0.0`) & `tw-animate-css` — Smooth UI micro-interactions and transitions.
- **State Management**: [Redux Toolkit](https://redux-toolkit.js.org/) (`^2.12.0`) & `react-redux` — Centralized global store for user sessions, live home analytics, and UI states.
- **Routing**: [React Router](https://reactrouter.com/) (`v7.18.2`) — Declarative client-side routing with protected route boundaries.
- **Tabular Data**: [TanStack Table](https://tanstack.com/table) (`^9.2.4`) — Headless table engine supporting sorting, multi-column filtering, pagination, and expandable rows.
- **Data Visualization**: [Recharts](https://recharts.org/) (`^3.8.0`) — Declarative charting library for 90-day visitor trends and metrics.
- **3D Graphics**: [Three.js](https://threejs.org/) (`^0.185.1`), [React Three Fiber](https://r3f.docs.pmnd.rs/) (`^9.7.0`), [React Three Drei](https://drei.pmnd.rs/) (`^10.7.8`) — WebGL rendering of 3D champion models with lighting, centering, and OrbitControls.
- **Drag & Drop**: [@dnd-kit](https://dndkit.com/) (`^6.3.1`) — Modular drag-and-drop system powering the Team Builder hex board.
- **Internationalization (i18n)**: [react-i18next](https://react.i18next.com/) (`^17.0.16`) & `i18next` — Complete multi-language translations (English, French, Spanish).
- **Theming**: [next-themes](https://github.com/pacocoursey/next-themes) (`^0.4.6`) — Dark and light mode switcher with persistent user preference.
- **Icons**: [Lucide React](https://lucide.dev/) (`^1.31.0`) — Clean vector icons throughout the interface.

---

### Backend Technologies and Frameworks

- **Core Framework**: [FastAPI](https://fastapi.tiangolo.com/) (`>= 0.141.1`) — High-performance asynchronous Python web framework with automated OpenAPI/Swagger generation.
- **Language & Runtime**: [Python 3.12](https://www.python.org/) managed with [uv](https://github.com/astral-sh/uv) (`>= 0.12.8`) — High-speed package management and frozen virtual environment execution.
- **Database & ORM**: [SQLAlchemy 2.0 Async](https://www.sqlalchemy.org/) (`>= 2.0.52`) with [AsyncPG](https://github.com/MagicStack/asyncpg) (`>= 0.31.0`) — Asynchronous relational Object-Relational Mapping.
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/) (`>= 1.19.2`) — Declarative database revision history and schema migrations.
- **Data Validation & Schemas**: [Pydantic v2](https://docs.pydantic.dev/) & `pydantic-settings` — Strict request/response payload validation and environment typing.
- **Real-Time Communication**: [WebSockets](https://websockets.readthedocs.io/) (`>= 17.1`) & FastAPI WebSocket endpoints — Full-duplex live connections for chat and stats broadcasting.
- **In-Memory Cache & Message Broker**: [Redis 7](https://redis.io/) (`redis-py >= 8.1.0`) — Redis Pub/Sub for distributed WebSocket broadcasts and active user presence tracking.
- **Rate Limiting**: [fastapi-limiter](https://github.com/long2ice/fastapi-limiter) (`>= 0.2.0`) & Redis — Rate limiting across authentication, public, and authenticated endpoints.
- **AI & RAG Pipeline**:
  - [BM25s](https://github.com/xhl-c/bm25s) (`>= 0.3.12`) — High-performance sparse lexical search index for TFT context retrieval.
  - [LangChain Text Splitters](https://python.langchain.com/) (`>= 1.1.3`) — Recursive character document chunking with metadata tracking.
  - [Ollama Python SDK](https://github.com/ollama/ollama-python) (`>= 0.6.3`) — Local LLM integration with `qwen3:0.6b`.
- **Authentication & Security**:
  - [pwdlib](https://github.com/frankie567/pwdlib) with [Argon2](https://github.com/p-h-c/phc-winner-argon2) (`>= 0.3.1`) — Password hashing.
  - [PyJWT](https://pyjwt.readthedocs.io/) (`>= 2.13.0`) — Secure JSON Web Token generation and cookie validation.
  - [httpx2](https://github.com/encode/httpx) (`>= 2.12.0`) — Asynchronous HTTP client for 42 OAuth token exchange and API lookups.
- **Image Processing**: [Pillow](https://python-pillow.org/) (`>= 12.3.0`) — Avatar file validation, sanitization, and thumbnail resizing.
- **Observability**: [prometheus-client](https://github.com/prometheus/client_python) (`>= 0.26.0`) — Exposing custom application metrics at `/api/prometheus/metrics`.

---

### Database System and Justification

The project uses **PostgreSQL 15** as its primary database.

**Why PostgreSQL was chosen:**
1. **Relational Data Integrity**: The core domain requires strong relationships (Users $\leftrightarrow$ Friendships, Users $\leftrightarrow$ Chat Messages, Champions $\leftrightarrow$ Spells $\leftrightarrow$ Skins $\leftrightarrow$ Tactical Info). PostgreSQL provides strict foreign key constraints, cascading deletes, and unique composite indexes (e.g. unique friendships between `uid1` and `uid2`).
2. **ACID Compliance**: Ensures that user authentication, password updates, friend requests, and account deletions execute with total transactional consistency.
3. **Hybrid Relational + JSON Capabilities**: PostgreSQL native `JSON` / `JSONB` support allows storing complex TFT attributes (e.g., dynamic spell coefficient arrays, item stat dictionaries, chroma colors) without requiring excessive normalization.
4. **Asynchronous Performance**: Exceptional performance when paired with the `asyncpg` non-blocking PostgreSQL driver in FastAPI.

---

### Other Significant Technologies and Libraries

- **Reverse Proxy**: **Nginx** running in a custom container handling TLS/SSL termination, enforcing rate limiting (`20r/s` with burst `40`), routing traffic to Web and Backend containers, and securing Prometheus via HTTP Basic Auth (`.htpasswd`).
- **Observability Stack**:
  - **Prometheus**: Scrapes metrics from backend, host system (`node-exporter`), container engine (`cadvisor`), and database (`postgres-exporter`).
  - **Alertmanager**: Evaluates threshold rules (high CPU, service outages) and manages alerts.
  - **Grafana**: Pre-provisioned dashboards visualizing system health, PostgreSQL queries, and application performance.

---

### Justification for Major Technical Choices

1. **FastAPI over Django/Flask**: FastAPI delivers native `async/await` execution necessary for high-concurrency WebSockets, automatic OpenAPI schema generation, and strict Pydantic data validation with minimal boilerplate.
2. **React 19 + Vite over Next.js/SSR**: Since ft_transcendence requires a Single Page Application (SPA) architecture, React 19 with Vite provides the fastest build times, clean client-side routing, and zero overhead for SSR server management.
3. **Redis Pub/Sub for WebSockets**: Rather than relying on in-memory Python dictionaries that break when scaling across multiple workers, Redis Pub/Sub enables horizontal scalability for real-time broadcasts.
4. **Local RAG with Ollama & BM25s over External Cloud APIs**: Using a local Qwen model with BM25s ensures 100% offline functionality, zero API costs, zero rate limits, and strictly grounded answers derived from curated local TFT game files.
5. **Three.js & React Three Fiber**: Directly embeds interactive 3D assets inside data table rows with WebGL hardware acceleration without degrading application responsiveness.

---

## Database Schema

### Visual Representation (Entity-Relationship Diagram)

```mermaid
erDiagram
    users ||--o{ chat_message : "owns"
    users ||--o{ friends : "requests / requested"
    champions ||--|| champion_tactical_info : "has"
    champions ||--|| champion_playstyle_info : "has"
    champions ||--|| champion_tag_info : "has"
    champions ||--|| champion_passives : "has"
    champions ||--o{ champion_roles : "has"
    champions ||--o{ champion_recommended_item_defaults : "recommends"
    champions ||--o{ skins : "has"
    champions ||--o{ spells : "casts"
    skins ||--o{ skin_lines : "belongs to"
    skins ||--o{ chromas : "has"
    chromas ||--o{ skin_descriptions : "described in"
    chromas ||--o{ skin_rarities : "has rarity"
    spells ||--|| spell_coefficients : "has"
    spells ||--|| spell_effect_amounts : "has"
    spells ||--|| spell_ammo : "has"

    users {
        int id PK
        string email UK
        string hashed_password
        string username UK
        string picture
    }

    friends {
        int id PK
        int requester FK
        int requested FK
        int uid1 FK
        int uid2 FK
        string status "Enum: pending | accepted"
    }

    chat_message {
        int id PK
        bigint date
        int owner_id FK
        string content
    }

    visit_model {
        date date PK
        int count
    }

    unit_stat {
        string unit PK
        int count
        int place
        int wins
        int top4
        json items
    }

    champions {
        int id PK
        string contentId
        string name
        string alias
        string title
        string shortBio
        boolean isVisibleInClient
        string squarePortraitPath
        string stingerSfxPath
        string chooseVoPath
        string banVoPath
    }

    spells {
        int id PK
        int champion_id FK
        string spellKey
        string name
        string abilityIconPath
        string abilityVideoPath
        string abilityVideoImagePath
        string cost
        string cooldown
        string description
        string dynamicDescription
        json range
        json costCoefficients
        json cooldownCoefficients
        int maxLevel
    }

    skins {
        int id PK
        int champion_id FK
        string contentId
        boolean isBase
        string name
        string skinClassification
        string splashPath
        string uncenteredSplashPath
        string tilePath
        string loadScreenPath
        string loadScreenVintagePath
        string skinType
        string rarity
        boolean isLegacy
    }
```

---

### Detailed Table Specifications

#### 1. `users`
Represents registered user accounts on the platform.
- `id` (`Integer`, Primary Key, autoincrement): Unique user identifier.
- `email` (`String`, Unique, Indexed): User email address.
- `hashed_password` (`String`): Argon2 secure password hash.
- `username` (`String`, Unique): Public username or 42 login.
- `picture` (`String`, Nullable): Path to uploaded avatar or remote OAuth image URL.

#### 2. `friends`
Manages bidirectional friendships and pending friend requests.
- `id` (`Integer`, Primary Key): Relationship identifier.
- `requester` (`Integer`, FK $\rightarrow$ `users.id`): User who sent the request.
- `requested` (`Integer`, FK $\rightarrow$ `users.id`): Recipient of the request.
- `uid1` (`Integer`, FK $\rightarrow$ `users.id`): Lower user ID for unique pairing.
- `uid2` (`Integer`, FK $\rightarrow$ `users.id`): Higher user ID for unique pairing.
- `status` (`Enum: friends_status`): Status (`pending` or `accepted`).
- **Constraints**: `UniqueConstraint('uid1', 'uid2')`, Check constraint preventing self-friending (`requested != requester`).

#### 3. `chat_message`
Stores messages exchanged in the global live chat.
- `id` (`Integer`, Primary Key, autoincrement): Unique message identifier.
- `date` (`BigInteger`): Unix timestamp in milliseconds.
- `owner_id` (`Integer`, FK $\rightarrow$ `users.id`, On Delete Cascade): Author user ID.
- `content` (`String`): Text content of the message.

#### 4. `visit_model`
Tracks aggregate daily unique visits for the analytics dashboard.
- `date` (`Date`, Primary Key): Calendar date of recorded visits.
- `count` (`Integer`, default `0`): Total visits recorded for the day.

#### 5. `unit_stat`
Aggregated TFT unit statistics loaded from Riot/MetaTFT data.
- `unit` (`String`, Primary Key): Unit name / identifier.
- `count` (`Integer`): Sample size of recorded games.
- `place` (`Integer`): Cumulative placement sum.
- `wins` (`Integer`): Total 1st place finishes.
- `top4` (`Integer`): Total Top 4 finishes.
- `items` (`JSON`): Frequency map of popular item pairings.

#### 6. TFT Game Data Tables
- `champions`, `champion_tactical_info`, `champion_playstyle_info`, `champion_tag_info`, `champion_passives`, `champion_roles`, `champion_recommended_item_defaults`, `skins`, `skin_lines`, `chromas`, `skin_descriptions`, `skin_rarities`, `spells`, `spell_coefficients`, `spell_effect_amounts`, `spell_ammo`: Fully normalized relational mapping of champion statistics, spells, coefficients, and skins.

---

## Features List

| Feature | Category | Contributor(s) | Description |
| --- | --- | --- | --- |
| **User Registration & Login** | Authentication | `nbodin` | Secure account registration and login using Argon2 password hashing and HTTP-only JWT cookies. |
| **42 Intra OAuth 2.0** | Authentication | `nbodin`, `sservant` | Remote authentication via 42 Intra with CSRF state protection, automatic account creation, and avatar sync. |
| **Profile Management** | User System | `nbodin`, `antbonin` | View user profile, modify username, upload custom avatar with automated Pillow image resizing, or remove avatar. |
| **Friends System** | Social | `nbodin`, `sservant` | Send, accept, refuse, and remove friend requests with relational constraints and pending invitation tabs. |
| **Live Presence Tracking** | Social & Real-Time | `julcleme`, `sservant` | Tracks active WebSocket connections in Redis to broadcast online/offline indicators for friends. |
| **Real-Time Global Chat** | Real-Time | `julcleme`, `sservant` | Persistent live chat room with full-duplex WebSockets, Redis Pub/Sub broadcasting, avatar display, and 200-message history cache. |
| **TFT Statistics Tables** | Analytics | `sservant` | High-performance interactive tables for Units, Items, Traits, and Augments with multi-column sorting, filtering, and pagination. |
| **3D Champion Visualizer** | 3D Graphics | `julcleme`, `sservant` | Expanding table rows renders interactive 3D champion `.glb` models with Three.js, React Three Fiber, lighting, and OrbitControls. |
| **Interactive Team Builder** | Gameplay Tool | `antbonin` | Drag-and-drop TFT board with `@dnd-kit`, hex board positioning, item equipping, dynamic trait synergy calculations, and augment selector. |
| **Composition Import & Export** | Gameplay Tool | `antbonin` | Export team compositions to clipboard as Base64-encoded JSON strings and import existing codes into the board. |
| **Multi-Format Data Export** | Data Management | `sservant` | Export statistics tables (Units, Items, Traits, Augments) directly to formatted JSON and XML files. |
| **Leaderboard / Rankings** | Analytics | `julcleme`, `antbonin` | Displays top 50 players globally or filtered by competitive region (EUW, NA, KR, etc.) with backend caching. |
| **Multi-Entity Search** | Search | `julcleme`, `sservant`, `nbodin` | Unified search bar resolving units, items, traits, augments, and live Riot summoner profiles (`gameName#tagLine`). |
| **Set 18 Patch Notes Viewer** | Content | `julcleme`, `antbonin` | Responsive patch notes reader with localized HTML content in English, French, and Spanish. |
| **AI / RAG Chatbot Assistant** | Artificial Intelligence | `julcleme`, `sservant` | In-chat AI assistant (`/question`) querying local Ollama (Qwen 3) with BM25s sparse retrieval over curated TFT documentation. |
| **Analytics Dashboard** | Observability | `julcleme`, `sservant` | Visualizes 90-day visitor trends using Recharts, platform activity metrics, and live GraphQL game stats from `teamfight.lol`. |
| **Internationalization (i18n)** | Accessibility | `sservant`, `antbonin` | Complete language switching between English (`en`), French (`fr`), and Spanish (`es`) across the UI and patch notes. |
| **Custom Design System & Theme** | UI/UX | `sservant`, `antbonin` | Cohesive UI design system built on Tailwind v4 and shadcn/ui with dark/light mode toggle and responsive mobile drawers. |
| **System Observability & Alerts** | DevOps | `sservant`, `julcleme` | Prometheus metrics scraping, node-exporter, cadvisor, postgres-exporter, Alertmanager threshold rules, and Grafana dashboards. |
| **Reverse Proxy & Rate Limiting** | Infrastructure | `julcleme`, `nbodin` | Nginx reverse proxy with SSL termination, HTTP to HTTPS redirect, Basic Auth protection, and Redis rate limiting. |

---

## 42 Modules

### Module Point Calculation

| Module Name | Module Type | Points | Implemented & Validated |
| --- | --- | --- | --- |
| **Full-Stack Framework** | Major | +2 | Yes (React 19 + FastAPI) |
| **User Management** | Major | +2 | Yes (Registration, profiles, avatars, security) |
| **User Interaction / Social System** | Major | +2 | Yes (Chat, friends, presence) |
| **Monitoring System** | Major | +2 | Yes (Prometheus, Grafana, Alertmanager, Exporters) |
| **Advanced 3D Graphics** | Major | +2 | Yes (Three.js / React Three Fiber / Drei) |
| **Complete RAG System** | Major | +2 | Yes (Ollama Qwen 3 + BM25s retrieval) |
| **Advanced Analytics Dashboard** | Major | +2 | Yes (Recharts visualizations + live stats) |
| **Team builder** | Major (Custom) | + 2 | Yes (/builder) |
| **Object-Relational Mapping (ORM)** | Minor | +1 | Yes (SQLAlchemy 2.0 Async + Alembic) |
| **OAuth 2.0 Authentication** | Minor | +1 | Yes (42 Intra OAuth 2.0) |
| **Data Import and Export** | Minor | +1 | Yes (JSON, XML, and Team Builder Base64 JSON) |
| **Multi-Language Support (i18n)** | Minor | +1 | Yes (English, French, Spanish) |
| **Advanced Search** | Minor | +1 | Yes (Multi-entity search + Riot Games API) |
| **User Activity Analytics** | Minor | +1 | Yes (90-day visitor tracking, usage counters) |
| **Custom Design System** | Minor | +1 | Yes (Tailwind v4 tokens, light/dark themes, >10 UI components) |
| **Chatbot** | Minor (custom) | +1 | Yes (with / in the chat) |
| **Total Points** | | **24** | *(Exceeds the 14-point minimum requirement)* |

---

### Major Modules (2 Points Each)

#### 1. Full-Stack Framework (2 Points)
- **Choice & Justification**: We chose **React 19** on the frontend and **FastAPI** on the backend. This combination provides a strict separation of concerns, high-speed asynchronous processing, automatic OpenAPI contract generation, and modular UI component development.
- **Implementation**: The frontend is built with React 19, TypeScript, and Vite; the backend is built with Python 3.12, FastAPI, and Pydantic v2. Communication flows through structured REST API endpoints and full-duplex WebSockets.
- **Worked on by**: Sacha Servanton (`sservant`), Nathan Bodin (`nbodin`), Antoine Bonin (`antbonin`), Jules Clement Massonnat (`julcleme`).

#### 2. Standard User Management (2 Points)
- **Choice & Justification**: Essential for securing personal settings, compositions, and social features across users.
- **Implementation**: Argon2 password hashing with `pwdlib`, secure HTTP-only JWT cookie management, profile page displaying user statistics, username editing, avatar upload with Pillow validation and thumbnail resizing, default avatar fallback, and GDPR-compliant account deletion.
- **Worked on by**: Nathan Bodin (`nbodin`), Sacha Servanton (`sservant`).

#### 3. User Interaction / Social System (2 Points)
- **Choice & Justification**: Elevates Tactyx from a passive data viewer into an active gaming community hub.
- **Implementation**: Real-time global chat powered by WebSockets, Redis Pub/Sub message broker, user presence tracking (online/offline badges), bidirectional friend requests with pending status management, and friend removal.
- **Worked on by**: Nathan Bodin (`nbodin`), Jules Clement Massonnat (`julcleme`), Sacha Servanton (`sservant`).

#### 4. Monitoring System with Prometheus and Grafana (2 Points)
- **Choice & Justification**: Ensures production observability, service health tracking, performance profiling, and proactive failure detection.
- **Implementation**: Prometheus scrapes metrics from the FastAPI backend (`/api/prometheus/metrics`), `node-exporter` (host resources), `cadvisor` (container stats), and `postgres-exporter`. Pre-configured Alertmanager rules trigger on high CPU or service failure. Grafana is provisioned with custom dashboards behind Nginx authentication.
- **Worked on by**: Sacha Servanton (`sservant`), Jules Clement Massonnat (`julcleme`).

#### 5. Advanced 3D Graphics (2 Points)
- **Choice & Justification**: Adds an immersive visual dimension by rendering authentic 3D models of TFT champions directly inside the application.
- **Implementation**: Integrated Three.js, React Three Fiber, and `@react-three/drei`. A custom `game_data` service downloads official `.glb` models. Expanding a champion row in the statistics table mounts a 3D Canvas with ambient lighting, directional shadows, automatic model centering, and user-controlled `OrbitControls`.
- **Worked on by**: Sacha Servanton (`sservant`), Jules Clement Massonnat (`julcleme`).

#### 6. Complete RAG System (2 Points)
- **Choice & Justification**: Provides intelligent, natural-language assistance about TFT strategies grounded in accurate, patch-specific data without hallucination or third-party API dependencies.
- **Implementation**: Document chunking with `langchain-text-splitters`, sparse lexical indexing with `bm25s`, local LLM inference using `qwen3:0.6b` via Ollama, and a curated knowledge base covering TFT mechanics, patch notes, esports, item combinations, and champion stats. Users invoke the assistant in chat using `/question`.
- **Worked on by**: Jules Clement Massonnat (`julcleme`), Sacha Servanton (`sservant`).

#### 7. Advanced Analytics Dashboard (2 Points)
- **Choice & Justification**: Empowers players to monitor platform engagement and community trends over time.
- **Implementation**: Interactive area and line charts built with Recharts, 90-day visitor tracking persisted in PostgreSQL, live counters for chat messages and accounts, and real-time updates broadcast via WebSockets.
- **Worked on by**: Sacha Servanton (`sservant`), Jules Clement Massonnat (`julcleme`).

#### 8. Team builder (custom) (2 Points)
- **Choice & Justification**: The team builder is an essential tool of this type; it allows players to visualize team compositions to optimize their chances of winning.
- **Implementation**: An interactive grid with the ability to place units and items.
- **Worked on by**: Antoine Bonin (`antbonin`).



---

### Minor Modules (1 Point Each)

#### 9. Object-Relational Mapping (ORM) (1 Point)
- **Choice & Justification**: Guarantees type safety, protects against SQL injection, and provides declarative schema management.
- **Implementation**: Implemented with **SQLAlchemy 2.0 Async** and **Alembic**. Models define relationships, foreign keys, cascades, and constraints with type hints (`Mapped[...]`).
- **Worked on by**: Nathan Bodin (`nbodin`), Jules Clement Massonnat (`julcleme`).

#### 10. OAuth 2.0 Authentication (1 Point)
- **Choice & Justification**: Simplifies onboarding for 42 students and guarantees secure identity delegation.
- **Implementation**: The user is redirected to `https://api.intra.42.fr/oauth/authorize` with a cryptographically secure `state` cookie. Upon callback, the backend exchanges the code for an access token, fetches the user's 42 profile (email, login, avatar), associates or creates the account in PostgreSQL, and issues an authenticated JWT session.
- **Worked on by**: Nathan Bodin (`nbodin`), Sacha Servanton (`sservant`).

#### 11. Data Import and Export (1 Point)
- **Choice & Justification**: Enables players to back up data, share team compositions, or analyze statistics externally.
- **Implementation**: Statistics tables export to **JSON** and **XML** formats using browser Blob downloads. The Team Builder supports exporting compositions to clipboard as Base64 JSON strings and importing codes to reconstruct the board.
- **Worked on by**: Sacha Servanton (`sservant`), Antoine Bonin (`antbonin`).

#### 12. Multi-Language Support (1 Point)
- **Choice & Justification**: Enhances accessibility for an international gaming user base.
- **Implementation**: Built with `react-i18next` supporting **English (`en`)**, **French (`fr`)**, and **Spanish (`es`)**. All navigation labels, form controls, table headers, error messages, and Set 18 patch notes are completely translated.
- **Worked on by**: Sacha Servanton (`sservant`), Antoine Bonin (`antbonin`), Jules Clement Massonnat (`julcleme`).

#### 13. Advanced Search (1 Point)
- **Choice & Justification**: Enables users to find TFT game items and players across a large dataset instantly.
- **Implementation**: Backend search endpoint querying units, items, traits, augments, and player summoners via Riot Games API (`name#tag`). Frontend features real-time search inputs with debounce and category-filtered results.
- **Worked on by**: Jules Clement Massonnat (`julcleme`), Sacha Servanton (`sservant`), Nathan Bodin (`nbodin`).

#### 14. User Activity Analytics (1 Point)
- **Choice & Justification**: Provides transparency into platform usage and community interaction.
- **Implementation**: Tracks daily user visits in `visit_model` across a 90-day rolling window, aggregate registered account counts, and live TFT platform data via GraphQL.
- **Worked on by**: Jules Clement Massonnat (`julcleme`), Sacha Servanton (`sservant`).

#### 15. Custom Design System (1 Point)
- **Choice & Justification**: Ensures visual polish, consistent spacing, and accessibility across all views.
- **Implementation**: Custom token-based design system built on Tailwind CSS v4, supporting dynamic light and dark themes via `next-themes`, and over 15 reusable UI components (dialogs, cards, sheets, sidebars, toolbars, badges, buttons, selects, avatars, tables).
- **Worked on by**: Sacha Servanton (`sservant`), Antoine Bonin (`antbonin`).

#### 16. Chatbot (custom) (1 Point)
- **Choice & Justification**: In the age of AI, this type of tool is essential for obtaining precise information from large datasets.
- **Implementation**: The chatbot is integrated with our RAG tool, allowing users to ask a question by placing a '/' before their input.
- **Worked on by**: Jules Clément Massonnat (`julcleme`) (back),  Sacha Servanton (`sservant`) (front).

---

## Individual Contributions

### Nathan Bodin (`nbodin`) — Project Manager & Developer

- **Role & Responsibilities**: Product Manager directing backlog prioritization, user story definition, acceptance criteria, and backend engineering.
- **Specific Components & Features Implemented**:
  - Engineered the FastAPI application structure, Alembic migration environment, and SQLAlchemy model hierarchy.
  - Implemented secure user authentication: registration, login with Argon2 hashing, JWT generation, and token expiration policies.
  - Developed the complete backend 42 OAuth 2.0 flow (`/api/auth/login_with_42` and `/callback`) with CSRF state validation and account linking.
  - Built user profile management: username updates, avatar image upload and sanitization using Pillow, and avatar removal.
  - Implemented the friendship system backend: friend request sending, acceptance, refusal, listing, and relational database constraints.
  - Integrated Redis-backed rate limiting (`fastapi-limiter`) across auth, basic, and authenticated endpoints.
  - Enforced Python coding standards and CI pipeline validation with Ruff.
- **Challenges Faced & Solutions**:
  - *Challenge*: Managing asynchronous session lifecycles across concurrent FastAPI dependencies while preventing session leaks or database connection deadlocks.
  - *Solution*: Implemented an async session context manager dependency (`AsyncSessionDep`) ensuring safe session closure per request.
  - *Challenge*: Multiple diverging Alembic migration heads created during parallel git branch development.
  - *Solution*: Established a strict migration merge procedure and resolved migration revisions before pull request merges.

---

### Sacha Servanton (`sservant`) — Tech Lead & Developer

- **Role & Responsibilities**: Project Manager organizing sprint tracking, task distribution, and lead frontend architect.
- **Specific Components & Features Implemented**:
  - Architected the React 19 + Vite frontend application structure, routing, and Redux global state.
  - Built the custom design system with Tailwind CSS v4 and shadcn/ui components, including full dark and light mode theming.
  - Designed the comprehensive Data Tables (TanStack Table) for Units, Items, Traits, and Augments with sorting, multi-attribute filtering, and pagination.
  - Implemented multi-format statistics export to JSON and XML.
  - Configured full internationalization (`react-i18next`) across English, French, and Spanish.
  - Implemented real-time frontend components: live chat interface, online status indicators, and home dashboard analytics.
  - Configured Prometheus, Alertmanager, and Grafana monitoring infrastructure in Docker Compose with custom dashboards.
  - Developed frontend 42 OAuth authentication flows, notification toasts, and GDPR deletion triggers.
- **Challenges Faced & Solutions**:
  - *Challenge*: Synchronizing TanStack Table state (sorting, pagination, row expansion) with dynamic WebGL Canvas mounts for 3D models without frame drops or memory leaks.
  - *Solution*: Encapsulated Three.js canvases inside isolated sub-components with Suspense boundaries and lazy rendering upon row expansion.
  - *Challenge*: Managing internationalization keys across rapidly evolving UI views without breaking missing translation fallbacks.
  - *Solution*: Structured nested i18n translation dictionaries with default English fallbacks and standardized translation hooks.

---

### Antoine Bonin (`antbonin`) — Product Owner & Developer

- **Role & Responsibilities**: Product Owner checking consistency, interface contracts, and core gameplay tools.
- **Specific Components & Features Implemented**:
  - Designed and built the complete interactive **Team Builder** from scratch:
    - Hexagonal board layout with drop targets.
    - Drag-and-drop mechanics using `@dnd-kit` (Mouse and Touch sensors).
    - Real-time TFT trait synergy activation and tier calculation based on champions placed on the board.
    - Item equipping on champions and augment selection bar.
    - Team composition export to clipboard (Base64 JSON) and import dialog.
  - Built the responsive application sidebar and overall layout navigation (`app_sidebar.tsx`, `layout.tsx`).
  - Implemented the Leaderboard / Ranking frontend table displaying competitive player ratings.
  - Developed the Patch Notes page with multi-language HTML rendering and custom stylesheet integration.
  - Crafted light/dark theme styling refinements and responsive mobile adaptations.
- **Challenges Faced & Solutions**:
  - *Challenge*: Implementing accurate hexagonal drag-and-drop collision detection and item equipping on small champion hex cells across both desktop and mobile viewports.
  - *Solution*: Leveraged `@dnd-kit` with custom collision detection (`pointerWithin`), center-to-cursor snap modifiers, and dedicated touch sensor activation delays.
  - *Challenge*: Dynamically recalculating complex TFT trait synergy tiers in real time whenever champions are dragged, swapped, or removed from the board.
  - *Solution*: Created memoized trait calculation algorithms that parse champion traits, filter duplicates, and compute active synergy thresholds instantly.

---

### Jules Clement Massonnat (`julcleme`) — Tech Lead & Developer

- **Role & Responsibilities**: Full-stack developer specializing in real-time systems, RAG / AI pipelines, data ingestion, and networking.
- **Specific Components & Features Implemented**:
  - Architected and implemented the local **RAG AI Assistant**:
    - Document chunking with `langchain-text-splitters`.
    - BM25s sparse lexical index creation and chunk retrieval.
    - Integration with local Ollama (`qwen3:0.6b`).
    - Curated comprehensive TFT knowledge dataset (gameplay, mechanics, meta, esports, Set 18 units & items).
  - Developed the real-time WebSocket architecture:
    - Distributed `WebsocketConnectionManager` backed by Redis Pub/Sub.
    - Client connection tracking and active user presence sets.
    - Live chat broadcasting and real-time home statistics dissemination.
  - Built the automated TFT game data pipelines and 3D model loader (`load_3d_models.py`) fetching official `.glb` assets.
  - Developed the advanced multi-entity search endpoint integrating the Riot Games API for live player profile lookups.
  - Created the Nginx reverse proxy configuration with TLS/SSL, rate limiting, and Basic Authentication.
  - Implemented GDPR account deletion endpoint (`/api/auth/me`).
- **Challenges Faced & Solutions**:
  - *Challenge*: Running a local LLM RAG assistant efficiently on student workstations without overwhelming memory or relying on external paid APIs.
  - *Solution*: Utilized the lightweight, highly quantized `qwen3:0.6b` model with Ollama, paired with fast BM25s sparse indexing to provide high-relevance context within seconds.
  - *Challenge*: Ensuring real-time chat messages and live metrics reach all connected users reliably across multiple backend processes.
  - *Solution*: Implemented a Redis Pub/Sub broadcast channel (`websocket:broadcast`) so that any backend worker can publish events that are instantly relayed to all connected WebSocket clients.

---

## Security

Security best practices were integrated throughout development:

1. **Password Hashing**: Passwords are hashed using the state-of-the-art **Argon2** algorithm (`pwdlib[argon2]`), protecting against GPU-based brute-force and dictionary attacks.
2. **Stateless JWT Authentication**: Sessions are authenticated using signed JSON Web Tokens (HS256) stored in `HttpOnly`, `SameSite=Lax`, and `Secure` cookies, mitigating Cross-Site Scripting (XSS) token theft.
3. **OAuth 2.0 State Verification**: 42 Intra OAuth flows utilize a cryptographically secure random `state` parameter validated against a temporary cookie to prevent Cross-Site Request Forgery (CSRF).
4. **Rate Limiting & DDoS Protection**:
   - Nginx enforces IP-based rate limiting (`limit_req_zone`, 20 req/s, burst 40).
   - FastAPI endpoints utilize `fastapi-limiter` backed by Redis on sensitive authentication and user routes.
5. **SQL Injection Prevention**: All database interactions are executed through SQLAlchemy 2.0 parameterized queries and ORM mappings, eliminating raw SQL injection vectors.
6. **Input Validation**: All incoming REST payloads are strictly validated using Pydantic v2 schemas; invalid types and extra unexpected fields are rejected.
7. **Image Sanitization**: Uploaded avatars are validated and processed using Pillow, stripping potentially malicious metadata and re-encoding images safely.
8. **GDPR / Privacy Compliance**: Users can trigger complete account deletion, purging personal data, messages, and relationships in compliance with GDPR.
9. **Environment Secret Segregation**: Database passwords, JWT keys, and API tokens are loaded exclusively from `.env` and are never committed to version control.
10. **Protected Observability**: Prometheus metrics endpoints are shielded behind Nginx HTTP Basic Authentication.

---

## Resources

### Official Documentation

- **Frontend**:
  - [React Documentation](https://react.dev/)
  - [Vite Documentation](https://vite.dev/)
  - [Tailwind CSS v4 Documentation](https://tailwindcss.com/docs)
  - [shadcn/ui Documentation](https://ui.shadcn.com/)
  - [Three.js Documentation](https://threejs.org/docs/)
  - [React Three Fiber Documentation](https://r3f.docs.pmnd.rs/)
  - [TanStack Table Documentation](https://tanstack.com/table/v8)
  - [Redux Toolkit Documentation](https://redux-toolkit.js.org/)
  - [react-i18next Documentation](https://react.i18next.com/)
  - [@dnd-kit Documentation](https://dndkit.com/)
- **Backend & Database**:
  - [FastAPI Documentation](https://fastapi.tiangolo.com/)
  - [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
  - [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
  - [PostgreSQL 15 Documentation](https://www.postgresql.org/docs/15/index.html)
  - [Redis Documentation](https://redis.io/docs/)
  - [Pydantic Documentation](https://docs.pydantic.dev/)
- **AI & RAG**:
  - [Ollama Documentation](https://github.com/ollama/ollama)
  - [BM25s GitHub Repository & Docs](https://github.com/xhl-c/bm25s)
  - [LangChain Text Splitters](https://python.langchain.com/docs/concepts/text_splitters/)
- **DevOps & Monitoring**:
  - [Docker & Docker Compose Documentation](https://docs.docker.com/)
  - [Prometheus Documentation](https://prometheus.io/docs/)
  - [Grafana Documentation](https://grafana.com/docs/)
  - [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
  - [Nginx Documentation](https://nginx.org/en/docs/)

### Articles and References

- *Asynchronous Python with FastAPI and SQLAlchemy 2.0*
- *Scaling WebSockets horizontally using Redis Pub/Sub*
- *Sparse Lexical Retrieval: Understanding the BM25 Algorithm*
- *WebGL and Three.js 3D Asset Optimization in React Applications*
- *RFC 6749: The OAuth 2.0 Authorization Framework*
- *RFC 7519: JSON Web Token (JWT) Architecture*

---

### AI Usage

In accordance with 42 curriculum guidelines, artificial intelligence tools were utilized responsibly as development accelerators. The breakdown of AI usage across the project is as follows:

1. **Documentation Synthesis & Exploration**:
   - Assisting in synthesizing modern framework changes (such as the migration to Tailwind CSS v4 and React 19 hook patterns).
   - Exploring best practices for configuring Alembic in an asynchronous SQLAlchemy 2.0 environment.
2. **Algorithm & RAG Design Brainstorming**:
   - Evaluating text chunking parameters (chunk size, overlap ratio) for the BM25 sparse index to optimize TFT question answering.
   - Designing the system prompt for the TFT assistant to eliminate hallucinations and enforce strict adherence to retrieved game context.
3. **Boilerplate & Schema Generation**:
   - Generating repetitive TypeScript interfaces and Pydantic validation schemas matching Riot Games and MetaTFT API payloads.
   - Drafting initial translation dictionary structures for multi-language support.
4. **Code Review & Debugging Support**:
   - Investigating subtle asynchronous race conditions in WebSocket connection lifecycles.
   - Suggesting linting compliance fixes for Ruff and ESLint.
5. **Documentation Structuring**:
   - Structuring and refining README sections according to 42 curriculum criteria.

*All architectural decisions, business logic, algorithmic implementations, and final code integrations were written, reviewed, tested, and validated by the team members.*

---

## Known Limitations

1. **Riot Games API Rate Limits**: Summoner lookups depend on a personal developer Riot Games API key, which is subject to Riot's default rate limits (20 requests per second, 100 requests per 2 minutes).
2. **Host-Dependent Ollama Service**: The AI assistant requires Ollama to run on the host machine (`ollama serve`). If Ollama is not active or `qwen3:0.6b` is not pulled, the chatbot endpoint will report an upstream connection error.
3. **Hardware Acceleration for 3D Models**: Rendering 3D champion models with WebGL relies on client GPU hardware acceleration; performance may vary on older hardware or non-accelerated virtual environments.
4. **Self-Signed SSL Certificate**: In the local development setup, the Nginx reverse proxy generates a self-signed SSL certificate, requiring a one-time security exception acceptance in the web browser.

---

## Future Improvements

- [ ] Support for user composition sharing and public upvoting in the social feed.
- [ ] Historical patch-by-patch comparison graphs for champion win rates.
- [ ] Real-time in-game match tracking overlay using the Riot Games In-Game Live Client API.
- [ ] Push notifications for friend requests and direct private messaging channels.
- [ ] Automated end-to-end integration test suite using Playwright or Cypress.
- [ ] Containerized Ollama service integrated directly into Docker Compose for single-command zero-host setup.

---

## License

This project was developed for educational purposes as part of the **42 Curriculum**.
[info] *(Add specific license information if applicable, e.g., MIT License).*

---

## Credits

Developed with passion by:
- **Nathan Bodin** (`nbodin`)
- **Sacha Servanton** (`sservant`)
- **Antoine Bonin** (`antbonin`)
- **Jules Clement Massonnat** (`julcleme`)

Special thanks to **42 Lyon Auvergne-Rhône-Alpes**, **Riot Games**, and **MetaTFT** for community data APIs.
