import pytest

from app.shingle_scorer import ShingleScorer


@pytest.fixture(scope="module")
def scorer():
    return ShingleScorer()


@pytest.fixture
def sentences():
    return [
        "Alle Gäste laufen in den gleichen Shorts und Shirts herum, es gibt "
        "Chips und Cola, und an den Spielautomaten wird gedaddelt.",
        "Experten wie der Bremer Rechtspsychologe Gerhard Meyer schätzen, dass"
        " es in Deutschland bis zu 290000 Spielsüchtige gibt.",
        "Und die meisten spielen nicht Roulette oder Lotto, sie daddeln am "
        "Automaten.",
        "Doch warum gehen die Menschen überhaupt in Spielotheken, um dort an "
        "Geld‑ und Unterhaltungsautomaten zu »daddeln«, wie es umgangssprach"
        "lich heißt?",
        "Ich habe mich von den anderen zurückgezogen, bin öfter abends in die"
        " Kneipe gegangen, habe drei Bier getrunken, aber drei Stunden lang "
        "gedaddelt.",
        "Es gibt heute in den Großstädten der westlichen Industrienationen "
        "eine Schicht von Jugendlichen, die Stunden und halbe Tage und Nächte "
        "damit verbringt, in Spielotheken zu stehen und zu daddeln.",
        "Heute daddeln in der U‑Bahn Frauen wie Männer, Kinder wie Senioren "
        "auf ihren Smartphones und Tablets.",
        "Browser‑Spiele müssen nicht einmal heruntergeladen werden, eine kurze"
        " Anmeldung reicht, dann kann gedaddelt werden.",
        "Heute macht neben übermäßigem Fernsehkonsum der Kids vor allem das "
        "»Daddeln« am Computer Eltern und Lehrern Sorge.",
        "Kinder und Schüler auf der ganzen Welt daddeln am Gameboy, und "
        "amerikanische Kids verbringen schon heute mehr Zeit in ihrer "
        "persönlichen Elektroniksphäre (Videospiele, Fernsehen, Radio, CDs) "
        "als mit Freunden oder in der Schule.",
    ]


def test_empty_query(scorer):
    result = scorer.compute_similarity_matrix({})
    assert result == {"ids": [], "matrix": []}


def test_one_query_sentence(scorer, sentences):
    test_sentence = {0: sentences[0]}
    result = scorer.compute_similarity_matrix(test_sentence)
    assert result == {"ids": [0], "matrix": [[1.0]]}


def test_score_for_same_sentence_is_1(scorer, sentences):
    test_sentences = dict(zip(range(2), sentences[0] * 2))
    result = scorer.compute_similarity_matrix(test_sentences)["matrix"][0][0]
    assert result == 1.0


def test_score_for_different_sentences_not_1(scorer, sentences):
    test_sentences = dict(zip(range(2), sentences[:2]))
    result = scorer.compute_similarity_matrix(test_sentences)["matrix"][0]
    assert result[1] != 1.0
    assert result[0] == 1.0


def test_that_all_ids_from_input_returned(scorer, sentences):
    test_sentences = dict(zip(range(len(sentences)), sentences))
    result = scorer.compute_similarity_matrix(test_sentences)["ids"]
    expected = list(range(len(sentences)))
    assert result == expected


def test_scores_multiple_sentences(scorer, sentences):
    test_sentences = dict(zip(range(len(sentences)), sentences))
    result = scorer.compute_similarity_matrix(test_sentences)["matrix"]
    eigen_scores = [result[i][i] for i in range(len(result))]
    assert eigen_scores[0] == 1
    assert pytest.approx(sum(eigen_scores)) == len(sentences)
