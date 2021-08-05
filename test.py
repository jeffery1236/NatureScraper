######################################
# Tests for the NatureScraper module #
######################################
import pytest
from NatureScraper import Scraper


def test_extract_nature_articles():
    scraper = Scraper()
    articles = scraper.extract_nature_articles("2020-02-01", "2020-02-24", 'coronavirus', save_pdf=False)
    expected_titles = [
        'HIV vaccine failure, coronavirus papers and an unprecedented glimpse of the Sun',
        'Did pangolins spread the China coronavirus to people?',
        'How scientists are fighting the novel coronavirus: A three minute guide',
        'CRISPR enhancement, coronavirus source and a controversial appointment',
        'Scientists fear coronavirus spread in countries least able to contain it',
        'More than 80 clinical trials launch to test coronavirus treatments',
        'When will the coronavirus outbreak peak?',
        'Coronavirus name, animal-research data and a Solar System snowman',
        'Scientists question China’s decision not to report symptom-free coronavirus cases',
        'China set to clamp down permanently on wildlife trade in wake of coronavirus',
        '‘No one is allowed to go out’: your stories from the coronavirus outbreak',
    ]
    expected_dates = [
        '2020-02-05', '2020-02-07', '2020-02-07', '2020-02-12',
        '2020-02-13', '2020-02-15', '2020-02-18', '2020-02-19',
        '2020-02-20', '2020-02-21', '2020-02-21',
    ]

    assert len(articles) == 11
    assert [a["Title"] for a in articles] == expected_titles
    assert [a["Published Date"] for a in articles] == expected_dates
