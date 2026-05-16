import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { executeSwarmCycle } from "./orchestrator.ts";

/**
 * Supabase Edge Function: Swarm Orchestrator
 * This is the entry point for your 200+ workers.
 */

serve(async (req) => {
    // 1. Get configuration from Environment Variables
    const MNEMONIC = Deno.env.get("SWARM_MNEMONIC");
    const WORKER_INDEX = parseInt(Deno.env.get("WORKER_INDEX") || "0");
    const PROJECT_NAME = Deno.env.get("PROJECT_NAME") || "BERACHAIN";

    if (!MNEMONIC) {
        return new Response(JSON.stringify({ error: "Missing SWARM_MNEMONIC" }), { status: 400 });
    }

    console.log(`🚀 Swarm Worker starting: Project=${PROJECT_NAME}, Index=${WORKER_INDEX}`);

    // 2. Random Jitter (Humanization)
    // Delay execution by 0-10 minutes so 200 accounts don't hit the chain at the same second.
    const jitterMs = Math.floor(Math.random() * 600000); 
    console.log(`[Jitter] Waiting ${Math.floor(jitterMs/1000)}s to simulate human behavior...`);
    await new Promise(resolve => setTimeout(resolve, jitterMs));

    // 3. Execute Project Tasks (Full Multi-Target Cycle)
    try {
        await executeSwarmCycle(MNEMONIC, WORKER_INDEX);
        // Add more projects here (Monad, Aleo, etc.)
        
        return new Response(JSON.stringify({ 
            status: "success", 
            worker: WORKER_INDEX,
            project: PROJECT_NAME 
        }), { 
            headers: { "Content-Type": "application/json" } 
        });
    } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500 });
    }
});
