import telebot
from telebot import types

TOKEN = '8998297014:AAFMfA_ohy3vWrvmuP1F3upFyukORGJP3Ws'
OWNER_ID = 8611694812

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id == OWNER_ID:
        bot.reply_to(message, "أهلاً بك يا مطوري محمد في سورس الحماية الخاص بك! 🚀")
    else:
        bot.reply_to(message, "أهلاً بك! أنا بوت الحماية الذكي المطور بواسطة محمد.")

@bot.message_handler(func=lambda message: message.text == "هلو")
def say_hello(message):
    bot.reply_to(message, "هلوات عيوني! نورت الكروب ✨")

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    for member in message.new_chat_members:
        if member.is_bot:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                bot.ban_chat_member(message.chat.id, member.id)
            except:
                pass
            continue
        
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اضغط هنا لإثبات أنك لست بوت 🤖✅", callback_data=f"verify_{member.id}")
        markup.add(btn)

        bot.send_message(
            message.chat.id,
            f"مرحباً بك يا {member.first_name} في المجموعة! ✨\n\n⚠️ يرجى الضغط على الزر أدناه لتأكيد وجودك.\n\n⚙️ مبرمج البوت: المطور محمد",
            reply_markup=markup
        )

@bot.message_handler(func=lambda message: message.from_user.id != OWNER_ID and any(x in message.text for x in ["http://", "https://", "t.me/", "@"]))
def anti_links(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.ban_chat_member(message.chat.id, message.from_user.id)
        bot.send_message(message.chat.id, "🚫 تم طرد العضو بسبب نشر رابط إعلاني!")
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('verify_'))
def verify_member(call):
    target_id = int(call.data.split('_')[1])
    if call.from_user.id == target_id:
        bot.answer_callback_query(call.id, "تم التحقق بنجاح! 🎉", show_alert=True)
        try:
            bot.edit_message_text(
                f"✅ تم التحقق من العضو {call.from_user.first_name} بنجاح.\n\n⚙️ حماية السورس: المطور محمد",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
        except:
            pass
    else:
        bot.answer_callback_query(call.id, "❌ هذا الزر مخصص للعضو الجديد فقط!", show_alert=True)

bot.infinity_polling()
