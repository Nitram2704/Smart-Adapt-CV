# PLAN: ATS Foreign Extension & Keyword Engine

## Context
Extend the Smart-Adapt CV system with a minimalist, high-parseability template for foreign markets (USA/EU) and an interactive keyword optimization workflow.

## Objectives
1. **ATS Foreign Template**: A 1-column, no-sidebar, minimalist design based on provided reference PDFs.
2. **Keyword Suggestion Engine**: A UI flow to identify missing keywords and naturally integrate them into the CV with user approval.
3. **Hybrid Architecture**: Ensure both Latam (Esthetics) and Foreign (ATS) flows coexist without interference.

## Phase 1: Foundation (Planning & Backend)
- [ ] Finalize `ats_foreign_template.html` (Minimalist, 1-column).
- [ ] Implement `POST /cv/generate-ats` endpoint.
- [ ] Implement `POST /ai/optimize-bullet` for targeted keyword integration.

## Phase 2: Core Implementation (Frontend)
- [ ] Add "ATS Foreign" tab to `ResultsView.tsx`.
- [ ] Build `KeywordOptimizer.tsx` for interactive suggest/diff/apply flow.
- [ ] Integrate keyword engine with backend AI rewriting logic.

## Phase 3: Polish & Verification
- [ ] Run PDF parseability tests on the new template.
- [ ] Verify "Zero Overwrite" policy (Latam flow remains untouched).
- [ ] Final security and linting checks.

## Agent Assignments
- **project-planner**: Orchestration and PLAN.md.
- **backend-specialist**: Template and FastAPI endpoints.
- **frontend-specialist**: React components and keyword UI.
- **test-engineer**: Verification scripts and PDF audits.
