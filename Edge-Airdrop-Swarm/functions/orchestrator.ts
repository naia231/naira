import { runInkTask } from "./ink-worker/index.ts";
import { runBerachainTask } from "./berachain-worker/index.ts"; 
import { runMegaETHTask } from "./megaeth-worker/index.ts";
import { runMovementTask } from "./movement-worker/index.ts";
import { runPlumeTask } from "./plume-worker/index.ts";
import { runAbstractTask } from "./abstract-worker/index.ts";

/**
 * Industrial Swarm Multi-Target Orchestrator
 * Cycles through 10+ airdrop targets per worker.
 */

export const executeSwarmCycle = async (mnemonic: string, index: number) => {
    console.log(`[Swarm] Starting full cycle for Worker ${index}...`);
    
    // ─────────────────────────────────────────────────────
    // PROJECT 1: INK (Kraken L2)
    // ─────────────────────────────────────────────────────
    try { await runInkTask(mnemonic, index); } catch (e) {}

    // ─────────────────────────────────────────────────────
    // PROJECT 2: MegaETH (High-Performance L2)
    // ─────────────────────────────────────────────────────
    try { await runMegaETHTask(mnemonic, index); } catch (e) {}

    // ─────────────────────────────────────────────────────
    // PROJECT 3: Movement (Move VM Testnet)
    // ─────────────────────────────────────────────────────
    try { await runMovementTask(mnemonic, index); } catch (e) {}

    // ─────────────────────────────────────────────────────
    // PROJECT 4: Plume (RWA Testnet)
    // ─────────────────────────────────────────────────────
    try { await runPlumeTask(mnemonic, index); } catch (e) {}

    // ─────────────────────────────────────────────────────
    // PROJECT 5: Abstract (Consumer L2)
    // ─────────────────────────────────────────────────────
    try { await runAbstractTask(mnemonic, index); } catch (e) {}

    // ... More modules will be added here

    console.log(`[Swarm] Cycle complete for Worker ${index}.`);
};
