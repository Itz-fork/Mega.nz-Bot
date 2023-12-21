# @Author: https://github.com/Itz-fork
# @Project: https://github.com/Itz-fork/Mega.nz-Bot
# @Version: nightly-0.2
# @Description: Contains pyrogram tools

from time import time
from math import floor


# Porogress bar for pyrogram
# Credits: SpEcHiDe's AnyDL-Bot
async def track_progress(current, total, client, ides, start):
    now = time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n**Process**: {2}%\n".format(
            "".join(["█" for i in range(floor(percentage / 5))]),
            "".join(["░" for i in range(20 - floor(percentage / 5))]),
            round(percentage, 2),
        )

        tmp = progress + "{0} of {1}\n**Speed:** {2}/s\n**ETA:** {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        try:
            await client.edit_message_text(ides[0], ides[1], f"{tmp}\n\n**Powered by @NexaBotsUpdates**")
        except:
            pass

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    pwrN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + pwrN[n] + "B"
