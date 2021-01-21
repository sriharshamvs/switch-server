from smartHome import db, app, ma
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    room = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))

    def __init__(self, username, room, password_hash):
        self.username = username
        self.room = room
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    @staticmethod
    def find_by_username(username=None, **kw):
        q = User.query.filter_by(**kw)
        if username:
            q = q.filter(User.username == username)
        return q.first()
    
    @staticmethod
    def find_all_users():
        q = User.query.filter(User.username != 'admin').all()
        return q

class Topics(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(10), nullable=False)
    device = db.Column(db.String(10), nullable=False)
    topic = db.Column(db.String(30), unique=True, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    
    def __init__(self, room, device, topic, status, icon):
        self.room = room
        self.device = device
        self.topic = topic
        self.status = status
        self.icon = icon

    @staticmethod
    def find_by_room(room=None, **kw):
        q = Topics.query.filter_by(**kw)
        if room:
            q = q.filter(Topics.room == room)
        return q.all()
    
    @staticmethod
    def find_all_topics():
        q = Topics.query.all()
        return q

class TopicsSchema(ma.Schema):
    class Meta:
        fields = ("room", "device", "topic", "status", "icon")

class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "room")