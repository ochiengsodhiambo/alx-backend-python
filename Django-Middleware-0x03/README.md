### Middleware Framework
This project implements a **custom middleware framework** in Django to handle logging, access control, rate limiting, and role-based permissions for the messaging application.

### Implemented Middleware

### 1. Request Logging Middleware
**File:** `middleware.py`  
- Logs every incoming request with the following format:  
  ```
  <timestamp> - User: <username/Anonymous> - Path: <request.path>
  ```
- Useful for auditing user activity and debugging request flows.
---
### 2. Restrict Access by Time Middleware
**File:** `middleware.py`  
- Restricts access to the messaging app **outside business hours**.  
- Denies requests with a **403 Forbidden** response when accessed between:
  - **9:00 PM → 6:00 AM**  

---

### 3. Offensive Language / Rate Limiting Middleware
**File:** `middleware.py`  
- Prevents spam or abuse in messaging by limiting message frequency.  
- Tracks the number of **POST requests per IP address**.  
- Restriction: **Max 5 messages per minute per IP**.  
- Exceeding the limit returns a **429 Too Many Requests** error.

---

### 4. Role Permission Middleware
**File:** `middleware.py`  
- Ensures only authorized roles can perform sensitive actions.  
- Example restrictions:
  - **Admins/Moderators** can access `/admin/` and `/messages/delete/`.  
- Non-admin users attempting restricted actions get a **403 Forbidden** response.

## Testing
- Run the server:
  ```bash
  python manage.py runserver
  ```
- Use **Postman** or any REST client to test endpoints.  
- Try requests during restricted hours, exceeding designated thresholds, and with different user roles to validate behavior.

---

This middleware framework enforces **security, accountability, and controlled access** across the messaging platform.
