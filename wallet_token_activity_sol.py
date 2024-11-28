import requests
import csv
import time
from datetime import datetime

# Helius API
API_KEY = '45d55a0f-b3db-4dd8-a060-6e18269aee57'

def get_transaction_details(wallet_address, token_mint):
    base_url = f"https://api.helius.xyz/v0/addresses/{wallet_address}/transactions?api-key={API_KEY}"
    last_signature = None

    # CSV file for the wallet
    csv_filename = f"{wallet_address}_Token_Transactions.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Transaction Signature', 'Date', 'From', 'To', 'Amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write header row

        while True:
            # Handle pagination
            url = base_url
            if last_signature:
                url += f"&before={last_signature}"

            try:
                response = requests.get(url)
                
                # Handle rate-limiting
                if response.status_code == 429:
                    print("Rate limit hit. Sleeping for 2 seconds before retrying...")
                    time.sleep(2)
                    continue  # Retry the same request

                if response.status_code == 200:
                    transactions = response.json()

                    # Break if no more transactions
                    if not transactions:
                        print(f"No more transactions available for wallet: {wallet_address}.")
                        break

                    # Process transactions
                    for transaction in transactions:
                        # Check if the transaction involves the specific token mint
                        if 'tokenTransfers' in transaction:
                            for transfer in transaction['tokenTransfers']:
                                if transfer.get('mint') == token_mint:
                                    # Extract details
                                    tx_signature = transaction.get('signature')
                                    timestamp = datetime.utcfromtimestamp(transaction.get('timestamp')).strftime('%Y-%m-%d %H:%M:%S')
                                    from_wallet = transfer.get('fromUserAccount')
                                    to_wallet = transfer.get('toUserAccount')
                                    Quantity = transfer.get('tokenAmount')

                                    # Filter: Only include transactions where wallet_address matches From or To
                                    if wallet_address == from_wallet or wallet_address == to_wallet:
                                        # Write to CSV
                                        writer.writerow({
                                            'Transaction Signature': tx_signature,
                                            'Date': timestamp,
                                            'From': from_wallet,
                                            'To': to_wallet,
                                            'Amount': Quantity
                                        })

                    # Update `last_signature` for pagination
                    last_signature = transactions[-1]['signature']
                    print(f"Fetched {len(transactions)} transactions for wallet: {wallet_address}.")
                    
                    # Throttle to respect API limits
                    time.sleep(0.15)  # 10 requests per second = 0.1s delay
                else:
                    print(f"Error for wallet {wallet_address}: {response.status_code} - {response.text}")
                    break
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                break

    print(f"Transactions involving token {token_mint} saved in {csv_filename}.")

# Wallet addresses and token mint to check
wallet_addresses = [
    "EoWofJZcE2oRm39fW8nmXZ1qiGomea8pi3kMxFFH9utT",
]
token_mint = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"  # Replace with the actual token mint address

for wallet in wallet_addresses:
    print(f"Fetching transactions for wallet: {wallet}")
    get_transaction_details(wallet, token_mint)
