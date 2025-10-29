import telebot
from telebot import types

TOKEN = "8462151858:AAGwgaVK1iR4jWXq1NIXsOljh2mhyO0-QAk"
bot = telebot.TeleBot(TOKEN)

# Данные портфеля (статичные для примера)
portfolio_data = {
    "collateral": [
        {"symbol": "ETH", "amount": 2.0, "price": 3200, "threshold": 0.80},
        {"symbol": "USDC", "amount": 1500, "price": 1.0, "threshold": 0.90}
    ],
    "debt": [
        {"symbol": "USDT", "amount": 3000, "price": 1.0},
        {"symbol": "WBTC", "amount": 0.5, "price": 67000}
    ]
}

# Алерты
alerts = [
    {"level": 1.10, "message": "HF упал ниже 1.10! Пополни коллатерал"},
    {"level": 1.05, "message": "Почти ликвидация, действуй СЕЙЧАС"},
    {"level": 1.00, "message": "Зона ликвидации!"}
]

def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📊 Статус", "🔔 Алерты")
    kb.row("💸 Безопасность", "📈 Анализ")
    return kb

def calculate_hf():
    total_collateral = sum(a["amount"] * a["price"] for a in portfolio_data["collateral"])
    total_debt = sum(d["amount"] * d["price"] for d in portfolio_data["debt"])
    weighted_collateral = sum(a["amount"] * a["price"] * a["threshold"] for a in portfolio_data["collateral"])
    return weighted_collateral / total_debt if total_debt > 0 else None

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "🏦 DeFi Risk Manager\n\n"
        "Функционал:\n"
        "• 📊 Статус - Health Factor и риски\n"
        "• 🔔 Алерты - уведомления о рисках\n"
        "• 💸 Безопасность - расчет параметров\n"
        "• 📈 Анализ - детали портфеля\n\n"
        "Выбери действие 👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: m.text == "📊 Статус")
def handle_status(message):
    hf = calculate_hf()
    total_coll = sum(a["amount"] * a["price"] for a in portfolio_data["collateral"])
    total_debt = sum(d["amount"] * d["price"] for d in portfolio_data["debt"])
    
    status = "🟢 Безопасно" if hf and hf > 1.5 else "🟡 Внимание" if hf and hf > 1.1 else "🔴 Опасно"
    
    text = (
        f"📊 Статус портфеля:\n"
        f"💰 Залог: ${total_coll:,.0f}\n"
        f"💸 Долг: ${total_debt:,.0f}\n"
        f"❤️ Health Factor: {hf:.2f}\n"
        f"⚠️ Статус: {status}"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "🔔 Алерты")
def handle_alerts(message):
    hf = calculate_hf()
    if not hf:
        bot.send_message(message.chat.id, "✅ Нет долга - нет рисков")
        return
    
    active_alerts = [a for a in alerts if hf <= a["level"]]
    if not active_alerts:
        bot.send_message(message.chat.id, f"✅ Всё окей. HF={hf:.2f}")
        return
    
    text = "🚨 АКТИВНЫЕ АЛЕРТЫ:\n" + "\n".join(f"• {a['message']}" for a in active_alerts)
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "💸 Безопасность")
def handle_safety(message):
    hf = calculate_hf()
    total_debt = sum(d["amount"] * d["price"] for d in portfolio_data["debt"])
    max_safe_debt = sum(a["amount"] * a["price"] * a["threshold"] for a in portfolio_data["collateral"]) / 1.3
    
    text = (
        f"🛡 Безопасные параметры:\n"
        f"🎯 Целевой HF: 1.30\n"
        f"📏 Макс. безопасный долг: ${max_safe_debt:,.0f}\n"
        f"💸 Текущий долг: ${total_debt:,.0f}\n"
    )
    
    if total_debt > max_safe_debt:
        text += f"⚠️ Перегруз: ${total_debt - max_safe_debt:,.0f}"
    else:
        text += "✅ В безопасной зоне"
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text == "📈 Анализ")
def handle_analysis(message):
    text = "🔐 Залоги:\n"
    for asset in portfolio_data["collateral"]:
        value = asset["amount"] * asset["price"]
        text += f"• {asset['symbol']}: {asset['amount']} = ${value:,.0f}\n"
    
    text += "\n💀 Долги:\n"
    for debt in portfolio_data["debt"]:
        value = debt["amount"] * debt["price"]
        text += f"• {debt['symbol']}: {debt['amount']} = ${value:,.0f}\n"
    
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "Выбери действие с кнопок 👇", reply_markup=main_keyboard())

if __name__ == "__main__":
    print("DeFi Risk Manager запущен...")
    bot.infinity_polling(skip_pending=True)
