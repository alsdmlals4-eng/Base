from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "public_video_research_ingest.py"


def load_module():
    spec = importlib.util.spec_from_file_location("public_video_research_ingest", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicVideoLocalTranscriptFallbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_local_vtt_ingest_works_without_ytdlp_and_preserves_hash_provenance(self) -> None:
        module = self.module
        payload = """WEBVTT\n\n00:00:01.000 --> 00:00:03.000\n첫 문장\n\n00:00:03.000 --> 00:00:05.000\n두 번째 문장\n"""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "captions.vtt"
            path.write_text(payload, encoding="utf-8")
            with mock.patch.object(module, "fetch_ytdlp_version") as ytdlp_version:
                packet = module.ingest_local_transcript(
                    "https://youtu.be/ItWEhmEm7jA",
                    path,
                    language="ko",
                )
        ytdlp_version.assert_not_called()
        self.assertEqual("local-file", packet["retrieval"]["tool"])
        self.assertEqual("local_vtt", packet["transcript"]["source_kind"])
        self.assertEqual("AVAILABLE", packet["transcript"]["timestamp_evidence"])
        self.assertEqual(2, packet["transcript"]["segment_count"])
        self.assertRegex(packet["local_transcript_input"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertNotIn(str(path.parent), json.dumps(packet, ensure_ascii=False))

    def test_local_srt_ingest_normalizes_timestamped_segments(self) -> None:
        module = self.module
        payload = """1\n00:00:01,000 --> 00:00:02,500\n첫 줄\n\n2\n00:00:03,000 --> 00:00:04,000\n둘째 줄\n"""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "captions.srt"
            path.write_text(payload, encoding="utf-8")
            packet = module.ingest_local_transcript("ItWEhmEm7jA", path, language="ko")
        self.assertEqual("local_srt", packet["transcript"]["source_kind"])
        self.assertEqual(1.0, packet["transcript"]["segments"][0]["start_sec"])
        self.assertEqual(4.0, packet["transcript"]["segments"][1]["end_sec"])

    def test_plain_text_is_ready_but_cannot_claim_timestamp_evidence(self) -> None:
        module = self.module
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "transcript.txt"
            path.write_text("첫 단락입니다.\n\n두 번째 단락입니다.", encoding="utf-8")
            packet = module.ingest_local_transcript("ItWEhmEm7jA", path, language="ko")
        self.assertEqual("READY", packet["transcript"]["status"])
        self.assertEqual("local_plain_text", packet["transcript"]["source_kind"])
        self.assertEqual("UNAVAILABLE", packet["transcript"]["timestamp_evidence"])
        self.assertEqual("TRANSCRIPT_TEXT_ONLY_NO_TIMESTAMP_FACT_VERIFICATION", packet["content_claim_ceiling"])
        self.assertIsNone(packet["transcript"]["segments"][0]["start_sec"])

    def test_local_input_rejects_unsupported_extension_and_oversized_file(self) -> None:
        module = self.module
        with tempfile.TemporaryDirectory() as temp_dir:
            unsupported = Path(temp_dir) / "captions.json"
            unsupported.write_text("{}", encoding="utf-8")
            with self.assertRaises(module.VideoIngestError) as unsupported_error:
                module.ingest_local_transcript("ItWEhmEm7jA", unsupported)
            self.assertEqual("UNSUPPORTED_LOCAL_TRANSCRIPT_FORMAT", unsupported_error.exception.code)

            oversized = Path(temp_dir) / "captions.txt"
            oversized.write_bytes(b"x" * (module.MAX_LOCAL_TRANSCRIPT_BYTES + 1))
            with self.assertRaises(module.VideoIngestError) as oversized_error:
                module.ingest_local_transcript("ItWEhmEm7jA", oversized)
            self.assertEqual("LOCAL_TRANSCRIPT_TOO_LARGE", oversized_error.exception.code)

    def test_cli_transcript_file_path_skips_ytdlp(self) -> None:
        module = self.module
        with tempfile.TemporaryDirectory() as temp_dir:
            transcript_path = Path(temp_dir) / "captions.vtt"
            transcript_path.write_text(
                "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n내용\n",
                encoding="utf-8",
            )
            output_path = Path(temp_dir) / "packet.json"
            with mock.patch.object(module, "fetch_ytdlp_version") as ytdlp_version:
                rc = module.main(
                    [
                        "ItWEhmEm7jA",
                        "--transcript-file",
                        str(transcript_path),
                        "--language",
                        "ko",
                        "--output",
                        str(output_path),
                    ]
                )
            self.assertEqual(0, rc)
            ytdlp_version.assert_not_called()
            packet = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual("local_vtt", packet["transcript"]["source_kind"])


if __name__ == "__main__":
    unittest.main()
