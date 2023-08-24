import io
import os
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse


app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def generate_text(sentence: str):
    # Specify the absolute path for the welcome.wav file
    wav_path = '/usr/src/app/output.wav'

    # Use a temporary file to hold the sentence
    with open('/tmp/sentence.txt', 'w') as file:
        file.write(sentence)

    # Construct the command to call Piper TTS, using the absolute path
    command = f"cat /tmp/sentence.txt | piper --model en_US-lessac-medium --output_file {wav_path}"

    # Execute the command and capture the output
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output for debugging
    print(result.stdout.decode())
    print(result.stderr.decode())

    # Check if the file was created
    if not os.path.exists(wav_path):
        raise Exception(f"File {wav_path} not found. Piper output: {result.stderr.decode()}")

    # Read the generated welcome.wav file using the absolute path
    with open(wav_path, 'rb') as file:
        buffer = io.BytesIO(file.read())

    buffer.seek(0)

    # Return the audio data as a streaming response
    return buffer


class TTSRequest(BaseModel):
    sentence: str
    engine: str = 'piper'


@app.post("/tts/")
@app.post("/tts")
async def text_to_speech(data: TTSRequest):
    sentence = data.sentence
    tts_engine = data.engine

    if not sentence:
        raise HTTPException(status_code=400, detail="Please provide a sentence.")

    buffer = generate_text(sentence)

    return StreamingResponse(buffer, media_type="audio/wav")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
