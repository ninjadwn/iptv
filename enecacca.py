from re import T
from pyrogram import *
from pyrogram.types import *
from pyromod import listen
import os
import json
import time

#modifica bot_token (linea 13), modifica NOME_CANALE, LINK_CANALE, LINK_SHOP, CHAT_ID, (da linea 15 a linea 17)
#modifica TAG_BOT (linea 29)

api_id = 11285037
api_hash = "aac332a54458b776a5c609e50ab69ce8"
bot_token = "5064065090:AAHeobJ39nKWO0w1ih6hpblQs4MsU8CQV5o"
app = Client("bot", api_id, api_hash, bot_token)
NOME_CANALE = "TopAccountGive 🇮🇹🇺🇸" # NOME CANALE ESATTO
LINK_CANALE = "t.me/TopAccountGive" # LINK CANALE
LINK_SHOP = "https://pornhub.com/gay" # LINK SHOP
CHAT_ID = -1001249138499
ACCOUNT_TYPE = "⚠️ NON SPECIFICATO" #non modificare non modificare non modificare
EMAIL_PASSWORD = "non definiti, contatta supporto."
ACC_PRESO = False# non cambiare
NOT_RUN = False# non cambiare
EP = None# non cambiare
EMAIL = ""# non cambiare
PASSWORD = ""# non cambiare
GIVE_ACTIVATED = False# non cambiare
PAROLA = "" # non cambiare
TAG_BOT = "Giveeeeeeeeebot" #metti tag bot senza la chiocciola.
VINCITORE_PAROLA = "" #NON MODIFICARE
DONE = False

if os.path.exists("storage.json"):
    with open("storage.json", "r+") as f:
        SAVES = json.load(f)
else:
    SAVES = {"Staff": [1138390279,910209349], "Bannati": []}
    with open("storage.json", "w+") as f:
        json.dump(SAVES, f)

if os.path.exists("./users/"):
    pass
else:
    os.mkdir("./users")

def add_account(user, account_type, account):
    file = open(f"./users/{user}/accounts.txt", "a")
    file.write(f"[{account_type}]: {account}\n")


def save():
    global SAVES
    with open("storage.json", "w+") as f:
        json.dump(SAVES, f)

@app.on_message(filters.command("start", [".", "/", "#"]) & filters.private)
async def start(Client, msg):
            fff = msg.text.split(" ")
            if not len(fff) == 2:
                if msg.from_user.id in SAVES["Staff"]:
                    if os.path.exists(f"./users/{str(msg.from_user.id)}/accounts.txt"):
                        await msg.reply_text(f"""👋 Benvenuto {msg.from_user.mention} nel tuo give bot di {NOME_CANALE}!

➡️ Puoi scegliere che tipo di give effettuare coi bottoni nel pannello admin, altrimenti coi relativi comandi.""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🎁 Canale Give', url=LINK_CANALE), InlineKeyboardButton('🛒 Shop', url=LINK_SHOP)],[InlineKeyboardButton('📜 Cronologia', "cronologia"), InlineKeyboardButton('📫 Pannello Admin', 'pannelloadmin')]]))
                    else:
                        os.mkdir(f"./users/{str(msg.from_user.id)}")
                        open(f"./users/{str(msg.from_user.id)}/accounts.txt","w+")
                        await msg.reply_text(f"""👋 Benvenuto {msg.from_user.mention} nel tuo give bot di {NOME_CANALE}!

➡️ Puoi scegliere che tipo di give effettuare coi bottoni nel pannello admin, altrimenti coi relativi comandi.""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🎁 Canale Give', url=LINK_CANALE), InlineKeyboardButton('🛒 Shop', url=LINK_SHOP)],[InlineKeyboardButton('📜 Cronologia', "cronologia"), InlineKeyboardButton('📫 Pannello Admin', 'pannelloadmin')]]))
                else:
                    if os.path.exists(f"./users/{str(msg.from_user.id)}/accounts.txt"):
                        await msg.reply_text(f"""👋 Benvenuto {msg.from_user.mention} nel give bot di {NOME_CANALE}!

➡️ Se sei abbastanza fortunato, puoi vincere account gratis grazie al nostro canale give.""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🎁 Canale Give', url=LINK_CANALE), InlineKeyboardButton('🛒 Shop', url=LINK_SHOP)],[InlineKeyboardButton('📜 Cronologia', "cronologia")]]))
                    else:
                        os.mkdir(f"./users/{str(msg.from_user.id)}")
                        open(f"./users/{str(msg.from_user.id)}/accounts.txt","w+")
                        await msg.reply_text(f"""👋 Benvenuto {msg.from_user.mention} nel give bot di {NOME_CANALE}!

➡️ Se sei abbastanza fortunato, puoi vincere account gratis grazie al nostro canale give.""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🎁 Canale Give', url=LINK_CANALE), InlineKeyboardButton('🛒 Shop', url=LINK_SHOP)],[InlineKeyboardButton('📜 Cronologia', "cronologia")]]))
            else:
                if os.path.exists(f"./users/{str(msg.from_user.id)}/accounts.txt"):
                    global GIVE_ACTIVATED
                    parola_response = await app.ask(msg.from_user.id, "✍️ Scrivi la parola:", timeout=30)
                    if GIVE_ACTIVATED == True:
                        if parola_response.text == PAROLA:
                            global vincitore
                            vincitore = msg.from_user.mention
                            add_account(user=str(msg.from_user.id), account_type=ACCOUNT_TYPE, account=EMAIL_PASSWORD)
                            await msg.reply_text(f"🎉 Hai vinto! L\'account è stato spedito nella tua cronologia.")
                            await app.send_message(CHAT_ID, f"🎉 {vincitore} è stato il primo a scrivere `{PAROLA}`.")
                            GIVE_ACTIVATED = False
                            DONE = True
                        else:
                            await msg.reply_text(f"Sbagliato!")
                    else:
                        await msg.reply_text(f"Nessun give a parola è attivo.")
                else:
                    os.mkdir(f"./users/{str(msg.from_user.id)}")
                    open(f"./users/{str(msg.from_user.id)}/accounts.txt","w+")
                    parola_response = await app.ask(msg.from_user.id, "✍️ Scrivi la parola:", timeout=30)
                    if GIVE_ACTIVATED == True:
                        if parola_response.text == PAROLA:
                            vincitore = msg.from_user.mention
                            add_account(user=str(msg.from_user.id), account_type=ACCOUNT_TYPE, account=EMAIL_PASSWORD)
                            await msg.reply_text(f"🎉 Hai vinto! L\'account è stato spedito nella tua cronologia.")
                            await app.send_message(CHAT_ID, f"**🎉 {vincitore}** __è stato il primo a scrivere __`{PAROLA}`.")
                            GIVE_ACTIVATED = False
                            DONE = True
                        else:
                            await msg.reply_text(f"Sbagliato!")
                    else:
                        await msg.reply_text(f"Nessun give a parola è attivo.")

@app.on_callback_query()
async def callback_handler(Client, cb):
    global ACCOUNT_TYPE, EMAIL_PASSWORD
    if cb.data == "pannelloadmin":
        await cb.message.edit_text(f"""🎛 Pannello admin

➡️ Da qui puoi scegliere che tipo di give effettuare.""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👆 Bottone Ottieni", 'bottoneottieni_setup')],[InlineKeyboardButton("❓ Quiz", 'quiz_setup'), InlineKeyboardButton("🔠 Parola", 'parola_setup')], [InlineKeyboardButton("◀️ Indietro", 'home')]]))
    if cb.data == "bottoneottieni_setup":
        global EMAIL, PASSWORD
        await cb.message.delete()
        response = await app.ask(cb.message.chat.id, '🔗 Invia ora il tipo di account da givvare:\n(se non rispondi entro 30 secondi, il give viene annullato. Se vai avanti senza definire l\'account, verrà segnato come NON DEFINITO)', timeout=30)
        ACCOUNT_TYPE = response.text
        emailpsw = await app.ask(cb.message.chat.id, f"""✅ Tipo di account salvato!

        -Ora invia email:password""")
        EMAIL_PASSWORD = emailpsw.text
        EP = EMAIL_PASSWORD.split(":")
        EMAIL = EP[0]
        PASSWORD = EP[1]
        await cb.message.reply_text(f"""👉 Ho appena givvato "{ACCOUNT_TYPE}"

📥 Credenziali:
📧 Email: {EP[0]}
🔑 Password: {EP[1]}""")
        await app.send_message(CHAT_ID, f"""**{ACCOUNT_TYPE}**

**🏆 VINCITORE: Nessuno!**

`> Clicca il bottone qui in basso "OTTIENI" per vincere il give, le credenziali verranno spedite direttamente sul bot! Prima però dovrai avviare il bot @bot`""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🗝 OTTIENI 🗝', 'ottieni')]]))
    if cb.data == "ottieni":
        global ACC_PRESO, NOT_RUN
        time.sleep(1)
        if ACC_PRESO == True:
            pass
        else:
            vincitore = cb.from_user.mention
            vincitore_id = cb.from_user.id
            ACC_PRESO = True
            try:
                try:
                    add_account(user=str(cb.from_user.id), account_type=ACCOUNT_TYPE, account=EMAIL_PASSWORD)
                    await app.send_message(cb.from_user.id, f"""{ACCOUNT_TYPE}

📥 Credenziali:
📧 Email: {EMAIL}
🔑 Password: {PASSWORD}""")
                except Exception as e:
                    print(e)
                    os.mkdir(f"./users/{vincitore_id}")
                    open(f"./users/{vincitore_id}/accounts.txt","w+")
                    add_account(user=str(cb.from_user.id), account_type=ACCOUNT_TYPE, account=EMAIL_PASSWORD)
                    await app.send_message(cb.from_user.id, f"""{ACCOUNT_TYPE}

📥 Credenziali:
📧 Email: {EMAIL}
🔑 Password: {PASSWORD}""")
                await cb.message.edit_text(f"""**{ACCOUNT_TYPE}**

**🏆 VINCITORE: {vincitore}!**

`> Se non trovi le credenziali, avresti dovuto avviare il bot prima. Puoi comunque avviare il bot ora e ottenere le credenziali andando nella sezione Cronologia.`""")
            except Exception as e:
                print(e)
                NOT_RUN = True
                try:
                    add_account(user=str(cb.from_user.id), account_type=ACCOUNT_TYPE, account=EMAIL_PASSWORD)
                except Exception as e:
                    print(e)
                    os.mkdir(f"./users/{vincitore_id}")
                    open(f"./users/{cb.from_user.id}/accounts.txt","w+")
                    add_account(user=str(cb.from_user.id), account_type=ACCOUNT_TYPE, account=EMAIL_PASSWORD)
                await cb.message.edit_text(f"""**{ACCOUNT_TYPE}**

**🏆 VINCITORE: {vincitore}!**

`🔎 Se non trovi le credenziali, avresti dovuto avviare il bot prima. Puoi comunque avviare il bot ora e ottenere le credenziali andando nella sezione Cronologia.`""")
            ACC_PRESO = False
    if cb.data == "cronologia":
        ff = open(f"./users/{cb.from_user.id}/accounts.txt", "r")
        wefg = ff.read().splitlines()
        accounts = "\n".join(wefg)
        if not accounts == "":
            await cb.message.edit_text(f"🎁 Ecco tutti i tuoi account vinti!: \n`{accounts}`")
        else:
            await cb.answer("Non hai vinto nessun account!")
    if cb.data == "parola_setup":
        global PAROLA, DONE, GIVE_ACTIVATED
        await cb.message.delete()
        response = await app.ask(cb.message.chat.id, '🔗 Invia ora il tipo di account da givvare:\n(se non rispondi entro 30 secondi, il give viene annullato. Se vai avanti senza definire l\'account, verrà segnato come NON DEFINITO)', timeout=30)
        ACCOUNT_TYPE = response.text
        emailpsw = await app.ask(cb.message.chat.id, f"""✅ Tipo di account salvato!

        -Ora invia email:password""")
        EMAIL_PASSWORD = emailpsw.text
        EP = EMAIL_PASSWORD.split(":")
        EMAIL = EP[0]
        PASSWORD = EP[1]
        erh = await app.ask(cb.message.chat.id, f"✍️ Inviami la parola che dovranno scrivere!")
        PAROLA = erh.text
        GIVE_ACTIVATED = True
        await cb.message.reply_text(f"""👉 Ho appena givvato "{ACCOUNT_TYPE}"

📥 Credenziali:
📧 Email: {EP[0]}
🔑 Password: {EP[1]}""")
        await app.send_message(CHAT_ID, f"""**{ACCOUNT_TYPE}**

`> Clicca il bottone "RISPONDI" qui sotto, e scrivi la parola qui sotto per vincere {ACCOUNT_TYPE}:`
✍️ __Parola:__ `{PAROLA}`""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🤔 RISPONDI 🤔', url='https://t.me/Giveeeeeeeeebot?start=parola')]]))



app.run()