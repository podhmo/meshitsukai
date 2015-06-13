# -*- coding:utf-8 -*-
import shlex
import random
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from meshitsukai.plugin import Plugin
from meshitsukai.langhelpers import reify
from meshitsukai.view import as_view
import logging


logger = logging.getLogger(__name__)
Session = scoped_session(sessionmaker())
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sa.Column(sa.String(32), nullable=False, default="", unique=True)


class UserMessage(Base):
    __tablename__ = 'user_message'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False)
    content = sa.Column(sa.Text, nullable=False, default="")
    user = orm.relationship(User, backref="messages")


def wrap(fn):
    def _wrap(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            Session.commit()
            return result
        except:
            logger.exception("hmm")
            Session.rollback()
    return _wrap


class Goroku(Plugin):
    def setup(self, context):
        super(Goroku, self).setup(context)
        engine = sa.create_engine(self.settings["db"])
        Session.configure(bind=engine)
        Base.metadata.bind = engine
        Base.metadata.create_all()

    specials = ["$create", "$list"]

    def predicate(self, request):
        line = request.body.strip()
        return any(line.startswith(s) for s in self.specials) or any(u in line for u in self.users)

    @reify
    def users(self):
        return self.get_candidates()

    def get_candidates(self):
        qs = Session.query(User).with_entities(User.name)
        return set("${}".format(u.name) for u in qs)

    @as_view(predicate="predicate")
    @wrap
    def process_message(self, request):
        name, *args = shlex.split(request.body)
        if name.startswith("$create"):
            newname = " ".join(args)
            self.users.add(newname)
            return create(newname)
        elif name.startswith("$list"):
            return "\n".join(u.name for u in Session.query(User).all())

        name = name[1:]  # "$foo" -> "foo"
        user = Session.query(User).filter(User.name == name).first()
        if user is None:
            return ""
        if not args:
            return get(user)
        else:
            return post(user, " ".join(args))


def create(name):
    Session.add(User(name=name))
    return "ok"


def get(user):
    if len(user.messages) <= 0:
        return ""
    return random.choice(user.messages).content


def post(user, message):
    message = UserMessage(user=user, content=message)
    Session.add(message)
    return "ok"
