from asyncio import run
from json import load
from realdebrid import RealDebrid


async def main():
    config = None

    with open("examples/config.json", "r") as f:
        config = load(f)

    async with RealDebrid(config["token"]) as rd:
        user = await rd.user.get()
        print(await user.json())


if __name__ == "__main__":
    run(main())
