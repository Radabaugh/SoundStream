import asyncio


class StreamRecorder:
    def __init__(self, voice_client, member, file_path):
        self.voice_client = voice_client
        self.member = member
        self.file_path = file_path
        self.task = None

    async def start(self):
        if self.task:
            return

        self.task = asyncio.create_task(self._record_stream())

    async def stop(self):
        if not self.task:
            return

        self.task.cancel()
        self.task = None

    async def _record_stream(self):
        user_stream = self.voice_client.source

        with open(self.file_path, "ab") as f:
            async for chunk in user_stream:
                f.write(chunk)
