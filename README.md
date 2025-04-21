# robo-atendimento-imperio

# 🤖 Robô de Atendimento - Império das Canecas BH

Este projeto é um sistema inteligente de **automação de atendimento via WhatsApp**, desenvolvido em Python. Ele simula conversas com clientes, gera relatórios gráficos de desempenho **antes e depois** da automação, organiza logs, envia mensagens via WhatsApp e opera automaticamente **fora do horário comercial**.

---

## 📋 Funcionalidades

✅ Simulação de conversas com clientes  
✅ Geração automática de catálogo de produtos  
✅ Registro em CSV de todas as interações  
✅ Comparativo de desempenho antes e depois da automação  
✅ 4 Gráficos gerados automaticamente:
- Barras e Pizza dos problemas antes do robô  
- Barras e Pizza das soluções depois do robô  
✅ Gráfico de frequência de problemas antes e depois  
✅ Envio automático de mensagens pelo WhatsApp (via `pywhatkit`)  
✅ Execução apenas fora do horário comercial  
✅ Simulação de respostas automáticas do robô

---

## 📊 Gráficos Gerados

- `grafico_problemas_barras.png`  
- `grafico_problemas_pizza.png`  
- `grafico_solucoes_barras.png`  
- `grafico_solucoes_pizza.png`  
- `grafico_problemas_descricao_antes.png`  
- `grafico_problemas_descricao_depois.png`

---

## 🛠 Tecnologias Utilizadas

- Python 3.x  
- Pandas  
- Matplotlib  
- PyWhatKit  
- CSV  
- Agendador de Tarefas do Windows

---

## 🕒 Execução Automática

O robô é executado **somente fora do horário comercial**:
- Segunda a sexta: entre 18h01 e 07h59  
- Fins de semana: robô sempre ativo

---

## 🧪 Como Testar

1. Instale as dependências:
```bash
pip install pandas matplotlib pywhatkit
