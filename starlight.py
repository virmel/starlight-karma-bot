import discord
import json

DISCORD_API_KEY = "NzE2ODM0NzYxNDE4NzM1NjM4.XtRiZQ.PMndOv3JYJjs1BaBYPjugIZpLSk"
GLITTER_BOYS_CHAT_ID = 993226709107220601
MUSIC_BOT_ID = 239631525350604801

# TODO:
# Have DISCORD_API_KEY and GLITTER as env_variables and hide it from the public when pushing it to Github
# rename variables
# hook this up to Heroku
# Refactor code - the section where karma is modified.

client = discord.Client()


@client.event
async def on_ready():
    print(f"We're in.. [{client.user}]")


@client.event
async def on_message(message):
    if(message.author.id == MUSIC_BOT_ID):
        return
    print(message.content)

    channel = client.get_channel(GLITTER_BOYS_CHAT_ID)

    if message.author == client.user:       # Bot ignores own messages
        return
    string_test = message.content
    if string_test[0] == '<':
        positive_karma = "++++" in message.content
        negative_karma = "----" in message.content

        if positive_karma and negative_karma:
            positive_karma, negative_karma = False
            return

        # e.g. 12343432596309 [int]
        mentioned_user_id = message.mentions[0].id
        # Handling user who gives themselves karma
        if(message.author.id == mentioned_user_id):
            read_karma_file = open("karma.txt", "r")
            karma_object = json.load(read_karma_file)
            read_karma_file.close()
            prev_karma = karma_object.get(f"{mentioned_user_id}", 0)
            karma_object[f"{mentioned_user_id}"] = prev_karma - 1
            write_karma_file = open("karma.txt", "w")
            json.dump(karma_object, write_karma_file)
            write_karma_file.close()

            await channel.send(f'<@{mentioned_user_id}> tried giving themselves karma. SMH my head. -1 karma')
        else:
            read_karma_file = open("karma.txt", "r")
            karma_object = json.load(read_karma_file)
            read_karma_file.close()

            prev_karma = karma_object.get(f"{mentioned_user_id}", 0)
            positive_karma_action_executed = False
            negative_karma_action_executed = False

            if positive_karma:
                karma_object[f"{mentioned_user_id}"] = prev_karma + 1
                positive_karma_action_executed = True
            elif negative_karma:
                karma_object[f"{mentioned_user_id}"] = prev_karma - 1
                negative_karma_action_executed = True

            current_karma = karma_object[f"{mentioned_user_id}"]
            write_karma_file = open("karma.txt", "w")
            json.dump(karma_object, write_karma_file)
            write_karma_file.close()

            if positive_karma_action_executed or negative_karma_action_executed:
                await announce_karma(mentioned_user_id, current_karma, positive_karma_action_executed)


async def announce_karma(mentioned_user_id, current_karma, positive_or_negative_karma):
    channel = client.get_channel(GLITTER_BOYS_CHAT_ID)
    positive_or_negative = positive_or_negative_karma
    await channel.send(
        f'<@{mentioned_user_id}> received karma! Total karma: {current_karma}') if positive_or_negative else await channel.send(f'<@{mentioned_user_id}> lost karma.. :pepehands:  Total karma: {current_karma}')


client.run(DISCORD_API_KEY)
