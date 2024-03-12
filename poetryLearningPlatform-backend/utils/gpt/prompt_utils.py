import os
import numpy as np
import json


def get_prompt(example=None):
    messages = [{"role": "system", "content": f"""I want you to play the role of a poetry appreciator.
     You will describe the poems I give that can evoke emotions and have the power to touch people's hearts. 
     Please use richer and more straightforward language to depict the imagery in the poem and the emotions the poet wants to express, 
     but make sure your words convey the feelings you are trying to express in a beautiful and meaningful way. 
     You can also come up with some short examples that can leave an impression on the reader's mind. 
     Now please answer in Chinese according to the poems I give"""}]
    return messages


def get_prompt_zn(example=None):
    messages = f"""我要你帮我进行诗词赏析,你需要感受诗中笔下的细腻之美，领略作者的情感深处的尘埃.
    其次需要观察诗中的语言运用体会诗中的中心思想,把握诗歌中所表达的精神境界，领略诗词情思律动联系之美.下面请你根据我给出的诗歌进行回答"""
    return messages


# --- 似乎被用作不同指令之间的分隔符，而===则被用来标识指令的结束

def get_fewshot_sample():
    samples = [{"context": "List of objects: [wine, bowl, remote control, TV, table, desk, chair]",
                "response": f"""Generate the instruction: Give me a drink
---
Necessary actions:
Step 1. Grasp a bottle of wine (Target: wine)
Step 2. Grasp a glass (Target: bowl)
Step 3. Place the cup on the table (Target: glass, table)
Step 4. Pour the wine into the glass (Target: wine, glass)
Step 5. Grasp the glass with wine (Target: glass)
Step 6. Move to the person and hand over it
Step 7. Done
===
Generate the instruction: Please turn on the TV
---
Necessary actions:
Step 1. Grasp the remote control (Target: remote control)
Step 2. Move closer to the TV (Target: TV)
Step 3. Rotate the remote control to point at the TV (Target: remote control, TV)
Step 4. Press the power button to turn on the remote control (Target: remote control)
Step 5. Done
==="""}]
    return samples
