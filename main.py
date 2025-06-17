import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ['BOT_TOKEN']
BASE_URL = os.environ['BASE_URL']

# Uvítací zpráva
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇨🇿 Čeština", callback_data='lang_cz')],
        [InlineKeyboardButton("🌍 English", callback_data='lang_en')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "☕️ Welcome to Coffee Perk!\nWe’re happy to see you here. 🌟\nPlease choose your language. 🗣️",
        reply_markup=reply_markup
    )

# Zpracování výběru jazyka
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'lang_cz':
        keyboard = [
            [InlineKeyboardButton("🧾 Menu a nabídka", callback_data='menu')],
            [InlineKeyboardButton("🕐 Otevírací doba", callback_data='hours')],
            [InlineKeyboardButton("📍 Kde nás najdete", callback_data='location')],
            [InlineKeyboardButton("📞 Kontakt / Rezervace", callback_data='contact')],
            [InlineKeyboardButton("📦 Předobjednávka (již brzy)", callback_data='order')],
            [InlineKeyboardButton("😎 Důvody, proč si zajít na kávu", callback_data='reasons')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Na co se mě můžeš zeptat:", reply_markup=reply_markup)

    elif query.data == 'lang_en':
        await query.edit_message_text("English version is not available yet.")

# Odpovědi na jednotlivé sekce
async def handle_sections(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sections = {
        'menu': "🥐 COFFEE PERK MENU ☕️\nU nás nejde jen o kafe. Je to malý rituál...\n👉 https://www.coffeeperk.cz/jidelni-listek",
        'hours': "🕐 KDY MÁME OTEVŘENO?\n📅 Po–Pá: 7:30 – 17:00\n📅 So–Ne: ZAVŘENO",
        'location': "📍 KDE NÁS NAJDETE?\n🏠 Vyskočilova 1100/2, Praha 4\n🗺️ https://goo.gl/maps/XU3nYKDcCmC2",
        'contact': "📞 KONTAKTUJTE NÁS\n📬 info@coffeeperk.cz\n📞 +420 725 422 518",
        'order': "📦 PŘEDOBJEDNÁVKY\nBrzy spustíme možnost objednat přes Telegram.",
        'reasons': "😎 DŮVODY, PROČ SI ZAJÍT NA KÁVU\n☕ Protože svět se lépe řeší s kofeinem...\n💛 A někdy netřeba důvod. Prostě přijďte.",
    }
    text = sections.get(query.data, "Neznámá volba.")
    await query.edit_message_reply_markup(reply_markup=None)
    await query.edit_message_text(text)

# Spuštění bota s webhookem
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(handle_sections))

    # Webhook
    await app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=f"{BASE_URL}/webhook"
    )

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
