import { ethers } from "https://esm.sh/ethers@6.12.1";

/**
 * Industrial Wallet Manager
 * Derives unique wallets from a single master seed phrase.
 * This allows managing 1000+ accounts with just one password.
 */
export class SwarmWalletManager {
    private masterMnemonic: string;

    constructor(mnemonic: string) {
        this.masterMnemonic = mnemonic;
    }

    /**
     * Derives a specific wallet for a worker based on its index.
     * @param index The worker index (0-999)
     * @returns Ethers wallet instance
     */
    getWallet(index: number, provider?: any) {
        const path = `m/44'/60'/0'/0/${index}`;
        const wallet = ethers.Wallet.fromPhrase(this.masterMnemonic).derivePath(path);
        return provider ? wallet.connect(provider) : wallet;
    }

    /**
     * Utility to generate a new master seed phrase.
     */
    static generateNewMnemonic(): string {
        return ethers.Wallet.createRandom().mnemonic!.phrase;
    }
}
