# Simulator & Media Pembelajaran Teori Bahasa dan Automata (TBO-Platform)

Platform interaktif yang menggunakan Web Flask ini dibuat khusus sebagai alat pembelajaran baru untuk memodelkan, mensimulasikan, dan menganalisis gagasan tentang matematika formal dalam mata kuliah Teori Bahasa dan Automata. Proyek ini dikembangkan dengan metode Outcome-Based Education (OBE) untuk menghubungkan teori yang kompleks dengan visualisasi komputasi yang mudah dimengerti dan responsif.


## Daftar Fitur Per Modul

### 1. Modul Finite State Automata (FSA)
Aplikasi menyediakan 4 tab simulator interaktif yang mendukung operasi mesin pengenang string tanpa memori:
*   **Deterministic Finite Automata (DFA):** Pengujian string biner/karakter dengan pelacakan *state* yang dinamis.
*   **Non-Deterministic Finite Automata (NFA):** Simulasi percabangan beberapa *state* sekaligus untuk satu input karakter.
*   **Moore Machine:** Transisi mesin otomata yang menghasilkan nilai *output* berdasarkan *state* saat ini.
*   **Mealy Machine:** Transisi mesin otomata yang menghasilkan nilai *output* berdasarkan *state* dan input karakter.
*   *Fitur Unggulan:* **State-Retention Cache**, menjaga hasil pelacakan pada tab sebelumnya tidak hilang saat pengguna berpindah antar-tab mesin.

### 2. Modul Regular Expression (Regex)
*   **Pencocokan Pola (Pattern Matching):** Validasi kecocokan string input menggunakan aturan sintaksis Regex Python secara utuh (`^` dan `$`).
*   **Grammar Generator:** Pembuatan otomatis aturan tata bahasa formal setara berupa **Right-Linear Grammar (Tata Bahasa Reguler Kanan)** dari pola yang dimasukkan.

### 3. Modul Pushdown Automata (PDA)
*   **Mekanisme Stack Tracer:** Visualisasi operasi memori tambahan (*Push*, *Pop*, dan *None*) langkah demi langkah untuk mengenali *Context-Free Language* seimbang $a^n b^n$.
*   **Derivation Tree Log:** Menampilkan runtunan pohon penurunan tata bahasa bebas konteks secara *Leftmost Derivation*.

### 4. Modul Chomsky Normal Form (CNF)
*   **Input CFG Dinamis:** Antarmuka berbasis teks area JSON yang memungkinkan pengguna memodifikasi aturan produksi tata bahasa bebas konteks secara mandiri.
*   **Transformasi Step-by-Step:** Visualisasi runtunan algoritma penyederhanaan formal mencakup:
    1. Eliminasi $\epsilon$-Production (Simbol Kosong).
    2. Eliminasi Unit Production ($V \rightarrow V$).
    3. Restrukturisasi simbol terminal dan variabel baru hingga menghasilkan aturan akhir Bentuk Normal Chomsky yang valid.

---

## 🛠️ Tech Stack

*   **Back-End Core:** Python 3.x, Flask Framework
*   **Front-End Core:** HTML5, CSS3 (Custom Responsive Media Queries), JavaScript (Vanilla ES6)
*   **Styling Theme:** Maroon (`#930500`), Light Blue (`#95BBEA`), & Cream Background (`#FFF8E7`)

---

## 💻 Cara Instalasi Lokal

Ikuti langkah-langkah berikut untuk menjalankan platform ini di komputer lokal Anda:

1. **Clone Repositori:**
   ```bash
   git clone [https://github.com/username/tbo-platform.git](https://github.com/username/tbo-platform.git)
   cd tbo-platform