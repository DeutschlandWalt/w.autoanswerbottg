import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import QThread, pyqtSignal
from telethon import TelegramClient, events

# Данные из my.telegram.org / Data from my.telegram.org
api_id = 'your_api_id'  # Замени на свой API ID
api_hash = 'your_api_hash'  # Замени на свой API Hash
phone_number = 'your_phone_number_tg'  # Номер телефона, привязанный к Telegram

# Создаем клиент Telegram / Creating our own new Telegram client
client = TelegramClient('session_name', api_id, api_hash)

class BotThread(QThread):
    bot_started = pyqtSignal()
    bot_stopped = pyqtSignal()

    def run(self):
        asyncio.run(self.run_bot())

    async def run_bot(self):
        await client.start(phone=phone_number)
        self.bot_started.emit()
        try:
            await client.run_until_disconnected()
        finally:
            self.bot_stopped.emit()

class BotGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("W.Bot")
        self.setGeometry(100, 100, 300, 200)

        self.status_label = QLabel("Статус: Ожидание", self)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_bot)

        self.creator_button = QPushButton("Creator is here", self)
        self.creator_button.clicked.connect(self.creator_mode)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_bot)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.creator_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.bot_running = False
        self.creator_here = False
        self.bot_thread = None

    def start_bot(self):
        if not self.bot_running:
            self.bot_running = True
            self.creator_here = False
            self.status_label.setText("Статус: Бот запущен")
            self.bot_thread = BotThread()
            self.bot_thread.bot_started.connect(lambda: self.status_label.setText("Статус: Бот работает"))
            self.bot_thread.bot_stopped.connect(lambda: self.status_label.setText("Статус: Бот остановлен"))
            self.bot_thread.start()

    def creator_mode(self):
        if self.bot_running:
            self.creator_here = True
            self.status_label.setText("Статус: Создатель здесь, бот молчит")

    def stop_bot(self):
        if self.bot_running:
            self.bot_running = False
            self.creator_here = False
            self.status_label.setText("Статус: Остановка бота...")
            client.disconnect()
            self.bot_thread.quit()
            self.bot_thread.wait()
            self.status_label.setText("Статус: Бот остановлен")

@client.on(events.NewMessage)
async def auto_reply(event):
    sender = await event.get_sender()
    message_text = event.message.message.lower()

    if event.is_private and not sender.bot:
        if window.bot_running and not window.creator_here:
            if "привет" in message_text:
                await event.reply("Привет! Я бот, который будет отвечать на ваши сообщения , пока что-то я незнаю много но мой создатель будет улучшать меня.. Надеюсь)")
            elif "как дела" in message_text:
                await event.reply("У меня всё отлично! А у тебя?")
            elif "что делаешь" in message_text:
                await event.reply("Отвечаю на сообщения, пока мой хозяин занят.")
            elif "спасибо" in message_text:
                await event.reply("Пожалуйста! Обращайся, если что-то нужно.")
            else:
                await event.reply("Извини, я пока не знаю, как ответить на это. Передам хозяину, когда он освободится!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotGUI()
    window.show()
    sys.exit(app.exec())
