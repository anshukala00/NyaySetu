# End-to-End Testing Checklist

## Prerequisites
- [ ] PostgreSQL is running on port 5432
- [ ] Database is seeded with test data (run `backend/scripts/seed_data.py`)
- [ ] Backend server is running on http://localhost:8000
- [ ] Frontend server is running on http://localhost:3000

## Quick Start
```bash
# Option 1: Use the batch file (Windows)
START_SERVERS.bat

# Option 2: Manual start
# Terminal 1 - Backend (PowerShell)
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend (WSL)
cd /mnt/d/NyaySetu/frontend
npm run dev
```

## Test Credentials
- **Citizen:** citizen1@example.com / password123
- **Judge:** judge1@example.com / password123

---

## Test 1: Auth Persistence (Reload Page)

### Steps:
1. [ ] Open http://localhost:3000
2. [ ] Click "Login" button
3. [ ] Login as citizen (citizen1@example.com / password123)
4. [ ] Verify redirect to /citizen-portal
5. [ ] Verify cases are displayed
6. [ ] **Press F5 to reload the page**
7. [ ] Verify you're still logged in (not redirected to login)
8. [ ] Verify cases are still displayed
9. [ ] Open DevTools Console (F12)
10. [ ] Check for these logs:
    - `Initializing auth: { token: 'exists', userId: '...', userRole: 'CITIZEN', email: '...' }`
    - `Fetching cases for citizen...`
    - `Cases fetched successfully: [...]`

### Expected Result:
✅ User remains logged in after page reload
✅ Cases are automatically loaded after reload
✅ No redirect to login page

---

## Test 2: Judge Sees All Cases

### Steps:
1. [ ] Logout if logged in
2. [ ] Login as judge (judge1@example.com / password123)
3. [ ] Verify redirect to /judge-dashboard
4. [ ] Click "All Cases" tab in sidebar
5. [ ] Open DevTools Console (F12)
6. [ ] Check for these logs:
    - `Fetching all cases for judge...`
    - `Cases fetched successfully: [...]`
7. [ ] Verify you see cases from multiple citizens (not just one user)
8. [ ] Count the number of cases displayed
9. [ ] Verify it matches the total in the database (should be 17 cases)

### Expected Result:
✅ Judge sees all cases in the system (17 total)
✅ Cases from different citizens are visible
✅ Case list shows: title, status, priority, filing date

---

## Test 3: Citizen Sees Only Own Cases

### Steps:
1. [ ] Logout if logged in
2. [ ] Login as citizen (citizen1@example.com / password123)
3. [ ] Navigate to "My Cases" tab
4. [ ] Open DevTools Console (F12)
5. [ ] Check for these logs:
    - `Fetching cases for citizen...`
    - `Cases fetched successfully: [...]`
6. [ ] Verify you only see cases filed by citizen1
7. [ ] Count the number of cases (should be 4 cases for citizen1)
8. [ ] Verify no cases from other citizens are visible

### Expected Result:
✅ Citizen sees only their own cases (4 total)
✅ No cases from other citizens are visible
✅ Authorization is working correctly

---

## Test 4: File New Case

### Steps:
1. [ ] Login as citizen (citizen1@example.com / password123)
2. [ ] Click "File New Case" button on dashboard
3. [ ] Verify navigation to case filing form
4. [ ] Fill in case title: "Test Case - E2E"
5. [ ] Fill in case description: "This is an urgent test case for E2E testing"
6. [ ] Click "Submit Case" button
7. [ ] Open DevTools Console (F12)
8. [ ] Check for success message
9. [ ] Verify redirect to case list or case detail view
10. [ ] Verify new case appears in "My Cases" list
11. [ ] Verify case has status "FILED"
12. [ ] Verify case has priority "HIGH" (because description contains "urgent")

### Expected Result:
✅ Case is successfully created
✅ AI triage automatically assigns HIGH priority
✅ Case appears in citizen's case list
✅ Case has correct status and priority

---

## Test 5: Click to Expand Case Details

### Steps:
1. [ ] Login as citizen (citizen1@example.com / password123)
2. [ ] Navigate to "My Cases" tab
3. [ ] Verify cases are displayed as cards
4. [ ] Click on any case card
5. [ ] Verify case details expand/appear
6. [ ] Verify you can see:
    - Full case title
    - Full case description
    - Status badge
    - Priority badge
    - Filing date
    - AI summary (if available)
7. [ ] Click on another case
8. [ ] Verify the previous case collapses and new case expands

### Expected Result:
✅ Cases are clickable
✅ Case details expand on click
✅ Full case information is visible
✅ Only one case is expanded at a time

---

## Test 6: Generate AI Summary (Judge)

### Steps:
1. [ ] Login as judge (judge1@example.com / password123)
2. [ ] Navigate to "All Cases" tab
3. [ ] Click on a case that doesn't have an AI summary
4. [ ] Verify case details are displayed
5. [ ] Click "Generate AI Summary" button
6. [ ] Verify loading spinner appears
7. [ ] Wait for summary generation
8. [ ] Verify AI summary appears with "[AI Generated Summary]" badge
9. [ ] Verify summary is saved (reload page and check it's still there)

### Expected Result:
✅ AI summary is generated successfully
✅ Summary is displayed in the UI
✅ Summary persists after page reload

---

## Test 7: Precedent Search (Judge)

### Steps:
1. [ ] Login as judge (judge1@example.com / password123)
2. [ ] Navigate to "Precedents" tab in sidebar
3. [ ] Enter search query: "property dispute"
4. [ ] Click "Search" button
5. [ ] Verify loading spinner appears
6. [ ] Verify search results are displayed
7. [ ] Verify each result shows:
    - Case title/name
    - Summary
    - Relevance score (%)
8. [ ] Verify results are ranked by relevance
9. [ ] Try another search: "contract breach"
10. [ ] Verify different results are returned

### Expected Result:
✅ Precedent search returns relevant results
✅ Results are ranked by relevance score
✅ Each result shows case name, summary, and score

---

## Test 8: Role-Based Access Control

### Steps:
1. [ ] Login as citizen (citizen1@example.com / password123)
2. [ ] Try to manually navigate to /judge-dashboard
3. [ ] Verify you're redirected or see "Access Denied" message
4. [ ] Logout
5. [ ] Login as judge (judge1@example.com / password123)
6. [ ] Try to file a new case (if UI allows)
7. [ ] Verify judges cannot file cases (citizen-only operation)

### Expected Result:
✅ Citizens cannot access judge dashboard
✅ Judges cannot file cases
✅ Role-based authorization is enforced

---

## Test 9: Error Handling

### Steps:
1. [ ] Try to login with invalid credentials
2. [ ] Verify error message is displayed: "Invalid credentials"
3. [ ] Try to register with existing email
4. [ ] Verify error message is displayed: "Email already registered"
5. [ ] Try to file a case with empty title
6. [ ] Verify validation error is displayed
7. [ ] Try to file a case with title > 200 characters
8. [ ] Verify validation error is displayed

### Expected Result:
✅ Error messages are clear and actionable
✅ Validation errors are displayed inline
✅ No crashes or unhandled errors

---

## Test 10: Logout

### Steps:
1. [ ] Login as any user
2. [ ] Click "Logout" button
3. [ ] Verify redirect to landing page or login page
4. [ ] Verify token is removed from localStorage
5. [ ] Try to navigate back to /citizen-portal or /judge-dashboard
6. [ ] Verify you're redirected to login page

### Expected Result:
✅ Logout clears authentication state
✅ Protected routes redirect to login after logout
✅ Token is removed from storage

---

## Known Issues / Bugs Found

### Issue 1: [Description]
- **Status:** [ ] Open / [ ] Fixed
- **Steps to Reproduce:**
- **Expected Behavior:**
- **Actual Behavior:**

### Issue 2: [Description]
- **Status:** [ ] Open / [ ] Fixed
- **Steps to Reproduce:**
- **Expected Behavior:**
- **Actual Behavior:**

---

## Test Summary

- **Total Tests:** 10
- **Passed:** ___
- **Failed:** ___
- **Blocked:** ___

### Critical Issues:
- [ ] None found
- [ ] List critical issues here

### Notes:
- Add any additional observations or notes here
- Document any workarounds needed
- Note any performance issues observed
