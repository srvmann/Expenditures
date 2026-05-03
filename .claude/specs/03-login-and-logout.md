# Spec: Login and Logout

## Overview
Implements user login and logout functionality with session-based authentication. This is Step 3 of the Spendly roadmap, building on the registration feature from Step 2.

## Depends on
- Step 1: Database Setup (complete)
- Step 2: Registration (complete)

## Routes
- `GET /login` — Show login form — public
- `POST /login` — Process login credentials — public
- `GET /logout` — Clear session and redirect — logged-in only

## Database changes
No new tables or columns. Uses existing `users` table.

## Templates
- **Modify:** `templates/login.html`
  - Add CSRF protection token
  - Add flash message display
  - Add link to registration page

## Files to change
- `app.py` — Add POST /login handler, logout handler, session management
- `templates/login.html` — Add CSRF token, flash messages
- `templates/base.html` — Show user name in nav when logged in

## Files to create
- None

## New dependencies
- No new dependencies (Flask sessions already available)

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Use `werkzeug.security.check_password_hash` for password verification
- Use Flask sessions for user authentication
- Store user_id and user_name in session after successful login
- Use CSRF protection on login form
- On success: redirect to profile page
- On error: re-render login.html with error message

## Definition of done
- [ ] GET /login returns the login form
- [ ] POST /login with correct credentials creates session
- [ ] POST /login with wrong credentials shows error
- [ ] Logged-in user sees their name in navigation
- [ ] GET /logout clears session and redirects to login
- [ ] Session persists across requests
- [ ] Protected routes redirect to login when not authenticated