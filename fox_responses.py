# fox_responses.py

import discord
import random

# 使用者好感度語氣描述
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

# 各等級的問候與回應選項
responses = {
    "morning": {
        (1, 20): ["啊 你好啊", "你好", "是你啊 早上好啊", "好 你好", "早上好"],
        (21, 40): ["喲 {user} 早上好呀", "早餐做好了 在哪裏", "呀 你起了", "早安 你的東西我幫你洗了", "吃完早餐 想去哪玩嗎？"],
        (41, 60): ["早安呀 {user}寶貝"]
    },
    "noon": {
        (1, 20): ["好", "中午好", "啊 怎麽了嗎？", "嗚 幹嘛", "打擾本狐仙的午休 你罪該萬死"],
        (21, 40): ["呀 中午果然是午休的好時間呢", "阿勒 你不午睡嗎", "中午了啊 想吃什麽嗎 我去買給你", "啊呀 時間過得真快呀 都中午了呢 {user}想吃什麽嗎 我去做", "嗯 晚飯吃什麽好呢"],
        (41, 60): ["中午了呢 想不想要和{bot}~~一起做一些大人的事情嗎~~"]
    },
    "evening": {
        (1, 20): ["Zzz", "睡了 晚安", "去去去 你睡了也沒人會知道", "好", "..."],
        (21, 40): ["唷 起來嗨喲", "阿 你要去睡覺了嗎 就不能和我一起玩嗎", "那就 晚安了 好麻吉"],
        (41, 60): ["(在你的房間呆呆地看著你)"]
    },
    "hungry": {
        (1, 20): ["那就去找東西吃啊", "你還在想什麽 等我做給你吃嗎", "蛤 你認爲我會幫你製作料理嗎 想太多了你", "你還是去 垃圾堆哪裏和狗狗搶食物吃好了你"],
        (21, 40): ["嗯 不然我請你吃東西", "想吃什麽 你請客 hehe開玩笑的啦 我請你吃飯"],
        (41, 60): ["肚子餓了嗎 呵呵 真是不爭氣的肚子呢 你想要吃我呢還是吃飯飯呢~"]
    }
}

# 根據用戶好感度和訊息內容回覆
async def handle_greeting(message, content_lower, user_data, bot_name="小狐狸"):
    level = user_data["level"]
    user_name = message.author.mention

    if "早上好" in content_lower:
        response_type = "morning"
    elif "中午好" in content_lower:
        response_type = "noon"
    elif "晚上好" in content_lower:
        response_type = "evening"
    elif "肚子餓了" in content_lower:
        response_type = "hungry"
    else:
        return  # 若無符合的關鍵詞則不回覆

    # 選擇符合等級範圍的回應
    for range_tuple, possible_responses in responses[response_type].items():
        if range_tuple[0] <= level <= range_tuple[1]:
            response = random.choice(possible_responses)
            response = response.format(user=user_name, bot=bot_name)
            await message.channel.send(response)
            break
