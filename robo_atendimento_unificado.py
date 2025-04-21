import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, time
import random
import pywhatkit as kit
import json

# ======================
# CARREGAR CONFIGURAÇÕES
# ======================
def carregar_configuracoes():
    try:
        with open("caminho/para/config.json", "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("Erro: O arquivo 'config.json' não foi encontrado.")
        return {"horario_comercial": {"inicio": "08:00", "fim": "18:00"}}  # Valores padrão

config = {
    "horario_comercial": {
        "inicio": "08:00",
        "fim": "18:00"
    }
}

# ======================
# VERIFICAR HORÁRIO
# ======================
def verificar_horario():
    agora = datetime.now()
    hora_atual = agora.time()
    dia_semana = agora.weekday()  # 0-6 (segunda-domingo)

    inicio_comercial = datetime.strptime(config["horario_comercial"]["inicio"], "%H:%M").time()
    fim_comercial = datetime.strptime(config["horario_comercial"]["fim"], "%H:%M").time()

    # Horário de atendimento humano: segunda a sexta
    if dia_semana < 5 and inicio_comercial <= hora_atual <= fim_comercial:
        return False  # Não executar o robô (horário comercial)
    return True  # Executar o robô (fora do horário comercial)

# ======================
# REGISTRAR LOG
# ======================
def registrar_log(mensagem):
    with open("log_execucao.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()} - {mensagem}\n")

if verificar_horario():
    registrar_log("Robô em execução (fora do horário comercial).")
    print("Robô em execução (fora do horário comercial)...")
else:
    registrar_log("Atendimento humano ativo (horário comercial). Robô pausado.")
    print("Atendimento humano ativo (horário comercial). Robô pausado.")

# ======================
# CATÁLOGO DE PRODUTOS
# ======================
catalogo = {
    "copos": {
        "twister 500ml": 2.50,
        "long drink 350ml": 2.90,
        "taça gin 580ml": 4.20
    },
    "canecas": {
        "caneca acrílica 300ml": 3.10,
        "caneca gel 500ml": 5.00
    }
}

# ======================
# HORÁRIO COMERCIAL
# ======================
horario_comercial = {
    "inicio": "08:00",
    "fim": "18:00"
}

# ======================
# SIMULAÇÃO DE CONVERSAS
# ======================
def gerar_conversas():
    clientes = ["Ana", "Bruno", "Carla", "Daniel", "Eduarda", "Fernando", "Gabriela", "Hugo"]
    mensagens = [
        "Quero catálogo e preços",
        "Qual valor da taça gin?",
        "Vocês têm copo twister?",
        "Preciso de canecas gel",
        "Demoraram muito para responder",
        "Atendimento horrível",
        "Quero comprar vários copos",
        "Têm desconto para grande quantidade?"
    ]
    return [{"cliente": random.choice(clientes), "mensagem": random.choice(mensagens)} for _ in range(20)]

conversas = gerar_conversas()

try:
    with open("conversas_log.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["data", "cliente", "mensagem", "resposta"])
        for conversa in conversas:
            resposta = "Catálogo: [link_catalogo_aqui]\n"
            writer.writerow([datetime.now(), conversa["cliente"], conversa["mensagem"], resposta.strip()])
except Exception as e:
    print(f"Erro ao criar o log de conversas: {e}")

# ======================
# SIMULAÇÃO DE DADOS
# ======================
def gerar_dados_antes():
    """
    Simula os dados antes da implementação do robô.
    Representa mensagens recebidas de clientes com problemas comuns.
    """
    problemas = [
        "Catálogo não enviado",
        "Orçamento solicitado no fim de semana",
        "Dúvida sobre preços de produtos",
        "Sem atendimento no fim de semana",
        "Venda perdida por falta de resposta"
    ]
    dados = []
    for _ in range(100):  # Simula até 100 mensagens recebidas
        dados.append({
            "Tempo_Resposta_Horas": random.uniform(24, 48),  # Resposta demorada (1 a 2 dias)
            "Resolvido": "Não",  # Todos os problemas não resolvidos
            "Descricao_Problema": random.choice(problemas)
        })
    return dados

def gerar_dados_depois():
    """
    Simula os dados depois da implementação do robô.
    Representa mensagens resolvidas automaticamente pelo robô.
    """
    solucoes = [
        "Catálogo enviado automaticamente",
        "Orçamento respondido no fim de semana",
        "Preços informados rapidamente",
        "Atendimento fora do horário realizado pelo robô",
        "Venda concretizada com resposta imediata"
    ]
    dados = []
    for _ in range(100):  # Simula até 100 mensagens resolvidas pelo robô
        dados.append({
            "Tempo_Resposta_Minutos": random.randint(1, 60),  # Resposta rápida (1 a 60 minutos)
            "Resolvido": "Sim",  # Todas resolvidas pelo robô
            "Descricao_Problema": random.choice(solucoes)
        })
    return dados

# ======================
# CRIAÇÃO DOS DATAFRAMES
# ======================
df_antes = pd.DataFrame(gerar_dados_antes())
df_depois = pd.DataFrame(gerar_dados_depois())

# Salvar os dados simulados em arquivos CSV
try:
    df_antes.to_csv("historico_atendimento_antes.csv", index=False)
    df_depois.to_csv("historico_atendimento_depois.csv", index=False)
except Exception as e:
    print(f"Erro ao salvar os dados históricos: {e}")

# Verificar valores únicos na coluna "Resolvido"
print("Valores únicos na coluna 'Resolvido':", df_antes["Resolvido"].unique())

# Verificar se o total de mensagens está correto
print(f"Total de mensagens simuladas antes do robô: {df_antes.shape[0]}")

# ======================
# GRÁFICOS DE PROBLEMAS (ANTES DO ROBÔ)
# ======================
def graficos_problemas_antes():
    """
    Gera gráficos baseados nos dados simulados antes do robô.
    """
    tempo_medio = df_antes["Tempo_Resposta_Horas"].mean()
    nao_resolvidos = df_antes.shape[0]  # Todos os problemas são "Não resolvidos"
    total = df_antes.shape[0]

    # Gráfico de Barras - Problemas
    plt.figure(figsize=(8, 5))
    bars = plt.bar(["Tempo Médio (Horas)", "Não Resolvidos", "Total"],
                   [tempo_medio, nao_resolvidos, total], 
                   color=['#87CEEB', '#FFA07A', '#D3D3D3'])
    plt.title("🔴 Indicadores Antes do Robô")
    plt.ylabel("Quantidade")

    # Adicionar rótulos em cada barra
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 1, 
                 f'{int(bar.get_height())}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("grafico_problemas_barras.png")
    plt.show()

    # Gráfico de Pizza - Problemas
    plt.figure(figsize=(6, 6))
    plt.pie([nao_resolvidos], 
            labels=["Não Resolvidos"],
            autopct=lambda p: f'{int(p)}%',
            colors=['#FFA07A'],
            startangle=90)
    plt.title("🔍 Resolução Antes do Robô")
    plt.tight_layout()
    plt.savefig("grafico_problemas_pizza.png")
    plt.show()

# ======================
# GRÁFICOS DE SOLUÇÕES (DEPOIS DO ROBÔ)
# ======================
def graficos_solucoes_depois():
    tempo_medio = df_depois["Tempo_Resposta_Minutos"].mean()
    resolvidos = df_depois[df_depois["Resolvido"] == "Sim"].shape[0]
    nao_resolvidos = df_depois[df_depois["Resolvido"] == "Nao"].shape[0]
    total = df_depois.shape[0]

    # Gráfico de Barras - Soluções
    plt.figure(figsize=(8, 5))
    plt.bar(["Tempo Médio (Minutos)", "Resolvidos", "Não Resolvidos", "Total"],
            [tempo_medio, resolvidos, nao_resolvidos, total], 
            color=['#98FB98', '#32CD32', '#FF6347', '#D3D3D3'])  # Cores mais definidas
    plt.title("🟢 Indicadores Depois do Robô")
    plt.tight_layout()
    plt.savefig("grafico_solucoes_barras.png")
    plt.show()

    # Gráfico de Pizza - Soluções
    plt.figure(figsize=(6, 6))
    plt.pie([resolvidos, max(1, nao_resolvidos)], 
            labels=["Resolvidos", "Não Resolvidos"],
            autopct=lambda p: f'{int(p)}%',  # Porcentagens inteiras
            colors=['#32CD32', '#FF6347'],  # Cores mais definidas
            startangle=90)
    plt.title("📊 Resolução Depois do Robô")
    plt.tight_layout()
    plt.savefig("grafico_solucoes_pizza.png")
    plt.show()

# ======================
# GRÁFICO POR DESCRIÇÃO
# ======================
def grafico_por_descricao(df, titulo, arquivo):
    descricao_counts = df["Descricao_Problema"].value_counts()
    plt.figure(figsize=(10, 6))
    descricao_counts.plot(kind="bar", color="skyblue")
    plt.title(titulo)
    plt.xlabel("Descrição do Problema")
    plt.ylabel("Quantidade")
    plt.tight_layout()
    plt.savefig(arquivo)
    plt.show()

# ======================
# GRÁFICOS COMPARATIVOS
# ======================
def gerar_graficos_comparativos():
    # Dados para gráficos
    resolvidos_antes = df_antes[df_antes["Resolvido"] == "Sim"].shape[0]
    nao_resolvidos_antes = df_antes[df_antes["Resolvido"] == "Não"].shape[0]

    resolvidos_depois = df_depois[df_depois["Resolvido"] == "Sim"].shape[0]
    nao_resolvidos_depois = df_depois[df_depois["Resolvido"] == "Não"].shape[0]

    # Gráficos de Pizza
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Antes do Robô
    ax1.pie([resolvidos_antes, nao_resolvidos_antes], 
            labels=["Resolvidos", "Não Resolvidos"], 
            autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'], startangle=90)
    ax1.set_title("Antes do Robô")

    # Depois do Robô
    ax2.pie([resolvidos_depois, nao_resolvidos_depois], 
            labels=["Resolvidos", "Não Resolvidos"], 
            autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'], startangle=90)
    ax2.set_title("Depois do Robô")

    plt.tight_layout()
    plt.savefig("graficos_comparativos.png")
    plt.show()

# ======================
# ENVIO DE MENSAGEM PELO WHATSAPP
# ======================
def enviar_mensagem_whatsapp(numero, mensagem):
    try:
        kit.sendwhatmsg_instantly(numero, mensagem, wait_time=10, tab_close=True)
        print(f"Mensagem enviada para {numero}: {mensagem}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {numero}: {e}")

# ======================
# SIMULAÇÃO DE ATENDIMENTO
# ======================
def simular_atendimento():
    """
    Simula o atendimento do robô com base em mensagens predefinidas.
    """
    mensagens_recebidas = [
        "Quero catálogo e preços",
        "Qual valor da taça gin?",
        "Vocês têm copo twister?",
        "Preciso de canecas gel",
        "Demoraram muito para responder",
        "Atendimento horrível",
        "Quero comprar vários copos",
        "Têm desconto para grande quantidade?"
    ]

    respostas_automaticas = {
        "Quero catálogo e preços": "Aqui está o catálogo: [link_catalogo]",
        "Qual valor da taça gin?": "A taça gin 580ml custa R$ 4,20.",
        "Vocês têm copo twister?": "Sim, temos copo twister 500ml por R$ 2,50.",
        "Preciso de canecas gel": "Claro! A caneca gel 500ml custa R$ 5,00.",
        "Demoraram muito para responder": "Pedimos desculpas pela demora. Como podemos ajudar?",
        "Atendimento horrível": "Sentimos muito pela experiência. Estamos aqui para resolver seu problema.",
        "Quero comprar vários copos": "Ótimo! Oferecemos descontos para grandes quantidades. Entre em contato para mais detalhes.",
        "Têm desconto para grande quantidade?": "Sim, temos descontos progressivos. Entre em contato para mais informações."
    }

    # Simula o recebimento de mensagens e as respostas do robô
    print("Simulação de Atendimento do Robô no WhatsApp")
    print("=" * 40)

    for mensagem in mensagens_recebidas:
        print(f"Cliente: {mensagem}")
        resposta = respostas_automaticas.get(mensagem, "Desculpe, não entendi sua mensagem.")
        print(f"Robô: {resposta}")
        print("-" * 40)

# ======================
# SIMULAÇÃO DE ATENDIMENTO COM MENU
# ======================
def simular_atendimento_com_menu():
    """
    Simula o atendimento do robô com base em um menu de opções predefinidas.
    """
    menu = """
    Olá! Sou um atendente virtual. Posso ajudar com as seguintes informações:
    1. Enviar o catálogo de produtos
    2. Informar o preço de um produto específico
    3. Verificar disponibilidade de produtos
    4. Informar sobre descontos para grandes quantidades
    5. Esclarecer dúvidas gerais
    0. Sair
    Por favor, envie o número da opção desejada.
    """

    respostas_automaticas = {
        "1": "Aqui está o catálogo: [link_catalogo]",
        "2": "Por favor, informe o nome do produto para que eu possa informar o preço.",
        "3": "Sim, temos todos os produtos do catálogo disponíveis. Qual produto você deseja?",
        "4": "Oferecemos descontos progressivos para grandes quantidades. Entre em contato para mais detalhes.",
        "5": "Estou aqui para ajudar! Por favor, envie sua dúvida.",
        "0": "Obrigado por entrar em contato! Até logo."
    }

    while True:
        print(menu)
        mensagem = input("Digite sua opção: ")
        resposta = respostas_automaticas.get(mensagem, "Opção inválida. Por favor, escolha uma opção válida do menu.")
        print(f"Robô: {resposta}")
        if mensagem == "0":
            break
        print("-" * 40)

# ======================
# MENU PRINCIPAL
# ======================
def menu_principal():
    """
    Menu principal para escolher qual funcionalidade executar.
    """
    while True:
        print("\n=== Menu Principal ===")
        print("1. Gerar gráficos automaticamente")
        print("2. Simular atendimento do robô")
        print("3. Simular atendimento com menu")
        print("4. Enviar mensagem de teste pelo WhatsApp")
        print("5. Gerar gráficos comparativos")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            # Gerar gráficos automaticamente
            print("Gerando gráficos...")
            graficos_problemas_antes()
            graficos_solucoes_depois()
            grafico_por_descricao(df_antes, "Problemas Antes do Robô", "grafico_problemas_descricao_antes.png")
            grafico_por_descricao(df_depois, "Problemas Depois do Robô", "grafico_problemas_descricao_depois.png")
            print("Gráficos gerados com sucesso!")
        elif opcao == "2":
            # Simular atendimento do robô
            print("Simulando atendimento do robô...")
            simular_atendimento()
        elif opcao == "3":
            # Simular atendimento com menu
            print("Simulando atendimento com menu...")
            simular_atendimento_com_menu()
        elif opcao == "4":
            # Enviar mensagem de teste pelo WhatsApp
            print("Enviando mensagem de teste pelo WhatsApp...")
            numero_teste = "+5531996037730"
            mensagem_teste = "Olá! Esta é uma mensagem de teste do robô de atendimento."
            enviar_mensagem_whatsapp(numero_teste, mensagem_teste)
        elif opcao == "5":
            # Gerar gráficos comparativos
            print("Gerando gráficos comparativos...")
            gerar_graficos_comparativos()
            print("Gráficos comparativos gerados com sucesso!")
        elif opcao == "0":
            # Sair do programa
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Executa o menu principal
menu_principal()