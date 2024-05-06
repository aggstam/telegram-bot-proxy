import sys
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
    def proxy(update):
        # Check message comes from the actual group
        if update['message']['chat_id'] == group_id:
            # Check if its the proxy command
            message_text = update['message']['content'].get('text', {}).get('text', '').lower()
            if message_text.startswith('/p'):
                tg.send_message(chat_id=bots_group_id, text=message_text[3:])

    # Define response handler
    def response_handler(update):
        # Check message comes from the bots group
        if update['message']['chat_id'] == bots_group_id and not update['message']['is_outgoing']:
            data = {
                'chat_id': group_id,
                'from_chat_id': bots_group_id,
                'message_ids': [update['message']['id']],
                'send_copy': True,
            }
            tg.call_method(method_name='forwardMessages', params=data, block=True)

    # Append handlers
    tg.add_message_handler(proxy)
    tg.add_message_handler(response_handler)

    # Wait for termination
    tg.idle()

if __name__ == "__main__":
    main()
