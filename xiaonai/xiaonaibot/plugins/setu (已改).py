"""
插件名称：权限组涩图自动撤回
作者：小咸鱼
时间：2020/8/21
如果bot是群员且群员发 ’/涩图‘ 就不发
如果bot是群员且群主或管理员发 ‘/涩图’ 就发
如果bot是管理员且群员发 ’/涩图‘ 就30s-10m的禁言再发
如果bot是管理员且管理员或群主发 ‘/涩图’ 就直接发
然后以上都是15s之后撤回
"""


import random
from nonebot import on_keyword
from nonebot.adapters.cqhttp import Message, GroupMessageEvent
from nonebot.typing import T_State
import requests
import re
import asyncio
from nonebot import on_command


"""涩图"""
ban = on_command('涩图')
list = ['admin', 'owner']
bad = ['member']


@ban.handle()
async def ramdom_ban(bot, event):
    uid = event.user_id
    gid = event.group_id
    times = random.randrange(30, 600, 30)#在30s-600s（10m）中随机抽取禁言时间
    owner = await bot.get_group_member_info(user_id=uid, group_id=gid)
    owner2 = await bot.get_group_member_info(user_id='……', group_id=gid)#“……“填你自己bot账号
    guanli = owner['role']
    bt = owner2['role']
    qunyuan = owner['role']
    if guanli in list:#如果bot是群员/管理员/群主且发送消息是管理/群主的话
        msg = '因为你是群主或管理，所以你可以看涩图'
        img = await setu()
        mes = await bot.send(event, Message(msg+img))
        await asyncio.sleep(15)#等15秒后撤回消息
        await bot.delete_msg(message_id=mes['message_id'])
    if bt in bad and qunyuan in bad:#如果bot是群员且发送消息是群员的话
        msg = '报错：我不是管理不能禁你，所以你没有涩图看'
        await bot.send(event, Message(msg))

    if bt in list and qunyuan in bad:#如果bot是管理员/群主且发送消息是群员的话
        q = int(times)
        scr = str(q)
        img = await setu()
        msg = f"你不就是要涩图嘛\n" \
              f"来 " + scr + "秒口球 请"
        await bot.set_group_ban(
            group_id=gid,
            user_id=uid,
            duration=times
        )
        mes = await bot.send(event, Message(msg + img))
        await asyncio.sleep(15)#等15秒后撤回消息
        await bot.delete_msg(message_id=mes['message_id'])
    else:
        pass


async def setu():
    url = "https://api.lolicon.app/setu/"
    da = requests.get(url).text
    ur = re.findall(r'url":"(.+?)"}]}', da)
    #setu=requests.get(ur).text
    st = ur[0]
    #st = requests.get(str).text
    tu= f'[CQ:image,file={st}]'
    return tu

bugouse = on_keyword({'不够涩', '不够色', '不色', '不涩'})


@bugouse.handle()
async def _(bot, event: GroupMessageEvent, state: T_State):
    msg = '这边建议您自己扮涩图嗷'
    await bugouse.finish(message=msg)


information = on_command("信息")#测试获取群员信息用的


@information.handle()
async def info(bot, event):
    group = event.group_id
    id = event.user_id
    info = await bot.get_group_member_info(user_id=id, group_id=group)
    msg = str(info)
    await bot.send(event, msg)
