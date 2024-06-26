import aiohttp

class BukkitDownloader():
    def __init__(self):
        self.paper_url = "https://papermc.io/api/v2/projects/paper/versions/"
        self.spigot_url = "https://download.getbukkit.org/spigot/spigot-"
        self.session = aiohttp.ClientSession()

    async def get_latest_paper_build(self):
        async with self.session.get(self.paper_url) as response:
            if response.status == 200:
                response_json = await response.json()
                versions = response_json["versions"]
                if not versions:
                    return None
                latest_version = versions[-1]
                return await self.get_paper_build(latest_version)
            return None

    async def get_paper_build(self, version):
        async with self.session.get(f"{self.paper_url}{version}/builds") as response:
            if response.status == 200:
                response_json = await response.json()
                builds = response_json["builds"]
                if not builds:
                    return None
                latest_build = builds[-1]["build"]
                return f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{latest_build}/downloads/paper-{version}-{latest_build}.jar"
            return None

    async def get_spigot_build(self, version):
        async with self.session.get(f"{self.spigot_url}{version}.jar") as response:
            if response.status == 200:
                return f"{self.spigot_url}{version}.jar"
            return None

    async def download(self, url, path):
        async with self.session.get(url) as response:
            if response.status == 200:
                with open(path, "wb") as f:
                    f.write(await response.read())

    async def close(self):
        await self.session.close()
