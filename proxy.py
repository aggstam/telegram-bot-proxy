import sys
import requests
from telegram.client import Telegram

# Main function
def main():
    # Initialize proxy
    api_id = int(sys.argv[1])
    api_hash = sys.argv[2]    
    phone = sys.argv[3]
    db_pass = sys.argv[4]
    db_path = sys.argv[5]
    group_id = int(sys.argv[6])
    bots_group_id = int(sys.argv[7])
    tg = Telegram(
        api_id=api_id,
        api_hash=api_hash,
        phone=phone,
        database_encryption_key=db_pass,
        files_directory=db_path,
    )
    tg.login()

    # Define proxy handler
    def proxy_handler(update):
        # Check message comes from the actual groups
        if update['message']['chat_id'] == group_id:
            # Check if its the proxy command
            message_text = update['message']['content'].get('text', {}).get('text', '').lower()
            if message_text.startswith('/p'):
                send_message_result = tg.send_message(chat_id=bots_group_id, text=message_text[3:])
                send_message_result.wait()
                if send_message_result.error:
                    print(f'Failed to send the message: {send_message_result.error_info}')
            elif message_text.startswith('/hl'):
                response = handle_hl(message_text.split("/hl", 1)[1])
                send_message_result = tg.send_message(chat_id=group_id, text=response)
                send_message_result.wait()
                if send_message_result.error:
                    print(f'Failed to send the message: {send_message_result.error_info}')
        elif update['message']['chat_id'] == bots_group_id and not update['message']['is_outgoing']:
            data = {
                'chat_id': group_id,
                'from_chat_id': bots_group_id,
                'message_ids': [update['message']['id']],
                'send_copy': True,
            }
            call_method_result = tg.call_method(method_name='forwardMessages', params=data, block=True)
            call_method_result.wait()
            if call_method_result.error:
                print(f'Failed to forward the message: {call_method_result.error_info}')
    def handle_hl(command):
        if command == "vault":
            url = "https://api.hyperliquid.xyz/info"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "type": "clearinghouseState",
                "user": "0x05ce3c3d5f66906a04dc5111c8ceda49e74df43a"
            }
            response = requests.post(url, json=data, headers=headers)
            # Check if the request was successful
            if response.status_code == 200:
                return hl_vault_info(response)
            else:
                print(f"Request failed with status code: {response.status_code}")
                print(response.text)  # Print the response text for more information

    def hl_vault_info(data):
        account_value = float(data["marginSummary"]["accountValue"])
        total_margin_used = float(data["marginSummary"]["totalMarginUsed"])
        position = data["assetPositions"][0]["position"]

        message = f"🚀 Trading Account Update 🚀\n\n"
        message += f"💰 Account Value: ${account_value:,.2f}\n"
        message += f"💼 Total Margin Used: ${total_margin_used:,.2f}\n"
        message += f"Margin Usage: {total_margin_used/account_value:.2%}\n\n"

        message += "📊 Position Details:\n"
        message += f"Coin: {position['coin']}\n"
        message += f"Size: {float(position['szi']):,.0f} coins\n"
        message += f"Entry Price: ${float(position['entryPx']):,.6f}\n"
        message += f"Position Value: ${float(position['positionValue']):,.2f}\n"
        
        unrealized_pnl = float(position['unrealizedPnl'])
        message += f"Unrealized P&L: ${unrealized_pnl:,.2f}"
        if unrealized_pnl > 0:
            message += " 📈\n"
        else:
            message += " 📉\n"
        
        message += f"Liquidation Price: ${float(position['liquidationPx']):,.6f}\n"
        message += f"Max Leverage: {position['maxLeverage']}x\n\n"

        cumulative_funding = position['cumFunding']
        message += "💸 Cumulative Funding:\n"
        message += f"All Time: ${float(cumulative_funding['allTime']):,.2f}\n"
        message += f"Since Open: ${float(cumulative_funding['sinceOpen']):,.2f}\n"
    return message

# Use the function with your data
telegram_message = format_telegram_message(data)
print(telegram_message)
    # Append handler
    tg.add_message_handler(proxy_handler)

    # Wait for termination
    tg.idle()
    
    def handle_hl(command):
        

if __name__ == "__main__":
    main()
