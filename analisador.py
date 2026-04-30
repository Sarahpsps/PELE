
import sqlite3

def analisar_ingredientes(lista_ingredientes: list, tipo_pele: str) -> dict:
    """
    Recebe uma lista de ingredientes e o tipo de pele,
    retorna o score do produto e os alertas encontrados.

    tipo_pele: "seca", "oleosa", "mista" ou "sensivel"
    """

    conn = sqlite3.connect("ingredientes_pele.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    scores = []
    alertas = []
    ingredientes_encontrados = []
    ingredientes_nao_encontrados = []

    coluna_score = f"score_pele_{tipo_pele}"

    for ingrediente in lista_ingredientes:
        ingrediente = ingrediente.strip()

        cursor.execute(f"""
            SELECT *, {coluna_score} as score_usuario
            FROM ingredientes
            WHERE LOWER(nome_inci) = LOWER(?)
            OR LOWER(nome_popular) = LOWER(?)
        """, (ingrediente, ingrediente))

        resultado = cursor.fetchone()

        if resultado:
            ingredientes_encontrados.append(dict(resultado))
            scores.append(resultado["score_usuario"])

            # Verifica alertas
            if resultado["comedogenico"] >= 3:
                alertas.append({
                    "ingrediente": resultado["nome_popular"] or resultado["nome_inci"],
                    "tipo": "⚠️ Comedogênico",
                    "mensagem": f'{resultado["nome_popular"]} pode entupir poros.'
                })
            if resultado["alcool_secante"]:
                alertas.append({
                    "ingrediente": resultado["nome_popular"] or resultado["nome_inci"],
                    "tipo": "🚫 Álcool Secante",
                    "mensagem": f'{resultado["nome_popular"]} resseca e irrita a pele.'
                })
            if resultado["fragancia_irritante"] and tipo_pele == "sensivel":
                alertas.append({
                    "ingrediente": resultado["nome_popular"] or resultado["nome_inci"],
                    "tipo": "🌸 Fragrância",
                    "mensagem": "Fragrância pode irritar pele sensível."
                })
            if not resultado["seguro_gestantes"]:
                alertas.append({
                    "ingrediente": resultado["nome_popular"] or resultado["nome_inci"],
                    "tipo": "🤰 Gestantes",
                    "mensagem": f'{resultado["nome_popular"]} não é recomendado na gestação.'
                })
        else:
            ingredientes_nao_encontrados.append(ingrediente)

    conn.close()

    score_final = round(sum(scores) / len(scores)) if scores else 0

    return {
        "score": score_final,
        "tipo_pele": tipo_pele,
        "total_ingredientes": len(lista_ingredientes),
        "ingredientes_reconhecidos": len(ingredientes_encontrados),
        "alertas": alertas,
        "detalhes": ingredientes_encontrados,
        "nao_encontrados": ingredientes_nao_encontrados
    }


# ─── TESTE ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Simula os ingredientes de um produto com álcool e ácido salicílico
    ingredientes_teste = [
        "Glycerin",
        "Niacinamide",
        "Salicylic Acid",
        "Alcohol Denat.",
        "Hyaluronic Acid",
        "Parfum"
    ]

    print("=== TESTE DO ANALISADOR ===\n")

    for pele in ["seca", "oleosa", "mista", "sensivel"]:
        resultado = analisar_ingredientes(ingredientes_teste, pele)
        print(f"Pele {pele.upper()}: Score {resultado['score']}/100")
        print(f"  Alertas: {len(resultado['alertas'])}")
        for alerta in resultado['alertas']:
            print(f"    {alerta['tipo']} → {alerta['mensagem']}")
        print()