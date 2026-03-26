# Security Audit Report - Smart-Adapt CV

**Date:** 2026-03-23
**Auditor:** Claude Code
**Scope:** Frontend (Next.js 16 + React 19) + Backend (FastAPI + Python)

---

## 🔴 CRITICAL VULNERABILITIES

### 1. XSS (Cross-Site Scripting) - KeywordOptimizer.tsx:133
**Location:** `frontend/src/components/KeywordOptimizer.tsx:133`

```tsx
dangerouslySetInnerHTML={{ __html: exp.suggested_rewrite }}
```

**Risk:** The LLM-generated content is rendered directly as HTML without sanitization. An attacker could potentially inject malicious JavaScript.

**Fix:** Use a sanitization library like DOMPurify:
```tsx
import DOMPurify from 'dompurify';
// ...
dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(exp.suggested_rewrite) }}
```

---

### 2. XSS in Cover Letter - main.py:282
**Location:** `backend/main.py:282`

```python
"content_body": cl_data.get("content", "").replace("\n", "<br>")
```

**Risk:** LLM-generated cover letter content is injected as HTML without escaping.

**Fix:** Escape HTML entities or use a template engine with auto-escaping.

---

## 🟠 HIGH SEVERITY

### 3. CORS Misconfiguration - main.py:39
**Location:** `backend/main.py:36-43`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ❌ Too permissive
    allow_credentials=True,  # ❌ Dangerous with allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Risk:** Allows any website to make authenticated requests to your API.

**Fix:** Restrict to specific origins:
```python
allow_origins=["http://localhost:3000", "https://yourdomain.com"]
```

---

### 4. Path Traversal - main.py:128
**Location:** `backend/main.py:124-130`

```python
upload_path = os.path.join(INPUTS_DIR, file.filename)  # ❌ No sanitization
with open(upload_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
```

**Risk:** Users can upload files with paths like `../../../etc/passwd`.

**Fix:** Generate safe filenames:
```python
import uuid
from werkzeug.utils import secure_filename

safe_filename = secure_filename(file.filename)
upload_path = os.path.join(INPUTS_DIR, f"{uuid.uuid4()}_{safe_filename}")
```

---

### 5. Unprotected Static Files - main.py:30
**Location:** `backend/main.py:30`

```python
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")
```

**Risk:** Anyone can access generated CVs/PDFs if they guess the filename.

**Fix:** Add authentication middleware or serve files through authenticated endpoints.

---

## 🟡 MEDIUM SEVERITY

### 6. No Rate Limiting
**Location:** All API endpoints

**Risk:** API can be abused for DDoS or excessive LLM API costs.

**Fix:** Implement rate limiting with slowapi:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/cv/parse")
@limiter.limit("10/minute")
async def parse_cv(...):
```

---

### 7. Excessive API Keys in Environment
**Location:** `backend/main.py:51-59`

**Risk:** Multiple API keys increase attack surface. If one leaks, others may too.

**Fix:** Use a single key rotation strategy or secrets manager.

---

### 8. Type Safety Issues
**Location:** Frontend multiple files

**Risk:** Use of `any` type everywhere makes type-based security analysis impossible.

**Fix:** Define proper TypeScript interfaces for all data structures.

---

## 🟢 LOW SEVERITY

### 9. Information Disclosure in Debug Logs
**Location:** Multiple `print(f"DEBUG: ...")` statements

**Risk:** Sensitive data may leak in logs.

**Fix:** Use proper logging levels and redact sensitive data.

---

### 10. No Input Size Limits
**Location:** All endpoints accepting text

**Risk:** Very large job descriptions could cause memory issues or excessive LLM costs.

**Fix:** Add Pydantic validators with max_length constraints.

---

## 📋 RECOMMENDATIONS SUMMARY

| Priority | Issue | Effort | Impact |
|----------|-------|--------|--------|
| 🔴 P0 | Fix XSS in KeywordOptimizer | Low | High |
| 🔴 P0 | Fix CORS configuration | Low | High |
| 🔴 P0 | Add path traversal protection | Low | High |
| 🟠 P1 | Protect static files | Medium | Medium |
| 🟠 P1 | Add rate limiting | Medium | Medium |
| 🟡 P2 | Add input validation | Low | Medium |
| 🟡 P2 | Remove debug logging from prod | Low | Low |
| 🟢 P3 | Add TypeScript types | Medium | Low |

---

## 🛠️ IMMEDIATE ACTIONS REQUIRED

1. **Sanitize all LLM outputs** before rendering as HTML
2. **Restrict CORS** to specific origins only
3. **Validate filenames** before saving uploads
4. **Add authentication** to `/outputs` endpoint
5. **Implement rate limiting** on AI endpoints
