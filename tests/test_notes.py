from unittest import TestCase
import datetime as dt
import os, os.path
from pdb import set_trace as bp
from pprint import pprint

from notes import _parse_title_and_author_name, _parse_highlight_info, _parse_highlighted_text


class TestNotes(TestCase):
    def setUp(self) -> None:
        pass

    def test_parse_title_and_author_name(self):
        s1 = 'The Billion Dollar Spy: A True Story of Cold War Espionage and Betrayal (David E. Hoffman)'
        assert _parse_title_and_author_name(s1) == \
               ('The Billion Dollar Spy: A True Story of Cold War Espionage and Betrayal', 'David E. Hoffman')

        s2 = 'Skiing with Demons: The Morzine Chalet Project (Tomlinson, Chris)'
        assert _parse_title_and_author_name(s2) == ('Skiing with Demons: The Morzine Chalet Project', 'Tomlinson, Chris')

        s3 = '\ufeffA Storm of Swords (George R. R. Martin)'
        assert _parse_title_and_author_name(s3) == ('A Storm of Swords', 'George R. R. Martin')

    def test_parse_highlight_info(self):
        s1 = 'Your Highlight at location 726-727 | Added on Thursday, 26 July 2018 01:29:40'
        assert _parse_highlight_info(s1) == ('726-727', dt.datetime(2018, 7, 26, 1, 29, 40))

    def test_parse_highlighted_text(self):
        s1 = "Cohen was a little different. He wasn’t particularly fantastic at math, he didn’t study global economies, he had no unique investing philosophy. He was just a great trader,"
        assert _parse_highlighted_text(s1) == "Cohen was a little different. He wasn’t particularly fantastic at math, he didn’t study global economies, he had no unique investing philosophy. He was just a great trader"

