// Struktur Data Contoh Default untuk Kebutuhan Demo Capstone Instan
const defaultData = {
    DFA: {
        type: "DFA",
        initial_state: "q0",
        final_states: ["q2"],
        transitions: {
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q2", "1": "q1"},
            "q2": {"0": "q2", "1": "q2"}
        }
    },
    NFA: {
        type: "NFA",
        initial_state: "q0",
        final_states: ["q2"],
        transitions: {
            "q0": {"0": ["q0", "q1"], "1": ["q0"]},
            "q1": {"1": ["q2"]}
        }
    },
    Moore: {
        type: "Moore",
        initial_state: "q0",
        state_outputs: {"q0": "Genap", "q1": "Ganjil", "q2": "Genap"},
        transitions: {
            "q0": {"1": "q1"},
            "q1": {"1": "q2"},
            "q2": {"1": "q1"}
        }
    },
    Mealy: {
        type: "Mealy",
        initial_state: "q0",
        transitions: {
            "q0": {"0": {"target": "q0", "output": "Nol"}, "1": {"target": "q1", "output": "Satu"}},
            "q1": {"0": {"target": "q0", "output": "Nol"}, "1": {"target": "q1", "output": "Satu"}}
        }
    }
};

// Fungsi Kontrol Navigasi Tab Visual
function switchTab(tabType) {
    // Ubah status tombol aktif
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Perbarui penanda tipe tersembunyi & judul panel
    document.getElementById('fsa-type').value = tabType;
    document.getElementById('panel-title').innerText = `Konfigurasi Mesin ${tabType}`;
    
    // Bersihkan kontainer hasil lama
    document.getElementById('result-container').style.display = 'none';
    document.getElementById('placeholder-text').style.display = 'block';
}

// Menangani Submit Form Menggunakan Fetch API
document.getElementById('fsa-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const type = document.getElementById('fsa-type').value;
    const inputString = document.getElementById('input-string').value;
    
    // Gabungkan data konfigurasi mesin default dengan string input dinamis dari user
    const payload = {
        ...defaultData[type],
        input_string: inputString
    };

    try {
        const response = await fetch('/fsa', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        
        // Sembunyikan placeholder, tampilkan kotak hasil
        document.getElementById('placeholder-text').style.display = 'none';
        const resBox = document.getElementById('result-container');
        resBox.style.display = 'block';
        
        const statusEl = document.getElementById('result-status');
        const traceEl = document.getElementById('result-trace');
        
        // Render Hasil Berdasarkan Respon Server
        document.getElementById('result-message').innerText = result.message;
        
        if (result.status === "accepted" || result.status === "success") {
            resBox.style.backgroundColor = "#e6f4ea";
            statusEl.innerText = "SUCCESS / ACCEPTED";
            statusEl.style.color = "#137333";
        } else {
            resBox.style.backgroundColor = "#fce8e6";
            statusEl.innerText = "REJECTED / ERROR";
            statusEl.style.color = "#c5221f";
        }

        // Tampilkan lintasan perpindahan state / output mesin jika ada
        if (result.output) {
            traceEl.innerHTML = `<strong>Path:</strong> ${JSON.stringify(result.trace)} <br><strong>Output String:</strong> ${result.output}`;
        } else {
            traceEl.innerText = JSON.stringify(result.trace);
        }
        
    } catch (err) {
        alert("Gagal melakukan simulasi ke server: " + err.message);
    }
});