# Requirements Document

## Introduction

JobTracker is a web application that allows users to track their job applications throughout the hiring process. Users can register and log in to a personal account, manage a list of job applications with full CRUD capabilities, and view a dashboard with statistics and charts summarizing their job search activity. The system is built with a Vue.js frontend, Flask backend, Neon (PostgreSQL) database, and Cloudinary for file storage. The Groq API is integrated but reserved for future AI features.

## Glossary

- **JobTracker**: The web application described in this document.
- **User**: An authenticated person who has registered and logged in to JobTracker.
- **Job Entry**: A record representing a single job application, including details such as company name, job title, status, location, salary range, and associated files.
- **Dashboard**: The main landing page shown to a User after login, displaying statistics and charts about their job applications.
- **Auth_Service**: The backend component responsible for user registration, login, and session management.
- **Job_Service**: The backend component responsible for creating, reading, updating, and deleting Job Entries.
- **File_Service**: The backend component responsible for uploading and managing files via the Cloudinary API.
- **Stats_Engine**: The backend component responsible for computing aggregated statistics from Job Entries.
- **Frontend**: The Vue.js single-page application served to the User's browser.
- **Database**: The Neon PostgreSQL database used to persist all application data.
- **Cloudinary**: The third-party cloud storage service used for file uploads.
- **Groq_Client**: The integrated Groq API client, reserved for future AI features.
- **JWT**: JSON Web Token used for stateless authentication between the Frontend and backend.
- **Application_Status**: The current stage of a Job Entry, one of: Applied, Phone Screen, Interview, Offer, Rejected, Withdrawn.
- **Phone Screen**: An initial short call (typically 15–30 minutes) conducted by a recruiter or HR representative to assess a candidate before advancing to formal interviews.
- **Salary_Min**: The lower bound of the expected or offered salary range for a Job Entry, stored as a numeric value.
- **Salary_Max**: The upper bound of the expected or offered salary range for a Job Entry, stored as a numeric value.

---

## Requirements

### Requirement 1: User Registration

**User Story:** As a new visitor, I want to register for a JobTracker account, so that I can start tracking my job applications.

#### Acceptance Criteria

1. THE Auth_Service SHALL provide a registration endpoint that accepts a unique email address and a password.
2. WHEN a registration request is received with a valid, unique email and a password of at least 8 characters, THE Auth_Service SHALL create a new User record in the Database and return a success response.
3. IF a registration request is received with an email address already associated with an existing User, THEN THE Auth_Service SHALL return a 409 Conflict error with a descriptive message.
4. IF a registration request is received with a password shorter than 8 characters, THEN THE Auth_Service SHALL return a 400 Bad Request error with a descriptive message.
5. THE Auth_Service SHALL store User passwords as cryptographic hashes and SHALL NOT store plaintext passwords in the Database.
6. THE Frontend SHALL display a registration form with fields for email and password.
7. WHEN a User submits the registration form with valid inputs, THE Frontend SHALL display a confirmation message and redirect the User to the login page.
8. IF the Auth_Service returns an error during registration, THEN THE Frontend SHALL display the error message to the User without clearing the form fields.

---

### Requirement 2: User Login

**User Story:** As a registered User, I want to log in to my account, so that I can access my job application data.

#### Acceptance Criteria

1. THE Auth_Service SHALL provide a login endpoint that accepts an email address and a password.
2. WHEN a login request is received with a valid email and matching password, THE Auth_Service SHALL return a signed JWT with a 24-hour expiry.
3. IF a login request is received with an email address not associated with any User, THEN THE Auth_Service SHALL return a 401 Unauthorized error.
4. IF a login request is received with an incorrect password, THEN THE Auth_Service SHALL return a 401 Unauthorized error.
5. THE Frontend SHALL display a login form with fields for email and password.
6. WHEN a User submits the login form and the Auth_Service returns a JWT, THE Frontend SHALL store the JWT in browser local storage and redirect the User to the Dashboard.
7. WHILE a User holds a valid JWT, THE Frontend SHALL include the JWT as a Bearer token in all requests to protected backend endpoints.
8. WHEN a JWT expires or is absent, THE Frontend SHALL redirect the User to the login page.

---

### Requirement 3: User Logout

**User Story:** As a logged-in User, I want to log out of my account, so that my session is ended securely.

#### Acceptance Criteria

1. THE Frontend SHALL provide a logout control accessible from all authenticated pages.
2. WHEN a User activates the logout control, THE Frontend SHALL remove the JWT from browser local storage and redirect the User to the login page.

---

### Requirement 4: Dashboard Statistics

**User Story:** As a logged-in User, I want to see summary statistics about my job applications on the Dashboard, so that I can understand the overall state of my job search at a glance.

#### Acceptance Criteria

1. WHEN a User navigates to the Dashboard, THE Stats_Engine SHALL compute and return the following counts for that User's Job Entries: total applications, total in Interview status, total in Offer status, and total in Rejected status.
2. THE Frontend SHALL display the statistics returned by the Stats_Engine as individual stat cards on the Dashboard.
3. WHEN a User's Job Entries are updated, THE Frontend SHALL refresh the Dashboard statistics to reflect the current state.
4. WHILE a User has zero Job Entries, THE Frontend SHALL display zero values in all stat cards.

---

### Requirement 5: Dashboard Charts

**User Story:** As a logged-in User, I want to see charts visualizing my job application data on the Dashboard, so that I can identify trends in my job search.

#### Acceptance Criteria

1. THE Frontend SHALL display a chart on the Dashboard showing the distribution of Job Entries by Application_Status.
2. THE Frontend SHALL display a chart on the Dashboard showing the number of Job Entries created per calendar week over the most recent 12 weeks.
3. WHEN a User's Job Entries are updated, THE Frontend SHALL refresh all Dashboard charts to reflect the current state.
4. WHILE a User has zero Job Entries, THE Frontend SHALL display empty chart states with a descriptive placeholder message.

---

### Requirement 6: Create Job Entry

**User Story:** As a logged-in User, I want to add a new job application to my list, so that I can track it going forward.

#### Acceptance Criteria

1. THE Frontend SHALL provide a form for creating a new Job Entry with the following required fields: company name, job title, and Application_Status.
2. THE Frontend SHALL provide the following optional fields on the Job Entry form: job posting URL, notes, application date, location, salary minimum (numeric), salary maximum (numeric), and file attachments.
3. WHEN a User submits the Job Entry form with all required fields populated, THE Job_Service SHALL create a new Job Entry record in the Database associated with that User and return the created record.
4. IF a User submits the Job Entry form with one or more required fields empty, THEN THE Frontend SHALL display a validation error for each missing field and SHALL NOT submit the request to the Job_Service.
5. WHEN a file attachment is included in the Job Entry form, THE File_Service SHALL upload the file to Cloudinary and store the returned file URL in the Job Entry record.
6. THE File_Service SHALL accept file attachments of the following types: PDF, PNG, JPG, and JPEG.
7. IF a file attachment exceeds 10 MB in size, THEN THE File_Service SHALL return a 400 Bad Request error with a descriptive message.
8. IF both Salary_Min and Salary_Max are provided, THEN THE Frontend SHALL validate that Salary_Min is less than or equal to Salary_Max and SHALL display a validation error if this condition is not met.

---

### Requirement 7: View Job Entries

**User Story:** As a logged-in User, I want to view all my job applications in a list, so that I can review my application history.

#### Acceptance Criteria

1. THE Job_Service SHALL provide an endpoint that returns all Job Entries associated with the authenticated User.
2. THE Frontend SHALL display the User's Job Entries in a sidebar-accessible list view.
3. THE Frontend SHALL display the following fields for each Job Entry in the list: company name, job title, Application_Status, application date, and location.
4. WHEN a User selects a Job Entry from the list, THE Frontend SHALL display the full details of that Job Entry including all stored fields (company name, job title, status, application date, location, salary range, URL, notes) and any attached file links.
5. WHILE a User has zero Job Entries, THE Frontend SHALL display an empty state message with a prompt to add the first job application.

---

### Requirement 8: Edit Job Entry

**User Story:** As a logged-in User, I want to edit an existing job application, so that I can keep its details up to date.

#### Acceptance Criteria

1. THE Frontend SHALL provide an edit form pre-populated with the existing data of a selected Job Entry.
2. WHEN a User submits the edit form with valid data, THE Job_Service SHALL update the corresponding Job Entry record in the Database and return the updated record.
3. IF a User submits the edit form with one or more required fields empty, THEN THE Frontend SHALL display a validation error for each missing field and SHALL NOT submit the request to the Job_Service.
4. IF a request to update a Job Entry is received for a Job Entry not associated with the authenticated User, THEN THE Job_Service SHALL return a 403 Forbidden error.
5. WHEN a new file attachment is provided during an edit, THE File_Service SHALL upload the new file to Cloudinary and replace the stored file URL in the Job Entry record.

---

### Requirement 9: Delete Job Entry

**User Story:** As a logged-in User, I want to delete a job application from my list, so that I can remove entries that are no longer relevant.

#### Acceptance Criteria

1. THE Frontend SHALL provide a delete control for each Job Entry in the list and detail views.
2. WHEN a User activates the delete control, THE Frontend SHALL display a confirmation dialog before proceeding.
3. WHEN a User confirms deletion, THE Job_Service SHALL delete the corresponding Job Entry record from the Database and return a 200 OK response.
4. IF a request to delete a Job Entry is received for a Job Entry not associated with the authenticated User, THEN THE Job_Service SHALL return a 403 Forbidden error.
5. WHEN a Job Entry with an associated Cloudinary file is deleted, THE File_Service SHALL delete the corresponding file from Cloudinary.

---

### Requirement 10: Sidebar Navigation

**User Story:** As a logged-in User, I want a sidebar navigation panel, so that I can move between the Dashboard and my Job List efficiently.

#### Acceptance Criteria

1. THE Frontend SHALL display a persistent sidebar navigation panel on all authenticated pages.
2. THE Frontend SHALL include navigation links in the sidebar for: Dashboard and Job List.
3. WHEN a User activates a sidebar navigation link, THE Frontend SHALL navigate to the corresponding page without a full page reload.
4. THE Frontend SHALL visually indicate the currently active navigation link in the sidebar.

---

### Requirement 11: Animated UI

**User Story:** As a User, I want the interface to include smooth animations and transitions, so that the application feels polished and responsive.

#### Acceptance Criteria

1. THE Frontend SHALL apply entrance animations to Dashboard stat cards when the Dashboard page loads.
2. THE Frontend SHALL apply transition animations when navigating between pages via the sidebar.
3. THE Frontend SHALL apply a loading animation while awaiting responses from backend endpoints.
4. THE Frontend SHALL apply hover and focus state animations to interactive controls such as buttons and form inputs.

---

### Requirement 12: Groq API Integration (Reserved)

**User Story:** As a developer, I want the Groq API client to be integrated into the backend, so that AI features can be added in future iterations without requiring architectural changes.

#### Acceptance Criteria

1. THE JobTracker backend SHALL include the Groq_Client as a configured dependency using the provided Groq API key.
2. THE Groq_Client SHALL be initialized at application startup and SHALL be accessible to backend service components.
3. WHILE no AI features are active, THE Groq_Client SHALL remain idle and SHALL NOT make any requests to the Groq API.
