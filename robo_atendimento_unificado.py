import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, time
import random
import pywhatkit as kit

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
    Inclui mensagens não respondidas durante o fim de semana.
    """
    problemas = [

        "Não respondido",
        "Demora",
        "Insatisfação",
        "Técnico"
    ]
    dados = []
    for _ in range(100):  # 100 mensagens por atendente no fim de semana
        dados.append({
            "Tempo_Resposta_Horas": random.uniform(24, 48),  # Resposta demorada (1 a 2 dias)
            "Resolvido": random.choice(["Nao", "Nao", "Sim"]),  # Maioria não resolvida
            "Descricao_Problema": random.choice(problemas)
        })
    return dados

def gerar_dados_depois():
    """
    Simula os dados depois da implementação do robô.
    Inclui mensagens resolvidas automaticamente pelo robô.
    """
    problemas = [
        "Respondido",
        "Resolvido rápido",
        "Satisfação"
    ]
    dados = []
    for _ in range(100):  # 100 mensagens por atendente no fim de semana
        dados.append({
            "Tempo_Resposta_Minutos": random.randint(1, 60),  # Resposta rápida (1 a 60 minutos)
            "Resolvido": "Sim",  # Todas resolvidas pelo robô
            "Descricao_Problema": random.choice(problemas)
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

# ======================
# GRÁFICOS DE PROBLEMAS (ANTES DO ROBÔ)
# ======================
def graficos_problemas_antes():
    tempo_medio = df_antes["Tempo_Resposta_Horas"].mean()
    resolvidos = df_antes[df_antes["Resolvido"] == "Sim"].shape[0]
    nao_resolvidos = df_antes[df_antes["Resolvido"] == "Nao"].shape[0]
    total = df_antes.shape[0]

    # Gráfico de Barras - Problemas
    plt.figure(figsize=(8, 5))
    plt.bar(["Tempo Médio (Horas)", "Resolvidos", "Não Resolvidos", "Total"],
            [tempo_medio, resolvidos, nao_resolvidos, total], color=['blue', 'navy', 'orange', 'gray'])
    plt.title("🔴 Indicadores Antes do Robô")
    plt.tight_layout()
    plt.savefig("grafico_problemas_barras.png")
    plt.show()

    # Gráfico de Pizza - Problemas
    plt.figure(figsize=(6, 6))
    plt.pie([resolvidos, max(1, nao_resolvidos)], labels=["Resolvidos", "Não Resolvidos"],
            autopct='%1.1f%%', colors=['navy', 'orange'], startangle=90)
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
            [tempo_medio, resolvidos, nao_resolvidos, total], color=['blue', 'navy', 'orange', 'gray'])
    plt.title("🟢 Indicadores Depois do Robô")
    plt.tight_layout()
    plt.savefig("grafico_solucoes_barras.png")
    plt.show()

    # Gráfico de Pizza - Soluções
    plt.figure(figsize=(6, 6))
    plt.pie([resolvidos, max(1, nao_resolvidos)], labels=["Resolvidos", "Não Resolvidos"],
            autopct='%1.1f%%', colors=['navy', 'orange'], startangle=90)
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

# Gráfico para os problemas antes do robô
grafico_por_descricao(df_antes, "Problemas Antes do Robô", "grafico_problemas_descricao_antes.png")

# Gráfico para os problemas depois do robô
grafico_por_descricao(df_depois, "Problemas Depois do Robô", "grafico_problemas_descricao_depois.png")

# ======================
# EXECUTAR GRÁFICOS
# ======================
graficos_problemas_antes()
graficos_solucoes_depois()

# ======================
# ENVIO DE MENSAGEM PELO WHATSAPP
# ======================
def enviar_mensagem_whatsapp(numero, mensagem):
    try:
        kit.sendwhatmsg_instantly(numero, mensagem, wait_time=10, tab_close=True)
        print(f"Mensagem enviada para {numero}: {mensagem}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {numero}: {e}")

# Enviar mensagem de teste
numero_teste = "+5531996037730"
mensagem_teste = "Olá! Esta é uma mensagem de teste do robô de atendimento."
enviar_mensagem_whatsapp(numero_teste, mensagem_teste)

# ======================
# AGENDAMENTO AUTOMÁTICO
# ======================
def verificar_horario():
    agora = datetime.now()
    hora_atual = agora.time()
    dia_semana = agora.weekday()
    if dia_semana < 5 and time(8, 0) <= hora_atual <= time(18, 0):
        return False  # Atendimento humano ativo
    return True  # Robô em execução

if verificar_horario():
    print("Robô em execução (fora do horário comercial)...")
else:
    print("Atendimento humano ativo. Robô pausado.")


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

# Executa a simulação
simular_atendimento()