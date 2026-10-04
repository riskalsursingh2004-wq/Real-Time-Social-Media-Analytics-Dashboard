from datetime import datetime
from models import db, Post, Hashtag, Keyword
from analysis.preprocessing import *
from analysis.engagement import engagement, engagement_rate
FMT = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]
PLATFORMS = ["Instagram", "X/Twitter", "Facebook", "YouTube", "LinkedIn", "Other"]
class DuplicateError(ValueError): pass
def _int(d, k):
    try: v = int(float(d.get(k) or 0))
    except (TypeError, ValueError): raise ValueError(f"'{k}' must be a number")
    if v < 0: raise ValueError(f"'{k}' cannot be negative")
    return v
def _ts(v):
    if not v or not str(v).strip(): return datetime.now()
    for f in FMT:
        try: return datetime.strptime(str(v).strip(), f)
        except ValueError: pass
    raise ValueError("Invalid timestamp (use YYYY-MM-DD HH:MM:SS)")
def ingest_post(d):
    """validate -> preprocess -> extract -> engagement -> store"""
    if not isinstance(d, dict): raise ValueError("Invalid request body")
    user = str(d.get("username") or "").strip().lstrip("@")[:80]
    text = str(d.get("text") or "").strip()
    plat = str(d.get("platform") or "").strip()
    if not user: raise ValueError("Username is required")
    if not text: raise ValueError("Post text cannot be empty")
    if plat not in PLATFORMS: raise ValueError("Platform must be one of: " + ", ".join(PLATFORMS))
    likes, com, sh, views = (_int(d, k) for k in ("likes", "comments", "shares", "views"))
    ts = _ts(d.get("timestamp"))
    if Post.query.filter_by(username=user, platform=plat, text=text, timestamp=ts).first():
        raise DuplicateError("Duplicate post")
    tags = sorted(set(extract_hashtags(text)) | set(parse_tags(d.get("hashtags"))))
    ments = sorted(set(extract_mentions(text)) | set(parse_tags(d.get("mentions"))))
    cleaned = clean_text(text); eng = engagement(likes, com, sh)
    p = Post(username=user, platform=plat, text=text, cleaned_text=cleaned, hashtags=" ".join(tags),
             mentions=" ".join(ments), likes=likes, comments=com, shares=sh, views=views,
             engagement=eng, engagement_rate=engagement_rate(eng, views), timestamp=ts)
    db.session.add(p); db.session.flush()
    db.session.add_all([Hashtag(hashtag=t, post_id=p.id) for t in tags])
    db.session.add_all([Keyword(keyword=k, post_id=p.id) for k in extract_keywords(cleaned)])
    db.session.commit()
    return p
