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

// Objek lokal untuk menyimpan riwayat hasil eksekusi tiap tipe mesin secara terpisah
const simulationCache = {
    DFA: null,
    NFA: null,
    Moore: null,
    Mealy: null
};

// Fungsi Kontrol Navigasi Tab Visual (Telah Diperbaiki)
function switchTab(tabType) {
    // Ubah status tombol aktif
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Perbarui penanda tipe tersembunyi & judul panel
    document.getElementById('fsa-type').value = tabType;
    document.getElementById('panel-title').innerText = `Konfigurasi Mesin ${tabType}`;
    
    // Cek apakah tab ini sudah pernah dijalankan sebelumnya dan punya riwayat di cache
    if (simulationCache[tabType]) {
        // Jika ada, langsung tampilkan kembali hasil lamanya
        document.getElementById('placeholder-text').style.display = 'none';
        renderVisualResult(simulationCache[tabType]);
    } else {
        // Jika belum pernah dijalankan, kembalikan ke tampilan default kosong (placeholder)
        document.getElementById('result-container').style.display = 'none';
        document.getElementById('placeholder-text').style.display = 'block';
    }
}

// Fungsi bantu untuk merender visualisasi hasil ke komponen UI
function renderVisualResult(result) {
    const resBox = document.getElementById('result-container');
    const statusEl = document.getElementById('result-status');
    const traceEl = document.getElementById('result-trace');
    
    resBox.style.display = 'block';
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

    if (result.output) {
        traceEl.innerHTML = `<strong>Path:</strong> ${JSON.stringify(result.trace)} <br><strong>Output String:</strong> ${result.output}`;
    } else {
        traceEl.innerText = JSON.stringify(result.trace);
    }
}

// Menangani Submit Form Menggunakan Fetch API
document.getElementById('fsa-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const type = document.getElementById('fsa-type').value;
    const inputString = document.getElementById('input-string').value;
    
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
        
        // Simpan hasil eksekusi teranyar ke dalam cache sesuai tipenya sebelum dirender
        simulationCache[type] = result;
        
        // Sembunyikan placeholder dan tampilkan hasil
        document.getElementById('placeholder-text').style.display = 'none';
        renderVisualResult(result);
        
    } catch (err) {
        alert("Gagal melakukan simulasi ke server: " + err.message);
    }
});