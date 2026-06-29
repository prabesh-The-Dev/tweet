# Tweetify — Project Report

---

## 1. Project Proposal

### Project Title
**Tweetify** — A Django-Based Social Media Micro-Blogging Web Application

### Project Overview
Tweetify is a web-based micro-blogging platform inspired by Twitter/X, built using the Django framework. The application allows users to register, log in, and post short messages ("tweets") that may include a title, description, and an optional image. Other users can view, edit, or delete these posts through a simple and intuitive feed interface.

This project is developed as a full-stack web application using Python and Django on the backend, SQLite as the database, and HTML/CSS with Django Templates on the frontend.

### Objectives
- Build a functional CRUD-based social posting system
- Implement user authentication (login/logout) using Django's built-in auth system
- Support media uploads (images) attached to tweets
- Provide a clean, responsive feed where all posts are visible
- Demonstrate the MVC (Model-View-Template) architectural pattern using Django

### Scope
- User login and session management
- Creating, reading, updating, and deleting tweets
- Image upload and storage
- Public tweet feed (all tweets visible to any visitor)
- Django admin panel for superuser management

---

## 2. Problem Statement

### Background
In today's digital world, people want quick, easy ways to share their thoughts, opinions, and updates with others. Existing platforms like Twitter are powerful but complex, making it difficult for developers or small communities to run their own self-hosted micro-blogging system.

### The Problem
There is no simple, lightweight, self-hosted micro-blogging tool that:
- Allows individuals or small groups to post short text + image updates
- Is easy to deploy and maintain without relying on third-party platforms
- Gives the owner full control over data and content
- Can be customised and extended as needed

Most people rely on commercial social platforms which:
- Collect and sell user data
- Impose algorithmic feeds and content restrictions
- Provide no control over data storage or moderation

### Problem Summary
> **How can we build a simple, self-hosted micro-blogging platform that gives users full control over their posts, media, and data — without depending on commercial social media services?**

---

## 3. Solution

### What Tweetify Solves
Tweetify addresses the problem by providing a minimal, self-hosted social posting platform with these solutions:

| Problem                              | Solution                                              |
|--------------------------------------|-------------------------------------------------------|
| No control over data                 | All data stored locally in SQLite database            |
| Complex platforms hard to self-host  | Django makes deployment straightforward               |
| No image support in simple tools     | Django ImageField with Pillow handles media uploads   |
| No authentication in basic tools     | Django's built-in auth system for login/logout        |
| Commercial platforms monetise users  | Fully open, no ads, no tracking                       |

### How It Works (Summary)
1. A user visits the home feed and sees all existing tweets
2. They log in using their credentials
3. They can create a new tweet with a title, description, and optional image
4. All tweets are stored in SQLite and displayed on the feed
5. Any tweet can be edited or deleted through the interface
6. Media images are stored on the server under `media/details/`

---

## 4. Data Flow Diagrams (DFD)

### Level 0 — Context Diagram
> Shows the system as a single process and its interaction with external entities.

```mermaid
flowchart LR
    User(["👤 User"])
    Admin(["🛠️ Admin"])
    System["🐦 Tweetify System"]

    User -- "Login, Post Tweet, View Feed, Edit/Delete" --> System
    System -- "Feed Page, Confirmation, Error Messages" --> User
    Admin -- "Manage Users & Tweets via Admin Panel" --> System
    System -- "Admin Dashboard Data" --> Admin
```

---

### Level 1 — System Decomposition
> Breaks the system into its major processes.

```mermaid
flowchart TD
    User(["👤 User"])
    Admin(["🛠️ Admin"])

    P1["1.0\nUser Authentication"]
    P2["2.0\nTweet Management"]
    P3["3.0\nMedia Handling"]
    P4["4.0\nAdmin Management"]

    DB[("🗄️ SQLite Database")]
    Media[("📁 Media Storage\n/media/details/")]

    User -->|"Credentials"| P1
    P1 -->|"Session Token"| User
    P1 <-->|"Read/Write User Records"| DB

    User -->|"Tweet Data"| P2
    P2 -->|"Feed / Confirmation"| User
    P2 <-->|"Read/Write Tweet Records"| DB

    P2 -->|"Image File"| P3
    P3 <-->|"Save / Serve Images"| Media

    Admin -->|"Admin Actions"| P4
    P4 <-->|"Read/Write All Records"| DB
```

---

### Level 2 — Process Breakdown
> Expands each Level 1 process into sub-processes.

```mermaid
flowchart TD
    User(["👤 User"])
    DB[("🗄️ SQLite DB")]
    Media[("📁 Media Storage")]

    subgraph AUTH ["1.0 User Authentication"]
        P1_1["1.1 Validate Credentials"]
        P1_2["1.2 Create Session"]
        P1_3["1.3 Destroy Session (Logout)"]
    end

    subgraph TWEET ["2.0 Tweet Management"]
        P2_1["2.1 Fetch All Tweets\n(Index View)"]
        P2_2["2.2 Create Tweet"]
        P2_3["2.3 Edit Tweet"]
        P2_4["2.4 Delete Tweet"]
    end

    subgraph MEDIA ["3.0 Media Handling"]
        P3_1["3.1 Receive Image Upload"]
        P3_2["3.2 Validate Image"]
        P3_3["3.3 Save to /media/details/"]
        P3_4["3.4 Serve Image via Media URL"]
    end

    User -->|"username + password"| P1_1
    P1_1 -->|"Query auth_user"| DB
    DB -->|"User Record"| P1_1
    P1_1 -->|"Valid?"| P1_2
    P1_2 -->|"Session Cookie"| User
    User -->|"Logout Request"| P1_3
    P1_3 -->|"Clear Session"| DB

    User -->|"GET /"| P2_1
    P2_1 -->|"SELECT * FROM two_tweet"| DB
    DB -->|"All Tweets"| P2_1
    P2_1 -->|"Rendered Feed"| User

    User -->|"POST /add_tweet/"| P2_2
    P2_2 -->|"INSERT tweet"| DB
    P2_2 -->|"Image File"| P3_1

    User -->|"POST /edit_tweet/id/"| P2_3
    P2_3 -->|"UPDATE tweet"| DB

    User -->|"POST /delete_tweet/id/"| P2_4
    P2_4 -->|"DELETE tweet"| DB

    P3_1 --> P3_2 --> P3_3
    P3_3 --> Media
    Media -->|"Serve Image"| P3_4
    P3_4 -->|"Image URL"| User
```

---

### Level 3 — Detailed Sub-Process: Tweet Creation
> Drills into the most critical process: creating a tweet.

```mermaid
flowchart TD
    User(["👤 User"])
    DB[("🗄️ SQLite DB\ntwo_tweet table")]
    Media[("📁 /media/details/")]

    Start(["Start: POST /add_tweet/"])
    ExtractTitle["2.2.1 Extract 'tittle' from POST data"]
    ExtractDesc["2.2.2 Extract 'desc' from POST data"]
    ExtractImg["2.2.3 Extract image from FILES"]

    ValidateTitle{"2.2.4 Title\nprovided?"}
    ValidateDesc{"2.2.5 Description\nprovided?"}
    ValidateImg{"2.2.6 Image\nattached?"}

    ErrorTitle["Return Error:\n'Title is compulsory'"]
    ErrorDesc["Return Error:\n'Description is required'"]

    SaveImage["2.2.7 Save image to\n/media/details/"]
    CreateRecord["2.2.8 INSERT into\ntwo_tweet table"]
    Redirect["2.2.9 Redirect to\n/ (index feed)"]

    User --> Start
    Start --> ExtractTitle --> ExtractDesc --> ExtractImg

    ExtractTitle --> ValidateTitle
    ValidateTitle -- "No" --> ErrorTitle --> User
    ValidateTitle -- "Yes" --> ValidateDesc

    ValidateDesc -- "No" --> ErrorDesc --> User
    ValidateDesc -- "Yes" --> ValidateImg

    ValidateImg -- "Yes" --> SaveImage
    SaveImage --> Media
    SaveImage --> CreateRecord

    ValidateImg -- "No" --> CreateRecord
    CreateRecord --> DB
    CreateRecord --> Redirect --> User
```

---

## 5. Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    USER {
        int id PK
        varchar username
        varchar password
        varchar email
        varchar first_name
        varchar last_name
        bool is_staff
        bool is_active
        datetime date_joined
    }

    TWEET {
        int id PK
        varchar tittle
        text desc
        varchar imag
        int user_id FK
    }

    SESSION {
        varchar session_key PK
        text session_data
        datetime expire_date
    }

    USER ||--o{ TWEET : "posts"
    USER ||--o{ SESSION : "has"
```

### ER Diagram Notes

| Entity    | Description                                                              |
|-----------|--------------------------------------------------------------------------|
| `USER`    | Django's built-in `auth_user` table. Stores login credentials and profile info. |
| `TWEET`   | The core content table (`two_tweet`). Each tweet belongs to one user.    |
| `SESSION` | Django's session table. Tracks logged-in user sessions.                  |

**Relationships:**
- One **User** can post **zero or many Tweets** (one-to-many)
- One **User** can have **zero or many Sessions** (one-to-many)
- Each **Tweet** belongs to **one User** (via `user_id` foreign key, nullable)

---

## 6. Summary

| Section         | Detail                                              |
|-----------------|-----------------------------------------------------|
| Platform        | Web Application                                     |
| Language        | Python 3.10+                                        |
| Framework       | Django 5.0                                          |
| Database        | SQLite                                              |
| Architecture    | MVC / MVT (Model-View-Template)                     |
| DFD Levels      | Level 0 (Context), Level 1, Level 2, Level 3        |
| Key Entities    | User, Tweet, Session                                |
| Core Feature    | CRUD micro-blogging with image uploads and auth     |
