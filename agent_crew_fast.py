import json
import urllib.request

def call_local_agent(system_persona, task_prompt, structural_context=""):
    url = "http://localhost:11434/api/generate"
    
    # Bundle the agent's persona, context from previous agents, and current task
    full_prompt = f"System Persona: {system_persona}\n\n"
    if structural_context:
        full_prompt += f"Context from previous engineering phase:\n{structural_context}\n\n"
    full_prompt += f"Task: {task_prompt}"
    
    data = {
        "model": "llama3.2",
        "prompt": full_prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }
    
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get('response', 'No output generated.')
    except Exception as e:
        return f"Error talking to local engine: {e}"

# --- MULTI-AGENT HANDOFF PIPELINE ---
if __name__ == "__main__":
    print("## Launching Local Native Multi-Agent Pipeline (Python 3.14 Safe) ##")
    
    # --- PHASE 1: THE NETWORK ARCHITECT ---
    architect_persona = "You are a Principal Network Architect specializing in loop-free core routing designs."
    architect_task = """Write a precise Cisco IOS-XE configuration for a gateway router performing 
mutual route redistribution between OSPF Process 100 and BGP AS 65001. 
You must use route-maps and apply a specific route tag (tag 100) to prevent loops."""
    
    print("\n[Pipeline] Agent 1 (Network Architect) is designing the infrastructure...")
    architecture_blueprint = call_local_agent(architect_persona, architect_task)
    print("\n>> Architect Output Received.")
    
    # --- PHASE 2: THE SECURITY AUDITOR ---
    auditor_persona = "You are a Lead Network Security Engineer specializing in infrastructure hardening and route-map policy validation."
    auditor_task = """Review the Cisco configuration blueprint provided by the architect below. 
Verify that the loop prevention tag logic is mathematically sound, and append standard 
control-plane hardening commands (like MD5 authentication or prefix-lists) to secure the process."""
    
    print("\n[Pipeline] Handoff -> Agent 2 (Security Auditor) is analyzing blueprint for risks...")
    final_audit = call_local_agent(auditor_persona, auditor_task, structural_context=architecture_blueprint)
    
    # --- PRINT FINAL PIPELINE RESULT ---
    print("\n=======================================================")
    print("## PIPELINE COMPLETE: COMPREHENSIVE INFRASTRUCTURE DELIVERY ##")
    print("=======================================================\n")
    print("### ARCHITECT ARCHITECTURE BLUEPRINT: ###\n")
    print(architecture_blueprint)
    print("\n### SECURITY AUDIT & HARDENING ADDENDUM: ###\n")
    print(final_audit)
