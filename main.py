from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import BadRequest
import logging
from base.loader import ModuleLoader
from config import config, CONF_FILE
import os
from logging.handlers import RotatingFileHandler


# Logger .-.
class ColorFormatter(logging.Formatter):
    status_colors = {
        logging.DEBUG: "",
        logging.INFO: "\u001b[32;1m",
        logging.WARN: "\u001b[1m\u001b[33;1m",
        logging.ERROR: "\u001b[1m\u001b[31;1m",
        logging.CRITICAL: "\u001b[1m\u001b[31;1m"
    }
    text_colors = {
        logging.DEBUG: "",
        logging.INFO: "",
        logging.WARN: "\u001b[33m",
        logging.ERROR: "\u001b[31m",
        logging.CRITICAL: "\u001b[31m"
    }
    name_color = "\u001b[37;1m"
    reset = "\u001b[0m"
    text_spacing = "\t" * 8

    def format(self, record: logging.LogRecord) -> str:
        f = f'%(asctime)s | ' \
            f'{self.status_colors[record.levelno]}%(levelname)s{self.reset} | ' \
            f'{self.name_color}%(name)s{self.reset} ' \
            f'\r{self.text_spacing}{self.text_colors[record.levelno]}%(message)s{self.reset}'

        return logging.Formatter(f).format(record)


# File/Console Logger
file_handler = RotatingFileHandler(filename='bot.log', maxBytes=128*1024)  # 128 MB limit

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(ColorFormatter())

handlers = [file_handler, stdout_handler]

logging.basicConfig(level="INFO", handlers=handlers)
logger = logging.getLogger(__name__)

# Root path
ROOT_DIR = os.getcwd()


def main(update_conf: bool = False):
    if config.token:
        # Try to run bot
        try:
            bot = Client(
                name="bot",
                api_id=config.api_id,
                api_hash=config.api_hash,
                bot_token=config.token,
                parse_mode=ParseMode.HTML
            )

        # Reset token and again run main
        except BadRequest:
            config.token = None
            config.api_id = None
            config.api_hash = None
            main(update_conf=True)

        # All ok, write token to config
        if update_conf:
            config.to_yaml_file(CONF_FILE)

        logger.info("Bot starting...")

        loader = ModuleLoader(bot, root_dir=ROOT_DIR)

        # Load modules
        loader.load_everything()

        # Launch bot
        bot.run()
    else:
        config.token = input("Input token: ")
        main(update_conf=True)


if __name__ == "__main__":
    print(
        """


        _/_/_/    _/_/_/    _/      _/                  _/            _/                      
       _/    _/  _/    _/  _/_/  _/_/    _/_/      _/_/_/  _/    _/  _/    _/_/_/  _/  _/_/   
      _/_/_/    _/_/_/    _/  _/  _/  _/    _/  _/    _/  _/    _/  _/  _/    _/  _/_/        
     _/        _/    _/  _/      _/  _/    _/  _/    _/  _/    _/  _/  _/    _/  _/           
    _/        _/_/_/    _/      _/    _/_/      _/_/_/    _/_/_/  _/    _/_/_/  _/            



    """
    )
    main(update_conf=False)
