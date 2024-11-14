import discord
from discord.ext import commands
from discord.ui import Button, View
import os
import random
import yaml
from dotenv import load_dotenv
from fox_responses import handle_greeting
import sys

# 加載環境變量
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_TEST_BOT')
AUTHOR_ID = int(os.getenv('AUTHOR_ID'))

# 設定初始變數
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# 設置好感度文件路徑
AFFECTION_FILE = 'affection_data.yml'

# 初始化或載入好感度數據
def load_affection_data():
    # 如果文件不存在，先創建一個空的 YAML 文件
    if not os.path.exists(AFFECTION_FILE):
        save_affection_data({})  # 創建空的 YAML 文件
    try:
        with open(AFFECTION_FILE, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return data if data else {}
    except FileNotFoundError:
        return {}

# 儲存好感度數據
def save_affection_data(data):
    with open(AFFECTION_FILE, 'w', encoding='utf-8') as file:
        yaml.safe_dump(data, file)

affection_data = load_affection_data()

# 語氣描述根據等級劃分
def get_affection_tone(level):
    if 1 <= level <= 20:
        return "如同陌生人般的冷淡"
    elif 21 <= level <= 40:
        return "如同好友般的好感"
    elif 41 <= level <= 60:
        return "如同熱戀般的情人"
    elif 61 <= level <= 80:
        return "如同老夫老妻般的好感"
    elif 81 <= level <= 100:
        return "如同互相離不開的存在"
    else:
        return "無法用言語形容的深情"

# 增加或查詢好感度的功能
def get_affection(user_id):
    user_data = affection_data.get(str(user_id), {"affection": 0, "level": 1, "limit": 100})
    return user_data

def add_affection(user_id, amount):
    user_id = str(user_id)
    if user_id not in affection_data:
        affection_data[user_id] = {"affection": 0, "level": 1, "limit": 100}

    user_data = affection_data[user_id]
    user_data["affection"] += amount

    # 等級提升邏輯
    if user_data["affection"] >= user_data["limit"]:
        user_data["affection"] -= user_data["limit"]
        user_data["level"] = min(user_data["level"] + 1, 100)  # 等級最大值為 100
        user_data["limit"] = int(user_data["limit"] * 1.1)  # 每升級增加10%限制

    save_affection_data(affection_data)
    return user_data

# 機器人上線事件
@bot.event
async def on_ready():
    print(f'已登入 {bot.user.name}')
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.playing, name='喜歡主人的愛')
    )
    try:
        synced = await bot.tree.sync()
        print(f'成功同步 {len(synced)} 个命令')
    except Exception as e:
        print(f'同步命令时出错: {e}')

# 訊息偵測事件
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content_lower = message.content.lower()
    user_data = get_affection(message.author.id)  # 獲取用戶好感度資料
    await handle_greeting(message, content_lower, user_data, bot_name=bot.user.name)

    # 隨機增加好感度
    if random.random() < 0.1:  # 10% 機率增加好感度
        user_data = add_affection(message.author.id, random.randint(1, 5))
        
        # 獲取當前語氣
        tone = get_affection_tone(user_data["level"])
        await message.channel.send(
            f'{message.author.mention} 的當前好感度: {user_data["affection"]}/{user_data["limit"]} '
            f'等級: {user_data["level"]} ({tone})'
        )

    await bot.process_commands(message)

@bot.tree.command(name="shutdown", description="关闭芙蘭")
async def shutdown(interaction: discord.Interaction):
    if interaction.user.id == AUTHOR_ID:
        await interaction.response.send_message("進入關閉狀態...")
        await bot.close()
    else:
        await interaction.response.send_message("就凴你也敢關閉我嗎 啊")

@bot.tree.command(name="restart", description="重启芙蘭")
async def restart(interaction: discord.Interaction):
    if interaction.user.id == AUTHOR_ID:
        await interaction.response.defer()
        await interaction.followup.send("你有本事等老娘回來")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await interaction.response.send_message("就凴你可以重啓我嗎 啊")

# 啟動機器人
bot.run(TOKEN)
