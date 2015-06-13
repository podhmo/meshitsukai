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

    @reify
    def users(self):
        return self.get_candidates()

    @reify
    def command_handler(self):
        return CommandHandler(self)

    def get_candidates(self):
        qs = Session.query(User).with_entities(User.name)
        return set("${}".format(u.name) for u in qs)

    @as_view()
    @wrap
    def process_message(self, request):
        command, *args = shlex.split(request.body)
        handler = CommandHandler(self)
        if command in handler:
            return handler(command, *args)

        name = command[1:]  # "$foo" -> "foo"
        user = Session.query(User).filter(User.name == name).first()
        if user is None:
            return ""
        handler = UserHandler(user)
        if len(args) <= 0:
            return handler.get()

        subcommand, *args = args
        if subcommand in handler:
            return handler(subcommand, *args)
        else:
            # $<user> <subcommand>
            return handler.add(subcommand)


class Handler(object):
    def __contains__(self, name):
        return name.startswith("$") and hasattr(self, name[1:])

    def __call__(self, name, *args, **kwargs):
        return getattr(self, name[1:])(*args, **kwargs)


class CommandHandler(Handler):
    def __init__(self, plugin):
        self.plugin = plugin

    def list(self, *args):
        return "\n".join(u.name for u in Session.query(User).all())

    def create(self, name, *args):
        if Session.query(Session.query(User).filter(User.name == name).exists()).scalar():
            return "ng"
        Session.add(User(name=name))
        self.plugin.users.add("${}".format(name))
        return "ok"

    def delete(self, name, *args):
        qs = Session.query(User).filter(User.name == name)
        if not Session.query(qs.exists()).scalar():
            return "ng"
        qs.delete()
        return "ok"


class UserHandler(Handler):
    def __init__(self, user):
        self.user = user

    def add(self, message, *args):
        message = UserMessage(user=self.user, content=message)
        Session.add(message)
        return "ok"

    def remove(self, message, *args):
        Session.query(UserMessage).filter(UserMessage.content == message).delete()
        return "ok"

    def list(self, *args):
        return "\n".join("- {}".format(m.content[:100]) for m in self.user.messages)

    def get(self):
        if len(self.user.messages) <= 0:
            return ""
        return random.choice(self.user.messages).content
