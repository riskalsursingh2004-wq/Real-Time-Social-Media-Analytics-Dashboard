from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    platform = db.Column(db.String(30), nullable=False, index=True)
    text = db.Column(db.Text, nullable=False)
    cleaned_text = db.Column(db.Text)
    hashtags = db.Column(db.String(500), default="")
    mentions = db.Column(db.String(500), default="")
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    engagement = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    def to_dict(self):
        return dict(id=self.id, username=self.username, platform=self.platform, text=self.text,
            hashtags=self.hashtags, mentions=self.mentions, likes=self.likes, comments=self.comments,
            shares=self.shares, views=self.views, engagement=self.engagement,
            engagement_rate=self.engagement_rate, timestamp=self.timestamp.strftime("%Y-%m-%d %H:%M:%S"))

class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String(80), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(80), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
