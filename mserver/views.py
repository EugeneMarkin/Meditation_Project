import logging
import asyncio
import time
from os.path import exists

from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings

from production import generate
from constants import OUT_WAV_PATH

logger = logging.getLogger(__name__)

# Create your views here.

async def generate_audio():
    await generate()

async def stream_audio(request):
    print("Streaming audio")
    task = asyncio.create_task(generate_audio())
    await task
    print("exists? ", exists(OUT_WAV_PATH))
    try:
        f = open(OUT_WAV_PATH, 'rb')
        return FileResponse(f, content_type='audio/wave')
    except e:
        print("exception", e)
        pass
