import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Ganti dengan Token dari BotFather
TOKEN = "8689353200:AAFixxsh-XkZf-M9swZYFmmYvKHKoa2jB6E"

# Masukkan ID Grup Publik dan Grup VIP Anda
TARGET_CHATS = [
    "-1002733560586"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Bot Multi-Group Anti-Malas Siap!**\n\n"
        "1️⃣ Kirim Sinyal Baru:\n"
        "`/s [pair] [buy/sell] [entry] [sl] [tp]`\n"
        "Contoh: `/s XAUUSD BUY 2350 2345 2365`\n\n"
        "2️⃣ Update TP Kena (Hit TP):\n"
        "`/tp [pair] [berapa pips/profit]`\n"
        "Contoh: `/tp XAUUSD HIT TP 150 Pips`",
        parse_mode="Markdown"
    )

async def send_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 5:
        await update.message.reply_text("⚠️ Format kurang lengkap!\nGunakan: `/s [pair] [buy/sell] [entry] [sl] [tp]`", parse_mode="Markdown")
        return
    
    pair = args[0].upper()
    action = args[1].upper()
    entry = args[2]
    sl = args[3]
    tp = args[4]
    
    action_emoji = "🟢 BUY" if "BUY" in action else "🔴 SELL"
    
    signal_message = (
        f"📢 **SIGNAL UPDATE**\n\n"
        f"🔹 **Pair:** {pair}\n"
        f"🔹 **Action:** {action_emoji}\n"
        f"🔹 **Entry:** {entry}\n"
        f"❌ **SL:** {sl}\n"
        f"✅ **TP:** {tp}\n\n"
        f"_Selalu gunakan manajemen risiko!_ ⚠️"
        f"_Wajib menggunakan Risk N Reward!_ ⚠️"
    )
    
    success_count = 0
    for chat_id in TARGET_CHATS:
        try:
            await context.bot.send_message(chat_id=chat_id.strip(), text=signal_message, parse_mode="Markdown")
            success_count += 1
        except Exception:
            pass

    if success_count > 0:
        await update.message.reply_text(f"✅ Sinyal berhasil dikirim ke {success_count} grup!")
    else:
        await update.message.reply_text("❌ Gagal mengirim sinyal.")

async def hit_tp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("⚠️ Format kurang lengkap!\nGunakan: `/tp [pair] [keterangan/pips]`", parse_mode="Markdown")
        return
    
    pair = args[0].upper()
    detail = " ".join(args[1:]) if len(args) > 1 else "Target Tercapai!"
    
    tp_message = (
        f"🎯 **UPDATE: HIT TP!** 🚀\n\n"
        f"🔹 **Pair:** {pair}\n"
        f"✅ **Status:** {detail}\n\n"
        f"_Congratulations bagi yang ikutan! 🎉_"
    )
    
    success_count = 0
    for chat_id in TARGET_CHATS:
        try:
            await context.bot.send_message(chat_id=chat_id.strip(), text=tp_message, parse_mode="Markdown")
            success_count += 1
        except Exception:
            pass

    if success_count > 0:
        await update.message.reply_text(f"✅ Update Hit TP berhasil dikirim ke {success_count} grup!")
    else:
        await update.message.reply_text("❌ Gagal mengirim update TP.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("s", send_signal))
    app.add_handler(CommandHandler("tp", hit_tp))
    print("Bot Multi-Group (Signal & TP Update) sedang berjalan...")
    app.run_polling()