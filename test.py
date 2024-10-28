import random
import unittest
from difflib import SequenceMatcher, unified_diff
from crypt import *
from student_code import decrypt  # Remplacer par le nom de la fonction de déchiffrement


def similarity_ratio(str1, str2):
    """
    Calcule le pourcentage de similarité entre deux chaînes de caractères.
    """
    return SequenceMatcher(None, str1, str2).ratio()


def print_diff(original, decrypted):
    """
    Imprime les différences entre le texte original et le texte déchiffré.
    """
    diff = unified_diff(
        original.splitlines(),
        decrypted.splitlines(),
        fromfile='Original',
        tofile='Déchiffré',
        lineterm=''
    )
    for line in diff:
        print(line)


class TestDecryption(unittest.TestCase):

    def test_decryption_accuracy(self):
        # Charger le premier corpus et enlever les 10 000 premiers caractères
        url1 = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"
        corpus1 = load_text_from_web(url1)
        corpus1 = corpus1[1905:]  # Enlever les 10 000 premiers caractères

        # Charger le deuxième corpus et enlever les 10 000 premiers caractères
        url2 = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"
        corpus2 = load_text_from_web(url2)
        corpus2 = corpus2[3749:]  # Enlever les 10 000 premiers caractères

        # Combiner les deux corpus
        corpus = corpus1 + corpus2

        caracteres = list(set(list(corpus)))
        nb_caracteres = len(caracteres)
        nb_bicaracteres = 256 - nb_caracteres
        bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(corpus)).most_common(nb_bicaracteres)]
        symboles = caracteres + bicaracteres
        nb_symboles = len(symboles)
        dictionnaire = gen_key(symboles)

        a = random.randint(3400, 7200)
        b = random.randint(12000, 15000)
        l = a+b
        c = random.randint(0, len(corpus)-l)

        M = corpus[c:c+l]

        K = gen_key(symboles)
        C = chiffrer(M, K, dictionnaire)


        # Charger le message original M
        original_message = M  # Remplacer par le texte original utilisé pour le chiffrement

        cryptogram = C  # Remplacer par le cryptogramme chiffré

        # Appeler la fonction de déchiffrement de l'étudiant
        decrypted_message = decrypt(cryptogram)

        # Calculer la similarité
        similarity = similarity_ratio(original_message, decrypted_message)
        print(f"Similarité : {similarity:.2%}")

        # Imprimer les différences si la similarité est inférieure à 95 %
        if similarity < 0.985:
            print("Différences entre les messages :")
            print_diff(original_message, decrypted_message)

        # Vérifier que la similarité entre le message original et le message déchiffré est d'au moins 95 %
        self.assertGreaterEqual(similarity, 0.985,
                                f"La similarité est seulement de {similarity:.2%}, ce qui est inférieur à 95 %.")


if __name__ == '__main__':
    unittest.main()
