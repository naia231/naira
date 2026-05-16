import { ethers } from "https://esm.sh/ethers@6.12.1";
import { SwarmWalletManager } from "../shared/wallets.ts";

/**
 * Plume Network Testnet Worker
 * RPC: https://testnet-rpc.plume.org
 * ChainID: 98867
 */

const RPC_URL = "https://testnet-rpc.plume.org";

export const runPlumeTask = async (mnemonic: string, index: number) => {
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const manager = new SwarmWalletManager(mnemonic);
    const wallet = manager.getWallet(index, provider);

    console.log(`[Plume Worker ${index}] Active: ${wallet.address}`);

    try {
        const balance = await provider.getBalance(wallet.address);
        console.log(`[Plume Worker ${index}] Balance: ${ethers.formatEther(balance)} PLUME`);

        if (balance < ethers.parseEther("0.01")) {
            console.log(`[Plume Worker ${index}] ⚠️ Low gas. Skip.`);
            return;
        }

        const tx = await wallet.sendTransaction({
            to: wallet.address,
            value: ethers.parseEther("0.001"),
            gasLimit: 21000
        });

        console.log(`[Plume Worker ${index}] ✅ Activity Tx Sent: ${tx.hash}`);
        await tx.wait();
        console.log(`[Plume Worker ${index}] 🏆 Transaction confirmed.`);

    } catch (error) {
        console.error(`[Plume Worker ${index}] ❌ Task Failed:`, error.message);
    }
};
