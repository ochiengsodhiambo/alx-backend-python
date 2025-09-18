 ##Messaging API with Django & Django REST Framework

This project is a simple **Messaging API** built using **Django** and **Django REST Framework (DRF)**.  
It allows one to manage **Users**, **Conversations**, and **Messages**, with support for relationships and clean RESTful endpoints.

---

### Features
- Custom **User model** (extends Django `AbstractUser`)
- **Conversations** between multiple users
- **Messages** sent by users in a conversation
- REST API endpoints using **DRF ViewSets**
- **UUID primary keys** for scalability
- Auto-generated endpoints using **DRF DefaultRouter**

---

### Tech Stack
- Python 3.x
- Django 5.x (or latest)
- Django REST Framework

---

### Project Structure
messaging_app/
 - chats/ # Messaging app
 - models.py # User, Conversation, Message models
 - serializers.py # DRF serializers
 - views.py # API ViewSets
 - urls.py # (optional) app-specific routes
 - messaging_app/
 - settings.py # Django settings
 - urls.py # Main project routes
 - manage.py # Django CLI


---

### Models Overview
**User**
id (UUID, primary key)
first_name, last_name
email (unique, used for login)
phone_number (optional)
role (guest, host, admin)
created_at

**Conversation**
id (UUID, primary key)
participants (many-to-many with User)
created_at

**Message**
id (UUID, primary key)
sender (FK → User)
conversation (FK → Conversation)
message_body
sent_at




