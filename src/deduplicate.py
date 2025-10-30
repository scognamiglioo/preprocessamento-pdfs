import json
from thefuzz import fuzz

def deduplicate(structured_data: dict, similarity_threshold: int = 90) -> dict:
    """
    Identifica e remove trechos redundantes ou muito semelhantes na estrutura do documento,
    utilizando similaridade de texto para detectar duplicatas aproximadas.

    Args:
        structured_data (dict): A estrutura do documento detectada pela função `detect_structure`.
        similarity_threshold (int): Limiar de similaridade (0-100) para considerar dois textos como duplicatas.

    Returns:
        dict: A estrutura do documento com trechos deduplicados.
    """
    deduplicated_data = structured_data.copy()

    def _deduplicate_paragraphs_fuzzy(paragraphs: list) -> list:
        unique_paragraphs = []
        unique_texts = []

        for para in paragraphs:
            current_text = para["texto"].strip()
            is_duplicate = False
            for unique_t in unique_texts:

                ratio = fuzz.token_set_ratio(current_text, unique_t)
                if ratio >= similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_paragraphs.append(para)
                unique_texts.append(current_text)
        return unique_paragraphs

    if "estrutura" in deduplicated_data:
        for item in deduplicated_data["estrutura"]:
            if "secoes" in item:
                for section in item["secoes"]:
                    if "artigos" in section:
                        for article in section["artigos"]:
                            if "paragrafos" in article:
                                article["paragrafos"] = _deduplicate_paragraphs_fuzzy(article["paragrafos"])
            elif "artigos" in item:
                for article in item["artigos"]:
                    if "paragrafos" in article:
                        article["paragrafos"] = _deduplicate_paragraphs_fuzzy(article["paragrafos"])

    return deduplicated_data