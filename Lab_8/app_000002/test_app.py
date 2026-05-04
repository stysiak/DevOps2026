import requests
import pytest

BASE_URL = "http://localhost:5000"


class TestUppercase:
    def test_basic_lowercase(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": "hello world"})
        assert r.status_code == 200
        assert r.json()["result"] == "HELLO WORLD"

    def test_already_uppercase(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": "ALREADY"})
        assert r.status_code == 200
        assert r.json()["result"] == "ALREADY"

    def test_mixed_case(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": "HeLLo WoRLd"})
        assert r.status_code == 200
        assert r.json()["result"] == "HELLO WORLD"

    def test_empty_text(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": ""})
        assert r.status_code == 200
        assert r.json()["result"] == ""

    def test_text_with_digits(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": "abc123def"})
        assert r.status_code == 200
        assert r.json()["result"] == "ABC123DEF"

    def test_missing_text_field(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={})
        assert r.status_code == 400
        assert "error" in r.json()

    def test_invalid_type_integer(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": 12345})
        assert r.status_code == 400
        assert "error" in r.json()

    def test_invalid_type_list(self):
        r = requests.post(f"{BASE_URL}/uppercase", json={"text": ["hello"]})
        assert r.status_code == 400
        assert "error" in r.json()

    def test_no_body(self):
        r = requests.post(f"{BASE_URL}/uppercase", data="not json",
                          headers={"Content-Type": "application/json"})
        assert r.status_code == 400


class TestReverse:
    def test_basic_reverse(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": "abcde"})
        assert r.status_code == 200
        assert r.json()["result"] == "edcba"

    def test_reverse_word(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": "hello"})
        assert r.status_code == 200
        assert r.json()["result"] == "olleh"

    def test_empty_text(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": ""})
        assert r.status_code == 200
        assert r.json()["result"] == ""

    def test_text_with_digits(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": "abc123"})
        assert r.status_code == 200
        assert r.json()["result"] == "321cba"

    def test_single_char(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": "x"})
        assert r.status_code == 200
        assert r.json()["result"] == "x"

    def test_missing_text_field(self):
        r = requests.post(f"{BASE_URL}/reverse", json={})
        assert r.status_code == 400
        assert "error" in r.json()

    def test_invalid_type_integer(self):
        r = requests.post(f"{BASE_URL}/reverse", json={"text": 42})
        assert r.status_code == 400
        assert "error" in r.json()


class TestWordCount:
    def test_basic_word_count(self):
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

    def test_text_with_multiple_spaces(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": "raz  dwa   trzy"})
        assert r.status_code == 200
        assert r.json()["count"] == 3

    def test_text_with_digits(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": "word1 word2 123"})
        assert r.status_code == 200
        assert r.json()["count"] == 3

    def test_whitespace_only(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": "   "})
        assert r.status_code == 200
        assert r.json()["count"] == 0

    def test_missing_text_field(self):
        r = requests.post(f"{BASE_URL}/word-count", json={})
        assert r.status_code == 400
        assert "error" in r.json()

    def test_invalid_type_integer(self):
        r = requests.post(f"{BASE_URL}/word-count", json={"text": 99})
        assert r.status_code == 400
        assert "error" in r.json()


class TestHealth:
    def test_health_status(self):
        r = requests.get(f"{BASE_URL}/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_health_response_structure(self):
        r = requests.get(f"{BASE_URL}/health")
        assert r.status_code == 200
        data = r.json()
        assert "status" in data
