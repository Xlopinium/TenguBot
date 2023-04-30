import discord
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

engine = create_engine('sqlite:///TenguDB.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    telegram_contacts = Column(String)

Base.metadata.create_all(engine)
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def telegram(ctx, member: discord.Member):
    # Открываем сессию
    session = Session()
    user = session.query(User).filter_by(name=member.name).first()
    if user:
        response = f"Telegram contacts for {user.name}:\n{user.telegram_contacts}"
    else:
        response = "User not found"
    await ctx.send(response)
    # Закрываем сессию
    session.close()

@bot.command()
async def save(ctx, name: str, role: str, telegram: str):
    user = User(name=name, role=role, telegram_contacts=telegram)
    session.add(user)
    session.commit()
    await ctx.send("User saved")

@bot.command()
async def users(ctx):
    # Открываем сессию
    session = Session()
    # Извлекаем все записи из таблицы users
    users = session.query(User).all()
    # Создаем список строк с информацией о каждом пользователе
    user_info = [f"{user.name}: {user.role}, {user.telegram_contacts}" for user in users]
    # Формируем ответ и отправляем его в чат
    response = "\n".join(user_info) if user_info else "No users found in the database."
    await ctx.send(response)
    # Закрываем сессию
    session.close()

bot.run('MTA5ODE1NzE0NTg0Mjc5NDU0Ng.GKI0AM.KvizC8wj5YvZ1KN-jWTYspOL7m02bEKlI9lICg')