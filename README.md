# 委托

海 這裏是還在趕工委托的Shiroko(Miya)

至於這個委托是別人的 所以 被炒了 我沒差 我也沒關係
### 該代碼所需要的庫
- python庫
  - discord.py
  - discord.ui
  - os
  - radom
  - pyyaml
  - python-dotenv
  - fox_responses.py
  - sys
```python
import discord
from discord.ext import commands
from discord.ui import Button, View
import os
import random
import yaml
from dotenv import load_dotenv
from fox_responses import handle_greeting
import sys
```
### 游戲狀態
這個的部分呢 其實是 我閑的 我也不知道委托人要什麽 所以只好 寫 “喜歡主人的愛”
```python
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
```
我不知道 我做好玩的 欸嘿
---
