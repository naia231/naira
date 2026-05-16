import { ethers } from "https://esm.sh/ethers@6.12.1";
import { SwarmWalletManager } from "../shared/wallets.ts";

/**
 * INK Sepolia Daily Worker (Kraken L2)
 * Tasks: 
 * 1. Build transaction history on Ink Sepolia Testnet.
 * 2. Interact with the core Bridge/DEX contracts.
 * 3. Builds eligibility for the Real $INK airdrop (Q3 2026).
 */

const RPC_URL = "https://rpc-gel-sepolia.inkonchain.com";
const INK_CHID = 763373;

// Minimal ABI for interaction
const ERC20_ABI = ["function transfer(address to, uint amount) returns (bool)"];

export const runInkTask = async (mnemonic: string, index: number) => {
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const manager = new SwarmWalletManager(mnemonic);
    const wallet = manager.getWallet(index, provider);

    console.log(`[INK Worker ${index}] Active: ${wallet.address}`);

    try {
        const balance = await provider.getBalance(wallet.address);
        console.log(`[INK Worker ${index}] Balance: ${ethers.formatEther(balance)} ETH`);

        if (balance < ethers.parseEther("0.001")) {
            console.log(`[INK Worker ${index}] ⚠️ Insufficient gas. Skip.`);
            return;
        }

        // ─────────────────────────────────────────────────────
        // Task: Interaction (Self-Transfer / Protocol Poke)
        // ─────────────────────────────────────────────────────
        // On testnets, simply having unique "Active Days" is the #1 criteria.
        // We perform a small transaction to keep the wallet "Warm".
        
        const tx = await wallet.sendTransaction({
            to: wallet.address, // Self-transfer to build volume/tx count for free
            value: ethers.parseEther("0.0001"),
            gasLimit: 21000
        });

        console.log(`[INK Worker ${index}] ✅ Warm-up Tx Sent: ${tx.hash}`);
        await tx.wait();
        console.log(`[INK Worker ${index}] 🏆 Account Warmed Up for the Day.`);

    } catch (error) {
        console.error(`[INK Worker ${index}] ❌ Task Failed:`, error.message);
    }
};
