from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from discord.ext import commands
import discord

engine = create_engine('sqlite:///mydatabase.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    telegram_contacts = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', role='{self.role}', telegram_contacts='{self.telegram_contacts}')>"

Base.metadata.create_all(engine)

# определ€ем intest согласно документации discord.py 
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='*', intents=intents)

@bot.command()
async def telegram(ctx, user):
    user_data = session.query(User).filter_by(name=user).first()
    if user_data:
        await ctx.send(f"User: {user_data.name}\nRole: {user_data.role}\nTelegram contacts: {user_data.telegram_contacts}")
    else:
        await ctx.send("User not found")

@bot.command()
async def all_users(ctx):
    all_users_data = session.query(User).all()
    if all_users_data:
        for user_data in all_users_data:
            await ctx.send(f"User: {user_data.name}, Role: {user_data.role}, Telegram contacts: {user_data.telegram_contacts}")
    else:
        await ctx.send("No users found")

@bot.command()
async def add_user(ctx, name, role, telegram_contacts):
    new_user = User(name=name, role=role, telegram_contacts=telegram_contacts)
    session.add(new_user)
    session.commit()
    await ctx.send(f"New user added: {name}")

@bot.command()
async def remove(ctx, user: discord.User):
    session = Session()

    try:
        # »щем пользовател€ в базе данных
        db_user = session.query(User).filter_by(id=user.id).one()

        # ”дал€ем пользовател€ из базы данных
        session.delete(db_user)
        session.commit()

        await ctx.send(f"User {user.name} has been removed from the database.")
    except NoResultFound:
        await ctx.send(f"User {user.name} is not in the database.")
    finally:
        
        session.close()

bot.run('Token')
