from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from discord.ext import commands
import random
import discord

# Создаем соединение с базой данных
engine = create_engine('sqlite:///contacts.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    discord_id = Column(String)
    role = Column(String)
    telegram_id = Column(String)
    def __repr__(self):
        return f"<User(discord_id='{self.discord_id}', role='{self.role}', telegram_id='{self.telegram_id}')>"

Base.metadata.create_all(engine)

# определяем intest согласно документации discord.py 
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def HowUFeel(ctx):
    responses = ['Good', 'Excellent', 'Too sunny today']
    chosen_response = random.choice(responses)
    await ctx.send(f'Feeling: {chosen_response}')

@bot.command()
async def add_user(ctx, discord_id: str, role: str, telegram_id: str):
    new_contact = Contact(discord_id=discord_id, role=role, telegram_id=telegram_id)
    session.add(new_contact)
    session.commit()
    await ctx.send(f'Contact added: Discord ID - {discord_id}, Role - {role}, Telegram ID - {telegram_id}')

@bot.command()
async def view_db(ctx):
    contacts = session.query(Contact).all()
    response = '\n'.join([f'Discord ID: {contact.discord_id}, Role: {contact.role}, Telegram ID: {contact.telegram_id}' for contact in contacts])
    await ctx.send(response)

@bot.command()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.close()

@bot.command()
@commands.is_owner()  # Эта команда доступна только владельцу бота
async def clear_db(ctx):
    session.query(Contact).delete()
    session.commit()
    await ctx.send("Database cleared.")
#Здесь сделаю после удаление, новое создание, либо ограничить команду просмотра БД, если БД пустая

@bot.command()
async def remove_user(ctx, discord_id: str):
    contact_to_remove = session.query(Contact).filter_by(discord_id=discord_id).first()
    
    if contact_to_remove:
        session.delete(contact_to_remove)
        session.commit()
        await ctx.send(f"Contact with Discord ID {discord_id} has been removed.")
    else:
        await ctx.send(f"Contact with Discord ID {discord_id} not found.")


bot.run('Token')

