import json, sys, re

REQUIRED_CONTENT = [
    "Nogueira",
    "Paiva",
    "nogueirapaiva",
    "wa.me/92993664378",
    "f-nome",
    "f-tel",
    "f-email",
    "f-area",
    "f-resumo",
    "Falar com um advogado",
    "diversas áreas",
]

def validate(path="index.html"):
    errors = []

    with open(path, "r") as f:
        content = f.read()

    lines = content.split("\n")
    if len(lines) < 185:
        errors.append("Arquivo menor que o esperado — estrutura inválida.")
        return errors

    line185 = lines[184]

    # 1. JSON válido
    try:
        html = json.loads(line185)
    except json.JSONDecodeError as e:
        errors.append(f"JSON inválido na linha 185: {e}")
        return errors

    # 2. Nenhum </script> sem escape no JSON bruto
    if "</script>" in line185:
        errors.append("</script> sem escape encontrado no JSON — vai quebrar o bundler.")

    # 3. Conteúdo obrigatório presente no HTML
    for item in REQUIRED_CONTENT:
        if item not in html:
            errors.append(f"Conteúdo ausente no HTML: '{item}'")

    return errors


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    errors = validate(path)
    if errors:
        print("FALHOU:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("OK — tudo válido.")
        sys.exit(0)
