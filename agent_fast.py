import json
import urllib.request

def run_local_agent(system_persona, user_task):
    url = "http://localhost:11434/api/generate"
    
    # Structure the agent prompt cleanly
    full_prompt = f"System Persona: {system_persona}\n\nTask: {user_task}"
    
    data = {
        "model": "llama3.2",
        "prompt": full_prompt,
        "stream": False
    }
    
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    
    print("\n## [Agent Thought]: Sending task to local Llama 3.2 execution engine...")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get('response', 'No output generated.')
    except Exception as e:
        return f"Error connecting to local agent server: {e}"

# --- EXECUTION LOOP ---
if __name__ == "__main__":
    persona = "You are a Senior Network Security Engineer with 15 years of infrastructure experience."
    task = "In two short sentences, why is LACP preferred over a static trunk port?"
    
    print("## Starting Local Zero-Dependency Agent ##")
    agent_output = run_local_agent(persona, task)
    
    print("\n## Final Agent Response ##")
    print(agent_output)
