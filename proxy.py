# --------------------------------------------------------------------------
#
# Self hosting proxy for sending prompts and grabbing responses from telegram bots.
#
# Author: Aggelos Stamatiou, May 2024
#
# This source code is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this source code. If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------

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

    # Append handler
    tg.add_message_handler(proxy_handler)

    # Wait for termination
    tg.idle()

if __name__ == '__main__':
    main()
