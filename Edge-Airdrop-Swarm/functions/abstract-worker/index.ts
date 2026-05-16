import { ethers } from "https://esm.sh/ethers@6.12.1";
import { SwarmWalletManager } from "../shared/wallets.ts";

/**
 * Abstract Testnet Worker
 * RPC: https://api.testnet.abs.xyz
 * ChainID: 11124
 */

const RPC_URL = "https://api.testnet.abs.xyz";

export const runAbstractTask = async (mnemonic: string, index: number) => {
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const manager = new SwarmWalletManager(mnemonic);
    const wallet = manager.getWallet(index, provider);

    console.log(`[Abstract Worker ${index}] Active: ${wallet.address}`);

    try {
        const balance = await provider.getBalance(wallet.address);
        console.log(`[Abstract Worker ${index}] Balance: ${ethers.formatEther(balance)} ETH`);

        if (balance < ethers.parseEther("0.001")) {
            console.log(`[Abstract Worker ${index}] ⚠️ Low gas. Skip.`);
            return;
        }

        const tx = await wallet.sendTransaction({
            to: wallet.address,
            value: ethers.parseEther("0.0001"),
            gasLimit: 21000
        });

        console.log(`[Abstract Worker ${index}] ✅ Activity Tx Sent: ${tx.hash}`);
        await tx.wait();
        console.log(`[Abstract Worker ${index}] 🏆 Account Warmed Up.`);

    } catch (error) {
        console.error(`[Abstract Worker ${index}] ❌ Task Failed:`, error.message);
    }
};
