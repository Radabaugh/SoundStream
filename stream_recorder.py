import wave


class StreamRecorder:
    def __init__(self, voice_client, member, file_path):
        self.voice_client = voice_client
        self.member = member
        self.file_path = file_path
        self.wave_file = None
        self.running = False

    async def start(self):
        if self.running:
            return

        self.running = True

        self.wave_file = wave.open(self.file_path, "wb")
        self.wave_file.setsampwidth(2)
        self.wave_file.setnchannels(2)
        self.wave_file.setframerate(3840)

        source = self.voice_client.source.read()
        async for chunk in source:
            if chunk.max() > 0:
                self.wave_file.writeframes(chunk)

    async def stop(self):
        if not self.running:
            return

        self.running = False
        self.wave_file.close()
        self.wave_file = None
