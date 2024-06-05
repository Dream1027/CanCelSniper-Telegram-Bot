from telethon import TelegramClient, events, Button
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
import logging
import time
import sys
# Configure logging
logging.basicConfig(filename='script_errors.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()
phone_number = os.getenv('PHONE_NUMBER')  # Your phone number in international format
minutes = os.getenv('MINUTES')
seconds = 60 * int(minutes)
percent=os.getenv('PERCENT')

# Replace with your actual values
api_id = '29822273'
api_hash = 'a5f85b06b7f821005a4a2891be886848'
bot_username = 'BananaGunSniper_bot'
cancel_called = False
token_address = None  # Variable to store the token address

# Create the client and connect
client = TelegramClient('banana_gun', api_id, api_hash)

def changeMinutes(value):
    global seconds
    seconds=value
def changePercent(value):
    global percent
    percent=value

async def click_button(message, button_text):
    retries=3
    for _ in range(retries):
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
        print(f"{button_text} button not found, retrying...")        
    print(f"Failed to click {button_text} button after {retries} retries")
    return False

async def cancel():
    global cancel_called
    print('Entered in Cancel Function...')
    try:
        async with client.conversation(bot_username) as conv:
            print('Send Start Message...')
            await conv.send_message('/start')

            time.sleep(2)  # Wait for a short time before continuing

            response = await conv.get_response()
            print('Received response to /start command:', response.raw_text)
            if await click_button(response, 'My Pending Snipes'):
                time.sleep(2)  # Wait for a short time before continuing

                response = await conv.get_response()
                print('Received response to "My Pending Snipes":', response.raw_text)
                if await click_button(response, 'Cancel all snipes'):
                    time.sleep(2)  # Wait for a short time before continuing

                    response = await conv.get_response()
                    print('Received response to "Cancel all snipes":', response.raw_text)
                    retries = 3
                    for _ in range(retries):
                        if await click_button(response, 'Yes'):
                            print('Yes button clicked. Cancelling all snipes.')
                            return
                        response = await conv.get_response()
                        time.sleep(1)  # Wait a bit before retrying
                    print("Failed to find the Yes button after retries")
            else:
                print("Failed to find 'My Pending Snipes' button.")
    except Exception as e:
        logging.error(f"Error in cancel function: {e}")
    finally:
        cancel_called = False

async def setup_limit_order():
    global token_address
    try:
        async with client.conversation(bot_username) as conv:
            print('Send Start Message...')
            time.sleep(1)  # Wait a bit longer before sending /start
            await conv.send_message('/start')

            time.sleep(2)  # Wait for a short time before continuing

            response = await conv.get_response()
            
            if await click_button(response, 'Setup limit order'):
                time.sleep(2)  # Wait for a short time before continuing
                response = await conv.get_response()                
                if await click_button(response, 'Setup Unlaunched Sell Limit Order'):
                    time.sleep(2)  # Wait for a short time before continuing                    
                    response = await conv.get_response()
                    if response and 'Input Token address to Setup Sell Limit Order' in response.raw_text:
                        await conv.send_message(token_address, reply_to=response.id)
                        print('Token pasted.')

                        time.sleep(2)  # Wait for a short time before continuing

                        response1 = await conv.get_response()
                        response2 = await conv.get_response()
                        if await click_button(response2, 'Custom'):
                            time.sleep(2)  # Wait for a short time before continuing
                            print('📈Custom button clicked')
                            response=await conv.get_response()
                            await conv.send_message(percent, reply_to=response.id)
                            print('The percent is inputed.')
                            print('======Sell Order End========')
                        else:
                            print('Failed to find 📈Custom button.')
                        
                    else:
                        print('Did not receive the expected prompt for token address.')
                else:
                    print('Failed to find Setup Unlaunched Sell Limit Order button.')
            else:
                print('Failed to find Setup limit order button.')
    except Exception as e:
        print(f"Error in setup_limit_order function: {e}")
        logging.error(f"Error in setup_limit_order function: {e}")
    finally:
        # Ensure the script continues even if an error occurs
        
        await asyncio.sleep(seconds)
        await cancel()
        

@client.on(events.NewMessage(from_users=bot_username))
async def handler(event):
    global cancel_called, token_address,seconds,percent
    if "Scraped " in event.raw_text and "0x" in event.raw_text:
        
        print('Second: '+str(seconds)+ ', Percentage:'+percent)
        
        if not cancel_called:
            cancel_called = True
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Detected 'New Token' message at {timestamp}. Setting up limit order immediately.")
            
            # Extract the token from the message
            token_address = "0x" + event.raw_text.split("0x")[1].split()[0]
            print(f"Scraped token address: {token_address}")
            await setup_limit_order()  # Run the setup limit order function

async def main():
        global seconds,percent
        print('Second: '+str(seconds)+ ', Percentage:'+percent)     
        
        try:
            await client.start(phone=phone_number)
            print("Client Created and Started")
            
            await client.run_until_disconnected()
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred: {e}")
            time.sleep(5)  # Wait a bit before reconnecting
def stop():
    sys.exit()

# Run the script
def start():    
    print('starting...')
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except:        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())