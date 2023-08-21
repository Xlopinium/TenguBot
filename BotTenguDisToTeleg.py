from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from discord.ext import commands
import discord

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    discord_id = Column(String)
    role = Column(String)
    telegram_id = Column(String)

# Создаем соединение с базой данных
engine = create_engine('sqlite:///contacts.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# определяем intest согласно документации discord.py 
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='*', intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def HowUFeel(ctx):
    responses = ['Good', 'Excellent', 'Too sunny today']
    await ctx.send(f'Feeling: {random.choice(responses)}')

@bot.command()
async def add_user(ctx, discord_id: str, role: str, telegram_id: str):
    new_contact = Contact(discord_id=discord_id, role=role, telegram_id=telegram_id)
    session.add(new_contact)
    session.commit()
    await ctx.send(f'Contact added: Discord ID - {discord_id}, Role - {role}, Telegram ID - {telegram_id}')

@bot.command()
async def View_BD(ctx):
    contacts = session.query(Contact).all()
    response = '\n'.join([f'Discord ID: {contact.discord_id}, Role: {contact.role}, Telegram ID: {contact.telegram_id}' for contact in contacts])
    await ctx.send(response)

@bot.command()
async def shutdown(ctx):
    await bot.logout()

bot.run('MTA5ODE1NzE0NTg0Mjc5NDU0Ng.GDfkgn.tIG-_dkmUy1wu7BSbNNJ-lwvkEDKjj9-0FopHk')

