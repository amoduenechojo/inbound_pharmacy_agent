from main import is_end_call


def test_recognizes_each_end_call_word():
    for word in ("bye", "goodbye", "hang up", "exit", "quit"):
        assert is_end_call(word) is True


def test_recognizes_end_call_word_inside_a_sentence():
    assert is_end_call("Okay, bye then") is True


def test_is_case_insensitive():
    assert is_end_call("BYE") is True


def test_does_not_match_unrelated_input():
    assert is_end_call("what does TJM Labs do?") is False
