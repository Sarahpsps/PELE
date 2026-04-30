
import sqlite3

# Conecta (ou cria) o banco de dados
conn = sqlite3.connect("ingredientes_pele.db")
cursor = conn.cursor()

# Cria a tabela de ingredientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_inci TEXT NOT NULL,
    nome_popular TEXT,
    score_pele_seca INTEGER,
    score_pele_oleosa INTEGER,
    score_pele_mista INTEGER,
    score_pele_sensivel INTEGER,
    comedogenico INTEGER DEFAULT 0,
    alcool_secante INTEGER DEFAULT 0,
    fragancia_irritante INTEGER DEFAULT 0,
    seguro_gestantes INTEGER DEFAULT 1,
    categoria TEXT,
    explicacao TEXT
)
""")

ingredientes = [
    # (nome_inci, nome_popular, seca, oleosa, mista, sensivel, comedogenico, alcool_secante, fragancia_irritante, gestantes, categoria, explicacao)

    # HIDRATANTES / EMOLIENTES
    ("Glycerin", "Glicerina", 95, 75, 80, 90, 0, 0, 0, 1, "Hidratante", "Umectante poderoso que atrai água para a pele. Ótimo para todos os tipos."),
    ("Hyaluronic Acid", "Ácido Hialurônico", 98, 90, 92, 95, 0, 0, 0, 1, "Hidratante", "Retém até 1000x seu peso em água. Um dos melhores ativos para hidratação."),
    ("Niacinamide", "Niacinamida", 80, 95, 90, 85, 0, 0, 0, 1, "Multifuncional", "Controla oleosidade, minimiza poros e uniformiza o tom. Excelente para pele oleosa."),
    ("Ceramide NP", "Ceramida", 98, 70, 80, 95, 0, 0, 0, 1, "Barreira cutânea", "Restaura a barreira da pele. Essencial para pele seca e sensível."),
    ("Squalane", "Esqualano", 92, 78, 82, 90, 0, 0, 0, 1, "Emoliente", "Óleo leve que imita o sebo da pele. Hidrata sem obstruir os poros."),
    ("Shea Butter", "Manteiga de Karité", 95, 40, 55, 80, 2, 0, 0, 1, "Emoliente", "Rico em ácidos graxos. Ótimo para pele seca, mas pode entupir poros em pele oleosa."),
    ("Jojoba Oil", "Óleo de Jojoba", 88, 80, 82, 85, 2, 0, 0, 1, "Emoliente", "Tecnicamente uma cera líquida. Equilibra a oleosidade e hidrata sem pesar."),
    ("Aloe Barbadensis Leaf Juice", "Babosa / Aloe Vera", 85, 88, 87, 92, 0, 0, 0, 1, "Calmante", "Hidrata, acalma e tem leve ação anti-inflamatória. Ótimo para pele sensível."),
    ("Panthenol", "Pró-vitamina B5", 90, 82, 85, 90, 0, 0, 0, 1, "Hidratante", "Hidrata e ajuda na cicatrização da pele. Muito bem tolerado por todos."),
    ("Centella Asiatica Extract", "Centella Asiática", 80, 82, 82, 95, 0, 0, 0, 1, "Calmante", "Acalma irritações, estimula colágeno e fortalece a barreira cutânea."),

    # ESFOLIANTES / ÁCIDOS
    ("Salicylic Acid", "Ácido Salicílico", 50, 95, 85, 60, 0, 0, 0, 0, "Esfoliante BHA", "Penetra nos poros e dissolve sebum. Excelente para acne e pele oleosa. Evitar na gestação."),
    ("Glycolic Acid", "Ácido Glicólico", 72, 85, 80, 45, 0, 0, 0, 0, "Esfoliante AHA", "Renova a pele e melhora textura. Pode irritar pele sensível. Evitar na gestação."),
    ("Lactic Acid", "Ácido Lático", 80, 78, 78, 70, 0, 0, 0, 0, "Esfoliante AHA", "Mais suave que o glicólico. Esfolia e hidrata ao mesmo tempo."),
    ("Mandelic Acid", "Ácido Mandélico", 75, 82, 80, 75, 0, 0, 0, 0, "Esfoliante AHA", "AHA de molécula grande, penetra mais lentamente e irrita menos."),
    ("Azelaic Acid", "Ácido Azelaico", 75, 85, 82, 85, 0, 0, 0, 1, "Multifuncional", "Combate acne, rosácea e manchas. Um dos poucos ácidos seguros na gestação."),

    # ANTIENVELHECIMENTO
    ("Retinol", "Retinol", 70, 80, 78, 40, 0, 0, 0, 0, "Antienvelhecimento", "Estimula colágeno e renova células. Muito eficaz, mas pode irritar. PROIBIDO na gestação."),
    ("Ascorbic Acid", "Vitamina C pura", 75, 80, 78, 55, 0, 0, 0, 1, "Antioxidante", "Clareia manchas e estimula colágeno. Instável e pode irritar peles sensíveis."),
    ("Sodium Ascorbyl Phosphate", "Vitamina C estabilizada", 78, 82, 80, 75, 0, 0, 0, 1, "Antioxidante", "Forma de vitamina C mais estável e menos irritante que o ácido puro."),
    ("Tocopherol", "Vitamina E", 88, 65, 72, 80, 2, 0, 0, 1, "Antioxidante", "Antioxidante que protege e hidrata. Pode ser comedogênico em altas concentrações."),
    ("Resveratrol", "Resveratrol", 82, 80, 80, 80, 0, 0, 0, 1, "Antioxidante", "Potente antioxidante com ação antienvelhecimento. Bem tolerado."),
    ("Coenzyme Q10", "CoQ10", 85, 78, 80, 82, 0, 0, 0, 1, "Antioxidante", "Antioxidante que ajuda na produção de energia celular e combate o envelhecimento."),
    ("Peptides", "Peptídeos", 88, 82, 84, 88, 0, 0, 0, 1, "Antienvelhecimento", "Estimulam a produção de colágeno. Suaves e eficazes para todos os tipos de pele."),

    # PROBLEMÁTICOS / A EVITAR
    ("Alcohol Denat.", "Álcool Desnaturado", 20, 60, 40, 10, 0, 1, 0, 1, "Álcool secante", "Seca e irrita a pele, destrói a barreira cutânea. Evitar especialmente pele seca e sensível."),
    ("Isopropyl Alcohol", "Álcool Isopropílico", 15, 55, 35, 10, 0, 1, 0, 1, "Álcool secante", "Álcool secante e irritante. Não recomendado para nenhum tipo de pele."),
    ("Parfum", "Fragrância / Perfume", 50, 50, 50, 10, 0, 0, 1, 1, "Fragrância", "Mistura de compostos aromáticos. Principal causa de alergia e irritação em cosméticos."),
    ("Sodium Lauryl Sulfate", "SLS", 20, 55, 38, 15, 0, 0, 0, 1, "Surfactante", "Detergente agressivo que remove a barreira natural da pele. Prefira versões mais suaves."),
    ("Cocamidopropyl Betaine", "Cocamidopropil Betaína", 70, 78, 75, 68, 0, 0, 0, 1, "Surfactante suave", "Surfactante mais gentil que o SLS. Usado em produtos para pele sensível."),
    ("Isopropyl Myristate", "Miristato de Isopropila", 60, 20, 35, 55, 5, 0, 0, 1, "Emoliente", "Altamente comedogênico. Pode causar espinhas e cravos, especialmente em pele oleosa."),
    ("Coconut Oil", "Óleo de Coco", 75, 15, 35, 60, 4, 0, 0, 1, "Emoliente", "Muito comedogênico. Ótimo para cabelos, mas pode entupir poros no rosto."),
    ("Lanolin", "Lanolina", 85, 30, 50, 55, 3, 0, 0, 1, "Emoliente", "Emoliente eficaz mas comedogênico. Pode causar reação alérgica em algumas pessoas."),

    # FILTROS SOLARES
    ("Zinc Oxide", "Óxido de Zinco", 82, 85, 85, 92, 0, 0, 0, 1, "Filtro solar físico", "Filtro mineral de amplo espectro. Seguro, calmante e indicado para pele sensível."),
    ("Titanium Dioxide", "Dióxido de Titânio", 80, 82, 82, 90, 0, 0, 0, 1, "Filtro solar físico", "Filtro mineral eficaz e seguro. Boa opção para pele sensível."),
    ("Octinoxate", "Octinoxato", 72, 68, 70, 60, 0, 0, 0, 0, "Filtro solar químico", "Filtro UVB químico. Pode causar irritação e é prejudicial aos corais. Evitar na gestação."),
    ("Oxybenzone", "Oxibenzona", 60, 58, 58, 45, 0, 0, 0, 0, "Filtro solar químico", "Filtro químico com risco de irritação e desregulação hormonal. Evitar na gestação."),

    # INGREDIENTES BRASILEIROS / NATURAIS
    ("Orbignya Oleifera Seed Oil", "Óleo de Babaçu", 88, 50, 65, 80, 2, 0, 0, 1, "Emoliente natural", "Óleo brasileiro com boa hidratação. Levemente comedogênico."),
    ("Mauritia Flexuosa Fruit Oil", "Óleo de Buriti", 90, 55, 68, 82, 1, 0, 0, 1, "Emoliente natural", "Rico em betacaroteno e vitamina E. Ótimo para pele seca e fotoproteção natural."),
    ("Passiflora Incarnata Seed Oil", "Óleo de Maracujá", 85, 70, 76, 85, 1, 0, 0, 1, "Emoliente natural", "Óleo leve rico em ácido linoleico. Bom para pele mista e sensível."),
    ("Coffea Arabica Seed Oil", "Óleo de Café", 80, 65, 70, 72, 0, 0, 0, 1, "Antioxidante", "Rico em antioxidantes. Ajuda na circulação e tem ação anti-olheiras."),
    ("Carapa Guaianensis Seed Oil", "Óleo de Andiroba", 82, 72, 75, 85, 1, 0, 0, 1, "Emoliente natural", "Óleo amazônico com propriedades anti-inflamatórias e repelentes naturais."),
    ("Theobroma Cacao Seed Butter", "Manteiga de Cacau", 92, 30, 50, 70, 4, 0, 0, 1, "Emoliente", "Muito comedogênica. Excelente para corpo, mas evitar no rosto em pele oleosa."),

    # OUTROS ATIVOS COMUNS
    ("Niacinamide", "Niacinamida (reforço)", 80, 95, 90, 88, 0, 0, 0, 1, "Multifuncional", "Reduz poros dilatados, controla brilho e uniformiza o tom de pele."),
    ("Caffeine", "Cafeína", 72, 80, 78, 75, 0, 0, 0, 1, "Antioxidante", "Estimula circulação e reduz inchaço. Popular em produtos para olheiras e celulite."),
    ("Allantoin", "Alantoína", 85, 80, 82, 92, 0, 0, 0, 1, "Calmante", "Suaviza, acalma e promove renovação celular. Muito bem tolerado."),
    ("Zinc PCA", "Zinco PCA", 65, 92, 85, 78, 0, 0, 0, 1, "Seborregulaor", "Controla a produção de sebo. Excelente para pele oleosa e acneica."),
    ("Sodium PCA", "Sódio PCA", 90, 75, 80, 85, 0, 0, 0, 1, "Hidratante", "Fator natural de hidratação da pele (NMF). Umectante eficaz e suave."),
    ("Dimethicone", "Dimeticone", 80, 55, 65, 78, 2, 0, 0, 1, "Silicone", "Satura a pele e cria barreira protetora. Pode acumular nos poros em pele oleosa."),
    ("Tranexamic Acid", "Ácido Tranexâmico", 80, 82, 82, 85, 0, 0, 0, 1, "Despigmentante", "Clareador eficaz e seguro para manchas. Boa tolerância pela maioria dos tipos de pele."),
    ("Kojic Acid", "Ácido Kójico", 72, 75, 74, 60, 0, 0, 0, 0, "Despigmentante", "Inibe a produção de melanina. Pode irritar peles sensíveis. Evitar na gestação."),
    ("Alpha Arbutin", "Alfa-Arbutina", 80, 80, 80, 82, 0, 0, 0, 1, "Despigmentante", "Clareador suave derivado da uva-ursina. Bem tolerado por todos os tipos de pele."),
    ("Polyglutamic Acid", "Ácido Poliglutâmico", 95, 85, 88, 92, 0, 0, 0, 1, "Hidratante", "Hidratante mais potente que o ácido hialurônico. Relativamente novo no mercado."),
]

cursor.executemany("""
INSERT INTO ingredientes (
    nome_inci, nome_popular,
    score_pele_seca, score_pele_oleosa, score_pele_mista, score_pele_sensivel,
    comedogenico, alcool_secante, fragancia_irritante, seguro_gestantes,
    categoria, explicacao
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", ingredientes)

conn.commit()
conn.close()

print(f"✅ Banco criado com sucesso! {len(ingredientes)} ingredientes cadastrados.")
print("📁 Arquivo: ingredientes_pele.db")
print("\nPara visualizar no VS Code, instale a extensão: SQLite Viewer")
