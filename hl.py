# --------------------------------------------------------------------------
#
# Handler functions to use Hyperliquid(https://hyperliquid.xyz/) API.
#
# Author: Aggelos Stamatiou, July 2022
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

from hyperliquid.info import Info
from hyperliquid.utils import constants

# Execute an info request toward HL for provided address and return the retrieved info.
# Retrieved information is formatted into a human readable message.
def hl_vault_info(address=str):
    # Define and execute the request
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    data = info.user_state(address)

    # Format retrieved data
    account_value = float(data['marginSummary']['accountValue'])
    total_margin_used = float(data['marginSummary']['totalMarginUsed'])
    position = data['assetPositions'][0]['position']

    message = f'🚀 Trading Account Update 🚀\n\n'
    message += f'💰 Account Value: ${account_value:,.2f}\n'
    message += f'💼 Total Margin Used: ${total_margin_used:,.2f}\n'
    message += f'Margin Usage: {total_margin_used/account_value:.2%}\n\n'

    message += '📊 Position Details:\n'
    message += f'Coin: {position['coin']}\n'
    message += f'Size: {float(position['szi']):,.0f} coins\n'
    message += f'Entry Price: ${float(position['entryPx']):,.6f}\n'
    message += f'Position Value: ${float(position['positionValue']):,.2f}\n'

    unrealized_pnl = float(position['unrealizedPnl'])
    message += f'Unrealized P&L: ${unrealized_pnl:,.2f}'
    if unrealized_pnl > 0:
        message += ' 📈\n'
    else:
        message += ' 📉\n'

    message += f'Liquidation Price: ${float(position['liquidationPx']):,.6f}\n'
    message += f'Max Leverage: {position['maxLeverage']}x\n\n'

    cumulative_funding = position['cumFunding']
    message += '💸 Cumulative Funding:\n'
    message += f'All Time: ${float(cumulative_funding['allTime']):,.2f}\n'
    message += f'Since Open: ${float(cumulative_funding['sinceOpen']):,.2f}'
    return message

# Parse provided string into an HL command and its parts, then execute it and return its output.
def hl_handle_command(command: str, default_address: str):
    # Vault info command
    if command.startswith('vault'):
        # Use default address if none was provided
        if len(command.strip()) == 5:
            return hl_vault_info(default_address)
        
        return hl_vault_info(command[6:].strip())
    
    # We can add rest commands handling here
    
    raise Exception('Unknown Hyperliquid command provided')
