import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
import wave
from email.message import Message
from http.client import IncompleteRead
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "synthesize_elevenlabs.py"
spec = importlib.util.spec_from_file_location("synthesize_elevenlabs", SCRIPT)
tts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tts)


class SynthesizeElevenLabsTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.text_path = Path(directory.name) / "chunk.txt"
        self.output = Path(directory.name) / "chunk.wav"
        self.text = "Kõigepealt näitan, kuidas töö käib."
        self.text_path.write_text(self.text, encoding="utf-8")
        self.pcm = b"\x04\x01" * 12_000
        self.urlopen = self.enterContext(patch.object(tts, "urlopen"))
        self.env = self.enterContext(patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test-key"}, clear=True))

    def run_cli(self, language="et", *, voice_id="chosenVoice"):
        args = [
            "--language", language, "--text-file", str(self.text_path),
            "--output", str(self.output),
        ]
        if voice_id is not None:
            args.extend(["--voice-id", voice_id])
        tts.main(args)

    def respond(self, body, content_type="application/octet-stream"):
        response = io.BytesIO(body)
        response.headers = Message()
        response.headers["Content-Type"] = content_type
        self.urlopen.return_value = response

    def assert_cli_error(self, expected, *, voice_id="chosenVoice", exit_code=2):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            self.run_cli(voice_id=voice_id)
        self.assertEqual(raised.exception.code, exit_code)
        self.assertIn(expected, stderr.getvalue())
        self.assertNotIn("test-key", stderr.getvalue())

    def test_estonian_locale_uses_selected_voice_and_produces_half_second_wav(self):
        self.respond(self.pcm)
        self.run_cli("et-EE", voice_id="nativeVoice")

        self.urlopen.assert_called_once()
        request = self.urlopen.call_args.args[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.full_url, "https://api.elevenlabs.io/v1/text-to-speech/nativeVoice?output_format=pcm_24000")
        self.assertEqual(request.get_header("Xi-api-key"), "test-key")
        self.assertEqual(request.get_header("Content-type"), "application/json")
        self.assertEqual(json.loads(request.data.decode("utf-8")), {
            "text": self.text,
            "model_id": "eleven_v4",
            "language_code": "et",
        })
        with wave.open(str(self.output), "rb") as wav:
            self.assertEqual((wav.getnchannels(), wav.getsampwidth(), wav.getframerate()), (1, 2, 24_000))
            self.assertEqual(wav.getnframes() / wav.getframerate(), 0.5)
            self.assertEqual(wav.readframes(wav.getnframes()), self.pcm)

    def test_explicit_voice_works_for_other_languages(self):
        self.respond(self.pcm, "audio/pcm")
        self.run_cli("en", voice_id="anotherVoice")
        request = self.urlopen.call_args.args[0]
        self.assertIn("/anotherVoice?", request.full_url)
        self.assertEqual(json.loads(request.data)["language_code"], "en")

    def test_missing_voice_id_fails_before_request(self):
        self.assert_cli_error("arguments are required: --voice-id", voice_id=None)
        self.urlopen.assert_not_called()

    def test_missing_key_fails_before_request(self):
        del self.env["ELEVENLABS_API_KEY"]
        self.assert_cli_error("Set ELEVENLABS_API_KEY")
        self.urlopen.assert_not_called()

    def test_invalid_voice_or_empty_text_fails_before_request(self):
        self.assert_cli_error("valid ElevenLabs voice ID", voice_id="../bad")
        self.text_path.write_text(" \n", encoding="utf-8")
        self.assert_cli_error("narration file is empty")
        self.urlopen.assert_not_called()

    def test_http_failure_preserves_previous_output_and_hides_response_details(self):
        self.output.write_bytes(b"previous WAV")
        self.urlopen.side_effect = HTTPError(
            "https://api.elevenlabs.io/", 401, "test-key", None, io.BytesIO(b"test-key"),
        )
        self.assert_cli_error("HTTP 401", exit_code=1)
        self.assertEqual(self.output.read_bytes(), b"previous WAV")

    def test_network_failure_leaves_no_output(self):
        for error in (TimeoutError(), IncompleteRead(b"partial")):
            with self.subTest(error=type(error).__name__):
                self.urlopen.side_effect = error
                self.assert_cli_error("Could not complete", exit_code=1)
                self.assertFalse(self.output.exists())

    def test_malformed_response_leaves_no_output(self):
        cases = (
            (b'{"detail":"test-key"}', "application/json", "non-audio"),
            (b"", "audio/pcm", "empty or incomplete"),
            (b"\x01", "audio/pcm", "empty or incomplete"),
        )
        for body, content_type, message in cases:
            with self.subTest(body=body):
                self.respond(body, content_type)
                self.assert_cli_error(message, exit_code=1)
                self.assertFalse(self.output.exists())
