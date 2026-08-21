from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "public_video_research_ingest.py"


def load_module():
    spec = importlib.util.spec_from_file_location("public_video_research_ingest", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("module spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicVideoResearchIngestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_extract_video_id_accepts_common_youtube_forms(self) -> None:
        module = self.module
        expected = "ItWEhmEm7jA"
        self.assertEqual(expected, module.extract_video_id(expected))
        self.assertEqual(expected, module.extract_video_id("https://youtu.be/ItWEhmEm7jA?si=x"))
        self.assertEqual(expected, module.extract_video_id("https://www.youtube.com/watch?v=ItWEhmEm7jA"))
        self.assertEqual(expected, module.extract_video_id("https://youtube.com/shorts/ItWEhmEm7jA?feature=share"))
        self.assertEqual(expected, module.extract_video_id("https://www.youtube.com/embed/ItWEhmEm7jA"))

    def test_extract_video_id_rejects_non_youtube_or_invalid_id(self) -> None:
        module = self.module
        for value in ("https://example.com/watch?v=ItWEhmEm7jA", "bad", "https://youtu.be/not-long-enough"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                module.extract_video_id(value)

    def test_choose_caption_track_prefers_manual_before_auto_and_vtt(self) -> None:
        module = self.module
        metadata = {
            "subtitles": {
                "en": [
                    {"ext": "srv3", "url": "https://www.youtube.com/caption-en-srv3"},
                    {"ext": "vtt", "url": "https://www.youtube.com/caption-en-vtt", "name": "English"},
                ]
            },
            "automatic_captions": {
                "ko": [{"ext": "vtt", "url": "https://www.youtube.com/caption-ko-auto", "name": "Korean (auto)"}]
            },
        }
        track = module.choose_caption_track(metadata, ["ko", "en"])
        self.assertEqual("youtube_manual_caption", track["source_kind"])
        self.assertEqual("en", track["language"])
        self.assertFalse(track["is_generated"])
        self.assertEqual("vtt", track["ext"])
        self.assertEqual("https://www.youtube.com/caption-en-vtt", track["url"])
        self.assertEqual("English", track["track_label"])

    def test_choose_caption_track_obeys_language_priority_within_source(self) -> None:
        module = self.module
        metadata = {
            "subtitles": {
                "en-US": [{"ext": "vtt", "url": "https://www.youtube.com/en-us"}],
                "ko": [{"ext": "vtt", "url": "https://www.youtube.com/ko"}],
            },
            "automatic_captions": {},
        }
        track = module.choose_caption_track(metadata, ["ko", "en"])
        self.assertEqual("ko", track["language"])
        self.assertEqual("https://www.youtube.com/ko", track["url"])

    def test_choose_caption_track_raises_when_no_caption_exists(self) -> None:
        module = self.module
        with self.assertRaises(module.NoCaptionTrack):
            module.choose_caption_track({"subtitles": {}, "automatic_captions": {}}, ["ko", "en"])

    def test_parse_vtt_normalizes_tags_entities_and_consecutive_duplicates(self) -> None:
        module = self.module
        vtt = """WEBVTT

00:00:00.000 --> 00:00:01.500 align:start position:0%
<c>첫 &amp; 문장</c>

00:00:01.500 --> 00:00:03.000
<c>첫 &amp; 문장</c>

00:00:03.000 --> 00:00:05.000
<00:00:03.000><c>두 번째</c>   문장

00:00:06.000 --> 00:00:07.000
첫 &amp; 문장
"""
        segments = module.parse_vtt(vtt)
        self.assertEqual(["첫 & 문장", "두 번째 문장", "첫 & 문장"], [item["text"] for item in segments])
        self.assertEqual(0.0, segments[0]["start_sec"])
        self.assertEqual(1.5, segments[0]["end_sec"])
        self.assertEqual(6.0, segments[-1]["start_sec"])

    def test_parse_vtt_rejects_empty_effective_transcript(self) -> None:
        module = self.module
        with self.assertRaises(module.EmptyTranscript):
            module.parse_vtt("WEBVTT\n\nNOTE no speech\nmetadata only\n")

    def test_validate_caption_url_is_fail_closed(self) -> None:
        module = self.module
        self.assertEqual("https://www.youtube.com/api/timedtext?x=1", module.validate_caption_url("https://www.youtube.com/api/timedtext?x=1"))
        self.assertEqual("https://r1.googlevideo.com/caption.vtt", module.validate_caption_url("https://r1.googlevideo.com/caption.vtt"))
        for value in ("http://www.youtube.com/api/timedtext", "https://example.com/caption.vtt", "file:///tmp/caption.vtt"):
            with self.subTest(value=value), self.assertRaises(module.VideoIngestError):
                module.validate_caption_url(value)

    def test_build_evidence_packet_preserves_provenance_and_local_storage_policy(self) -> None:
        module = self.module
        metadata = {
            "id": "ItWEhmEm7jA",
            "title": "Example",
            "uploader": "Creator",
            "duration": 125.5,
            "upload_date": "20260822",
            "webpage_url": "https://www.youtube.com/watch?v=ItWEhmEm7jA",
        }
        track = {
            "source_kind": "youtube_auto_caption",
            "language": "ko",
            "is_generated": True,
            "track_label": "Korean (auto)",
            "url": "https://www.youtube.com/caption",
            "ext": "vtt",
        }
        segments = [{"start_sec": 1.0, "end_sec": 2.0, "text": "내용"}]
        packet = module.build_evidence_packet(
            metadata,
            source_url="https://youtu.be/ItWEhmEm7jA",
            tool_version="2026.08.22",
            track=track,
            segments=segments,
            status="READY",
            checked_at="2026-08-22T00:00:00Z",
        )
        self.assertEqual(1, packet["schema_version"])
        self.assertEqual("ItWEhmEm7jA", packet["video_id"])
        self.assertEqual("2026-08-22", packet["published_or_uploaded_at"])
        self.assertEqual("youtube_auto_caption", packet["transcript"]["source_kind"])
        self.assertTrue(packet["transcript"]["is_generated"])
        self.assertEqual("LOCAL_RESEARCH_ONLY", packet["storage_policy"]["full_transcript"])
        self.assertEqual(".tmp/public-video-research", packet["storage_policy"]["default_output_root"])

    def test_build_no_caption_packet_marks_asr_fallback_required(self) -> None:
        module = self.module
        metadata = {"id": "ItWEhmEm7jA", "title": "Example"}
        packet = module.build_evidence_packet(
            metadata,
            source_url="https://youtu.be/ItWEhmEm7jA",
            tool_version="2026.08.22",
            track=None,
            segments=[],
            status="ASR_FALLBACK_REQUIRED",
            checked_at="2026-08-22T00:00:00Z",
        )
        self.assertEqual("ASR_FALLBACK_REQUIRED", packet["transcript"]["status"])
        self.assertEqual("none", packet["transcript"]["source_kind"])
        self.assertEqual([], packet["transcript"]["segments"])
        self.assertEqual("BLOCKED_UNVERIFIED", packet["content_claim_ceiling"])

    def test_write_packet_uses_video_id_not_untrusted_title(self) -> None:
        module = self.module
        packet = {
            "video_id": "ItWEhmEm7jA",
            "title": "../../unsafe title",
            "transcript": {"status": "READY"},
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = module.write_packet(packet, output=None, default_root=Path(temp_dir))
            self.assertEqual("ItWEhmEm7jA.json", path.name)
            self.assertEqual(Path(temp_dir), path.parent)
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("ItWEhmEm7jA", loaded["video_id"])


if __name__ == "__main__":
    unittest.main()
