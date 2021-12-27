from telethon import TelegramClient, events, sync
import asyncio
import os
import json
import io
import math
import urllib.request
 
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon import functions, types
api_id = 7058291
api_hash = "5b9ea5b6baa2905c7ae2822a04b8e835"

bot = TelegramClient('ub', api_id, api_hash)

HELPER = {}

def register(**args):
    pattern = args.get('pattern', None)

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    def decorator(func):
        bot.add_event_handler(func, events.NewMessage(**args))
        bot.add_event_handler(func, events.MessageEdited(**args))
        return func

    return decorator

#FILTRI
if not os.path.exists("storage.json"):
  with open("storage.json", "w+") as f:
    data = {}
    data["filtri"] = []
    data["reply"] = []
    json.dump(data, f)
 
@register(outgoing=True, pattern="^[.]addfiltro ")
async def setFilter(e):
  with open("storage.json", "r") as f:
    data = json.load(f)
  st = e.text.split(" ", 2)
  if st.__len__() == 3:
    if not "filtri" in data or not st[1] in data["filtri"]:
      data["filtri"].append(st[1])
      data["reply"].append(st[2])
      with open("storage.json", "w+") as f:
        json.dump(data, f)
      await e.edit("**✅ Filtro Aggiunto ✅**")
    else:
      await e.edit("**❌ Filtro già presente ❌**")
  else:
    await e.edit("**❌ Errore Di Sintassi ❌**")
 
@register(outgoing=True, pattern="^[.]delfiltro ")
async def unFilter(e):
  filtro = e.text.split(" ")[1]
  with open("storage.json", "r") as f:
    data = json.load(f)
  if "filtri" in data and filtro in data["filtri"]:
    for i in range(data["filtri"].__len__()):
      if data["filtri"][i] == filtro:
        data["reply"].remove(data["reply"][i])
        break
    await e.edit("**🚫 Filtro Rimosso 🚫**")
    data["filtri"].remove(filtro)
    with open("storage.json", "w+") as f:
      json.dump(data, f)
  else:
    await e.edit("**❌ Filtro Non Esistente ❌**")
 
@register(outgoing=True, pattern="^[.]filtri$")
async def filterList(e):
  with open("storage.json", "r") as f:
    data = json.load(f)
  filtri = "**LISTA FILTRI**__\n"
  if "filtri" in data:
    for i in data["filtri"]:
      filtri += "\n- " + i
  await e.edit(filtri + "__")
 
@register(outgoing=True)
async def Filter(e):
  with open("storage.json", "r") as f:
    data = json.load(f)
  if "filtri" in data:
    for i in range(data["filtri"].__len__()):
      if e.text.lower() == data["filtri"][i].lower():
        await e.edit(data["reply"][i])
        break

@register(outgoing=True, pattern="^.as")
async def addsticker(args):
    if not args.text[0].isalpha() and args.text[0] not in ("/", "#", "@", "!"):
        user = await bot.get_me()
        if not user.username:
            user.username = user.first_name
        message = await args.get_reply_message()
        photo = None
        emojibypass = False
 
        if message and message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo = io.BytesIO()
                photo = await bot.download_media(message.photo, photo)
            elif "image" in message.media.document.mime_type.split('/'):
                photo = io.BytesIO()
                await bot.download_file(message.media.document, photo)
                if (DocumentAttributeFilename(file_name='sticker.webp')
                        in message.media.document.attributes):
                    emoji = message.media.document.attributes[1].alt
                    emojibypass = True
            else:
                await args.edit("❌` File non supportato!`")
                return
        else:
            await args.edit("❌ `Rispondi ad una foto...`")
            return
 
        if photo:
            image = await resize_photo(photo)
            splat = args.text.split()
            if not emojibypass:
                emoji = "🤔"
            pack = "1"
            if len(splat) == 3:
                pack = splat[2]     #User sent both
                emoji = splat[1]
            elif len(splat) == 2:
                if splat[1].isnumeric():
                    #User wants to push into different pack, but is okay with thonk as emote.
                    pack = int(splat[1])
                else:
                    #User sent just custom emote, wants to push to default pack
                    emoji = splat[1]
 
            packname = f"StickerPackeqwighewig"
            response = urllib.request.urlopen(
                urllib.request.Request(f'http://t.me/addstickers/{packname}')
            )
            htmlstr = response.read().decode("utf8").split('\n')
            file = io.BytesIO()
            file.name = "sticker.png"
            image.save(file, "PNG")
            if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in htmlstr:
                async with bot.conversation('Stickers') as conv:
                    await conv.send_message('/addsticker')
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packname)
                    await conv.get_response()
                    file.seek(0)
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.send_file(file, force_document=True)
                    await conv.get_response()
                    await conv.send_message(emoji)
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message('/done')
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
            else:
                await args.edit("Il tuo userbot non ha ancora uno stickerpack, te lo creo io tranquillo.")
                async with bot.conversation('Stickers') as conv:
                    await conv.send_message('/newpack')
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(f"Sticker Pack EGweherj")
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                    await conv.get_response()
                    await conv.send_message(emoji)
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message("/publish")
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message("/skip")
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message(packname)
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await bot.send_read_acknowledge(conv.chat_id)
 
            await args.edit(
                f"Sticker aggiunto! Puoi vedere il tuo pack [qui](t.me/addstickers/{packname})",
                parse_mode='md'
            )
 
async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512/size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512/size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)
 
    return image


@register(outgoing=True, pattern="^[.]creator$")
async def cre(e):
  await e.edit("__Creatore @appacificarsi__")

@register(outgoing=True, pattern="^[.]verify$")
async def Verify(e):
  global verify
  verify = e
  await e.client.send_message("@SpamBot", "/start")

@register(incoming=True)
async def checkVerify(e):
  global verify
  global verify
  if verify != None:
    if e.chat_id == 178220800:
      if ":" in e.text:
        st = e.text.split(" ")
        for i in range(st.__len__()):
          if ":" in st[i]:
            fine = st[i - 3] + " " + st[i - 2] + " " + st[i - 1] + " Ore: " +st[i]
            break
        await verify.edit(f"**❌ Sei limitato fino al {fine} ❌**")
        verify = None
        await e.client(functions.messages.DeleteHistoryRequest(e.chat_id, 0, False, True))
      else:
        await verify.edit("**✅ Non sei limitato ✅**")
        verify = None
        await e.client(functions.messages.DeleteHistoryRequest(e.chat_id, 0, False, True))

if os.path.exists("saves.json"):
	with open("saves.json", "r+") as f:
		SAVES = json.load(f)
else:
	SAVES = {"AFKMode": False, "Approved": [], "mutedList": [], "AFK-Mex": "Puoi customizzare il seguente messaggio con .msgafk", "Block-Mex": "Puoi customizzare il seguente messaggio con .msgblock"}
	with open("saves.json", "w+") as f:
		json.dump(SAVES, f)
	

async def save():
	global SAVES
	with open("saves.json", "w+") as f:
		json.dump(SAVES, f)



inWait = []
	
@register(outgoing=True, pattern="^[.]msgafk")
async def setAFKMex(e):
	global SAVES
	st = e.text.split(" ", 1)
	if st.__len__() == 2:
		SAVES["AFK-Mex"] = st[1]
		'(save)'
		await e.edit("**✅ Messaggio Impostato Correttamente ✅**")
	else:
		await e.edit("**❌ Specificare il messaggio ❌**")


@register(outgoing=True, pattern="^[.]afk$")
async def setAFK(e):
	global SAVES
	if SAVES["AFKMode"]:
		SAVES["AFKMode"] = False
		'(save)'
		await e.edit("**❌ AFK Mode Disattivata ❌**")
	else:
		SAVES["AFKMode"] = True
		'(save)'
		await e.edit("**✅ AFK Mode Attivata ✅**")
	
@register(outgoing=True, pattern="^[.]approve$")
async def approveUser(e):
	global SAVES
	if e.chat_id in SAVES["Approved"]:
		await e.edit("**❌ Quest utente è già approvato ❌**")
	else:
		SAVES["Approved"].append(e.chat_id)
		'(save)'
		await e.edit("**✅ Utente Approvato ✅**")
	
@register(outgoing=True, pattern="^[.]disapprove$")
async def disapproveUser(e):
	global SAVES
	if e.chat_id in SAVES["Approved"]:
		SAVES["Approved"].remove(e.chat_id)
		'(save)'
		await e.edit("**❌ Utente Disapprovato ❌**")
	else:
		await e.edit("**❌ Quest utente non è approvato ❌**")
	

@register(incoming=True)
async def doAFK(e): 
	global SAVES, inWait
	if SAVES["AFKMode"] and e.is_private and not (await e.get_sender()).bot and not e.chat_id in SAVES["Approved"]:
		await e.delete()
		if not e.chat_id in inWait: 
			inWait.append(e.chat_id)
			if e.text == None or e.text == "":
				mex = "__MEDIA__"
			else:
				mex = e.text
			await e.respond(SAVES["AFK-Mex"].replace("{msg}", mex))
			await asyncio.sleep(30)
			inWait.remove(e.chat_id)

@register(outgoing=True, pattern="^.spam")
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[6:8])
        spam_message = str(e.text[8:])
        await asyncio.wait([e.respond(spam_message) for i in range(counter)])
        await e.delete()

@register(outgoing=True, pattern="^[.]comandi")
async def comandi(e):
	await asyncio.wait([e.edit("[🔗Clicca qui](https://telegra.ph/Comandi-UserBot-07-25)")])

if os.path.exists("gruppigmex.json"):
    with open("gruppigmex.json", "r+") as f:
        Groups = json.load(f)
else:
    Groups = {}
    with open("gruppigmex.json", "w+") as f:
      json.dump(Groups, f)

async def updateGroups():
    global Groups
    with open("gruppigmex.json", "w+") as f:
        json.dump(Groups, f)
    return True

@register(outgoing=True, pattern="^[.]gmex")
async def GmexFunction(e):
    global Groups
    st = e.text.split(" ", 1)
    if len(st) == 2:
        if len(Groups) > 0:
            await e.edit("**⚠️ Avviso** » __Sto gmexando, Attendere...__")
            await asyncio.wait([e.client.send_message(int(chat), st[1]) for chat in Groups])
            await e.edit("**✅ » Gmex completato con successo!**")
        else:
            await e.edit("**⚠️ Errore** » __Non ci sono gruppi in cui gmexare!__")
    else:
         await e.edit("**⚠️ Errore** » __Specifica il messaggio che devo gmexare!__")

@register(outgoing=True, pattern="^[.]addgroup")
async def addChat(e):
    global Groups
    st = e.text.replace("-100", "").split(" ", 1)
    if len(st) == 2:
        if st[1].isnumeric():
            mex = int(st[1])
        else:
            mex = st[1]
        try:
            group = await e.client.get_entity(mex)
        except:
            await e.edit(f"**⚠️ Errore** » __Chat non trovata, controlla di aver inserito l'username/ID corretto!__")
            return
        if type(group).__name__ == "User":
            await e.edit("**⚠️ Errore** » __Puoi aggiungere solo gruppi o canali!__")
            return
        if not str(group.id) in Groups:
            Groups[str(group.id)] = group.title
            await updateGroups()
            await e.edit(f"**✅ » Chat** {group.title} **aggiunta con successo!**")
        else:
            await e.edit(f"**⚠️ Errore** » __Chat__ {group.title} __già presente nel database__")
    else:
        await e.edit("**⚠️ Errore** » __Specifica la chat da aggiungere!__")

@register(outgoing=True, pattern="^[.]delgroup")
async def remChat(e):
    global Groups
    st = e.text.replace("-100", "").split(" ", 1)
    if len(st) == 2:
        if st[1].isnumeric():
            mex = int(st[1])
        else:
            mex = st[1]
        try:
            group = await e.client.get_entity(mex)
        except:
            await e.edit("**⚠️ Errore** »__Chat non trovata__ ")
            return
        if str(group.id) in Groups:
            del Groups[str(group.id)]
            await updateGroups()
            await e.edit(f"**🚫 » Chat** {group.title} **rimossa con successo!**")
        else:
            await e.edit(f"**⚠️ Errore** » __Chat__ {group.title} __non presente nel database__**")
    else:
        await e.edit("**⚠️ Errore** » __Specifica la Chat da rimuovere!__")

@register(outgoing=True, pattern="^[.]group$")
async def chatsList(e):
    global Groups
    if len(Groups) > 0:
        msg = "**💬 LISTA CHAT 💬**\n"
        for id in Groups:
            msg += "\n" + Groups[id] + f" [`-100{id}`]"
        await e.edit(msg + "\n\n__📂 Chat  »__ `" + str(len(Groups)) + "`")
    else:
        await e.edit("**⚠️ Nessuna Chat Aggiunta ⚠️**")


import os

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName


TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./")


@register(pattern=".info(?: |$)(.*)", outgoing=True)
async def who(event):
    if event.fwd_from:
        return
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    replied_user = await get_user(event)
    photo, caption = await fetch_info(replied_user, event)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    try:
        await event.client.send_file(event.chat_id, photo, caption=caption, link_preview=False, force_document=False, reply_to=message_id_to_reply, parse_mode="html")
    except:
        await event.edit("**❌ ERRORE SCONOSCIUTO, RIPROVARE! ❌**")
    if not photo.startswith("http"):
        os.remove(photo)
    await event.delete()

async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except:
            await event.edit("**❌ Utente Non Trovato ❌**")
            return None
    return replied_user

async def fetch_info(replied_user, event):
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    if replied_user.user.bot:
        user_is_bot = "✅"
    else:
        user_is_bot = "❌"
    try:
        photo = await event.client.download_profile_photo(user_id, TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg", download_big=True)
    except:
        photo = "https://thumbs.dreamstime.com/b/no-user-profile-picture-24185395.jpg"
    first_name = first_name.replace("\u2060", "") if first_name else (
        "❌")
    last_name = last_name.replace("\u2060", "") if last_name else (
        "❌")
    username = "@{}".format(username) if username else (
        "❌")
    user_bio = "❌" if not user_bio else "\n" + user_bio
    caption = f"<b>⚙ INFO UTENTE ⚙</b>\n\n<b>👨🏻‍🔧Nome:</b> {first_name}\n<b>🤵🏻Cognome:</b> {last_name}\n<b>🌐Username:</b> {username}\n🆔ID:</b> <code>{user_id}</code>\n<b>🤖Bot:</b> {user_is_bot}\n<b>💬Chat In Comune:</b> {common_chat}\n<b>🔗PermaLink:</b> <a href=\"tg://user?id={user_id}\">{first_name}</a>\n<b>📕Bio:</b> <code>{user_bio}</code>"
    return photo, caption


bot.start()
bot.connect()
bot.run_until_disconnected()

#test