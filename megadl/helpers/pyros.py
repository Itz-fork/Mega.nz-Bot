# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Tools and helper functions related to pyrogram

from time import time
from math import floor
from humans import human_time, human_bytes


# Porogress bar for pyrogram
# Improved version of SpEcHiDe's AnyDL-Bot
async def track_progress(
    current, total, client, chat_id: int, msg_id: int, start: float, **kwargs
):
    now = time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = human_time(elapsed_time)
        estimated_total_time = human_time(estimated_total_time)

        filled = floor(percentage / 5)
        progress = f"[{'█'*filled}{'░'*(20-filled)}]\n**Process**: {round(percentage,2)}%\n"

        pmsg = f"{progress}{human_bytes(current)} of {human_bytes(total)}\n**Speed:** {human_bytes(speed)}/s\n**ETA:** {estimated_total_time if estimated_total_time != '' else '0 s'}\n\n\n**Powered by @NexaBotsUpdates**"
        try:
            await client.edit_message_text(chat_id, msg_id, pmsg, **kwargs)
        except:
            pass
