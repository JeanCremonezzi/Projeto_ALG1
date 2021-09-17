import csv
from time import sleep

def menu():
    print("\n 1- Carregar dados do arquivo.")
    print(" 2- Listar todos os dados organizados por região.")
    print(" 3- Informar os 3 países com maior população.")
    print(" 4- Crie uma nova coluna do continente.")
    print(" 5- Informar a média de taxa de natalidade dos países de cada continente.")
    print(" 6- Qual a renda per capita de cada continente.")
    print(" 7- Quais os menores países do mundo em área.")
    print(" 8- Criar arquivo com os dados da Europa.")
    print(" 9- Buscar país mais semelhante.")
    print(" 10- Preencher dados faltantes (por semelhança).")
    print(" 11- Informe o país que mais tem telefone por habitante em cada uma das regiões.")
    print(" 12- Qual a região que tem o melhor renda per capita.")
    print(" 13- Permita o cadastro de um novo país fictício que surgiu.")
    print(" 14- Qual o país com maior taxa de Agricultura, Indústria e Serviço respectivamente.")
    print(" 15- Criar arquivo formatado")

def lerArquivo(path):
    
    # Abre arquivo
    with open(path, newline='') as inputFile:

        # Lê arquivo
        reader = csv.reader(inputFile, delimiter=",")

        # Pula e armazena valores do header
        header = next(reader)
        qntKeys = len(header)

        paises = []

        # Cria dicionário para cada país lido
        for row in reader:
            pais = {}

            for key in range(qntKeys):
                pais[header[key]] = row[key]

            # Retira espaço em branco no final do nome dos países
            if (pais["Country"][-1] == " "):
                pais["Country"] = pais["Country"][:-1]
            
            # Retira espaço em branco no final das regiões
            while (pais["Region"][-1] == " "):
                pais["Region"] = pais["Region"][:-1]

            paises.append(pais)
    
    return paises

def escreverArquivo(path, paises, delimiter):
    
    # Abre arquivo para escrever
    with open(path, "w", newline='') as outputFile:

        writer = csv.writer(outputFile, delimiter=delimiter)

        # Escreve header
        writer.writerow(paises[0].keys())

        # Escreve linhas
        for pais in paises:
            writer.writerow(pais.values())

    return

def ordenarPorColuna(paises, coluna, reverse):

    # Ordena a lista de dicionários por uma coluna especificada
    ordenada = []

    if (coluna == "Population") or (coluna == "Area (sq. mi.)"):
        ordenada = sorted(paises, key = lambda pais: int(pais[coluna]), reverse = reverse)
    else:
        ordenada = sorted(paises, key = lambda pais: pais[coluna], reverse = reverse)

    # lambda é uma função anônima

    # Seria o mesmo que:
    # def ordenaColuna(pais) : return pais[coluna] 
    # ordenada = sorted(paises, key = ordenaColuna)
    # Key recebe a função ordenaColuna que retorna o valor da coluna em cada linha

    return ordenada

def colunaContinente(paises, nomeColuna, path):

    lenPaises = len(paises)

    # América, Europa, África, Ásia, Oceania

    for posicao in range(lenPaises):
        regiao = paises[posicao]["Region"]
        continente = ""

        if (regiao == "NORTHERN AMERICA") or (regiao == "LATIN AMER. & CARIB"):
            continente = "America"

        elif (regiao == "C.W. OF IND. STATES") or (regiao == "ASIA (EX. NEAR EAST)") or (regiao == "NEAR EAST"):
            continente = "Asia"

        elif (regiao == "EASTERN EUROPE") or (regiao == "WESTERN EUROPE") or (regiao == "BALTICS"):
            continente = "Europe"

        elif (regiao == "OCEANIA"):
            continente = "Oceania"

        elif (regiao == "NORTHERN AFRICA") or (regiao == "SUB-SAHARAN AFRICA"):
            continente = "Africa"

        else:
            continente = "Outro"

        paises[posicao][nomeColuna] = continente

    escreverArquivo(path, paises, ",")

    return paises

def natalidadeContinentes(paises):

    colunaContinenteExiste  = verificarColunaEuropa(paises[0])
    if not colunaContinenteExiste:
        print(" > A coluna de continentes ainda não foi criada!")
        return

    else:
        medias = {
            "America": {"soma": 0, "quantidade": 0},
            "Europe": {"soma": 0, "quantidade": 0},
            "Africa": {"soma": 0, "quantidade": 0},
            "Asia": {"soma": 0, "quantidade": 0},
            "Oceania": {"soma": 0, "quantidade": 0},
        }

        for pais in paises:
            continentePais = pais["Continent"]

            # Pula paises que não tem os dados disponíveis
            if (pais["Birthrate"] == ""):
                pass
            else:
                natalidade = float(pais["Birthrate"].replace(',', '.'))

                medias[continentePais]["soma"] += natalidade
                medias[continentePais]["quantidade"] += 1

        for continente, dados in medias.items():
            media = dados["soma"] / dados["quantidade"]

            medias[continente] = round(media, 2)
                
        for keys, values in medias.items():
            print(" > " + keys + ": " + str(values))

        print(" >>> Países sem os dados de natalidade não foram contabilizados.")

        return

def rendaContinentes(paises):

    colunaContinenteExiste  = verificarColunaEuropa(paises[0])
    if not colunaContinenteExiste:
        print(" > A coluna de continentes ainda não foi criada!")
        return
    else:

        continentes = {
            "America": {"populacao": 0, "pib": 0},
            "Europe": {"populacao": 0, "pib": 0},
            "Asia": {"populacao": 0, "pib": 0},
            "Africa": {"populacao": 0, "pib": 0},
            "Oceania": {"populacao": 0, "pib": 0},
        }

        nomeColuna = "GDP ($ per capita)"

        for pais in paises:
            if (pais[nomeColuna] != ""):
                populacaoPais = int(pais["Population"])
                pibTotalPais = int(pais[nomeColuna]) * populacaoPais

                continente = pais["Continent"]
                continentes[continente]["populacao"] += populacaoPais
                continentes[continente]["pib"] += pibTotalPais
            else:
                pass
            
        for continente, dados in continentes.items():
            pib = dados["pib"] / dados["populacao"]

            continentes[continente] = format(int(pib), ',d').replace(',', '.')
        
        for keys, values in continentes.items():
            print(" > " + keys + ": " + str(values))

        print(" >>> Países sem os dados de renda não foram contabilizados.")

        return

def arquivoContinente(paises, continente, nomeArquivo, path):

    colunaContinenteExiste  = verificarColunaEuropa(paises[0])
    if not colunaContinenteExiste:
        print(" > A coluna de continentes ainda não foi criada!")
        return
    else:

        caminhoArquivo = path + nomeArquivo + ".csv"
        
        with open(caminhoArquivo, 'w', newline='') as outputfile:
            writer = csv.writer(outputfile, delimiter=';')

            paisContinente = {"Country": "", "Population": "", "Birthrate": "", "GDP ($ per capita)": ""}

            header = paisContinente.keys()
            writer.writerow(header)

            for pais in paises:
                if pais["Continent"] == continente:

                    paisContinente["Country"] = pais["Country"]
                    paisContinente["Population"] = pais["Population"]
                    paisContinente["Birthrate"] = pais["Birthrate"]
                    paisContinente["GDP ($ per capita)"] = pais["GDP ($ per capita)"]

                    writer.writerow(paisContinente.values())
        
        return

def buscarSemelhante(paises, nomePaisBase):

    def calcSemelhanca(paisBase, paisComparar):

        # ----- Calcula a semelhança de mortalidade em porcentagem -----
        mortBase = float(paisBase["Infant mortality (per 1000 births)"].replace(',', '.'))
        mortComparar = float(paisComparar["Infant mortality (per 1000 births)"].replace(',', '.'))

        semelhancaMort = float()

        if (mortBase > mortComparar):
            semelhancaMort = round(((mortComparar / mortBase) * 100 ), 2)
        else:
            semelhancaMort = round(((mortBase / mortComparar) * 100 ), 2)

        # ----- Calcula a semelhança da renda em porcentagem -----
        rendaBase = int(paisBase["GDP ($ per capita)"])
        rendaComparar = int(paisComparar["GDP ($ per capita)"])

        semelhancaRenda = float()

        if (rendaBase > rendaComparar):
            semelhancaRenda = round(((rendaComparar / rendaBase) * 100 ), 2)
        else:
            semelhancaRenda = round(((rendaBase / rendaComparar) * 100 ), 2)
        
        # ----- Calcula média de semelhança em porcentagem -----
        media = round(((semelhancaRenda + semelhancaMort) / 2))
        return media

    # Encontra dados do país base
    paisesBase = [pais for pais in paises if pais["Country"] == nomePaisBase]

    if not paisesBase:
        return  {   "message": " > País não encontrado!",
                    "content": {}
                }
    else:
        dadosBase = paisesBase[0]
        maiorSemelhanca = float()
        paisSemelhante = {}

    if (dadosBase["Infant mortality (per 1000 births)"] == "") or (dadosBase["GDP ($ per capita)"] == ""):
        print("Dados faltando")
        return

    else:
        for pais in paises:

            if (pais["Infant mortality (per 1000 births)"] == "") or (pais["GDP ($ per capita)"] == "") or (pais["Country"] == nomePaisBase):
                pass

            else:
                semelhanca = calcSemelhanca(dadosBase, pais)

                if (not maiorSemelhanca) or (semelhanca > maiorSemelhanca):
                    maiorSemelhanca = semelhanca
                    paisSemelhante = pais

    return  {   "message": " > " + paisSemelhante["Country"] + " é o país mais semelhante à(ao) " + nomePaisBase + "!",
                "content": paisSemelhante
            }

def completarDados(paises, path):
    
    for pais in paises:

        # Se houverem campos vazios
        if ("" in pais.values()):

            # Se o campo vazio não for Mortalidade Infantil e Renda Per Capita
            if (pais["Infant mortality (per 1000 births)"] != "") and (pais["GDP ($ per capita)"] != ""):
                paisesBuscar = paises.copy()

                encontrou = False
                while not encontrou:
                    semelhante = buscarSemelhante(paisesBuscar, pais["Country"])["content"]

                    # Verifica se o país semelhante não tem valores vazios
                    if ("" in semelhante.values()):
                        paisesBuscar.remove(semelhante)
                    else:
                        encontrou = True

                # Gera novos valores
                for key, value in semelhante.items():
                    if pais[key] == "":
                        pais[key] = value
            else:
                # Filtra paises da mesma regiao
                mesmaRegiao = [paisBuscar for paisBuscar in paises if paisBuscar["Region"] == pais["Region"]]

                # Ordenada por população
                ordenada = ordenarPorColuna(mesmaRegiao, "Population", True)
                
                indicePais = ordenada.index(pais)
                paisSemelhante = {}


                # Se país for o mais populoso da região, utilize o país logo abaixo
                if (indicePais == 0):
                    paisSemelhante = ordenada[1]

                # Se país for o menos populoso da região, utilize o país logo acima
                elif (indicePais == (len(ordenada) - 1)):
                    paisSemelhante = ordenada[indicePais - 1]

                else:
                    paisAcima = ordenada[indicePais + 1]
                    paisAbaixo = ordenada[indicePais - 1]
                        
                    # Verifica qual dos países tem a menor diferença de população
                    if (abs(int(paisAcima["Population"])) < abs(int(paisAbaixo["Population"]))):
                        paisSemelhante = paisAcima
                    else:
                        paisSemelhante = paisAbaixo

                # Gera novos valores
                for key, value in paisSemelhante.items():
                    if pais[key] == "":
                        pais[key] = value

        # Altera o país na lista com todos os paises
        index = paises.index(pais)
        paises[index] = pais

    escreverArquivo(path,paises, ",")
    return paises

def telefoneRegiao(paises):
    dados = {}

    for pais in paises:

        if (pais["Phones (per 1000)"] == ""):
            pass

        else: 
            regiao = pais["Region"]
            phones = float(pais["Phones (per 1000)"].replace(",", "."))
            pais = pais["Country"]

            if (regiao not in dados.keys()):
                infoPais = {"Country": pais, "Phones (per 1000)": phones}
                dados[regiao] = infoPais
            
            else:
                if (phones > dados[regiao]["Phones (per 1000)"]):
                    dados[regiao]["Country"] = pais
                    dados[regiao]["Phones (per 1000)"] = phones

    for key, values in dados.items():
        print(" > " + key + ": " + values["Country"] + " - " + str(values["Phones (per 1000)"]))

def rendaRegiao(paises):
    dados = {}

    for pais in paises:

        if (pais["GDP ($ per capita)"] == ""):
            pass
        else:
            regiao = pais["Region"]
            renda = int(pais["GDP ($ per capita)"])

            if (regiao not in dados.keys()):
                infoPais = {"GDP": renda, "qntPaises": 1}
                dados[regiao] = infoPais

            else:
                dados[regiao]["GDP"] += renda
                dados[regiao]["qntPaises"] += 1
    
    for regiao in dados.keys():
        qntPaises = dados[regiao]["qntPaises"]
        rendaTotal = dados[regiao]["GDP"]
        
        media = rendaTotal / qntPaises

        dados[regiao]["media"] = round(media, 2)

    maior = {"media": 0}
    for regiao in dados.keys():
        if (dados[regiao]["media"] > maior["media"]) or (not maior):
            maior = dados[regiao]
            maior["regiao"] = regiao
    
    print(" > " + maior["regiao"] + ": " + str(maior["media"]))

def registrarPais(paises, path):

    valido = False
    while not valido:
        country = input("\n > Nome do país: ")
        region = input(" > Regiao do país: ").upper()
        population = input(" > População do país: ")
        area = input(" > Área do país: ")
        density = input(" > Densidade populacional do país: ")
        coastline = input(" > Área litorânea do país: ")

        if (country != "") and (region != "") and (population != "") and (area != "") and (density != "") and (coastline != ""):
            valido = True

            continente = input("\n > Continente do país: ").title()
            migration = input(" > Migração no país: ")
            infantMort = input(" > Mortalidade infantil no país: ")
            gdp = input(" > PIB per capita no país: ")
            literacy = input(" > Alfabetização no país: ")
            phones = input(" > Celulares por 1000 habitantes no país: ")
            arable = input(" > Porcentagem de área arável no país no país: ")
            crops = input(" > Porcentagem de área de cultivo no país no país: ")
            other = input(" > Outras áreas no país no país: ")
            clima = input(" > Tipo de clima no país: ")
            birthrate = input(" > Natalidade no país: ")
            deathrate = input(" > Mortalidade no país: ")
            agriculture = input(" > Índice de atividades agrícolas no país: ")
            industry = input(" > Índice de atividades industriais no país: ")
            service = input(" > Índice de atividades de serviços no país: ")

        else:
            print(" >>> Estes dados são obrigatórios!")

    newPais = {
        "Country": country, "Region": region, "Population": population, "Area (sq. mi.)": area,
        "Pop. Density (per sq. mi.)": density, "Coastline (coast/area ratio)": coastline,
        "Continent": continente, "Net migration": migration, "Infant mortality (per 1000 births)": infantMort,
        "GDP ($ per capita)": gdp, "Literacy (%)": literacy, "Phones (per 1000)": phones,
        "Arable (%)": arable, "Crops (%)": crops, "Other (%)": other, "Climate": clima,
        "Birthrate": birthrate, "Deathrate": deathrate, "Agriculture": agriculture,
        "Industry": industry, "Service": service
    }

    paises.append(newPais)
    escreverArquivo(path, paises, ",")

    return paises

def verificarColunaEuropa(pais):

    if ("Continent" in pais.keys()):
        return True

    else:
        return False

def paisesMaiorSetores(paises):

    maiorAgricultura = {}
    maiorIndustria = {}
    maiorServico = {}

    for pais in paises:

        if (pais["Agriculture"] != ""):
            agricultura = float(pais["Agriculture"].replace(',', '.'))

            if (not maiorAgricultura) or (agricultura > float(maiorAgricultura["Agriculture"].replace(',', '.'))):
                maiorAgricultura = pais
        
        if (pais["Industry"] != ""):
            industria = float(pais["Industry"].replace(',', '.'))
            
            if (not maiorIndustria) or (industria > float(maiorIndustria["Industry"].replace(',', '.'))):
                maiorIndustria = pais

        if (pais["Service"] != ""):
            servico = float(pais["Service"].replace(',', '.'))

            if (not maiorServico) or (servico > float(maiorServico["Service"].replace(',', '.'))):
                maiorServico = pais

    print(" > Maior taxa de agricultura: " + maiorAgricultura["Country"] + " | " + maiorAgricultura["Agriculture"])
    print(" > Maior taxa de indústria: " + maiorIndustria["Country"] + " | " + maiorIndustria["Industry"])
    print(" > Maior taxa de serviços: " + maiorServico["Country"] + " | " + maiorServico["Service"])
        
# ----- VARIÁVEIS GLOBAIS ----- #
nomeArquivo = "countries of the world.csv"
path = ".\\" + nomeArquivo

listaPaises = lerArquivo(path)
# ---------------------------- #

while True:

    if not listaPaises:
        print("\n >>> Não há uma lista de países.")
        break

    else:
        menu()
        option = input("\n > Escolha uma opção: ")

        if (option == "1"):
            print("\n >>> Carregando dados...")
            sleep(1)

            listaPaises = lerArquivo(path)
            print(" >>> Dados carregados!")

        elif (option == "2"):
            ordenada = ordenarPorColuna(listaPaises, "Region", False)

            lenPaises = len(ordenada)

            for index in range(lenPaises):
                if (index == 0) or (ordenada[index - 1]["Region"] != ordenada[index]["Region"]):
                    print("\n > " + ordenada[index]["Region"] + ": ")
                
                print("\n")
                for keys,values in ordenada[index].items():
                    print("  - " + keys + ": " + values) 

                #print ("  - " + ordenada[index]["Country"])
        
        elif (option == "3"):
            ordenada = ordenarPorColuna(listaPaises, "Population", True)

            numPaises = 3

            for index in range(numPaises):
                pais = ordenada[index]
                populacao = format(int(pais["Population"]), ',d').replace(',', '.')

                print(f" > {index + 1}º - " + pais["Country"] + ": " + populacao)

        elif (option == "4"):
            newPaises = colunaContinente(listaPaises, "Continent", path)

            listaPaises = newPaises
        
        elif (option == "5"):
            print("\n >>> Buscando dados...")
            sleep(1)

            natalidadeContinentes(listaPaises)

        elif (option == "6"):
            print("\n >>> Buscando dados...")
            sleep(1)

            rendaContinentes(listaPaises)
        
        elif (option == "7"):
            ordenada = ordenarPorColuna(listaPaises, "Area (sq. mi.)", False)

            numPaises = 5

            for index in range(numPaises):
                pais = ordenada[index]
                area = format(int(pais["Area (sq. mi.)"]), ',d').replace(',', '.')

                print(f" > {index + 1}º - " + pais["Country"] + ": " + area)
        
        elif (option == "8"):
            arquivoContinente(listaPaises, "Europe", "Europe Countries", ".\\")

        elif (option == "9"):
            nomePais = input("\n > Buscar país semelhante à(ao): ").title()

            resp = buscarSemelhante(listaPaises, nomePais)
            print(resp["message"])

        elif (option == "10"):
            retorno = completarDados(listaPaises, path)
            listaPaises = retorno
        
        elif (option == "11"):
            telefoneRegiao(listaPaises)

        elif (option == "12"):
            rendaRegiao(listaPaises)

        elif (option == "13"):
            newPaises = registrarPais(listaPaises, path)
            listaPaises = newPaises

            print(" > País inserido!")

        elif (option == "14"):
            paisesMaiorSetores(listaPaises)

        elif (option == "15"):
            escreverArquivo(".\\formated.csv", listaPaises, ";")
            
            print(" >  Arquivo criado!")
        
        else:
            print("\n >>> Opção inválida!")