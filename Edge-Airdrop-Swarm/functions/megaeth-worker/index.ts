import { ethers } from "https://esm.sh/ethers@6.12.1";
import { SwarmWalletManager } from "../shared/wallets.ts";

/**
 * MegaETH Testnet Worker
 * RPC: https://carrot.megaeth.com/rpc
 * ChainID: 6343
 */

const RPC_URL = "https://carrot.megaeth.com/rpc";

export const runMegaETHTask = async (mnemonic: string, index: number) => {
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const manager = new SwarmWalletManager(mnemonic);
    const wallet = manager.getWallet(index, provider);

    console.log(`[MegaETH Worker ${index}] Active: ${wallet.address}`);

    try {
        const balance = await provider.getBalance(wallet.address);
        console.log(`[MegaETH Worker ${index}] Balance: ${ethers.formatEther(balance)} ETH`);

        if (balance < ethers.parseEther("0.001")) {
            console.log(`[MegaETH Worker ${index}] ⚠️ Low gas. Skip.`);
            return;
        }

        // Perform a small transaction to build activity
        const tx = await wallet.sendTransaction({
            to: wallet.address,
            value: ethers.parseEther("0.0001"),
            gasLimit: 21000
        });

        console.log(`[MegaETH Worker ${index}] ✅ Activity Tx Sent: ${tx.hash}`);
        await tx.wait();
        console.log(`[MegaETH Worker ${index}] 🏆 Transaction confirmed.`);

    } catch (error) {
        console.error(`[MegaETH Worker ${index}] ❌ Task Failed:`, error.message);
    }
};
