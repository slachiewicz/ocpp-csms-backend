import argparse
import asyncio

from loguru import logger
from sqlalchemy.exc import IntegrityError

from manager.services.accounts import create_account
from manager.views.accounts import CreateAccountView

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name')

args = parser.parse_args()
data = CreateAccountView(name=args.name)
try:
    asyncio.run(create_account(data))
except IntegrityError:
    logger.error("It seems the account with the given name to be existing.")
