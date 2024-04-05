import discord
from discord.ext import commands
import re
import random
import string

# 定义所需的 Intents
intents = discord.Intents.all()

# 创建客户端实例，并传递 Intents 参数
# bot = discord.Bot(command_prefix='/', intents=intents)
bot = discord.Bot(intents=intents)

# 当客户端准备好时调用
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# 当接收到消息时调用
@bot.event
async def on_message(message):
    # 防止 bot 自身触发事件
    if message.author == bot.user:
        return
    
    # 打印消息内容和作者的用户名
    print(f"Message Content: {message.content}")
    print(f"Author: {message.author.name}")

    # 处理命令
    # await bot.process_commands(message)

@bot.command()
async def add_identitygroup(ctx, group_id: str):
    """将新的身份组添加进 许可列表 中"""
    # print(ctx.guild.owner)
    if not is_supporter(ctx):
        # print(ctx)
        await ctx.respond("对不起，您没有权限执行该命令。", ephemeral=True)
        return
    # 使用正则表达式提取19位数字
    match = re.search(r'<@&(\d{19})>', group_id)
    if match:
        group_id = match.group(1)
        # 检查 ID 是否已经存在于 roles.db 文件中
        with open('roles.db', 'r') as file:
            if group_id in file.read():
                await ctx.respond("该身份组已进入许可列表", ephemeral=True)
            else:
                # 追加到 roles.db 文件中
                with open('roles.db', 'a') as file:
                    file.write(f"{group_id}\n")
                await ctx.respond(f"Identity Group ID {group_id} 已添加到 roles.db 文件中", ephemeral=True)
    else:
        await ctx.respond("无效的 Identity Group ID 格式", ephemeral=True)

# 身份组检查
def is_supporter(ctx):
    # 检查用户是否 允许执行
    print(discord.utils)
    print(ctx.author.roles)
    
    if ctx.guild.owner == ctx.author:
        return True

    # 检查用户是否在 许可列表 中
    with open('roles.db', 'r') as file:
        for line in file:
            # 移除行尾的换行符
            role_id = line.strip()
            # 检查用户是否具有该角色
            if discord.utils.get(ctx.author.roles, id=int(role_id)) is not None:
                return True
    return False

@bot.command()
async def delete_channel(ctx, regex: str):
    """删除名称匹配 regex 的频道"""
    sum=0
    # 打印消息内容和作者的用户名
    # print(f"Message Content: {ctx.message.content}")
    print(f"Author: {ctx.author.name}")
    print(f"参数：{regex}")
    if not is_supporter(ctx):
        # print(ctx)
        await ctx.respond("对不起，您没有权限执行该命令。", ephemeral=True)
        return
    await ctx.respond("正在删除频道...",ephemeral=True)
    # 遍历服务器中的所有文本频道
    for channel in ctx.guild.text_channels:
        # 如果频道名称匹配正则表达式
        if re.search(regex, channel.name):
            # 删除频道
            await channel.delete()
            sum+=1
            # await ctx.respond(f"频道 '{channel.name}' 已删除",ephemeral=True)
    if sum==0:
        await ctx.respond(f"未找到匹配的频道",ephemeral=True)
    else:
        await ctx.respond(f"共删除 {sum} 个频道",ephemeral=True)


# @bot.command()
# async def cc(ctx, num: int):
#     """创建 num 个频道，每个频道名称为 Closed- 后跟一个四位随机数"""
#     # 创建 num 个频道
#     for _ in range(num):
#         random_suffix = ''.join(random.choices(string.digits, k=4))
#         channel_name = f'Closed-{random_suffix}'
#         # 创建频道
#         await ctx.guild.create_text_channel(channel_name)
#         await ctx.respond(f"频道 '{channel_name}' 已创建",ephemeral=True)


with open("token.dbt","r") as main:
    token=main.read()
# print(token)
bot.run(token)