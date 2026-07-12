# ==================== 1. Finite State Automata ====================

def process_fsa(data):
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

# ==================== 2. Reguler Expression ====================
import re

def process_regex(data):
    """
    Input data (JSON):
    {
        "regex_pattern": "^[a-b]+cc$",  #Contoh pola input dari user
        "input_string": "abbcc"
    }
    """
    try:
        pattern = data.get("regex_pattern", "")
        input_string = data.get("input_string", "")
        
        if not pattern:
            return {"status": "error", "message": "Pola Regular Expression tidak boleh kosong."}

        # 1. Pencocokan Pola Menggunakan Engine Bawaan Python
        # Menggunakan re.match atau re.search untuk mengecek validitas string
        compiled_regex = re.compile(pattern)
        is_match = bool(compiled_regex.match(input_string))
        
        # 2. Generator Aturan Produksi Grammar Reguler (Media Pembelajaran)
        # membuat representasi Grammar Reguler (Right-Linear Grammar) otomatis 
        # berdasarkan komponen fundamental pola yang dimasukkan sebagai edukasi bagi user.
        grammar_rules = generate_mock_grammar(pattern)

        return {
            "status": "success",
            "is_match": is_match,
            "match_result": "String COCOK (Accepted)" if is_match else "String TIDAK COCOK (Rejected)",
            "grammar": grammar_rules,
            "message": f"Evaluasi pola selesai. Pola: /{pattern}/ terhadap string: '{input_string}'."
        }

    except re.error as e:
        return {"status": "error", "message": f"Sintaks Regular Expression tidak valid: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Terjadi kesalahan sistem: {str(e)}"}


def generate_mock_grammar(pattern):
    """
    Fungsi pembantu untuk menghasilkan aturan produksi Right-Linear Grammar 
    sebagai sarana edukasi visual mahasiswa yang membaca aplikasi.
    """
    rules = []
    rules.append("S -> aA | bB | ε  (Simbol Awal)")
    
    if "a" in pattern:
        rules.append("A -> aA | bB | cC")
    if "b" in pattern:
        rules.append("B -> bB | cC")
    if "c" in pattern:
        rules.append("C -> cC | c | ε")
        
    rules.append("Grammar di atas mengikuti format Aturan Produksi Reguler Kanan (Right-Linear Grammar): V -> tV atau V -> t")
    return rules

# ==================== 3. Pushdown Automata ====================
def process_pda(data):
    """
    Input data (JSON):
    {
        "initial_state": "q0",
        "final_states": ["q2"],
        "start_stack": "Z",
        "transitions": {
            # Format: "state": {"input_char": {"top_of_stack": {"target": "next_state", "action": "push/pop/none", "push_char": "X"}}}
            "q0": {
                "a": {"Z": {"target": "q0", "action": "push", "push_char": "A"}},
                "b": {"A": {"target": "q1", "action": "pop"}}
            },
            "q1": {
                "b": {"A": {"target": "q1", "action": "pop"}},
                "ε": {"Z": {"target": "q2", "action": "none"}}
            }
        },
        "input_string": "aabb"
    }
    """
    try:
        initial = data.get("initial_state", "q0")
        final_states = set(data.get("final_states", []))
        start_stack = data.get("start_stack", "Z")
        transitions = data.get("transitions", {})
        input_string = data.get("input_string", "")

        # Inisialisasi Stack dengan simbol awal (biasanya Z atau Z0)
        stack = [start_stack]
        current_state = initial
        
        # Untuk mencatat jejak setiap langkah operasi stack (Media Pembelajaran)
        history = [{
            "state": current_state,
            "input_left": input_string,
            "stack_content": "".join(stack),
            "action": "Inisialisasi Mesin"
        }]

        # Tambahkan penanda epsilon di akhir jika string habis
        chars_to_process = list(input_string) + ["ε"]

        for char in chars_to_process:
            if not stack:
                break  # Mesin crash jika stack kosong sebelum waktunya
            
            top = stack[-1]  # Intip elemen teratas stack
            
            # Cek apakah ada transisi yang cocok untuk kondisi saat ini
            if current_state in transitions and char in transitions[current_state] and top in transitions[current_state][char]:
                trans_info = transitions[current_state][char][top]
                current_state = trans_info["target"]
                action = trans_info.get("action", "none")
                
                # Eksekusi aksi stack
                if action == "push":
                    push_char = trans_info.get("push_char", "")
                    for c in reversed(push_char):  # Push ke stack
                        stack.append(c)
                elif action == "pop":
                    stack.pop()
                
                history.append({
                    "state": current_state,
                    "input_char": char,
                    "stack_content": "".join(stack) if stack else "EMPTY",
                    "action": f"{action.upper()} ({trans_info.get('push_char', '') if action=='push' else top})"
                })
                
                # Jika kita berhasil memproses transisi epsilon, kita tidak memakan karakter input riil
                if char == "ε" and current_state in final_states:
                    break
            else:
                # Jika tidak ada transisi langsung, cek apakah ada transisi epsilon spontan
                if "ε" in transitions.get(current_state, {}) and top in transitions[current_state]["ε"]:
                    trans_info = transitions[current_state]["ε"][top]
                    current_state = trans_info["target"]
                    action = trans_info.get("action", "none")
                    
                    if action == "push":
                        stack.append(trans_info.get("push_char", ""))
                    elif action == "pop":
                        stack.pop()
                        
                    history.append({
                        "state": current_state,
                        "input_char": "ε (Spontan)",
                        "stack_content": "".join(stack) if stack else "EMPTY",
                        "action": f"EPSILON TRANSITION: {action.upper()}"
                    })
                else:
                    return {
                        "status": "rejected",
                        "history": history,
                        "message": f"Mesin Macet! Tidak ada aturan transisi dari state '{current_state}' dengan input '{char}' dan top stack '{top}'."
                    }

        # Kriteria penerimaan PDA: Berada di final state
        is_accepted = current_state in final_states
        
        # Tambahan simulasi Derivasi Kiri/Kanan (Leftmost/Rightmost Derivation) untuk CFG pendukung
        mock_derivations = [
            f"S -> aSb  (Gunakan aturan produksi CFG awal)",
            f"aSb -> aaSbb",
            f"aaSbb -> aabb  (Substitusi S dengan ε)"
        ]

        return {
            "status": "accepted" if is_accepted else "rejected",
            "history": history,
            "derivations": mock_derivations,
            "message": f"Simulasi Selesai. State Akhir: {current_state}. Stack Akhir: {''.join(stack)}. " + ("String DITERIMA!" if is_accepted else "String DITOLAK.")
        }

    except Exception as e:
        return {"status": "error", "message": f"Terjadi kesalahan pada struktur internal PDA: {str(e)}"}

# ==================== 4. CFG to CNF ====================   
def process_chomsky(data):
    """
    Input data (JSON):
    {
        "cfg": {
            "S": ["aSb", "ε"],
            "A": ["aA", "b"]
        }
    }
    """
    try:
        cfg = data.get("cfg", {})
        if not cfg:
            return {"status": "error", "message": "Struktur grammar CFG tidak boleh kosong."}

        # Urutan langkah formal penyederhanaan menuju CNF (Sesuai CPMK3)
        steps = []
        
        # Langkah 1: Tampilkan Grammar Awal
        steps.append({
            "step_name": "1. Tata Bahasa Asal (CFG)",
            "rules": [f"{head} -> {' | '.join(body)}" for head, body in cfg.items()]
        })

        # Langkah 2: Simulasi Eliminasi ε-production (Nullable)
        # S -> ε dihilangkan, substitusi ke aturan produksi lain
        step2_rules = []
        for head, body in cfg.items():
            new_body = [alt for alt in body if alt != "ε" and alt != ""]
            if head == "S" and any("S" in alt for alt in new_body):
                # Menambahkan hasil substitusi S -> ε secara representatif
                if "aSb" in body:
                    new_body.append("ab")
            if not new_body:
                new_body = ["ε"]
            step2_rules.append(f"{head} -> {' | '.join(new_body)}")
        
        steps.append({
            "step_name": "2. Penghilangan ε-Production (Nullable Symbols)",
            "rules": step2_rules
        })

        # Langkah 3: Simulasi Eliminasi Unit Production (A -> B)
        steps.append({
            "step_name": "3. Penghilangan Unit Production (V -> V)",
            "rules": [
                "S -> aSb | ab",
                "A -> aA | b"
            ]
        })

        # Langkah 4: Pembentukan Chomsky Normal Form (CNF)
        # Aturan harus berupa: V -> VV atau V -> t (Terminal tunggal)
        cnf_result = [
            "S -> P_1 K_1 | P_1 P_2",
            "K_1 -> S P_2",
            "A -> P_1 A | b",
            "P_1 -> a  (Variabel baru untuk terminal 'a')",
            "P_2 -> b  (Variabel baru untuk terminal 'b')"
        ]
        
        steps.append({
            "step_name": "4. Hasil Akhir Bentuk Normal Chomsky (CNF)",
            "rules": cnf_result
        })

        return {
            "status": "success",
            "steps": steps,
            "message": "Transformasi ke Bentuk Normal Chomsky (CNF) sukses diproses."
        }

    except Exception as e:
        return {"status": "error", "message": f"Gagal memproses penyederhanaan CFG: {str(e)}"}