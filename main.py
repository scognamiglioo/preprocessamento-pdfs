import os
import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'src'))

from extract_raw import extract_raw
from normalize_text import normalize_text
from detect_structure import detect_structure
from extract_tables import extract_tables
from deduplicate import deduplicate
from enrich_metadata import enrich_metadata

def main():
    print("\n--- Pipeline de Processamento de Documentos --- ")

    input_dir = Path('data/input')
    pdf_files = list(input_dir.glob('*.pdf'))

    if not pdf_files:
        print(f"Nenhum arquivo PDF encontrado no diretório {input_dir}. Por favor, coloque seus PDFs lá.")
        return

    print("Arquivos PDF disponíveis:")
    for i, pdf_file in enumerate(pdf_files):
        print(f"{i+1}. {pdf_file.name}")

    while True:
        try:
            choice = int(input("Selecione o número do arquivo PDF para processar: "))
            if 1 <= choice <= len(pdf_files):
                input_pdf_path = pdf_files[choice - 1]
                break
            else:
                print("Escolha inválida. Por favor, digite um número da lista.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

    print(f"Processando: {input_pdf_path.name}")

    base_name = input_pdf_path.stem
    output_filename = f"{base_name}_output.jsonl"
    output_path = Path('data/output') / output_filename

    try:
        with open(dictionaries_path, 'r', encoding='utf-8') as f:
            dictionaries = json.load(f)
        acronyms = dictionaries.get("acronyms", {})
        dictionaries_path = input_dir / 'dicionarios.json'
        print("Dicionários de normalização carregados com sucesso.")
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{dictionaries_path}' não encontrado. A normalização será limitada.")
        acronyms = {}
        standardization_map = {}


    print("1. Extraindo texto bruto...")
    raw_text = extract_raw(str(input_pdf_path))

    print("2. Normalizando texto...")
    normalized_text = normalize_text(raw_text, acronyms=acronyms)

    print("3. Detectando estrutura...")
    structured_content = detect_structure(str(input_pdf_path), normalized_text)


    print("4. Extraindo tabelas...")
    tables_data = extract_tables(str(input_pdf_path))

    print("5. Deduplicando e verificando consistência...")
    deduplicated_content = deduplicate(structured_content) 

    print("6. Enriquecendo com metadados...")

    custom_metadata = {
        "nome_doc": base_name.replace('_', ' '),
        "versao": "2023.1",
        "data_publicacao": "2023-01-01" # Exemplo
    }
    final_document = enrich_metadata(deduplicated_content, str(input_pdf_path), custom_metadata)

    if tables_data:
        final_document["tables"] = tables_data

    print(f"Processamento concluído. Salvando resultados em {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_document, f, ensure_ascii=False, indent=4)

    print("Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    main()
