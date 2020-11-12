import numpy as np
import json

fronteiras = {"AC": ["AM", "RO"],
            "AM": ["AC", "RO", "MT", "PA", "RR"],
            "RO": ["AC", "MT", "AM"],
            "RR": ["AM", "PA"],
            "MT": ["RO", "MS", "GO", "TO", "PA", "AM"],
            "PA": ["AM", "MT", "TO", "MA", "AP", "RR"],
            "MS": ["PR", "SP", "MG", "GO", "MT"],
            "AP": ["PA"],
            "RS": ["SC"],
            "SC": ["RS", "PR"],
            "PR": ["SC", "SP", "MS"],
            "SP": ["MS", "PR", "RJ", "MG"],
            "RJ": ["SP", "MG", "ES"],
            "MG": ["GO", "DF", "MS", "SP", "RJ", "ES", "BA"],
            "GO": ["MT", "MS", "MG", "BA", "TO", "DF"],
            "DF": ["GO", "MG"],
            "ES": ["MG", "RJ", "BA"],
            "BA": ["TO", "GO", "MG", "ES", "SE", "AL", "PE", "PI"],
            "TO": ["PA", "MT", "GO", "BA", "PI", "MA"],
            "MA": ["PA", "TO", "PI"],
            "PI": ["MA", "TO", "BA", "PE", "CE"],
            "CE": ["PI", "PB", "PB", "RN"],
            "RN": ["CE", "PB"],
            "PB": ["RN", "CE", "PE"],
            "PE": ["PB", "CE", "PI", "BA", "AL"],
            "AL": ["BA", "SE", "PE"],
            "SE": ["AL", "BA"]}

file = open("fronteiras_municipios.json", "r")
fileOut = open('municipiosVizinhos.csv', 'w')
json_objects = json.load(file)

fileOut.write("A,EstadoA,B,EstadoB\n")

qtdd_cidades = len(json_objects)
print(qtdd_cidades, "cidades")

for i in range(qtdd_cidades):
    a = json_objects[i]
    for j in range(i+1, qtdd_cidades):
        b = json_objects[j]

        # verifica se os municípios a e b podem ser vizinhos de acordo com os estados
        if a["city"]["state"] == b["city"]["state"] or b["city"]["state"] in fronteiras[a["city"]["state"]]:
            
            vizinhos = False
            for k in range(len(a["borders"][0])):
                for l in range(len(b["borders"][0])):

                    if a["borders"][0][k] == b["borders"][0][l]:
                        fileOut.write(a["city"]["name"]+","+a["city"]["state"] + "," + b["city"]["name"]+","+b["city"]["state"]+"\n")
                        vizinhos = True
                        break
        
                if vizinhos:
                    break

    print('{:.2f}%'.format(100*(i+1)/qtdd_cidades))

file.close()
fileOut.close()