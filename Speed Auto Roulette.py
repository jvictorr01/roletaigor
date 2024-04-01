import requests
import telebot
import time
import schedule

# Configurações do bot
telegram_token = "6905777810:AAEjNb_oRVsbdpZu67g3iXzeT5t9r7iOHEM"  #TOKEN DO BOT
chat_id = "-1002100958648" #ID BOT

# Configurações do jogo
API_URL = "https://casino.betfair.com/api/tables-details"
MARTINGALE_STEPS = 0

# Inicialização do bot
bot = telebot.TeleBot(telegram_token)
# Envia mensagem de início do robô
#bot.send_message(chat_id=chat_id, text='🔥 ATENÇÃO VAMOS INICIAR! 🔥', parse_mode="html")
print("💰 Speed Auto Roulette - LIGADA! 💰")

# Variáveis de controle
check_resultado = []
sinal = False
indicacao1 = 0
indicacao2 = 0
entrada = 0
todas_entradas =  []
operacoes = []
quantidade_operacoes = 0
quatidade_greens = 0
quatidade_reds = 0
greens_seguidos = 0
sinal_message_id = None
check_dados = []

# Função para obter o resultado atual do jogo
def obter_resultado():
    headers = {"cookie": "vid=210bec56-62f7-4616-939d-077cf4ff0f25"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code != 200:
        return []
    data = response.json()
    data = data['gameTables']
    for x in data:
        if x['gameTableId'] == 'SpeedAutoRo00001': #mudar roleta

            try:
                data = x['lastNumbers']
                print(x["lastNumbers"])
                time.sleep(0)

                return data
            except KeyError:
                continue
        
def caracteristicas(data):
    if data is None:
        return []
    
    caracteristicas = []
    for numero in data:
        try:
            numero = int(numero)

            coluna = 1 if numero in [1,4,7,10,13,16,19,22,25,28,31,34] else 2 if numero in [2,5,8,11,14,17,20,23,26,29,32,35] else 3 if numero in [3,6,9,12,15,18,21,24,27,30,33,36] else 0
            caracteristicas.append({'numero': numero, 'coluna': coluna})
        except ValueError:
            continue
    return caracteristicas

def verificar_alerta(data):
    global sinal
    global indicacao1
    global indicacao2
    
    data = caracteristicas(data)
    numeros = [numero['numero'] for numero in data]
    colunas = [coluna['coluna'] for coluna in data]
    if len(numeros) > 0:
        ultimo_numero = numeros[0]

        if sinal == True:        
            correcao(numeros, colunas, indicacao1, indicacao2)
        else:
            if colunas[:4] == [1,1,1,1]:
                sinal = True
                indicacao1 = 2
                indicacao2 = 3
                enviar_sinal(indicacao1, indicacao2, ultimo_numero)
                print('SINAL ENVIADO')
            if colunas[:4] == [2,2,2,2]:
                sinal = True
                indicacao1 = 1
                indicacao2 = 3
                enviar_sinal(indicacao1, indicacao2, ultimo_numero)
                print('SINAL ENVIADO')
            if colunas[:4] == [3,3,3,3]:
                sinal = True
                indicacao1 = 1
                indicacao2 = 2
                enviar_sinal(indicacao1, indicacao2, ultimo_numero)
                print('SINAL ENVIADO')
################################################################
    return

def correcao(numeros, colunas, indicacao1, indicacao2):
    global todas_entradas
    if colunas[0] == indicacao1 or colunas[0] == indicacao2 or colunas[0] == 0:
        todas_entradas.append(numeros[0])
        green()
        reset()
        return
    else:
        martingale()
        return    

def enviar_sinal(indicacao1, indicacao2, ultimo_numero):
    texto = f'''
🎯 Entrada confirmada 🎯

🔥 Entrar na {indicacao1}º e {indicacao2}ª Coluna | Cobrir o 0️⃣
🎰 <a href='https://royalbet.win/games/play/11954/SpeedAutoRo00001'>Speed Auto Roulette</a>
➡️ ENTRADA ÚNICA S/G

🧨 Último número: {ultimo_numero}

🤑 <a href='https://arbety.com/?invite=p&code=mp'>CADASTRE-SE AQUI</a>
'''

    # Enviar mensagem e armazenar o ID da mensagem
    global sinal_message_id
    message = bot.send_message(chat_id=chat_id, text=texto, parse_mode="html", disable_web_page_preview=True)
    sinal_message_id = message.message_id  # Armazenar o ID da mensagem
    time.sleep(20)
    return message

def alerta():
    texto = f"⚠️ AGUARDE CONFIRMAR ⚠️"
    message = bot.send_message(chat_id=chat_id, text=texto, parse_mode="html")
    time.sleep(7)
    bot.delete_message(chat_id=chat_id, message_id=message.message_id) 
    reset()   
    return message

def martingale():
    global entrada
    global MARTINGALE_STEPS        
    entrada += 1
    
    if entrada <= MARTINGALE_STEPS:
        texto = f"🔁 ENTRAMOS NO {entrada}° GALE 🔁"
        message = bot.send_message(chat_id=chat_id, text=texto, parse_mode="html")
        print('VAMOS PARA O GALE')
        time.sleep(10)
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    else:
        red()
        reset()
    return

def green():
    global quatidade_greens
    global todas_entradas
    global operacoes
    global quantidade_operacoes
    quantidade_operacoes += 1
    quatidade_greens += 1
    texto = f'''✅ VITÓRIA | {todas_entradas}'''
    print('GREEN ✅')
    # Responder à mensagem de sinal
    global sinal_message_id
    if sinal_message_id is not None:
        bot.send_message(chat_id=chat_id, text=texto, reply_to_message_id=sinal_message_id)
        sinal_message_id = None  # Limpar o ID da mensagem
    return

def red():
    global quatidade_reds
    global todas_entradas
    global operacoes
    global quantidade_operacoes
    quantidade_operacoes += 1
    quatidade_reds += 1
    texto = f'''❌ SIGA GESTÃO'''
    print('RED 🔻')
    # Responder à mensagem de sinal
    global sinal_message_id
    if sinal_message_id is not None:
        bot.send_message(chat_id=chat_id, text=texto, reply_to_message_id=sinal_message_id)
        sinal_message_id = None  # Limpar o ID da mensagem
    return

def reset():
    global sinal
    global entrada
    global todas_entradas
    
    entrada = 0
    todas_entradas.clear()
    sinal = False
    return

# Função para gerar um relatório e resetar o placar
# def generate_report_and_reset():
#     global quatidade_greens
#     global quatidade_reds
#     global operacoes
#     global quantidade_operacoes
#     global greens_seguidos
#     result = '\n'.join(str(item) for item in operacoes)
#     total = quatidade_greens + quatidade_reds
#     porcentagem = (quatidade_greens / total) * 100
#     porcentagem = format(porcentagem, '.0f')
#     texto = f'''
#     ► PLACAR = ✅ {quatidade_greens} x 🚫 {quatidade_reds}{result}
#     ► Consecutivas = {greens_seguidos}
#     ► Assertividade = {porcentagem}%
# '''
#     print(texto)  # Apenas para fins de depuração
#     reset()  # Chame a função reset para zerar o placar

# Agendar a função generate_report_and_reset para meia-noite todos os dias
#schedule.every().day.at("00:00").do(generate_report_and_reset)

while True:
    data = obter_resultado()

    if data != check_dados:
        verificar_alerta(data)
        check_dados = data
        #if quantidade_operacoes >= 1:
            #generate_report()
    #schedule.run_pending()  # Executar as tarefas agendadas
    time.sleep(5)