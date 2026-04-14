from telethon import TelegramClient, events, Button
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
phone_number =os.getenv('PHONE_NUMBER')  # Your phone number in international format
minutes=os.getenv('MINUTES')
seconds=60*int(minutes)

# Replace with your actual values
api_id = 'api_id'
api_hash = 'api_hash'
bot_username = 'BananaGunSniper_bot'
cancel_called = False
# Create the client and connect
client = TelegramClient('banana_gun_session', api_id, api_hash)

async def click_button(message, button_text):
    for row in message.buttons:
        for button in row:
            if button_text.lower() in button.text.lower():
                await client(GetBotCallbackAnswerRequest(
                    peer=message.peer_id,
                    msg_id=message.id,
                    data=button.data
                ))
                print(f"{button_text} button clicked")
                return True
    return False

async def cancel():
    global cancel_called
    print('Entered in Cancel Function...')          
    # Wait for the "My Pending Snipes" button and click it
    async with client.conversation(bot_username) as conv:
        print('Send Start Message...') 
        # Send the /start command
        await conv.send_message('/start')

        # Wait for the first response
        response = await conv.get_response()
        await click_button(response, 'My Pending Snipes')

        # Wait for the next response
        response = await conv.get_response()
        await click_button(response, 'Cancel all snipes')

        # Wait for the next response and retry clicking "Yes" button
        retries = 3
        for _ in range(retries):
            response = await conv.get_response()
            if await click_button(response, 'Yes'):
                await client.disconnect()
                return
            await asyncio.sleep(1)  # Wait a bit before retrying
        print("Failed to find the Yes button after retries")
    cancel_called = False 
@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):  
    global cancel_called  
    if "Scraped " in event.raw_text and "0x" in event.raw_text:
        if not cancel_called:
            cancel_called = True
            print("Detected 'New Token' message. Waiting for 3 minutes...")
            await asyncio.sleep(seconds)  # Wait for 3 minutes (180 seconds)        
            print('=================')
            await cancel()  # Run the cancel function

async def main():
    await client.start(phone=phone_number)
    print("Client Created and Started")
    await client.run_until_disconnected()

# Run the script
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
