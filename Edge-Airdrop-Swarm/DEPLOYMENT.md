# The China Way: Airdrop Swarm Deployment Guide (v1.0)

This project allows you to manage 200+ unique identities across multiple Supabase accounts to farm massive crypto airdrops.

## 1. Setup Your Master Seed
You only need **one** seed phrase for all 200 wallets.
1. Generate a new 12-word mnemonic (Seed Phrase).
2. **SAVE IT SECURELY.** If you lose this, you lose all 200 wallets.

## 2. Deploy to Supabase
You can have 10 accounts with 20 workers each.
1. In Supabase, create a new Project.
2. Go to **Edge Functions** and deploy the `main.ts` script.
3. Set these **Secrets** (Environment Variables) for each function:
   - `SWARM_MNEMONIC`: Your 12-word seed phrase.
   - `WORKER_INDEX`: The number for this specific worker (0, 1, 2, ... 199).
   - `PROJECT_NAME`: `BERACHAIN`

## 3. Funding the Swarm (The "Manual" Part)
Since faucet captchas are hard for bots, follow this strategy:
1. Every Sunday, claim $BERA tokens from the [Berachain Faucet](https://artio.faucet.berachain.com/) to your **Main Wallet**.
2. Run the `fund_swarm.py` script (below) from your laptop. It will take the $BERA from your main wallet and distribute small amounts (0.1 BERA) to all 200 of your swarm wallets.
3. Once funded, the Supabase workers will automatically perform daily trades for you.

## 4. Scheduling (Cron)
In Supabase, you can trigger your Edge Functions using a **Cron Job**. 
- Set it to run **once every 24 hours**.
- Each worker will wake up at a random time (thanks to the "Jitter" logic) and perform its tasks.

---

## 5. Wallet Funding Script (`fund_swarm.py`)
Run this locally on your PC to distribute test tokens.

```python
from web3 import Web3
from eth_account import Account

# CONFIG
RPC_URL = "https://artio.rpc.berachain.com/"
PRIVATE_KEY = "YOUR_MAIN_WALLET_PRIVATE_KEY"
MNEMONIC = "YOUR_200_WALLET_SEED_PHRASE"
COUNT = 200

w3 = Web3(Web3.HTTPProvider(RPC_URL))
main_acc = Account.from_key(PRIVATE_KEY)
Account.enable_unaudited_hdwallet_features()

for i in range(COUNT):
    # Derive swarm wallet address
    swarm_acc = Account.from_mnemonic(MNEMONIC, account_path=f"m/44'/60'/0'/0/{i}")
    
    print(f"[*] Funding Worker {i}: {swarm_acc.address}")
    
    # Send 0.1 BERA
    tx = {
        'to': swarm_acc.address,
        'value': w3.to_wei(0.1, 'ether'),
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(main_acc.address),
        'chainId': 80085
    }
    
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"    ✅ Done: {tx_hash.hex()}")
```
