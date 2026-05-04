"""
Testy pytest dla aplikacji Flask (Lab_8).
Używają biblioteki requests do komunikacji z serwerem na localhost:5000.
Aplikacja musi być uruchomiona przed wywołaniem testów.
"""

import requests
import pytest

BASE_URL = "http://localhost:5000"


# ─── /health ──────────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_returns_ok(self):
        r = requests.get(f"{BASE_URL}/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}


# ─── /uppercase ───────────────────────────────────────────────────────────────

class TestUppercase:
    def test_basic_lowercase(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": "hello world"})
        assert r.status_code == 200
        assert r.json()["result"] == "HELLO WORLD"

    def test_already_uppercase(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": "HELLO"})
        assert r.status_code == 200
        assert r.json()["result"] == "HELLO"

    def test_mixed_case(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": "HeLLo WoRLd"})
        assert r.status_code == 200
        assert r.json()["result"] == "HELLO WORLD"

    def test_empty_text(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": ""})
        assert r.status_code == 200
        assert r.json()["result"] == ""

    def test_text_with_digits(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": "abc 123 def"})
        assert r.status_code == 200
        assert r.json()["result"] == "ABC 123 DEF"

    def test_text_with_multiple_spaces(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": "hello   world"})
        assert r.status_code == 200
        assert r.json()["result"] == "HELLO   WORLD"

    def test_missing_text_field(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={})
        assert r.status_code == 400

    def test_invalid_type_integer(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": 42})
        assert r.status_code == 400

    def test_invalid_type_list(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": ["hello"]})
        assert r.status_code == 400

    def test_invalid_type_none(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": None})
        assert r.status_code == 400


# ─── /reverse ─────────────────────────────────────────────────────────────────

class TestReverse:
    def test_basic_reverse(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": "abcde"})
        assert r.status_code == 200
        assert r.json()["result"] == "edcba"

    def test_single_character(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": "a"})
        assert r.status_code == 200
        assert r.json()["result"] == "a"

    def test_empty_text(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": ""})
        assert r.status_code == 200
        assert r.json()["result"] == ""

    def test_text_with_digits(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": "abc123"})
        assert r.status_code == 200
        assert r.json()["result"] == "321cba"

    def test_text_with_spaces(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": "hello world"})
        assert r.status_code == 200
        assert r.json()["result"] == "dlrow olleh"

    def test_text_with_multiple_spaces(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": "a  b"})
        assert r.status_code == 200
        assert r.json()["result"] == "b  a"

    def test_missing_text_field(self):
        r = requests.post(f"{BASE_URL}/reverse", json={})
        assert r.status_code == 400

    def test_invalid_type_integer(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": 99})
        assert r.status_code == 400

    def test_invalid_type_bool(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": True})
        assert r.status_code == 400


# ─── /word-count ──────────────────────────────────────────────────────────────

class TestWordCount:
    def test_basic_count(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": "raz dwa trzy"})
        assert r.status_code == 200
        assert r.json()["count"] == 3

    def test_single_word(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": "hello"})
        assert r.status_code == 200
        assert r.json()["count"] == 1

    def test_empty_text(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": ""})
        assert r.status_code == 200
        assert r.json()["count"] == 0

    def test_only_spaces(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": "   "})
        assert r.status_code == 200
        assert r.json()["count"] == 0

    def test_multiple_spaces_between_words(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": "hello   world"})
        assert r.status_code == 200
        assert r.json()["count"] == 2

    def test_text_with_digits(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": "abc 123 def"})
        assert r.status_code == 200
        assert r.json()["count"] == 3

    def test_leading_trailing_spaces(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": "  hello world  "})
        assert r.status_code == 200
        assert r.json()["count"] == 2

    def test_missing_text_field(self):
        r = requests.post(f"{BASE_URL}/word-count", json={})
        assert r.status_code == 400

    def test_invalid_type_float(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": 3.14})
        assert r.status_code == 400

    def test_invalid_type_dict(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": {"nested": "value"}})
        assert r.status_code == 400
