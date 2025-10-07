import re
import string
from unidecode import unidecode

def normalize_text(raw_text: str, acronyms: dict = None) -> str:
    """
    Normaliza o texto, padronizando-o, removendo acentos e expandindo siglas.

    Args:
        raw_text (str): O texto bruto a ser normalizado.
        acronyms (dict): Um dicionário onde as chaves são as siglas e os valores são suas expansões.
                         Ex: {"ONU": "Organização das Nações Unidas"}.

    Returns:
        str: O texto normalizado.
    """
    if acronyms is None:
        acronyms = {}

    normalized_text = raw_text

    sorted_acronyms = sorted(acronyms.items(), key=lambda item: len(item[0]), reverse=True)

    for acronym, expansion in sorted_acronyms:
        normalized_text = re.sub(r'\b' + re.escape(acronym) + r'\b', expansion, normalized_text, flags=re.IGNORECASE)

    normalized_text = normalized_text.lower()

    normalized_text = unidecode(normalized_text)

    translator = str.maketrans("", "", string.punctuation)
    normalized_text = normalized_text.translate(translator)

    normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()

    return normalized_text