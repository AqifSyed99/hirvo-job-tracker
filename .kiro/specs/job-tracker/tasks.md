# Implementation Plan: JobTracker

## Overview

Implement JobTracker as a Vue.js SPA backed by a Flask REST API, Neon PostgreSQL database, Cloudinary file storage, and a dormant Groq client. The plan proceeds layer by layer — project scaffolding, database models, backend services, frontend setup, views, and UI polish — with property-based tests (Hypothesis) and unit/component tests (Vitest) placed close to the code they validate.

---

## Tasks

- [x] 1. Project scaffolding
  - Create the backend directory structure: `backend/`, `backend/app/`, `backend/app/services/`, `backend/app/models/`, `backend/tests/`
  - Create `backend/requirements.txt` pinning Flask, Flask-SQLAlchemy, psycopg2-binary, PyJWT, bcrypt, cloudinary, groq, hypothesis, pytest, pytest-flask
  - Create `backend/app/__init__.py` with Flask app factory (`create_app`), CORS setup, and global error handlers (400, 401, 403, 404, 409, 500)
  - Create `backend/config.py` loading `DATABASE_URL`, `JWT_SECRET`, `CLOUDINARY_*`, and `GROQ_API_KEY` from environment variables
  - Create the frontend directory structure using Vite + Vue 3: `frontend/src/`, `frontend/src/views/`, `frontend/src/components/`, `frontend/src/store/`, `frontend/src/router/`
  - Add frontend dependencies to `frontend/package.json`: vue-router, pinia, axios, chart.js, vue-chartjs, vitest, @vue/test-utils
  - _Requirements: 1.1, 2.1, 6.1, 10.1, 12.1_

- [x] 2. Database models and migrations
  - [x] 2.1 Define SQLAlchemy `User` and `JobEntry` models in `backend/app/models/models.py`
    - Implement `User` with `id`, `email` (unique, not null), `password_hash`, `created_at`, and `entries` relationship
    - Implement `JobEntry` with all columns from the schema including the `status` CHECK constraint for the six `Application_Status` values
    - Add `db.create_all()` call in the app factory so tables are created on first run
    - _Requirements: 1.2, 6.3_

  - [ ]* 2.2 Write property test for `JobEntry` model round-trip (Property 10)
    - **Property 10: Job entry creation round-trip**
    - **Validates: Requirements 6.3**
    - Use Hypothesis `@given` to generate valid job entry field combinations; insert via SQLAlchemy and re-fetch; assert all field values match

- [x] 3. Groq client initialization
  - Create `backend/app/groq_client.py` that imports `Groq` and initializes `groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))` as a module-level singleton
  - Import `groq_client` in the app factory to ensure it is initialized at startup; do not wire it to any route
  - _Requirements: 12.1, 12.2, 12.3_

  - [ ]* 3.1 Write property test for Groq client idle behavior (Property 21)
    - **Property 21: Groq client makes no requests during normal operation**
    - **Validates: Requirements 12.3**
    - Mock the HTTP transport layer; exercise all backend endpoints; assert zero calls were made to any Groq API host

- [x] 4. Auth_Service — backend
  - [x] 4.1 Implement `backend/app/services/auth_service.py`
    - `register(email, password)`: validate email uniqueness and password length ≥ 8; hash password with bcrypt; insert `User`; return created user or raise appropriate HTTP error
    - `login(email, password)`: look up user by email; verify bcrypt hash; issue JWT signed with `JWT_SECRET`, expiry 24 h, payload `{ "user_id": <id> }`; return token + user object
    - `require_auth` decorator: extract `Authorization: Bearer <token>` header; verify signature and expiry; attach `g.current_user`; return 401 on failure
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_

  - [ ]* 4.2 Write property test for password hashing (Property 1)
    - **Property 1: Password never stored as plaintext**
    - **Validates: Requirements 1.5**
    - Generate random valid passwords; call `register`; query `users.password_hash`; assert hash ≠ plaintext

  - [ ]* 4.3 Write property test for valid registration (Property 2)
    - **Property 2: Valid registration creates a user record**
    - **Validates: Requirements 1.2**
    - Generate unique emails + passwords ≥ 8 chars; call register endpoint; assert 201 and exactly one new user row

  - [ ]* 4.4 Write property test for duplicate email rejection (Property 3)
    - **Property 3: Duplicate email rejected on registration**
    - **Validates: Requirements 1.3**
    - Register an email; attempt second registration with same email; assert 409 and no duplicate row

  - [ ]* 4.5 Write property test for short password rejection (Property 4)
    - **Property 4: Short password rejected on registration**
    - **Validates: Requirements 1.4**
    - Generate passwords of length 0–7; assert 400 and no user created

  - [ ]* 4.6 Write property test for JWT issuance (Property 5)
    - **Property 5: JWT issued on valid login**
    - **Validates: Requirements 2.2**
    - Generate valid credentials; call login; decode JWT; assert payload contains `user_id` and expiry ≈ now + 24 h (within 60 s tolerance)

  - [ ]* 4.7 Write property test for invalid credentials rejection (Property 6)
    - **Property 6: Invalid credentials rejected**
    - **Validates: Requirements 2.3, 2.4**
    - Generate wrong email/password combos; assert 401 and no token in response

  - [x] 4.8 Register auth Blueprint and wire routes in `backend/app/__init__.py`
    - `POST /api/auth/register` → `auth_service.register`
    - `POST /api/auth/login` → `auth_service.login`
    - _Requirements: 1.1, 2.1_

- [x] 5. Checkpoint — backend auth
  - Ensure all auth tests pass, ask the user if questions arise.

- [x] 6. Job_Service — backend
  - [x] 6.1 Implement `backend/app/services/job_service.py`
    - `get_all(user_id)`: return all `JobEntry` rows for the user
    - `get_one(user_id, entry_id)`: return entry or 404; enforce ownership or 403
    - `create(user_id, data)`: validate required fields (`company_name`, `job_title`, `status`); insert and return new entry
    - `update(user_id, entry_id, data)`: enforce ownership; update fields; return updated entry
    - `delete(user_id, entry_id)`: enforce ownership; delete entry; return 200
    - _Requirements: 6.3, 7.1, 8.2, 8.4, 9.3, 9.4_

  - [ ]* 6.2 Write property test for job list isolation (Property 15)
    - **Property 15: Job list isolation between users**
    - **Validates: Requirements 7.1**
    - Generate two users with distinct entry sets; call GET `/api/jobs` for each; assert each response contains only own entries

  - [ ]* 6.3 Write property test for ownership enforcement (Property 19)
    - **Property 19: Ownership enforcement on write operations**
    - **Validates: Requirements 8.4, 9.4**
    - Generate user pairs and entries; attempt cross-user PUT and DELETE; assert 403 and entry unchanged in DB

  - [ ]* 6.4 Write property test for job entry update round-trip (Property 18)
    - **Property 18: Job entry update round-trip**
    - **Validates: Requirements 8.2**
    - Generate valid update payloads; PUT then GET; assert all updated field values match

  - [ ]* 6.5 Write property test for deletion removes entry (Property 20)
    - **Property 20: Deletion removes entry from the system**
    - **Validates: Requirements 9.3**
    - DELETE an owned entry; GET the same ID; assert 404 and entry absent from list

  - [x] 6.6 Register Job Blueprint and wire CRUD routes
    - `GET /api/jobs`, `POST /api/jobs`, `GET /api/jobs/<id>`, `PUT /api/jobs/<id>`, `DELETE /api/jobs/<id>` — all behind `@require_auth`
    - _Requirements: 6.3, 7.1, 8.2, 9.3_

- [x] 7. File_Service — backend
  - [x] 7.1 Implement `backend/app/services/file_service.py`
    - `upload(file)`: validate MIME type (PDF, PNG, JPG, JPEG) and size ≤ 10 MB; call `cloudinary.uploader.upload`; return secure URL and public ID
    - `delete(public_id)`: call `cloudinary.uploader.destroy`
    - Integrate with `job_service.create` and `job_service.update` (upload on create/edit) and `job_service.delete` (delete asset on entry removal)
    - _Requirements: 6.5, 6.6, 6.7, 8.5, 9.5_

  - [ ]* 7.2 Write property test for file type enforcement (Property 13)
    - **Property 13: File type enforcement**
    - **Validates: Requirements 6.6**
    - Generate random MIME types; assert only PDF/PNG/JPG/JPEG pass, all others return 400

  - [ ]* 7.3 Write property test for file size enforcement (Property 14)
    - **Property 14: File size enforcement**
    - **Validates: Requirements 6.7**
    - Generate file sizes around the 10 MB boundary; assert >10 MB returns 400, ≤10 MB with valid type proceeds

- [x] 8. Stats_Engine — backend
  - [x] 8.1 Implement `backend/app/services/stats_service.py`
    - Query `job_entries` for the authenticated user
    - Compute `total`, `interview`, `offer`, `rejected`, `by_status` (all six statuses), and `weekly_counts` (exactly 12 calendar weeks, most recent first)
    - Return the stats JSON object defined in the design
    - _Requirements: 4.1, 4.4, 5.1, 5.2_

  - [ ]* 8.2 Write property test for stats count consistency (Property 8)
    - **Property 8: Stats counts are consistent with stored entries**
    - **Validates: Requirements 4.1, 4.4**
    - Generate random sets of job entries with random statuses (including empty set); call stats endpoint; assert counts match, zero case returns all zeros

  - [ ]* 8.3 Write property test for weekly counts length (Property 9)
    - **Property 9: Weekly counts always cover exactly 12 weeks**
    - **Validates: Requirements 5.2**
    - Generate entry sets with various dates; call stats endpoint; assert `weekly_counts` has exactly 12 elements

  - [x] 8.4 Register Stats Blueprint and wire route
    - `GET /api/stats` behind `@require_auth`
    - _Requirements: 4.1, 5.1_

- [x] 9. Checkpoint — backend services
  - Ensure all backend service tests pass, ask the user if questions arise.

- [x] 10. Frontend setup
  - Configure `frontend/src/main.js`: create Vue app, install Vue Router and Pinia, set axios `baseURL` to the Flask API origin, attach JWT interceptor that reads from `localStorage` and sets `Authorization: Bearer <token>` on every request
  - Implement `frontend/src/router/index.js` with routes for `/login`, `/register`, `/dashboard`, `/jobs`, and a catch-all redirect to `/dashboard`; add a global navigation guard that redirects unauthenticated users to `/login`
  - _Requirements: 2.7, 2.8, 10.3_

  - [ ]* 10.1 Write property test for Bearer token inclusion (Property 7)
    - **Property 7: Bearer token included in all authenticated requests**
    - **Validates: Requirements 2.7**
    - Use Vitest to mock axios; set a token in the auth store; dispatch various store actions; assert each outgoing request includes `Authorization: Bearer <token>`

- [x] 11. Pinia stores
  - [x] 11.1 Implement `frontend/src/store/auth.js`
    - State: `token` (string | null), `user` (object | null)
    - `login(email, password)`: POST `/api/auth/login`; store token in `localStorage` and state; redirect to `/dashboard`
    - `logout()`: clear `localStorage` and state; redirect to `/login`
    - Computed `isAuthenticated`: returns true when token is present and not expired
    - Rehydrate token from `localStorage` on store initialization
    - _Requirements: 2.6, 2.7, 2.8, 3.1, 3.2_

  - [x] 11.2 Implement `frontend/src/store/jobs.js`
    - State: `entries` (array), `selected` (object | null), `stats` (object | null), `loading` (boolean), `error` (string | null)
    - Actions: `fetchAll()`, `create(data)`, `update(id, data)`, `remove(id)`, `fetchStats()`
    - Catch API errors in each action; set `error` state; clear error on new requests
    - On 401 response, call `authStore.logout()`
    - _Requirements: 6.3, 7.1, 8.2, 9.3, 4.1_

- [x] 12. Common components
  - Create `frontend/src/components/common/LoadingSpinner.vue`: animated CSS spinner shown while `loading` is true
  - Create `frontend/src/components/common/ErrorBanner.vue`: displays `error` string at top of view; dismissible
  - _Requirements: 11.3_

- [x] 13. Authenticated layout and sidebar
  - Create `frontend/src/components/layout/AppSidebar.vue`
    - Render navigation links for Dashboard (`/dashboard`) and Job List (`/jobs`)
    - Highlight the active link using Vue Router's `router-link-active` class
    - Include a logout button that calls `authStore.logout()`
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 3.1_
  - Create `frontend/src/layouts/AuthenticatedLayout.vue` (or equivalent wrapper) that renders `AppSidebar` alongside a `<router-view>`; apply page-transition CSS classes for route changes
  - _Requirements: 10.1, 11.2_

- [x] 14. Auth views
  - [x] 14.1 Implement `frontend/src/views/RegisterView.vue`
    - Form with email and password fields
    - On submit: call `authStore.register(email, password)`; on success show confirmation and redirect to `/login`; on error display `ErrorBanner` without clearing fields
    - _Requirements: 1.6, 1.7, 1.8_

  - [x] 14.2 Implement `frontend/src/views/LoginView.vue`
    - Form with email and password fields
    - On submit: call `authStore.login(email, password)`; on success redirect to `/dashboard`; on error display `ErrorBanner`
    - _Requirements: 2.5, 2.6_

- [x] 15. Dashboard view
  - [x] 15.1 Create `frontend/src/components/dashboard/StatCard.vue`
    - Props: `label` (string), `value` (number)
    - Apply CSS entrance animation (fade + slide-up) on mount
    - _Requirements: 4.2, 11.1_

  - [x] 15.2 Create `frontend/src/components/dashboard/StatusChart.vue`
    - Doughnut chart (Chart.js via vue-chartjs) showing job entry counts by `Application_Status`
    - Show placeholder message when all counts are zero
    - _Requirements: 5.1, 5.4_

  - [x] 15.3 Create `frontend/src/components/dashboard/WeeklyChart.vue`
    - Bar chart showing applications per calendar week for the most recent 12 weeks
    - Show placeholder message when all counts are zero
    - _Requirements: 5.2, 5.4_

  - [x] 15.4 Implement `frontend/src/views/DashboardView.vue`
    - On mount: call `jobsStore.fetchStats()`; render four `StatCard` components (Total, Interview, Offer, Rejected) and both chart components
    - Re-fetch stats whenever job entries are mutated
    - Show `LoadingSpinner` while fetching; show `ErrorBanner` on error
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4_

  - [ ]* 15.5 Write Vitest component tests for `StatCard`
    - Test that label and value props render correctly
    - Test zero-value display
    - _Requirements: 4.2, 4.4_

- [x] 16. Job List view and CRUD components
  - [x] 16.1 Create `frontend/src/components/jobs/JobListItem.vue`
    - Props: `entry` (JobEntry object)
    - Display: company name, job title, Application_Status badge, application date, location
    - Emit `select` event on click
    - _Requirements: 7.3_

  - [ ]* 16.2 Write property test for list item field display (Property 16)
    - **Property 16: List item displays all required fields**
    - **Validates: Requirements 7.3**
    - Use Vitest + Vue Test Utils; generate random job entries; mount `JobListItem`; assert all five required fields are present in rendered output

  - [x] 16.3 Create `frontend/src/components/jobs/JobList.vue`
    - Render a scrollable list of `JobListItem` components from `jobsStore.entries`
    - Show empty-state message with "Add your first job application" prompt when list is empty
    - _Requirements: 7.2, 7.5_

  - [x] 16.4 Create `frontend/src/components/jobs/JobForm.vue`
    - Shared create/edit form with all fields from the design (required: company name, job title, status; optional: URL, notes, date, location, salary min/max, file)
    - Inline validation: highlight missing required fields on submit attempt
    - Salary range validation: if both provided, assert `salary_min ≤ salary_max`; show inline error if violated
    - File input: accept PDF, PNG, JPG, JPEG only; show file name when selected
    - Pre-populate all fields when an `entry` prop is provided (edit mode)
    - Emit `submitted` event with form data; do not call API directly
    - _Requirements: 6.1, 6.2, 6.4, 6.8, 8.1, 8.3_

  - [ ]* 16.5 Write property test for required field validation (Property 11)
    - **Property 11: Required field validation prevents submission**
    - **Validates: Requirements 6.4, 8.3**
    - Use Vitest; generate subsets of required fields with some missing; mount `JobForm`; trigger submit; assert validation errors shown and no `submitted` event emitted

  - [ ]* 16.6 Write property test for salary range ordering (Property 12)
    - **Property 12: Salary range ordering enforced**
    - **Validates: Requirements 6.8**
    - Generate `(salary_min, salary_max)` pairs where `min > max`; mount `JobForm`; trigger submit; assert validation error shown and no `submitted` event emitted

  - [ ]* 16.7 Write property test for edit form pre-population (Property 17)
    - **Property 17: Edit form pre-populated with existing data**
    - **Validates: Requirements 8.1**
    - Generate random job entries; mount `JobForm` with `entry` prop; assert every field value matches the entry's stored values

  - [x] 16.8 Create `frontend/src/components/jobs/JobDetail.vue`
    - Display all fields of the selected entry including file link (if present)
    - Provide Edit and Delete buttons
    - _Requirements: 7.4_

  - [x] 16.9 Create `frontend/src/components/jobs/DeleteDialog.vue`
    - Modal confirmation dialog with Confirm and Cancel buttons
    - Emit `confirm` and `cancel` events
    - _Requirements: 9.1, 9.2_

  - [ ]* 16.10 Write Vitest unit tests for `DeleteDialog`
    - Test that `confirm` event is emitted on confirm click
    - Test that `cancel` event is emitted on cancel click
    - _Requirements: 9.2_

  - [x] 16.11 Implement `frontend/src/views/JobListView.vue`
    - On mount: call `jobsStore.fetchAll()`
    - Render `JobList` alongside a detail/form panel
    - Handle create: show blank `JobForm`; on `submitted` call `jobsStore.create(data)`
    - Handle edit: show `JobForm` pre-populated with selected entry; on `submitted` call `jobsStore.update(id, data)`
    - Handle delete: show `DeleteDialog`; on confirm call `jobsStore.remove(id)`
    - Show `LoadingSpinner` while loading; show `ErrorBanner` on error
    - _Requirements: 6.3, 7.2, 8.2, 9.3_

- [x] 17. Checkpoint — core feature complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 18. Animations and UI polish
  - Add CSS `@keyframes` entrance animation (fade + translate-Y) to `StatCard.vue`; trigger on component mount via a CSS class toggle
  - Add Vue `<transition>` wrapper around `<router-view>` in the authenticated layout with `fade` enter/leave CSS classes for page transitions
  - Add CSS `transition` rules for hover and focus states on all buttons and form inputs (color, shadow, transform)
  - Ensure `LoadingSpinner` is visible during all async operations (auth, job CRUD, stats fetch)
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [ ] 19. Integration tests
  - [ ]* 19.1 Write backend integration test: full CRUD flow
    - Register → Login → Create job entry → GET list → GET single → PUT update → DELETE
    - Run against an in-memory SQLite database (or test Neon instance)
    - Assert correct HTTP status codes and response bodies at each step
    - _Requirements: 1.2, 2.2, 6.3, 7.1, 8.2, 9.3_

  - [ ]* 19.2 Write backend integration test: stats consistency after mutations
    - Create a set of entries with known statuses; call GET `/api/stats`; assert counts match; delete one entry; re-fetch stats; assert counts updated
    - _Requirements: 4.1, 4.3_

  - [ ]* 19.3 Write frontend integration test: navigation guard
    - Use Vitest + Vue Router; simulate unauthenticated state; attempt to navigate to `/dashboard`; assert redirect to `/login`
    - _Requirements: 2.8_

- [x] 20. Final checkpoint — all tests pass
  - Ensure all tests pass, ask the user if questions arise.

---

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Property tests use Hypothesis (backend) and Vitest (frontend); each runs a minimum of 100 iterations
- Checkpoints at tasks 5, 9, 17, and 20 ensure incremental validation
- The Groq client (task 3) is wired at startup but makes no API calls during normal operation
- File_Service Cloudinary calls should be mocked in unit and property tests; use a dedicated Cloudinary test environment for integration tests
