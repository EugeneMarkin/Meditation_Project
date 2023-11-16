import logging
import asyncio
import time
from os.path import exists

from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings

from production import generate
from logic.constants import OUT_MP3_PATH

logger = logging.getLogger(__name__)

# Create your views here.

async def generate_audio():
    await generate()

async def stream_audio(request):
    print("Streaming audio")
    task = asyncio.create_task(generate_audio())
    await task
    time.sleep(3)
    print("exists? ", exists(OUT_MP3_PATH))

    try:
        f = open(OUT_MP3_PATH, 'rb')
        return FileResponse(f, content_type='audio/mpeg')
    except e:
        print("exception", e)
        pass
