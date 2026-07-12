def process_fsa(data):
    """
    Menangani simulasi DFA dan NFA
    Input data (JSON): 
    {
        "type": "DFA" atau "NFA",
        "states": ["q0", "q1", "q2"],
        "alphabet": ["0", "1"],
        "initial_state": "q0",
        "final_states": ["q2"],
        "transitions": {
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q2", "1": "q1"},
            "q2": {"0": "q2", "1": "q2"}
        }, # Catatan: Untuk NFA, value dari simbol adalah list target state, misal: "0": ["q0", "q1"]
        "input_string": "010"
    }
    """
    try:
        fsa_type = data.get("type", "DFA")
        initial = data.get("initial_state")
        final_states = set(data.get("final_states", []))
        transitions = data.get("transitions", {})
        input_string = data.get("input_string", "")

        # --- SIMULASI DFA ---
        if fsa_type == "DFA":
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
                        "message": f"String ditolak: Tidak ada transisi dari {current_state} dengan simbol '{char}'."
                    }
            
            is_accepted = current_state in final_states
            return {
                "status": "accepted" if is_accepted else "rejected",
                "trace": trace,
                "message": f"Selesai di state {current_state}. " + ("String DITERIMA!" if is_accepted else "String DITOLAK karena bukan final state.")
            }

        # --- SIMULASI NFA ---
        elif fsa_type == "NFA":
            # NFA melacak sekumpulan state aktif sekaligus (current states set)
            current_states = {initial}
            trace = [[initial]]  # Melacak perkembangan kumpulan state aktif

            for char in input_string:
                next_states = set()
                for state in current_states:
                    if state in transitions and char in transitions[state]:
                        # transitions[state][char] diasumsikan berupa list/array untuk NFA
                        targets = transitions[state][char]
                        if isinstance(targets, list):
                            next_states.update(targets)
                        else:
                            next_states.add(targets)
                
                if not next_states:
                    trace.append(["DITOLAK (Macet)"])
                    return {
                        "status": "rejected",
                        "trace": trace,
                        "message": f"String ditolak: Mesin macet, tidak ada transisi yang valid untuk simbol '{char}'."
                    }
                
                current_states = next_states
                trace.append(list(current_states))

            # Cek apakah ada salah satu state aktif yang merupakan final state
            is_accepted = any(state in final_states for state in current_states)
            return {
                "status": "accepted" if is_accepted else "rejected",
                "trace": trace,
                "message": f"State akhir yang dicapai: {list(current_states)}. " + ("String DITERIMA!" if is_accepted else "String DITOLAK.")
            }

    except Exception as e:
        return {"status": "error", "message": f"Input tidak valid atau rusak: {str(e)}"}

# Dummy placeholder untuk modul berikutnya agar routing tidak error
def process_regex(data): return {"status": "success", "message": "Regex Engine Ready"}
def process_pda(data): return {"status": "success", "message": "PDA Engine Ready"}
def process_chomsky(data): return {"status": "success", "message": "Chomsky Engine Ready"}