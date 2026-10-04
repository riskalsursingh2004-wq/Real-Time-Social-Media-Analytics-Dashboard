# Real-Time Social Media Analytics Dashboard (core version)
Flask + SQLAlchemy + SQLite + Bootstrap 5 + Chart.js. All dashboard numbers are computed from the database.
## Run
    pip install -r requirements.txt
    python app.py          # http://localhost:5000
Then open **CSV Upload** and upload `data/sample_posts.csv` (regenerate fresh timestamps with `python data/generate_sample.py`).
## Docker
    docker build -t real-time-social-analytics .
    docker run -d --name social-analytics -p 5000:5000 real-time-social-analytics
## Input methods
Form (`/add`), CSV (`/upload`), REST `POST /api/posts` with JSON: username, platform, text, hashtags[], mentions[], likes, comments, shares, views, timestamp.
## Formulas
Engagement = likes + comments + shares. Rate = engagement / views x 100 (only if views > 0).
Growth % = (current window posts - previous equal window posts) / previous x 100; "Trending upward" only if growth > 0 from stored data.
## API
POST/GET /api/posts, GET /api/posts/<id>, /api/hashtags, /api/keywords, /api/platforms, /api/analytics?minutes=60, /api/trends, /api/live-feed
## Limitations
Not connected to real social platforms (data comes from form/CSV/API). Polling every 5s. Not yet built: reports/PDF, time-analysis page, settings, platform/analytics-history tables.
