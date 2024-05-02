from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from models import DBDConnector

router = Router()
db = DBDConnector()


@router.message(Command('start'))
async def start(msg: Message):
    await msg.answer(text='/add *задача* (добавить задачу)\n'
                          '/lst (список всех задач)')


@router.message(Command('add'))
async def add(msg: Message):
    await db.add_user(user_id=msg.from_user.id)
    tasks = msg.text.replace('/add ', '').split(',')
    if '/add' in tasks:
        await msg.answer(text='Вы не ввели задачу.')
    else:
        for task in tasks:
            await db.add_task(msg.from_user.id, task)
        await msg.answer(text='Задача добавлена!')


@router.message(Command('lst'))
async def hyi(msg: Message):
    tasks = await db.get_user_tasks(msg.from_user.id)
    tasks_text = '\n'.join(task[0] for task in tasks)
    await msg.answer(text=tasks_text)
