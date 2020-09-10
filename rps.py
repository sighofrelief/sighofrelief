    @commands.command(aliases=["rps"])
    async def rockpaperscissors(self, ctx):
        """Play a game of Rock Paper Scissors against an opponent or against Cookie Dough."""
        if len(ctx.message.mentions) is not 1 or ctx.message.mentions[0].mention == ctx.author.mention:
            await ctx.send('Please @mention someone other than yourself that you\'d like to play with! \
(Only one opponent at a time please)')
            return
        else:
            player1 = ctx.author
            player2 = ctx.message.mentions[0]
            challenge = await ctx.send(f'{player2.mention} would you like to play {player1.mention} in a game of rock \
paper scissors?')
            await challenge.add_reaction('👍')
            await challenge.add_reaction('👎')

            def invitecheck(reaction, user):
                return reaction.message.id == challenge.id and user == player2 and str(reaction.emoji) == '👍' or \
                       reaction.message.id == challenge.id and user == player2 and str(reaction.emoji) == '👎'

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=invitecheck)
            except asyncio.TimeoutError:
                await ctx.channel.send(f'Oop, I didn\'t get a response from {player2.name}.')
                return
            if reaction.emoji == '👎':
                await ctx.channel.send(f'{player2.mention} has declined to battle with you {player1.mention}')
            elif reaction.emoji == '👍':
                async def send_check(player, opponent):
                    message = await player.send(f'Would you like to use <:rock:753111611740258305>, \
<:paper:753111606090661949>, or ✂️ against {opponent.mention}?')

                    await asyncio.wait_for(message.add_reaction('<:rock:753111611740258305>'), timeout=5)
                    await asyncio.wait_for(message.add_reaction('<:paper:753111606090661949>'), timeout=5)
                    await asyncio.wait_for(message.add_reaction('✂️'), timeout=5)
                    return message

                # Send out the checks to DMs and notify players with the link to them
                p1game, p2game = asyncio.gather(send_check(player1, player2), send_check(player2, player1))
                await ctx.channel.send(f'Here\'s some quick links to my DM so you can make your choices! \n\
    {player1.mention}: {p1game.jump_url} \n {player2.mention}: {p2game.jump_url}')

                async def battlecheck(player, message):
                    async def wait_func(reaction, user):
                        return reaction.message.id == message.id and user == player and str(
                            reaction.emoji) == '<:rock:753111611740258305>' or \
                               reaction.message.id == message.id and user == player and str(
                            reaction.emoji) == '<:paper:753111606090661949>' or \
                               reaction.message.id == message.id and user == player and str(reaction.emoji) == '✂️'

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=wait_func)
                    except asyncio.TimeoutError:
                        await ctx.channel.send(f'Oops, I didn\'t get a response from {player.name}. Try Again!')
                        return None
                    emoji = None
                    if reaction.emoji.name.lower() == 'rock':
                        emoji = '<:rock:753111611740258305>'
                    elif reaction.emoji.name.lower() == 'paper':
                        emoji = '<:paper:753111606090661949>'
                    elif reaction.emoji == '✂️':
                        emoji = '✂️'
                    # Should not be none because of wait_func conditions
                    await ctx.channel.send(f'{player.name} responded {emoji}')
                    return emoji

                # Wait for responses (or non-responses)
                p1response, p2response = asyncio.gather(battlecheck(player1, p1game), battlecheck(player2, p2game))

                # Do stuff with the responses here
