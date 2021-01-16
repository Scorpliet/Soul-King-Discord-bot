async def lastMessage(ctx, users_id: int):
    oldestMessage = None
    fetchMessage = await ctx.channel.history().find(lambda m: m.author.id == users_id)

    if oldestMessage is None:
        oldestMessage = fetchMessage
    else:
        if fetchMessage.created_at > oldestMessage.created_at:
            oldestMessage = fetchMessage

    if (oldestMessage is not None):
        return oldestMessage.content