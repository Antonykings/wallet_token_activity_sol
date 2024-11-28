#Helius Supports only 100 Txn per request
import requests
import csv

# Helius API
API_KEY = '45d55a0f-b3db-4dd8-a060-6e18269aee57'
WALLET_ADDRESS = "3MFPrGojrEU3PPaRDz2fvBYk8MVU52NXPaJnb1TAbzuU"

def get_transaction_details(WALLET_ADDRESS):
    base_url = f"https://api.helius.xyz/v0/addresses/{WALLET_ADDRESS}/transactions?api-key={API_KEY}"
    last_signature = None
    all_transactions = []

    # CSV
    with open('Transactions.csv', 'w', newline='') as csvfile:
        fieldnames = ['Transaction Signature', 'Date', 'From', 'To', 'Buy/Sell', 'Swap/Transfer', 'Amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Header row

        while True:
            # Add pagination parameter if applicable
            url = base_url
            if last_signature:
                url += f"&before={last_signature}"

            response = requests.get(url)
            if response.status_code == 200:
                transactions = response.json()

                # Break if no more transactions
                if not transactions:
                    print("No more transactions available.")
                    break
                
                # Update `last_signature` for pagination
                last_signature = transactions[-1]['signature']
                print(f"Fetched {len(transactions)} transactions.")
                all_transactions.extend(transactions)
            else:
                print(f"Error: {response.status_code} - {response.text}")
                break

    print(f"Total transactions fetched: {len(all_transactions)}")

# Fetch and save transactions
get_transaction_details(WALLET_ADDRESS)
