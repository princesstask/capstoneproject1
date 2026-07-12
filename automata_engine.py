def process_fsa(data):
    """
    Menangani simulasi DFA, NFA, Moore, dan Mealy Machine
    """
    try:
        fsa_type = data.get("type", "DFA")
        initial = data.get("initial_state")
        input_string = data.get("input_string", "")
        transitions = data.get("transitions", {})

# ==================== 1. SIMULASI DFA ====================
        if fsa_type == "DFA":
            final_states = set(data.get("final_states", []))
            current_state = initial
            trace = [current_state]

            for char in input_string:
                if current_state in transitions and char in transitions[current_state]:
                    current_state = transitions[current_state][char]
                    trace.append(current_state)
                else:
                    return {
                        "status": "rejected",
                        "trace": trace,
                        "message": f"Ditolak: Tidak ada transisi dari {current_state} dengan simbol '{char}'."
                    }
            
            is_accepted = current_state in final_states
            return {
                "status": "accepted" if is_accepted else "rejected",
                "trace": trace,
                "message": f"Selesai di state {current_state}. " + ("String DITERIMA!" if is_accepted else "String DITOLAK.")
            }

# ==================== 2. SIMULASI NFA ====================
        elif fsa_type == "NFA":
            final_states = set(data.get("final_states", []))
            current_states = {initial}
            trace = [[initial]]

            for char in input_string:
                next_states = set()
                for state in current_states:
                    if state in transitions and char in transitions[state]:
                        targets = transitions[state][char]
                        if isinstance(targets, list):
                            next_states.update(targets)
                        else:
                            next_states.add(targets)
                
                if not next_states:
                    trace.append(["Macet"])
                    return {
                        "status": "rejected",
                        "trace": trace,
                        "message": f"Ditolak: Mesin macet pada simbol '{char}'."
                    }
                
                current_states = next_states
                trace.append(list(current_states))

            is_accepted = any(state in final_states for state in current_states)
            return {
                "status": "accepted" if is_accepted else "rejected",
                "trace": trace,
                "message": f"State akhir: {list(current_states)}. " + ("String DITERIMA!" if is_accepted else "String DITOLAK.")
            }

# ==================== 3. MOORE MACHINE ====================
        elif fsa_type == "Moore":
            # Moore membutuhkan kamus output untuk tiap state. Contoh: {"q0": "0", "q1": "1"}
            state_outputs = data.get("state_outputs", {})
            current_state = initial
            
            # Moore menghasilkan output awal dari initial state bahkan sebelum membaca input
            output_generated = state_outputs.get(current_state, "")
            trace = [current_state]

            for char in input_string:
                if current_state in transitions and char in transitions[current_state]:
                    current_state = transitions[current_state][char]
                    trace.append(current_state)
                    output_generated += state_outputs.get(current_state, "")
                else:
                    return {
                        "status": "error",
                        "trace": trace,
                        "message": f"Simulasi terhenti: Tidak ada transisi dari {current_state} untuk input '{char}'."
                    }
            
            return {
                "status": "success",
                "trace": trace,
                "output": output_generated,
                "message": f"Simulasi Moore selesai. Output yang dihasilkan: {output_generated}"
            }

# ==================== 4. MEALY MACHINE ====================
        elif fsa_type == "Mealy":
            # Mealy menyimpan output di dalam transisi. 
            # Contoh struktur: {"q0": {"0": {"target": "q1", "output": "Z"}}}
            current_state = initial
            output_generated = ""
            trace = [current_state]

            for char in input_string:
                if current_state in transitions and char in transitions[current_state]:
                    trans_info = transitions[current_state][char]
                    
                    # Mengambil target state dan output dari transisi
                    if isinstance(trans_info, dict) and "target" in trans_info:
                        current_state = trans_info["target"]
                        output_generated += trans_info.get("output", "")
                    else:
                        return {"status": "error", "message": "Format transisi Mealy di back-end salah."}
                    
                    trace.append(current_state)
                else:
                    return {
                        "status": "error",
                        "trace": trace,
                        "message": f"Simulasi terhenti: Tidak ada transisi dari {current_state} untuk input '{char}'."
                    }
            
            return {
                "status": "success",
                "trace": trace,
                "output": output_generated,
                "message": f"Simulasi Mealy selesai. Output yang dihasilkan: {output_generated}"
            }

    except Exception as e:
        return {"status": "error", "message": f"Terjadi kesalahan logika: {str(e)}"}

# Dummy placeholder untuk modul berikutnya agar routing tidak error
def process_regex(data): return {"status": "success", "message": "Regex Engine Ready"}
def process_pda(data): return {"status": "success", "message": "PDA Engine Ready"}
def process_chomsky(data): return {"status": "success", "message": "Chomsky Engine Ready"}