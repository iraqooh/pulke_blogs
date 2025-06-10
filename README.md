# Pulke Blogs API

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Overview

Pulke Blogs API is a RESTful backend service for a blogging platform built using **Flask** and **SQLite**. It offers essential blog features including user authentication, role-based access control, posts, comments, tags, bookmarks, likes, post view tracking, and analytics.

The API follows RESTful principles to provide a clean, intuitive interface for frontend applications or third-party clients.

## Features

- **User Authentication & Authorization**  
  Register, login, logout with JWT tokens. Role-based access (admin, author, reader, moderator).

- **Post Management**  
  Create, read, update, delete posts. Support for drafts and publishing workflows.  
  Automatic slug generation from titles.

- **Comments**  
  Threaded comments with nested replies. Comment editing and moderation.

- **Bookmarks**  
  Users can bookmark posts for quick access later.

- **Post Views Tracking**  
  Track and log post views by user or IP address.

- **Likes & Reactions**  
  Like posts and comments. Enforces one like per user per resource.

- **Tags & Categories**  
  Tagging system with many-to-many relationships. Category management by admins.

- **Search, Pagination, and Filtering**  
  Full-text search in posts and tags. Filter posts by category, tags, author, and more.

- **User Profiles & Analytics**  
  Public author profiles with post listings. Analytics endpoints for views, likes, popular posts.

- **Media Uploads**  
  Upload and manage images or videos attached to posts.

- **Notifications & Subscriptions**  
  Subscribe to categories or blogs and receive notifications.

## Tech Stack

- Python 3.x  
- Flask (with Flask-RESTful / Flask-JWT-Extended)  
- SQLite (for lightweight database storage)  
- Marshmallow (for serialization & validation)  
- JWT for secure authentication

## Getting Started

### Prerequisites

- Python 3.8+  
- pip package manager

### Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/yourusername/pulke-blogs-api.git
   cd pulke-blogs-api
   ```
2. Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Initialize the database

```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the development server

```bash
flask run
```
The API will be available at http://localhost:5000.

## API Documentation

Detailed API endpoint documentation is available in the /docs folder or via the /swagger route when the server is running.

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contribution

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

Please follow the code of conduct and contributing guidelines.

## Author
Harry Iraku — Finalist Software Engineering Student at Makerere University.

## Acknowledgments

- Flask and Flask-RESTful community

- SQLite database

- JWT for secure authentication

- Inspiration from modern blogging platforms and REST API best practices
