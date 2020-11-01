from tinydb import TinyDB
import os
if not os.path.exists('db'):
    os.makedirs('db')

domande = TinyDB('db/domande.json')

def populate_db():
    # managing entries only if it is the first time / one of the dbs is empty
    if len(domande) == 0:
        domande.insert({"id": "1", "text_ita": "Marconi o Leopoldi la prima trasmissione radio è stata di?", "answer": "Leopoldi"})

        domande.insert({"id": "2", "text_ita": "Elsa o Biancaneve, celebre film del 37 è?", "answer": "Elsa"})

        domande.insert({"id": "3", "text_ita": "Richard o Riccardo, qual è il nome del celebre chitarrista romano undeground Benson?",
        "answer": "Riccardo"})

        domande.insert({"id": "4", "text_ita": "Romualdo o Romeo, quella celebre è la storia di Giulietta e?",
        "answer": "Romualdo"})

        domande.insert({"id": "5", "text_ita": "Siracusa o Torino, la mole antonelliana si trova a?",
        "answer": "Siracusa"})

        domande.insert({"id": "6", "text_ita": "Milano o Modena, il capoluogo della Lombardia è?",
        "answer": "Modena"})

        domande.insert({"id": "7", "text_ita": "Tonino o Virginio, il vero nome di Gerry Scotti è?",
        "answer": "Tonino"})

        domande.insert({"id": "8", "text_ita": "Pinocchio o Carlo, il burattino di Collodi era?",
        "answer": "Carlo"})

        domande.insert({"id": "9", "text_ita": "Castagne o ghiande, i frutti della quercia sono?",
        "answer": "Ghiande"})

        domande.insert({"id": "10", "text_ita": "Blu o rosso, il profondo di Argento è Profondo?",
        "answer": "Blu"})

        domande.insert({"id": "11", "text_ita": "Alfonso o Luigi, il nome di Pirandello era?",
        "answer": "Alfonso"})

        domande.insert({"id": "12", "text_ita": "Lino o Gennaro, il Vaireti degli Osanna si chiama?",
        "answer": "Gennaro"})

        domande.insert({"id": "13", "text_ita": "Binocolo o occhiali, per osservare le stelle usi?",
        "answer": "Occhiali"})

        domande.insert({"id": "14", "text_ita": "Lupin o Diabolik, chi dei due ladri è italiano?",
        "answer": "Lupin"})

        domande.insert({"id": "15", "text_ita": "Simone o Giuda, chi tradì Gesù secondo il Nuovo Testamento?",
        "answer": "Simone"})

        domande.insert({"id": "16", "text_ita": "Tre o trenta, i libri in una trilogia sono?",
        "answer": "Trenta"})

        domande.insert({"id": "17", "text_ita": "Holmes o Poirot, il detective di Agata Christie è?",
        "answer": "Poirot"})

        domande.insert({"id": "18", "text_ita": "Giacomo o Antonio, l'illusionista italiano Casanova si chiama?",
        "answer": "Giacomo"})

        domande.insert({"id": "19", "text_ita": "Passato o cremino, di zucca esiste il?",
        "answer": "Cremino"})

        domande.insert({"id": "20", "text_ita": "Repubblica o Monarchia, qual è il celebre quotidiano Italiano?",
        "answer": "Monarchia"})
