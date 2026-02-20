# 🎼 Orchestration Plan: Robust PDF Rendering

## Context
The current `WeasyPrint` setup on Windows is failing to render modern CSS layouts (Flexbox/Float), resulting in "invisible" content.
**Goal:** Implement a "Bulletproof" PDF layout using **HTML Tables** and **System Fonts**.

## Agents & Roles
1.  **`project-planner`**: Define the architecture of the Table-based layout.
2.  **`frontend-specialist`**: Rewrite `cv_template.html` using `<table>` for the main grid (Sidebar vs Content).
3.  **`backend-specialist`**: Force font fallback to `Arial/Helvetica` to prevent font rendering failures.

## Phase 1: Planning (Current)
- [x] Analyze failure modes (Flexbox = Collapse, Float = Unstable).
- [x] Select solution: **Table Layout** (Old-school but 100% reliable for PDF).

## Phase 2: Implementation (Pending Approval)
### Step 1: Font Safety (Backend Specialist)
- Update CSS to use `font-family: Arial, sans-serif;` strictly.
- Remove any reliance on 'Segoe UI' which might be blocked by WeasyPrint's sandbox.

### Step 2: Table Layout (Frontend Specialist)
- **Structure:**
  ```html
  <table width="100%" style="border-collapse: collapse;">
    <tr>
      <td width="30%" valign="top" class="sidebar">...</td>
      <td width="5%"></td> <!-- Spacer -->
      <td width="65%" valign="top" class="content">...</td>
    </tr>
  </table>
  ```
- **Why:** Tables enforce width and height even when CSS fails to load perfectly.

### Step 3: Verification (Test Engineer)
- Run `test_pdf_render.py`.
- Verify PDF size > 30KB.
- **Critical Check:** Text extraction test.

## Execution Order
1.  **Backend Specialist:** Sanitize Fonts.
2.  **Frontend Specialist:** Implement Table Layout.
3.  **Test Engineer:** Verify output.
