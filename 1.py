import os
from collections import defaultdict

def count_files_by_extension(root_dir):
    # Dicionário para armazenar contagens de arquivos por extensão
    extensions_count = defaultdict(int)

    # Percorrer todas as pastas e subpastas a partir da raiz
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Obter a extensão do arquivo
            ext = os.path.splitext(file)[1]
            # Incrementar a contagem para a extensão correspondente
            extensions_count[ext] += 1

    return extensions_count

def main():
    root_dir = input("Digite o caminho da pasta raiz: ")
    extensions_count = count_files_by_extension(root_dir)

    print("Contagem de arquivos por extensão:")
    for ext, count in extensions_count.items():
        print(f"{ext if ext else 'Sem extensão'}: {count}")

if __name__ == "__main__":
    main()