# bot.py
import requests
import asyncio
import discord

from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

token = ""
my_user_id = ""

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.wait_until_ready()
    print(f'We have logged in as {client.user}')
    # maine_response = requests.get("https://ttp.cbp.dhs.gov/schedulerapi/slot-availability?locationId=5500", headers={'content-type': 'application/json'})
    response = requests.get("https://ttp.cbp.dhs.gov/schedulerapi/slot-availability?locationId=5020", headers={'content-type': 'application/json'})
    print(f"Blaine Available Appointments: {response.json()}")
    available_slots = response.json()["availableSlots"]
    if available_slots:
        all_formatted_available_slots = []
        for slot in available_slots:
            available_slot_timestamp = slot["startTimestamp"]
            date_obj = datetime.strptime(available_slot_timestamp, "%Y-%m-%dT%H:%M")
            good_date_string = datetime.strftime(date_obj, "%B %d %Y at %I:%M %p")
            all_formatted_available_slots.append(good_date_string)
        channel = client.get_channel(885766153723592704)
        format_to_string = ", ".join(all_formatted_available_slots)
        await channel.send(f"{my_user_id} APPOINTMENTS AVAILABLE:\n{format_to_string}") 
    await asyncio.sleep(3600)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$get_status'):
        response = requests.get("https://ttp.cbp.dhs.gov/schedulerapi/slot-availability?locationId=5020", headers={'content-type': 'application/json'})
        available_slots = response.json()["availableSlots"]
        if available_slots:
            all_formatted_available_slots = []
            for slot in available_slots:
                available_slot_timestamp = slot["startTimestamp"]
                date_obj = datetime.strptime(available_slot_timestamp, "%Y-%m-%d")
                good_date_string = datetime.strftime(date_obj, "%B %d %Y at %I:%M %p")
                all_formatted_available_slots.append(good_date_string)
            channel = client.get_channel(885766153723592704)
            format_to_string = ", ".join(all_formatted_available_slots)
            final_format = f"{message.author.mention} APPOINTMENTS AVAILABLE:\n{format_to_string}"
        else:
            last_date = response.json()["lastPublishedDate"].split("T")[0]
            date_obj = datetime.strptime(last_date, "%Y-%m-%d")
            good_date_string = datetime.strftime(date_obj, "%B %d %Y")
            final_format = f"{message.author.mention} No available appointments in Blaine, Washington.\nBlaine is booked until {good_date_string}\ndebug:{response.json()}"
        await message.channel.send(final_format)

client.run(token)