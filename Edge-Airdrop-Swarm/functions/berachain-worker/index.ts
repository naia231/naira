import { ethers } from "https://esm.sh/ethers@6.12.1";
import { SwarmWalletManager } from "../shared/wallets.ts";

/**
 * Berachain Artio Daily Worker
 * Tasks: 
 * 1. Check BERA balance.
 * 2. Swap BERA -> HONEY (using BEX).
 * 3. Wrap/Unwrap some HONEY to build tx history.
 */

const RPC_URL = "https://artio.rpc.berachain.com/";
const BEX_ROUTER = "0xAB827b1Cc3535A9e549EE387A6E9C3F02B481B77"; // Artio BEX Router
const HONEY_ADDR = "0x7Ee88148b38617C77C615005834b7cc491A670EE";

// Minimal ABI for BEX Swap
const BEX_ABI = [
    "function swapExactTokensForTokens(uint amountIn, uint amountOutMin, address[] path, address to, uint deadline) returns (uint[] amounts)"
];

export const runBerachainTask = async (mnemonic: string, index: number) => {
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const manager = new SwarmWalletManager(mnemonic);
    const wallet = manager.getWallet(index, provider);

    console.log(`[Worker ${index}] Active: ${wallet.address}`);

    try {
        const balance = await provider.getBalance(wallet.address);
        console.log(`[Worker ${index}] Balance: ${ethers.formatEther(balance)} BERA`);

        if (balance < ethers.parseEther("0.01")) {
            console.log(`[Worker ${index}] ⚠️ Low balance. Needs funding.`);
            return;
        }

        // ─────────────────────────────────────────────────────
        // Task: Swap BERA to HONEY
        // ─────────────────────────────────────────────────────
        const amountToSwap = ethers.parseEther("0.005"); // Swap tiny amount to build history
        const deadline = Math.floor(Date.now() / 1000) + 600;
        
        // Path: [WBERA, HONEY] - Note: BEX uses WBERA internally
        const path = ["0x7507c1dc16935B8969142181f28642192A8D9344", HONEY_ADDR]; 

        const contract = new ethers.Contract(BEX_ROUTER, BEX_ABI, wallet);
        
        console.log(`[Worker ${index}] Swapping BERA for HONEY...`);
        const tx = await contract.swapExactTokensForTokens(
            amountToSwap,
            0, // Accept any slippage for testnet
            path,
            wallet.address,
            deadline,
            { value: amountToSwap } // Sending native BERA
        );

        console.log(`[Worker ${index}] ✅ Tx Sent: ${tx.hash}`);
        await tx.wait();
        console.log(`[Worker ${index}] 🏆 Swap Confirmed.`);

    } catch (error) {
        console.error(`[Worker ${index}] ❌ Task Failed:`, error.message);
    }
};
