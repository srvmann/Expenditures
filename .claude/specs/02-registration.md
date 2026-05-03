# Spec: Registration

## Overview
Implements user registration functionality with form validation, password hashing, and database insertion. This is Step 2 of the Spendly roadmap, building on the database foundation from Step 1.

## Depends on
- Step 1: Database Setup (must be complete)

## Routes
- `GET /register` — Show registration form — public
- `POST /register` — Process registration form — public

## Database changes
No new tables or columns. Uses existing `users` table from Step 1.

## Templates
- **Modify:** `templates/register.html`
  - Add CSRF protection token
  - Add success message display

## Files to change
- `app.py` — Add POST /register handler, session management, import required modules
- `templates/register.html` — Add CSRF token and success message

## Files to create
- None

## New dependencies
- No new dependencies (Flask sessions already available)

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use Flask sessions for user authentication
- Use Flask's `csrf` extension or manual token for CSRF protection
- All templates extend `base.html`
- Validate: name (required), email (required, valid format, unique), password (min 8 chars)
- On success: redirect to `/login` with success message
- On error: re-render register.html with error message

## Definition of done
- [ ] GET /register returns the registration form
- [ ] POST /register with valid data creates a new user in database
- [ ] Password is hashed before storage
- [ ] Duplicate email shows error message
- [ ] Invalid form data shows appropriate error messages
- [ ] Successful registration redirects to login with success message
- [ ] User can login with registered credentials
- [ ] Session persists across requests after login