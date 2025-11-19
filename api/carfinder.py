from flask import Flask, jsonify
import requests
import time

app = Flask(_name_)

# ----------------------------------------
# CONFIGURAÇÕES
# ----------------------------------------

MODELOS = [
    "Honda Civic",
    "Honda Fit",
    "Honda HRV",
    "Toyota Corolla",
    "Toyota Etios",
    "Fiat Strada",
    "Hyundai Creta",
    "Hyundai HB20"
]

MARGEM_MIN = 12000
MARGEM_MAX = 15000

PORTAIS = [
    "https://www.olx.com.br/autos-e-pecas?q=",
    "https://mg.olx.com.br/autos-e-pecas?q=",
    "https://rj.olx.com.br/autos-e-pecas?q="
]

# ----------------------------------------
# BUSCA FIPE
# ----------------------------------------

def buscar_fipe(modelo):
    try:
        url = f"https://veiculos.fipe.org.br/api/veiculos/{modelo.replace(' ', '%20')}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return int(data.get("preco", 0))
        return 0
    except:
        return 0

# ----------------------------------------
# BUSCA ANÚNCIOS
# ----------------------------------------

def buscar_anuncios(modelo):
    resultados = []

    for portal in PORTAIS:
        try:
            url = portal + modelo.replace(" ", "+")
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue

            resultados.append({
                "portal": portal,
                "modelo": modelo,
                "link": url
            })

        except:
            continue

    return resultados

# ----------------------------------------
# FILTRO DE OPORTUNIDADE
# ----------------------------------------

def analisar_oportunidades():
    oportunidades = []

    for modelo in MODELOS:
        fipe = buscar_fipe(modelo)
        anuncios = buscar_anuncios(modelo)

        for anuncio in anuncios:
            # (Aqui entra a parte real de scraping — por enquanto apresentamos links)
            oportunidades.append({
                "modelo": modelo,
                "fipe": fipe,
                "margem_desejada": f"{MARGEM_MIN} a {MARGEM_MAX}",
                "portal": anuncio["portal"],
                "link": anuncio["link"]
            })

    return oportunidades

# ----------------------------------------
# ROTA PRINCIPAL
# ----------------------------------------

@app.route("/api/carfinder")
def api_carfinder():
    resultado = analisar_oportunidades()
    return jsonify({"status": "ok", "resultados": resultado})

# ----------------------------------------
# LOOP LOCAL (não roda na Vercel)
# ----------------------------------------

if _name_ == "_main_":
    while True:
        print("Rodando busca...")
        print(analisar_oportunidades())
        time.sleep(60)
