import json
import urllib.request

def run_local_agent(system_persona, user_task):
    url = "http://localhost:11434/api/generate"
    full_prompt = f"System Persona: {system_persona}\n\nTask: {user_task}"
    
    data = {
        "model": "llama3.2",
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.2  # Kept low for precise, predictable syntax output
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    
    print("\n## [Agent Architecture Engine]: Processing routing configuration script...")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get('response', 'No output generated.')
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    persona = """You are an expert Principal Network Security Architect. 
Your goal is to build secure, loop-free multi-protocol routing environments. 
Always use standard Cisco IOS-XE configuration syntax. 
Be precise, implement strict loop prevention, and explain your tagging logic."""

    task = """We have two data center edge routers (DC-GW-01 and DC-GW-02) performing mutual route redistribution between an internal OSPF Process 100 and an external BGP AS 65001. 

To prevent suboptimal routing and routing loops, write a Cisco IOS-XE configuration for DC-GW-01 that:
1. Redistributes OSPF into BGP, tagging OSPF routes with route-tag 100.
2. Redistributes BGP into OSPF, denying any routes that already have tag 200 (coming from DC-GW-02) and tagging allowed BGP routes with tag 100.
3. Uses a route-map to safely handle the redistribution.

Provide the exact Cisco IOS-XE CLI configuration blocks and a brief architectural verification explanation."""

    print("## Launching Local Routing Agent ##")
    agent_output = run_local_agent(persona, task)
    
    print("\n## Final Agent Blueprint Output ##\n")
    print(agent_output)
