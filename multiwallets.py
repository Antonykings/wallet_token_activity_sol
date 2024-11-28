import requests
import csv

# Helius API
API_KEY = '45d55a0f-b3db-4dd8-a060-6e18269aee57'

def get_transaction_details(wallet_address):
    base_url = f"https://api.helius.xyz/v0/addresses/{wallet_address}/transactions?api-key={API_KEY}"
    last_signature = None
    all_transactions = []
    transfer_count = 0  

    # CSV file for the wallet
    csv_filename = f"{wallet_address}_Transactions.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Transaction Signature', 'Date', 'From', 'To', 'Buy/Sell', 'Swap/Transfer', 'Amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Header row

        while True:
            # pagination
            url = base_url
            if last_signature:
                url += f"&before={last_signature}"

            response = requests.get(url)
            if response.status_code == 200:
                transactions = response.json()

                # Break if no more transactions
                if not transactions:
                    print(f"No more transactions available for wallet: {wallet_address}.")
                    break

                # Count batch-specific TRANSFERS
                batch_transfer_count = 0

                # Process transactions
                for transaction in transactions:
                    # Check if the transaction type is TRANSFER
                    if transaction.get('type') == 'TRANSFER':
                        transfer_count += 1
                        batch_transfer_count += 1
                    

                # Update `last_signature` for pagination
                last_signature = transactions[-1]['signature']
                print(f"Fetched {len(transactions)} transactions for wallet: {wallet_address}.")
                print(f"Number of TRANSFER transactions in this batch: {batch_transfer_count}")
                all_transactions.extend(transactions)
            else:
                print(f"Error for wallet {wallet_address}: {response.status_code} - {response.text}")
                break

    print(f"Total transactions fetched for wallet {wallet_address}: {len(all_transactions)}")
    print(f"Total number of TRANSFER transactions: {transfer_count}")
    print(f"Transactions saved in {csv_filename}")

# multiple wallets
wallet_addresses = [
    "3MFPrGojrEU3PPaRDz2fvBYk8MVU52NXPaJnb1TAbzuU",
]

for wallet in wallet_addresses:
    print(f"Fetching transactions for wallet: {wallet}")
    get_transaction_details(wallet)
