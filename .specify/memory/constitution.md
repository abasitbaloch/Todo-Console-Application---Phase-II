<!--
Sync Impact Report:
- Version: 1.0.0 → 2.0.0 (MAJOR - Breaking architectural changes)
- Modified principles:
  1. Spec-First Development → Spec-Driven Absolutism (strengthened with Task ID requirement)
  2. Deterministic Behavior → REMOVED (not applicable to stateful web apps)
  3. Separation of Concerns → Monorepo Separation (redefined for client/server architecture)
  4. AI-Generated Code Only → RETAINED (unchanged)
  5. CLI-First Interface → REMOVED (replaced with Web Interface)
  6. Simplicity and Clarity → RETAINED (unchanged)
- Added principles:
  7. User Isolation (absolute data privacy)
  8. Stateless Architecture (JWT-based authentication)
  9. Security First (API authentication requirements)
- Technology Stack: Complete replacement (Python CLI → Next.js + FastAPI + PostgreSQL)
- Constraints: Major changes (persistence now in scope, web interface now in scope)
- Templates requiring updates:
  ✅ plan-template.md - Constitution Check section aligns with new principles
  ✅ spec-template.md - User story structure supports web application requirements
  ✅ tasks-template.md - Task organization supports monorepo structure
  ⚠ PENDING: README.md needs update with Phase II setup instructions
  ⚠ PENDING: CLAUDE.md may need updates for web development guidance
- Follow-up TODOs:
  - User input was truncated at "Tasks survive a server resta" - assumed "restart"
  - Verify JWT shared secret configuration between frontend and backend
  - Document Neon PostgreSQL connection setup
-->

# Phase II Todo App Constitution

## Core Principles

### I. Spec-Driven Absolutism

No line of code shall be written without a corresponding Task ID from tasks.md. Every feature, requirement, and behavior must be explicitly documented in Markdown specifications, translated into an architectural plan, broken down into testable tasks, and only then implemented with explicit task references.

**Rationale**: Spec-Driven Development ensures complete traceability from user intent through design decisions to implementation artifacts. Task IDs create an audit trail that connects every code change to its originating requirement, enabling precise impact analysis and preventing scope drift.

**Rules**:
- MUST create or update spec.md before any code changes
- MUST obtain user approval on specifications before planning
- MUST create plan.md with architectural decisions before task generation
- MUST generate tasks.md with unique Task IDs before implementation
- MUST reference Task ID in every commit message (e.g., "Implementing T-001")
- MUST map every implementation artifact to an explicit task and requirement
- MUST NOT assume or infer undocumented features
- MUST NOT write code without a corresponding Task ID

### II. User Isolation

Absolute data privacy between users. A user MUST NEVER be able to query, view, modify, or access another user's data through any means—API endpoints, database queries, or application logic.

**Rationale**: Multi-user web applications require strict data isolation to maintain trust and comply with privacy expectations. Every data access operation must be scoped to the authenticated user's context.

**Rules**:
- MUST filter all database queries by authenticated user_id
- MUST validate user ownership before any read, update, or delete operation
- MUST NOT expose user_id in URLs or client-accessible identifiers
- MUST implement server-side authorization checks (never rely on client-side filtering)
- MUST test data isolation with multi-user scenarios
- MUST treat any cross-user data access as a critical security vulnerability

### III. Monorepo Separation

Clear architectural boundary between Client (Frontend) and Server (Backend). Each subsystem has distinct responsibilities, technology stacks, and deployment targets. Communication occurs exclusively through well-defined API contracts.

**Rationale**: Separation of concerns enables independent development, testing, and scaling of frontend and backend. Clear boundaries prevent tight coupling and allow technology choices optimized for each domain.

**Rules**:
- MUST maintain separate `/frontend` and `/backend` directories at repository root
- MUST define API contracts before implementation (in specs/[feature]/contracts/)
- MUST NOT import backend code into frontend or vice versa
- MUST communicate exclusively through HTTP REST APIs
- MUST version API contracts and handle breaking changes explicitly
- MUST enable independent deployment of frontend and backend

### IV. Stateless Architecture

The backend relies entirely on JWT tokens for authentication context, storing no session state in memory or database. Every request is self-contained and independently verifiable.

**Rationale**: Stateless architecture enables horizontal scaling, simplifies deployment, and eliminates session synchronization complexity. JWT tokens carry all necessary authentication context, making each request independently processable.

**Rules**:
- MUST authenticate every protected request via JWT token in Authorization header
- MUST extract user_id from verified JWT claims (never from request body or query params)
- MUST NOT store session state in backend memory or database
- MUST share JWT signing secret between frontend auth system and backend verification
- MUST validate JWT signature and expiration on every protected endpoint
- MUST treat missing or invalid JWT as unauthorized (401) response

### V. AI-Generated Code Only

All source code MUST be generated by Claude Code from approved specifications and tasks. No manual coding, no direct file editing, no human-written implementation.

**Rationale**: This principle validates the Spec-Driven Development methodology and ensures consistency between specification, plan, tasks, and implementation. It demonstrates AI-native development patterns and maintains traceability.

**Rules**:
- MUST use Claude Code for all code generation
- MUST generate code from tasks.md with explicit Task ID references
- MUST NOT manually edit generated source files
- MUST regenerate code if specifications or tasks change
- MUST document any exceptions in ADRs with explicit justification

### VI. Simplicity and Clarity

Choose simple solutions over clever ones. Prefer readability over brevity. Avoid premature optimization, abstraction, or generalization. Build only what the specification requires.

**Rationale**: Simple code is maintainable code. Clarity demonstrates understanding. This is a Phase II MVP demonstrating full-stack capabilities, not production-scale software requiring complex optimizations.

**Rules**:
- MUST prefer straightforward implementations
- MUST NOT add features beyond specification scope
- MUST NOT create abstractions for single-use cases
- MUST write code that can be understood in a single reading
- MUST follow YAGNI (You Aren't Gonna Need It)
- MUST prioritize working software over architectural perfection

### VII. Security First

All API routes (except `/health` and `/auth/*`) MUST verify the `Authorization: Bearer <token>` header. Security is not optional, not deferred, and not negotiable.

**Rationale**: Web applications are exposed to untrusted networks and malicious actors. Authentication and authorization must be enforced at the API gateway level before any business logic executes.

**Rules**:
- MUST require valid JWT token for all protected endpoints
- MUST return 401 Unauthorized for missing or invalid tokens
- MUST return 403 Forbidden for valid tokens with insufficient permissions
- MUST validate input data against strict schemas (Pydantic on backend, Zod on frontend)
- MUST sanitize all user inputs to prevent injection attacks
- MUST NOT expose sensitive data (secrets, tokens, internal IDs) in responses or logs
- MUST use HTTPS in production (enforced at deployment level)

## Technology Stack

### Frontend
**Framework**: Next.js 16+ (App Router)
- TypeScript (Strict mode enabled)
- React Server Components where applicable
- Client components for interactivity

**Styling**: Tailwind CSS
- Modern SaaS aesthetic
- Consistent spacing and typography
- Responsive design (mobile-first)

**UI Components**:
- lucide-react for icons
- Shadcn/ui or custom components following design system

**Authentication**: Better Auth
- Issues JWT tokens on successful login
- Manages token refresh and expiration
- Handles user registration and password reset

**API Client**:
- Fetch API or axios for HTTP requests
- Authorization header injection for protected routes
- Type-safe request/response handling

### Backend
**Framework**: FastAPI (Python 3.13+)
- Async/await for I/O operations
- Automatic OpenAPI documentation
- Pydantic v2 for request/response validation

**ORM**: SQLModel
- Type-safe database operations
- Alembic for schema migrations
- Pydantic integration for validation

**Database**: Neon Serverless PostgreSQL
- Connection pooling via asyncpg
- Environment-based configuration
- Migration management

**Authentication**: JWT Verification
- Shared secret with Better Auth (frontend)
- python-jose or PyJWT for token verification
- User context extraction from claims

**API Design**: RESTful
- JSON request/response bodies
- Standard HTTP status codes
- Typed error responses

### Development Tools
**Version Control**: Git
- Feature branches per spec
- Conventional commit messages with Task IDs
- Pull requests for review

**Spec Management**: Spec-Kit Plus
- Markdown specifications in `/specs`
- Templates in `/.specify/templates`
- Scripts in `/.specify/scripts`

**Code Generation**: Claude Code
- AI-driven implementation from tasks
- Prompt History Records (PHRs) for traceability
- Architecture Decision Records (ADRs) for significant choices

## Development Workflow

### 1. Specification Phase
1. User provides feature requirements
2. Claude Code creates or updates spec.md with user stories and acceptance criteria
3. User reviews and approves specification
4. Specification frozen until planning complete

### 2. Planning Phase
1. Claude Code analyzes specification
2. Creates plan.md with technical approach and architecture decisions
3. Defines data models in data-model.md
4. Defines API contracts in contracts/ directory
5. Creates quickstart.md for feature validation
6. User approves plan

### 3. Task Generation
1. Claude Code generates tasks.md from approved spec and plan
2. Tasks are concrete, testable, and ordered by dependencies
3. Each task has unique ID (T-001, T-002, etc.)
4. Tasks organized by user story for independent delivery
5. User approves task list

### 4. Implementation Phase
1. Claude Code implements tasks in dependency order
2. Each commit references Task ID in message
3. Code is generated, not manually written
4. Frontend and backend developed in parallel where possible
5. API contracts enforced between subsystems

### 5. Validation Phase
1. User tests implementation against specification
2. Verification of acceptance criteria per user story
3. Bug reports reference specific spec requirements and Task IDs
4. Cycle back to specification if changes needed

### 6. Documentation Phase
1. Update README.md with setup instructions
2. Ensure CLAUDE.md reflects actual usage patterns
3. Document architectural decisions in ADRs
4. Create Prompt History Records (PHRs) for all major interactions

## Constraints

### In Scope (Phase II)
- User authentication and registration (Better Auth)
- JWT-based stateless authentication
- Multi-user support with data isolation
- Full CRUD operations on todos (Create, Read, Update, Delete, Mark Complete)
- Persistent storage in PostgreSQL database
- RESTful API backend (FastAPI)
- Modern web UI (Next.js + Tailwind)
- Responsive design (desktop and mobile)
- API authentication and authorization
- Database migrations and schema management

### Out of Scope (Phase II)
- Real-time collaboration or WebSockets
- Advanced todo features (tags, priorities, due dates, attachments, subtasks)
- Search and filtering beyond basic list view
- Email notifications or external integrations
- Social features (sharing, comments, collaboration)
- Performance optimization beyond basic responsiveness
- Internationalization or localization
- Advanced security (2FA, OAuth providers, rate limiting)
- Analytics or usage tracking
- Admin dashboard or user management UI

### Non-Negotiable Requirements
- Next.js 16+ (App Router) for frontend
- Python 3.13+ with FastAPI for backend
- Neon Serverless PostgreSQL for database
- Better Auth for frontend authentication
- JWT tokens for backend authentication
- Monorepo structure (`/frontend`, `/backend`, `/specs`, `/.specify`)
- All API routes (except `/health` and `/auth/*`) require valid JWT
- Absolute user data isolation (no cross-user access)
- Task ID references in all commits
- AI-generated code only (via Claude Code)
- Specification approval required before implementation

## Governance

### Amendment Process
1. Propose constitutional change with rationale
2. Document in ADR if architecturally significant
3. Update constitution version (semantic versioning)
4. Propagate changes to dependent templates (plan, spec, tasks)
5. Update CLAUDE.md if agent guidance changes
6. Create sync impact report (HTML comment at top of file)
7. Commit with clear change description

### Versioning Policy
- **MAJOR** (X.0.0): Breaking changes to core principles, technology stack, or architectural constraints
- **MINOR** (0.X.0): New principle added or existing principle materially expanded
- **PATCH** (0.0.X): Clarifications, wording fixes, non-semantic changes

### Compliance
- All specifications MUST reference constitution principles
- All plans MUST include "Constitution Check" gate
- All tasks MUST map to approved plan and spec
- All commits MUST reference Task IDs
- All code reviews MUST verify constitutional compliance
- Violations MUST be justified in plan.md Complexity Tracking table
- No violations permitted without explicit user approval and ADR documentation

### Success Criteria
This constitution succeeds when:
- Users can register, login, and manage their own todos
- Frontend successfully authenticates with backend via JWT
- Backend correctly extracts user_id from JWT and enforces data isolation
- Todos persist across server restarts (database storage)
- No user can access another user's data
- All code is traceable to Task IDs and specifications
- Application exhibits modern, polished UI/UX
- Codebase is readable, maintainable, and follows architectural boundaries
- Phase II deliverables demonstrate full-stack AI-native development

**Version**: 2.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2026-01-07
