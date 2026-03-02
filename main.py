Python
import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
DATA = "points.json"

def load():
    if os.path.exists(DATA):
        with open(DATA, "r") as f:
            return json.load(f)
    return {"users": {}, "teams": {}}

def save(data):
    with open(DATA, "w") as f:
        json.dump(data, f, indent=4)

if not os.path.exists(DATA):
    save({"users": {}, "teams": {}})

data = load()

async def dxp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("استخدم: /dxp اسم عدد")
    user = context.args[0]
    amount = int(context.args[1])
    data["users"][user] = data["users"].get(user, 0) + amount
    save(data)
    await update.message.reply_text("✅ تم إضافة نقاط")

async def rep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("استخدم: /rep اسم عدد")
    user = context.args[0]
    amount = int(context.args[1])
    data["users"][user] = data["users"].get(user, 0) - amount
    save(data)
    await update.message.reply_text("❌ تم خصم نقاط")

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_users = sorted(data["users"].items(), key=lambda x: x[1], reverse=True)[:10]
    text = "🏆 أفضل 10 أعضاء:\n"
    for i, (u, p) in enumerate(sorted_users, 1):
        text += f"{i}- {u} | {p}\n"
    await update.message.reply_text(text)

if not TOKEN:
    raise ValueError("TOKEN غير موجود")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("dxp", dxp))
app.add_handler(CommandHandler("rep", rep))
app.add_handler(CommandHandler("top", top))

app.run_polling()
