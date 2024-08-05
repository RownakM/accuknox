# Social Networking API

## Overview

This project is a social networking API built using Django Rest Framework. It provides functionalities for user signup, login, searching users, sending and managing friend requests, and listing friends. 

## Features

- User Signup and Login
- Search users by email or name (with pagination)
- Send, accept, and reject friend requests
- List friends and pending friend requests
- Rate-limiting on friend requests to prevent abuse

## Installation

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+

### Setup

1. Clone the repository:

```bash
git clone https://github.com/RownakM/accuknox.git
cd accuknox
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your database. Update the database settings in `settings.py` as needed.

5. Run database migrations:

```bash
python manage.py migrate
```

6. Create a superuser to access the admin panel:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```


### Docker Setup

1. Build and run the Docker containers:

```bash
docker-compose up
```

2. The API will be accessible at `http://localhost:8000`.


### API Collection

1. API Collection is available at _collection_ folder of this repo

## Contact

For any issues or inquiries, please contact [rownakm.kol@gmail.com](mailto:rownakm.kol@gmail.com).