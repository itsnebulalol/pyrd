from asyncio import run
from json import load
from realdebrid import RealDebrid


async def main():
    config = None

    with open("examples/config.json", "r") as f:
        config = load(f)

    async with RealDebrid(config["token"]) as rd:
        torrents = await rd.torrents.get()
        print(await torrents.json())


if __name__ == "__main__":
    run(main())
