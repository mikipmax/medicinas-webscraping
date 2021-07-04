import requests
from bs4 import BeautifulSoup
import json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"
}

abecedario = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
              "v", "w", "x", "y", "z"]

medicinas_json = []
contador = 1
url_base = "https://www.vademecum.es/equivalencias-internacionales-ecuador-26-"

for categoria in abecedario:
    respuesta = requests.get(url_base + categoria + "_1", headers=headers)
    soup = BeautifulSoup(respuesta.text, features="lxml")
    paginas = soup.findAll('li', class_='unavailable')
    paginas = paginas[0].text.split(sep=' ')
    num_max_pagina = paginas[len(paginas) - 1]
    url_con_pagina = url_base + categoria + "_"
    print("Categoria: " + categoria, end=" - Páginas[")
    for pagina_actual in range(1, int(num_max_pagina) + 1):
        respuesta = requests.get(url_con_pagina + str(pagina_actual), headers=headers)
        soup = BeautifulSoup(respuesta.text, features="lxml")
        medicinas = soup.findAll('div', class_='small-5 columns')
        descripciones = soup.findAll('div', class_='small-3 columns')
        for i, medicina in enumerate(medicinas):
            medicinas_json.append({
                "id": contador,
                'medicina': medicina.text.strip("\n"),
                'descripcion': descripciones[2 * i + 1].text.strip("\n")})
            contador += 1
        print(pagina_actual, end=" ")
    print("]")
with open('medicinas.json', 'w') as file:
    json.dump(medicinas_json, file, indent=4, ensure_ascii=False)
