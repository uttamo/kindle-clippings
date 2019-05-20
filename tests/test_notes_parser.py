from unittest import TestCase
import datetime as dt
import os.path

from notes_parser import parse_file, parse_title_and_author_name, parse_highlight_info, parse_highlighted_text


class TestNotesParser(TestCase):
    def test_parse_title_and_author_name(self):
        s1 = 'The Billion Dollar Spy: A True Story of Cold War Espionage and Betrayal (David E. Hoffman)'
        assert parse_title_and_author_name(s1) == \
               ('The Billion Dollar Spy: A True Story of Cold War Espionage and Betrayal', 'David E. Hoffman')

        s2 = 'Skiing with Demons: The Morzine Chalet Project (Tomlinson, Chris)'
        assert parse_title_and_author_name(s2) == ('Skiing with Demons: The Morzine Chalet Project', 'Tomlinson, Chris')

        s3 = '\ufeffA Storm of Swords (George R. R. Martin)'
        assert parse_title_and_author_name(s3) == ('A Storm of Swords', 'George R. R. Martin')

    def test_parse_highlight_info(self):
        s1 = 'Your Highlight at location 726-727 | Added on Thursday, 26 July 2018 01:29:40'
        assert parse_highlight_info(s1) == ('726-727', dt.datetime(2018, 7, 26, 1, 29, 40))

    def test_parse_highlighted_text(self):
        s1 = "Cohen was a little different. He wasn’t particularly fantastic at math, he didn’t study global economies, he had no unique investing philosophy. He was just a great trader,"
        assert parse_highlighted_text(
            s1) == "Cohen was a little different. He wasn’t particularly fantastic at math, he didn’t study global economies, he had no unique investing philosophy. He was just a great trader"

    def test_parse(self):
        filename = os.path.join('tests', 'testdata', 'clippings_test.txt')
        parsed_file = parse_file(filename)
        assert parsed_file == {
            'Black Edge: Inside Information, Dirty Money, and the Quest to Bring Down the Most Wanted Man on Wall Street': {
                'author': 'Sheelah Kolhatkar', 'notes': [
                    {'location': '726-727', 'time_added': dt.datetime(2018, 7, 26, 1, 29, 40),
                     'highlighted_text': 'Cohen was a little different. He wasn’t particularly fantastic at math, he '
                                         'didn’t study global economies, he had no unique investing philosophy. He was'
                                         ' just a great trader,'},
                    {'location': '756-756', 'time_added': dt.datetime(2018, 7, 26, 1, 37, 14),
                     'highlighted_text': 'The key to making money, they believed, was by intelligently controlling '
                                         'their losses'},
                    {'location': '2555-2558', 'time_added': dt.datetime(2018, 8, 2, 23, 44, 15),
                     'highlighted_text': 'An agent met Ali Far in the lobby and escorted him to a conference room on '
                                         'the sixth floor; after making sure the elevator was clear, Andrew Michaelson '
                                         'met Far’s partner, C. B. Lee, and brought him to the fifth floor. Michaelson '
                                         'and another prosecutor, Josh Klein, raced back and forth between the two '
                                         'rooms, trying to act as if nothing unusual was going on. The goal was to '
                                         'play them off against one another and try to pressure them to cooperate '
                                         'fully, all without alienating them. It was a delicate situation.'},
                    {'location': '3431-3433', 'time_added': dt.datetime(2018, 8, 8, 0, 43, 44),
                     'highlighted_text': 'Mathew’s performance wasn’t enough to get him into Harvard, and his father '
                                         'was furious at his son. His anger drove him to a stunning act of paternal '
                                         'cruelty. A few weeks after Mathew’s eighteenth birthday, he presented his '
                                         'son with a plaque that said: “Son Who Shattered His Father’s Dream.”'},
                    {'location': '5107-5108', 'time_added': dt.datetime(2018, 8, 16, 0, 2, 48),
                     'highlighted_text': 'The financial industry has evolved to be so complex that large parts of it '
                                         'are almost completely beyond the reach of regulators and law enforcement'},
                    {'location': '5110-5110', 'time_added': dt.datetime(2018, 8, 16, 0, 4, 49),
                     'highlighted_text': 'it has become almost impossible, due to a lack of will'},
                    {'location': '5110-5111', 'time_added': dt.datetime(2018, 8, 16, 0, 4, 54),
                     'highlighted_text': 'it has become almost impossible, due to a lack of will or expertise, to '
                                         'prosecute corporate criminals who'}]},
            'A Storm of Swords': {'author': 'George R. R. Martin', 'notes': [
                    {'location': '2392-2392', 'time_added': dt.datetime(2018, 8, 11, 20, 2, 25),
                     'highlighted_text': 'was hot and smoky. Baskets of burning peat'},
            ]}}

    def test_parse_duplicated_notes(self):
        filename = os.path.join('tests', 'testdata', 'duplicate_test.txt')
        parsed_file = parse_file(filename)
        assert parsed_file == {'Black Edge: Inside Information, Dirty Money, and the Quest to Bring Down the '
                               'Most Wanted Man on Wall Street':
                                   {'author': 'Sheelah Kolhatkar',
                                    'notes': [{'location': '726-727',
                                               'time_added': dt.datetime(2018, 7, 26, 1, 29, 52),
                                               'highlighted_text': 'Cohen was a little different. He wasn’t '
                                                                   'particularly fantastic at math, he didn’t study '
                                                                   'global economies, he had no unique investing '
                                                                   'philosophy. He was just a great trader,'}]}}
