import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

BOT_TOKEN = os.environ["BOT_TOKEN"]
BASE_URL  = os.environ["BASE_URL"]    # např. https://tvuj-servis.onrender.com
PORT      = int(os.environ.get("PORT", 5000))

# Flask server
app = Flask(__name__)

# Telegram-bot
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

# -- HANDLERY --

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇨🇿 Čeština",  callback_data="lang_cs"),
            InlineKeyboardButton("🌍 English",  callback_data="lang_en")
        ]
    ]
    await update.message.reply_text(
        "☕️ Welcome to Coffee Perk!\nWe’re happy to see you here. 🌟\nPlease choose your language. 🗣️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# volba jazyka
async def lang_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.callback_query.data
    await update.callback_query.answer()
    if code == "lang_cs":
        keyboard = [
            [InlineKeyboardButton("🧾 Menu a nabídka", callback_data="menu_cs")],
            [InlineKeyboardButton("🕐 Otevírací doba", callback_data="hours_cs")],
            [InlineKeyboardButton("📍 Kde nás najdete", callback_data="where_cs")],
            [InlineKeyboardButton("📞 Kontakt / Rezervace", callback_data="contact_cs")],
            [InlineKeyboardButton("📦 Předobjednávka", callback_data="preorder_cs")],
            [InlineKeyboardButton("😎 Proč k nám?", callback_data="why_cs")]
        ]
        await update.callback_query.edit_message_text(
            "Na co se mě můžeš zeptat:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        keyboard = [
            [InlineKeyboardButton("🧾 Menu & Offer", callback_data="menu_en")],
            [InlineKeyboardButton("🕐 Opening Hours", callback_data="hours_en")],
            [InlineKeyboardButton("📍 Location", callback_data="where_en")],
            [InlineKeyboardButton("📞 Contact / Booking", callback_data="contact_en")],
            [InlineKeyboardButton("📦 Pre-order", callback_data="preorder_en")],
            [InlineKeyboardButton("😎 Why Visit", callback_data="why_en")]
        ]
        await update.callback_query.edit_message_text(
            "What can you ask me:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# jednotlivé sekce
SECTIONS = {
    "menu_cs":
        "🥐 **COFFEE PERK MENU** ☕️\n\n"
        "☕ Výběrová káva\n"
        "🍳 Snídaně (lehké i pořádné)\n"
        "🍰 Domácí dorty\n"
        "🥗 Brunch a saláty\n\n"
        "📄 Kompletní menu:\n"
        "👉 https://www.coffeeperk.cz/jidelni-listek\n\n"
        "Ať už si dáte espresso, matchu nebo zázvorovku – tady to chutná líp. 💛",
    "hours_cs":
        "🕐 **KDY MÁME OTEVŘENO?**\n\n"
        "📅 Pondělí–Pátek: 7:30 – 17:00\n"
        "📅 Sobota & Neděle: ZAVŘENO\n\n"
        "Chcete nás navštívit? Jsme tu každý všední den od brzkého rána. ☕",
    "where_cs":
        "📍 **KDE NÁS NAJDETE?**\n\n"
        "🏠 Vyskočilova 1100/2, Praha 4\n"
        "🗺️ Mapa: https://goo.gl/maps/XU3nYKDcCmC2\n\n"
        "Najdete nás snadno – stylová kavárna, příjemná atmosféra a lidé, co kávu berou vážně i s úsměvem.",
    "contact_cs":
        "📞 **KONTAKTUJTE NÁS**\n\n"
        "📬 E-mail: info@coffeeperk.cz\n"
        "📞 Telefon: +420 725 422 518\n\n"
        "Rádi vám pomůžeme s rezervací nebo výběrem.",
    "preorder_cs":
        "📦 **PŘEDOBJEDNÁVKY**\n\n"
        "Brzy spustíme možnost objednat si kávu a snídani předem přes Telegram. Zatím nás navštivte osobně. ☕️",
    "why_cs":
        "😎 **DŮVODY, PROČ SI ZAJÍT NA KÁVU**\n\n"
        "☕ Protože svět se lépe řeší s kofeinem.\n"
        "📚 Práce počká – espresso ne.\n"
        "💬 Dobrý rozhovor začíná u šálku.\n"
        "🧠 Mozek startuje po druhé kávě.\n\n"
        "Někdy netřeba důvod – prostě přijďte. 💛",

    # *** English ***
    "menu_en":
        "🥐 **COFFEE PERK MENU** ☕️\n\n"
        "☕ Specialty coffee\n"
        "🍳 Breakfast (light & hearty)\n"
        "🍰 Homemade cakes\n"
        "🥗 Brunch & salads\n\n"
        "📄 Full menu:\n"
        "👉 https://www.coffeeperk.cz/jidelni-listek\n\n"
        "Whether it’s espresso, matcha or ginger tea – it tastes better here. 💛",
    "hours_en":
        "🕐 **OPENING HOURS**\n\n"
        "📅 Mon–Fri: 7:30 AM – 5 PM\n"
        "📅 Sat & Sun: CLOSED\n\n"
        "Drop by any weekday morning for great coffee. ☕",
    "where_en":
        "📍 **LOCATION**\n\n"
        "🏠 Vyskočilova 1100/2, Prague 4\n"
        "🗺️ Map: https://goo.gl/maps/XU3nYKDcCmC2\n\n"
        "Stylish café, friendly vibes – find us easily!",
    "contact_en":
        "📞 **CONTACT / BOOKING**\n\n"
        "📬 Email: info@coffeeperk.cz\n"
        "📞 Phone: +420 725 422 518\n\n"
        "We’re happy to help you book a table or answer your questions.",
    "preorder_en":
        "📦 **PRE-ORDER**\n\n"
        "Coming soon: order your coffee & breakfast ahead via Telegram. Stay tuned!",
    "why_en":
        "😎 **WHY VISIT US?**\n\n"
        "☕ Because life’s better with caffeine.\n"
        "📚 Work can wait – coffee can’t.\n"
        "💬 Great chats start over a cup.\n"
        "🧠 Brain fires up after that second cup.\n\n"
        "No reason needed – just come by. 💛",
}

async def show_section(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = update.callback_query.data
    await update.callback_query.answer()
    text = SECTIONS.get(key, "❌ Sekce nenalezena.")
    await update.callback_query.edit_message_text(text)

# registrace
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(lang_select, pattern=r"^lang_"))
bot_app.add_handler(CallbackQueryHandler(show_section, pattern=r"^(menu|hours|where|contact|preorder|why)_"))

# webhook receiver
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot_app.bot)
    bot_app._handle_update(update)  # interní volání
    return "OK"

if __name__ == "__main__":
    # nastavíme webhook u Telegramu
    bot_app.job_queue.run_once(lambda _: bot_app.bot.set_webhook(f"{BASE_URL}/{BOT_TOKEN}"), when=0)
    # spustíme Flask + PTB webhook listener
    bot_app.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN
    )
    bot_app.idle()
