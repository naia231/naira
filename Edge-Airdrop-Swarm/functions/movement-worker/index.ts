import { ethers } from "https://esm.sh/ethers@6.12.1";
import { SwarmWalletManager } from "../shared/wallets.ts";

/**
 * Movement Testnet Worker (Bardock)
 * RPC: https://testnet.movementnetwork.xyz/v1
 * ChainID: 250
 */

const RPC_URL = "https://testnet.movementnetwork.xyz/v1";

export const runMovementTask = async (mnemonic: string, index: number) => {
    // Movement uses a custom Move VM, but has an EVM compatibility layer.
    // We use the EVM RPC for simplicity in the swarm.
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const manager = new SwarmWalletManager(mnemonic);
    const wallet = manager.getWallet(index, provider);

    console.log(`[Movement Worker ${index}] Active: ${wallet.address}`);

    try {
        const balance = await provider.getBalance(wallet.address);
        console.log(`[Movement Worker ${index}] Balance: ${ethers.formatEther(balance)} MOVE`);

        if (balance < ethers.parseEther("0.1")) {
            console.log(`[Movement Worker ${index}] ⚠️ Low balance. Skip.`);
            return;
        }

        const tx = await wallet.sendTransaction({
            to: wallet.address,
            value: ethers.parseEther("0.01"),
            gasLimit: 21000
        });

        console.log(`[Movement Worker ${index}] ✅ Tx Sent: ${tx.hash}`);
        await tx.wait();
        console.log(`[Movement Worker ${index}] 🏆 Account Warmed.`);

    } catch (error) {
        console.error(`[Movement Worker ${index}] ❌ Task Failed:`, error.message);
    }
};
