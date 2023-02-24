import asyncio
import pandas as pd
from src.pygpt import PyGPT
from pycookiecheat import chrome_cookies
import requests
from pathlib import Path
from src.inputparser import parse_arguments
import logging

from typing import Optional, Tuple


def get_current_session_id(
    cookie_file_path: str ='snap/chromium/common/chromium/Default/Cookies'
):
    """Get current session id from static cookies file

    Args:
        cookie_file_path (str, optional): A path to cookies file. 
            Defaults to 'snap/chromium/common/chromium/Default/Cookies'.
            Chrome: ".config/google-chrome/Default/Cookies"
            Chromium "snap/chromium/common/chromium/Default/Cookies"
    Returns:
        _type_: A cookie
    """

    url = 'https://chat.openai.com/api/auth/session'

    cookies_path = Path(cookie_file_path)
    if not cookies_path.is_absolute():
        cookies_path = Path(Path.home()) / cookies_path
    
    if not cookies_path.exists():
        logging.error("Cookies file doesn't exist under {} path".format(
            str(cookies_path))
        )
    
    logging.info("Loading cookies from file: {}".format(cookies_path))

    try:
        cookies = chrome_cookies(url, cookie_file=cookies_path)
    except UnicodeDecodeError:
        raise Exception(
            "Provided cookies file is invalid! Try using Chromium!"
        )
    
    r = requests.get(url, cookies=cookies)
    
    logging.info("Loaded cookies {}".format(cookies))

    try:
        cookies = cookies['__Secure-next-auth.session-token']
    except KeyError:
        raise KeyError(
            "GPT API cookie not found. Remember to login on page: {}".format(
                "https://chat.openai.com/auth/login"
            )
        )
    return cookies

async def initialize_new_connection(
    cookies_path: str,
    token: Optional[str] = None,
    separate_conversations: bool = False
    ) -> PyGPT:
    """Create new connection with GPT API

    Args:
        cookies_path (str): A path to cookies file.

    Returns:
        _type_: PyGPT session.
    """
    if not token:
        logging.info("Loading token from file ...")
        token = get_current_session_id(cookies_path)
    chat_gpt = PyGPT(token, timeout=600, conversation_spam_mode=separate_conversations)
    await chat_gpt.connect()
    await chat_gpt.wait_for_ready()
    return chat_gpt


async def start_interrogation(
    texts: Tuple[str, int],
    cookies_path: str,
    output_dir: str,
    token: Optional[str] = None,
    starting_index: int = 0,
    separate_conversations: bool = False
) -> None:
    """Start interrogation of Chat GPT

    Args:
        texts (Tuple[int, str]): Texts should be a list with tuples: (prompt, text_index)
        cookies_path (str): A path to cookies file stored by chromium
        output_dir (str): Output directory for results
        starting_index (int): Filter out texts with id smaller than this value.
        separate_conversations (bool): Send one prompt per one conversation.

    """
    texts = [(text, text_id) for text, text_id in texts if text_id >= starting_index]
    chat_gpt = await initialize_new_connection(cookies_path, token, separate_conversations)
    output_path = Path(output_dir) / 'outputs.csv'
    for count, (text, text_index) in enumerate(texts):
        try:
            while True:
                answer, status = await chat_gpt.ask(text)
                answer = answer.replace('\n', ' ').replace('\r', ' ')
                if status == 1:
                    break
                elif status == 0: # Docelowo zmiana używanego konta
                    logging.warning("Too many requests. Waiting 10 min with interrogation")
                    await asyncio.sleep(600)
                else: #status == 2
                    await chat_gpt.disconnect()
                    token = chat_gpt.session_token if chat_gpt.session_token else token
                    chat_gpt = await initialize_new_connection(cookies_path, token)
        except Exception as e:
            logging.warning("Got exception {}".format(e))
            await chat_gpt.disconnect()
            token = chat_gpt.session_token if chat_gpt.session_token else token
            chat_gpt = await initialize_new_connection(cookies_path, token)
            answer, status = await chat_gpt.ask(text)
            logging.info("Got status {}".format(status))
            answer = answer.replace('\n', ' ').replace('\r', ' ')
           
        with open(output_path, 'a') as the_file:
            logging.info("{}: Writing text with text_index {} to file.".format(
                count, text_index
                )
            )
            the_file.write(f'{text_index};{answer}\n') # tutaj tab/średnik zamiast przecinka
    await chat_gpt.disconnect()

if __name__ == '__main__':

    args = parse_arguments()
    log_level = args.verbose

    logging.basicConfig(
        level=log_level,
        format=r"%(asctime)s %(funcName)s %(filename)s %(lineno)d [%(levelname)s]: %(message)s",
        # encoding="utf-8",
        handlers=[
            logging.FileHandler(
                "interrogation-api.log",
                mode='w',
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )

    token = args.token
    token_path = args.token_path
    if token_path:
        if Path(token_path).exists():
            with open(token_path, 'r') as token_file:
                token = token_file.read().strip()
            logging.info("Token loaded from file!")
        else:
            logging.warning("Token couldn't be loaded from file {}".format(token_path))
            raise Exception("File {} doesn't exist!".format(token_path))

    df = pd.read_csv(args.data_path)
   
    logging.info("Using {} columns".format(args.columns))

    if args.generate:
        if "id" not in df.columns:
            df = df.reset_index(names="id")

    tuples = list(df[args.columns].itertuples(index=False, name=None))
    logging.debug("Tuples length: {}".format(len(tuples)))

    if log_level == "DEBUG":
        for count, (text, text_index) in enumerate(tuples): # w csv będzie kolumna 'id' i 'prompt'
            print(text_index, "->>>>", text)

    logging.info("One text per one conversation mode: {}".format(args.sep))
    asyncio.run(
        start_interrogation(
            tuples,
            args.cookies,
            args.output,
            token,
            args.start,
            args.sep,
        )
    )
