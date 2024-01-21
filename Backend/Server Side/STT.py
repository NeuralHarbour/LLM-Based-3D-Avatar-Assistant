import asyncio
import websockets
import speech_recognition as sr
import whisper
import os

async def receive_audio_stream(websocket, path):
    global model
    print("Unity connected")

    try:
        while True:
            data = await websocket.recv()
            if not data:
                break

            audio_data = b""
            audio_data += data
            with open("received_audio.wav", "wb") as wav_file:
                wav_file.write(audio_data)

            audio = whisper.load_audio("received_audio.wav")
            audio = whisper.pad_or_trim(audio)

            # make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(model.device)

            # detect the spoken language
            _, probs = model.detect_language(mel)
            detected_language = max(probs, key=probs.get)
            print(f"Detected language: {max(probs, key=probs.get)}")

            await recognize_speech("received_audio.wav", websocket, detected_language)

            # Delete the audio file after processing
            os.remove("received_audio.wav")

    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket connection closed by the client")

async def recognize_speech(file_path, websocket, detected_language):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            if detected_language == 'en':
                text = recognizer.recognize_google(audio_data)
            elif detected_language == 'ja':
                text = recognizer.recognize_google(audio_data, language="ja-JP")
            elif detected_language == 'zh':
                text = recognizer.recognize_google(audio_data, language="zh-CN")
            elif detected_language == 'es':
                text = recognizer.recognize_google(audio_data, language="es-ES")
            elif detected_language == 'ru':
                text = recognizer.recognize_google(audio_data,language = "ru-RU")
            else:
                text = recognizer.recognize_google(audio_data)  # Default to English if language is unknown
            print("Recognized text:", text)
            text_without_apostrophe = text.replace("'", "")
            text_with_lang = f"{text_without_apostrophe} [{detected_language}]"
            await websocket.send(text_with_lang)

        except sr.UnknownValueError:
            error_message = "please say again"
            print(error_message)
            await websocket.send(error_message)
        except sr.RequestError as e:
            print("Error during speech recognition:", e)

if __name__ == "__main__":
    model = whisper.load_model("base")

    start_server = websockets.serve(receive_audio_stream, '0.0.0.0', 8888)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
