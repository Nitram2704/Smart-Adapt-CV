# Antigravity Kit + ECC Architecture

> Comprehensive AI Agent Capability Expansion Toolkit
>
> **Fusion of Antigravity Kit + Everything Claude Code (ECC)**

---

## Overview

This is a unified framework combining:
- **Antigravity Kit** - Original skills, agents, and workflows
- **Everything Claude Code (ECC)** - 125+ additional skills, 28 agents, 60 commands

### Stats

| Metric               | Count |
|---------------------|-------|
| **Agents**          | 48    |
| **Skills**          | 160   |
| **Commands**        | 60    |
| **Workflows**       | 11    |
| **Rules**           | 12 languages |
| **Hooks**           | Hooks system with hooks.json |
| **Contexts**        | 3 (dev, research, review) |
| **MCP Configs**     | MCP server configurations |

---

## Directory Structure

```
.agent/
├── ARCHITECTURE.md          # This file
├── agents/                  # 48 Specialist Agents
├── skills/                  # 160 Skills
├── commands/                # 60 Slash Commands (from ECC)
├── workflows/               # 11 Workflows (from Antigravity)
├── rules/                   # Language-specific rules
│   ├── common/             # Universal rules
│   ├── python/             # Python patterns
│   ├── typescript/         # TypeScript/JS rules
│   ├── golang/             # Go patterns
│   ├── rust/               # Rust patterns
│   └── ...                 # 12 languages total
├── hooks/                   # Hook automations
│   ├── hooks.json          # Hook definitions
│   └── README.md           # Hook documentation
├── contexts/               # Dynamic context injection
│   ├── dev.md
│   ├── research.md
│   └── review.md
├── mcp-configs/            # MCP server configurations
├── scripts/                # Validation scripts
└── .shared/                # Shared resources (ui-ux-pro-max)
```

---

## Agents (48)

### From Antigravity Kit (20)

| Agent                    | Focus                      |
| ------------------------ | -------------------------- |
| `orchestrator`           | Multi-agent coordination   |
| `project-planner`        | Discovery, task planning   |
| `frontend-specialist`    | Web UI/UX                  |
| `backend-specialist`     | API, business logic        |
| `database-architect`     | Schema, SQL                |
| `mobile-developer`       | iOS, Android, RN           |
| `game-developer`         | Game logic, mechanics      |
| `devops-engineer`        | CI/CD, Docker              |
| `security-auditor`       | Security compliance        |
| `penetration-tester`     | Offensive security         |
| `test-engineer`          | Testing strategies         |
| `debugger`               | Root cause analysis        |
| `performance-optimizer`  | Speed, Web Vitals          |
| `seo-specialist`         | Ranking, visibility        |
| `documentation-writer`   | Manuals, docs              |
| `product-manager`        | Requirements, user stories |
| `product-owner`          | Strategy, backlog, MVP     |
| `qa-automation-engineer` | E2E testing, CI pipelines  |
| `code-archaeologist`     | Legacy code, refactoring   |
| `explorer-agent`         | Codebase analysis          |

### From ECC (28)

| Agent                    | Focus                      |
| ------------------------ | -------------------------- |
| `planner`                | Feature implementation planning |
| `architect`              | System design decisions    |
| `tdd-guide`              | Test-driven development    |
| `code-reviewer`          | Quality and security review |
| `security-reviewer`      | Vulnerability analysis     |
| `build-error-resolver`   | Build error resolution     |
| `e2e-runner`             | Playwright E2E testing     |
| `refactor-cleaner`       | Dead code cleanup          |
| `doc-updater`            | Documentation sync         |
| `docs-lookup`            | Documentation/API lookup    |
| `chief-of-staff`         | Communication triage       |
| `loop-operator`          | Autonomous loop execution   |
| `harness-optimizer`      | Harness config tuning      |
| `typescript-reviewer`    | TypeScript/JavaScript review |
| `python-reviewer`        | Python code review         |
| `go-reviewer`            | Go code review             |
| `go-build-resolver`      | Go build errors            |
| `java-reviewer`          | Java code review           |
| `java-build-resolver`    | Java build errors          |
| `kotlin-reviewer`        | Kotlin code review         |
| `kotlin-build-resolver`  | Kotlin build errors        |
| `rust-reviewer`          | Rust code review           |
| `rust-build-resolver`    | Rust build errors          |
| `cpp-reviewer`           | C++ code review            |
| `cpp-build-resolver`     | C++ build errors           |
| `database-reviewer`      | Database/Supabase review   |
| `pytorch-build-resolver` | PyTorch/CUDA errors        |
| `flutter-reviewer`       | Flutter/Dart code review   |

---

## Skills (160)

### Categories

#### AI/LLM (New from ECC)
- `claude-api` - Claude SDK usage, streaming, tool use
- `prompt-optimizer` - Analyzes and optimizes prompts
- `continuous-learning` - Auto-extracts patterns from sessions
- `continuous-learning-v2` - Advanced pattern extraction
- `cost-aware-llm-pipeline` - Cost optimization for LLM calls
- `ai-first-engineering` - AI-native development patterns

#### Python/Backend
- `python-patterns` - Type hints, error handling, context managers
- `python-testing` - pytest patterns, mocking, fixtures
- `django-patterns` - Django best practices
- `django-security` - Django security patterns
- `django-tdd` - Django test-driven development
- `postgres-patterns` - PostgreSQL optimization, RLS
- `api-design` - REST conventions, pagination, versioning

#### Frontend/Next.js
- `frontend-patterns` - React composition, hooks, performance
- `nextjs-turbopack` - Turbopack optimization
- `nuxt4-patterns` - Nuxt.js patterns

#### Testing
- `tdd-workflow` - Test-driven development workflow
- `e2e-testing` - End-to-end testing patterns
- `verification-loop` - Automated verification cycles
- `benchmark` - Performance benchmarking

#### DevOps/Infrastructure
- `docker-patterns` - Dockerfile best practices, Compose
- `deployment-patterns` - CI/CD, deployment strategies
- `mcp-server-patterns` - Model Context Protocol servers

#### Security
- `security-review` - Input validation, XSS/CSRF prevention
- `security-scan` - Security scanning automation

#### Languages
- `golang-patterns`, `golang-testing`
- `rust-patterns`, `rust-testing`
- `java-coding-standards`, `jpa-patterns`
- `kotlin-patterns`, `kotlin-coroutines-flows`
- `swiftui-patterns`, `swift-concurrency-6-2`
- `cpp-coding-standards`, `cpp-testing`
- `perl-patterns`, `perl-security`

#### Frameworks
- `springboot-patterns`, `springboot-security`
- `laravel-patterns`, `laravel-security`
- `flutter-dart-code-review`

#### Specialized
- `pytorch-patterns` - PyTorch/CUDA patterns
- `clickhouse-io` - ClickHouse database patterns
- `android-clean-architecture` - Android Clean Architecture

#### Meta/Utility
- `configure-ecc` - ECC setup and configuration
- `skill-stocktake` - Audit installed components
- `search-first` - Research-first development
- `blueprint` - Epic-scope project planning

---

## Commands (60)

From ECC - invoke with `/command`:

### Planning & Execution
- `/plan` - Feature implementation planning
- `/tdd` - Test-driven development workflow
- `/code-review` - Code quality review
- `/build-fix` - Build error resolution
- `/e2e` - End-to-end testing
- `/refactor-clean` - Dead code cleanup

### Learning & Evolution
- `/learn` - Extract patterns from session
- `/learn-eval` - Evaluate learned patterns
- `/instinct-status` - Check instinct status
- `/evolve` - Evolve learned skills

### Multi-Agent
- `/multi-plan` - Multi-agent planning
- `/multi-execute` - Multi-agent execution
- `/multi-backend` - Backend-focused multi-agent
- `/multi-frontend` - Frontend-focused multi-agent
- `/orchestrate` - Agent coordination

### Language-Specific
- `/python-review` - Python code review
- `/go-review`, `/go-test`, `/go-build` - Go workflow
- `/kotlin-review`, `/kotlin-test`, `/kotlin-build` - Kotlin
- `/rust-review`, `/rust-test`, `/rust-build` - Rust
- `/cpp-review`, `/cpp-test`, `/cpp-build` - C++

### Quality
- `/security-scan` - Security vulnerability scan
- `/test-coverage` - Test coverage analysis
- `/quality-gate` - Quality gate enforcement
- `/verify` - Verification workflow

### Session Management
- `/save-session` - Save session state
- `/resume-session` - Resume saved session
- `/sessions` - List all sessions
- `/checkpoint` - Create checkpoint

### Project Management
- `/pm2` - Project management workflow
- `/setup-pm` - Setup project management
- `/projects` - List projects

### Utilities
- `/prompt-optimize` - Optimize prompts
- `/harness-audit` - Audit harness configuration
- `/model-route` - Model routing
- `/context-budget` - Context budget management

---

## Workflows (11)

From Antigravity Kit:

| Command          | Description              |
| ---------------- | ------------------------ |
| `/brainstorm`    | Socratic discovery       |
| `/create`        | Create new features      |
| `/debug`         | Debug issues             |
| `/deploy`        | Deploy application       |
| `/enhance`       | Improve existing code    |
| `/orchestrate`   | Multi-agent coordination |
| `/plan`          | Task breakdown           |
| `/preview`       | Preview changes          |
| `/status`        | Check project status     |
| `/test`          | Run tests                |
| `/ui-ux-pro-max` | Design with 50 styles    |

---

## Rules (12 Languages)

Language-specific coding rules in `rules/`:

| Directory    | Language        |
| ------------ | --------------- |
| `common/`    | Universal rules |
| `python/`    | Python          |
| `typescript/`| TypeScript/JS   |
| `golang/`    | Go              |
| `rust/`      | Rust            |
| `java/`      | Java            |
| `kotlin/`    | Kotlin          |
| `cpp/`       | C++             |
| `swift/`     | Swift           |
| `php/`       | PHP             |
| `csharp/`    | C#              |
| `perl/`      | Perl            |

---

## Hooks

The hooks system allows automatic actions on events:

Located in `hooks/hooks.json` with documentation in `hooks/README.md`.

Hook types:
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool execution
- `Stop` - On session end

---

## Contexts

Dynamic system prompt injection for different modes:

| Context      | Purpose                    |
| ------------ | -------------------------- |
| `dev.md`     | Development context        |
| `research.md`| Research context           |
| `review.md`  | Code review context        |

---

## Quick Reference

| Need        | Agent                 | Skills                                |
| ----------- | --------------------- | ------------------------------------- |
| Web App     | `frontend-specialist` | `frontend-patterns`, `react-best-practices` |
| API         | `backend-specialist`  | `api-patterns`, `python-patterns`    |
| Database    | `database-architect`  | `postgres-patterns`, `database-design` |
| Security    | `security-reviewer`   | `security-review`, `security-scan`    |
| Testing     | `tdd-guide`           | `tdd-workflow`, `testing-patterns`    |
| Debug       | `debugger`            | `systematic-debugging`                |
| Plan        | `planner`             | `plan-writing`, `brainstorming`      |
| AI/LLM      | -                     | `claude-api`, `prompt-optimizer`      |
| Docker      | `devops-engineer`     | `docker-patterns`                    |

---

## Sources

- **Antigravity Kit** - Original framework
- **Everything Claude Code (ECC)** - by affaan-m (Anthropic Hackathon Winner)
  - GitHub: https://github.com/affaan-m/everything-claude-code
  - License: MIT