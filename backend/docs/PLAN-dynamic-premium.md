# Orchestration Plan: Dynamic Premium Content Adaptation

**Goal:** Automate the "Opción A" logic into the `AIEngine` so that all future CV generations automatically feature high-impact quantified achievements and senior-level technical language.

## Agents & Roles
1.  **`project-planner`**: Coordinate the integration of premium instructions into the existing STAR methodology.
2.  **`backend-specialist`**: Refine the prompts in `backend/core/ai_engine.py` to enforce the "Senior Persona" rules.
3.  **`test-engineer`**: Verify that the generated content correctly balances high-impact language with factual accuracy and still fits on 1 page.

## Phase 1: Planning (Current)
- [x] Analyze `ai_engine.py` prompt structure.
- [x] Define "Senior Persona" prompt requirements (metrics, strong verbs, scale).
- [ ] Create this plan and obtain user approval.

## Phase 2: Implementation (Pending)

### Step 1: Prompt Engineering (Backend Specialist)
- Update `generate_optimized_content` system prompt.
- **Rules to Inject**:
    - "Every highlight must include at least one metric or scale indicator (e.g., %, ms, scale of data)."
    - "Use active, senior-level verbs: Architected, Orchestrated, Engineered, Deployed."
    - "Strictly follow STAR but normalize for 'Executive Impact'."

### Step 2: Logic Verification (Test Engineer)
- Generate a CV for a new job description using the updated engine.
- Verify that the resulting highlights are significantly higher impact than the default.
- Use `check_pdf_pages.py` to confirm 1-page compliance.

### Step 3: Polish (Backend Specialist)
- Ensure the prompt doesn't cause hallucinations if the master profile is thin.
- Add fallbacks for "Metric-lite" roles.

---

## ⏸️ CHECKPOINT: User Approval
✅ Plan creado: `backend/docs/PLAN-dynamic-premium.md`

**¿Onaylıyor musunuz? (Y/N)**
- Y: Implementation başlatılır
- N: Planı düzeltirim
