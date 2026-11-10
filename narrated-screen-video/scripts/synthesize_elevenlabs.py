#!/usr/bin/env python3
"""Generate one narration chunk as PCM WAV using ElevenLabs."""

import argparse
import json
import os
import re
import tempfile
import wave
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def synthesize(text: str, language: str, voice_id: str, api_key: str, output: Path) -> None:
    payload = {"text": text, "model_id": "eleven_v4", "language_code": language}
    request = Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=pcm_24000",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    # Keep the credential on the original request if the server redirects.
    request.add_unredirected_header("xi-api-key", api_key)
    try:
        with urlopen(request, timeout=60) as response:
            content_type = response.headers.get_content_type()
            if not (content_type.startswith("audio/") or content_type == "application/octet-stream"):
                raise RuntimeError("ElevenLabs returned a non-audio response.")
            pcm = response.read()
    except HTTPError as exc:
        exc.close()
        raise RuntimeError(f"ElevenLabs speech request failed (HTTP {exc.code}).") from None
    except (OSError, HTTPException, ValueError):
        raise RuntimeError("Could not complete the ElevenLabs speech request.") from None

    if not pcm or len(pcm) % 2:
        raise RuntimeError("ElevenLabs returned empty or incomplete 16-bit PCM audio.")

    with tempfile.TemporaryDirectory(dir=output.parent) as directory:
        wav_path = Path(directory) / "chunk.wav"
        with wave.open(str(wav_path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(24_000)
            wav.writeframes(pcm)
        wav_path.replace(output)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", required=True, help="Narration language, such as et or et-EE.")
    parser.add_argument("--voice-id", required=True, help="Selected ElevenLabs voice ID.")
    parser.add_argument("--text-file", required=True, type=Path, help="UTF-8 file containing the words to speak.")
    parser.add_argument("--output", required=True, type=Path, help="Output WAV path.")
    args = parser.parse_args(argv)

    language = args.language.strip().lower().split("-", 1)[0]
    if not re.fullmatch(r"[a-z]{2,3}", language):
        parser.error("Provide a language code such as et or et-EE.")

    voice_id = args.voice_id
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", voice_id):
        parser.error("Provide a valid ElevenLabs voice ID.")

    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        parser.error("Set ELEVENLABS_API_KEY in the environment.")
    if not args.output.parent.is_dir():
        parser.error("The output directory must already exist.")

    try:
        text = args.text_file.read_text(encoding="utf-8").strip()
    except UnicodeError:
        parser.error("The narration file must be UTF-8 text.")
    except OSError as exc:
        parser.error(str(exc))
    if not text:
        parser.error("The narration file is empty.")

    try:
        synthesize(text, language, voice_id, api_key, args.output)
    except (OSError, RuntimeError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
