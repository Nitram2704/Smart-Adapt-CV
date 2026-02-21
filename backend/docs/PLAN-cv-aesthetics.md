# 🎼 Orchestration Plan: Aesthetic Refinement (Option A)

## Context
Goal: Elevate the CV's visual appeal to a "Premium" level while maintaining a single-page layout.
**User Preferences:** Professional typography, blue accents (matching the header), minimalist icons for contact/skills, and a sharp professional finish.

## Agents & Roles
1. **`project-planner`**: Coordinate the visual system and consistency.
2. **`frontend-specialist`**: Implement modern CSS, custom font stacks (Inter/Roboto), and SVG icons.
3. **`test-engineer`**: Verify visual integrity and single-page fit.

## Phase 1: Planning (Current)
- [x] Brainstorm options and gather user preferences.
- [ ] Define the design system (Typography, Colors, Spacing).
- [ ] Create `docs/PLAN-cv-aesthetics.md`.

## Phase 2: Implementation (Pending Approval)
### Step 1: Typography & Global Styles (Frontend Specialist)
- Import **Inter** via Google Fonts (or use a robust system stack).
- Apply `font-family: 'Inter', sans-serif;` for body content.
- Increase H1/H2 font-weight and letter-spacing for a premium feel.

### Step 2: Color Palette & Icons (Frontend Specialist)
- Define a professional **Deep Blue** accent (`#1a365d` or similar) for separators and icons.
- Replace text-based icons (📞, @) with clean **SVG icons**.
- Add subtle shadow to the sidebar or header for depth.

### Step 3: Geometry & Polish (Frontend Specialist)
- Apply sharp-yet-refined borders (`border-radius: 2px`).
- Refine separator lines with the new accent color.
- Ensure the "Experience" section uses consistent indentation.

### Step 4: Verification (Test Engineer)
- Render the final PDF via `fast_render.py`.
- Verify the PDF still fits on **1 page** using `check_pdf_pages.py`.
- Manual visual audit of the generated PDF.

## Execution Order
1. **Frontend Specialist:** Design System & CSS.
2. **Frontend Specialist:** SVG Icon integration.
3. **Test Engineer:** PDF verification.
