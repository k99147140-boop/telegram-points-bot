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

# تأكد إن الملف ينشأ لو غير موجود
if not os.path.exists(DATA):
    save({"users": {}, "teams": {}})

data = load()

# ===== المستخدمين =====

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

# ===== الفرق =====

async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("استخدم: /CreaTeam اسم الفريق")
    team = " ".join(context.args)
    data["teams"][team] = 0
    save(data)
    await update.message.reply_text("✅ تم إنشاء الفريق")

async def dpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("استخدم: /dpt اسم الفريق عدد")
    team = context.args[0]
    amount = int(context.args[1])
    data["teams"][team] = data["teams"].get(team, 0) + amount
    save(data)
    await update.message.reply_text("✅ نقاط للفريق أضيفت")

async def ttop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_teams = sorted(data["teams"].items(), key=lambda x: x[1], reverse=True)[:10]
    text = "🏆 أفضل 10 فرق:\n"
    for i, (t, p) in enumerate(sorted_teams, 1):
        text += f"{i}- {t} | {p}\n"
    await update.message.reply_text(text)

# ===== تشغيل =====

if not TOKEN:
    raise ValueError("TOKEN غير موجود في متغيرات البيئة")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("dxp", dxp))
app.add_handler(CommandHandler("rep", rep))
app.add_handler(CommandHandler("top", top))
app.add_handler(CommandHandler("CreaTeam", create_team))
app.add_handler(CommandHandler("dpt", dpt))
app.add_handler(CommandHandler("ttop", ttop))

app.run_polling() 
