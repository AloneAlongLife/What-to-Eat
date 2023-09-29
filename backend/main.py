from asyncio import run

from api import run as run_api
from sql_init import sql_init

async def main():
    await sql_init()

    await run_api()

if __name__ == "__main__":
    run(main())
