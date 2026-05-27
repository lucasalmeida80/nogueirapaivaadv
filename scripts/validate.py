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

    # Localiza o template pelo marcador, não por número de linha fixo
    tag = '<script type="__bundler/template">'
    idx = content.find(tag)
    if idx == -1:
        errors.append("Tag __bundler/template não encontrada — estrutura inválida.")
        return errors

    idx_content = idx + len(tag)
    idx_end = content.find("</script>", idx_content)
    if idx_end == -1:
        errors.append("Fechamento da tag __bundler/template não encontrado.")
        return errors

    template_raw = content[idx_content:idx_end].strip()

    # 1. JSON válido
    try:
        html = json.loads(template_raw)
    except json.JSONDecodeError as e:
        errors.append(f"JSON inválido no template: {e}")
        return errors

    # 2. Nenhum </script> sem escape no JSON bruto
    if "</script>" in template_raw:
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
