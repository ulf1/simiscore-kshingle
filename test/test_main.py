import pytest
from starlette.testclient import TestClient

from app.main import app, srvurl


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


def test_get_info():
    client = TestClient(app)
    response = client.get(f"{srvurl}/")
    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0"}


def test_docs_reachable():
    client = TestClient(app)
    response = client.get(f"{srvurl}/docs")
    assert response.status_code == 200


def test_post_empty_list():
    client = TestClient(app)
    response = client.post(f"{srvurl}/similarities/", json=[])
    assert response.status_code == 200
    assert response.json() == {"ids": [], "matrix": []}


def test_post_multiple_sentences(sentences):
    client = TestClient(app)
    response = client.post(f"{srvurl}/similarities/", json=sentences)
    result = response.json()["matrix"]
    assert response.status_code == 200
    assert result[0][0] == 1
