# Script-SI

Script-SI adalah sebuah website yang memungkinkan pengguna untuk menghasilkan ide penelitian berdasarkan kepakaran dosen. Dengan Script-SI, Anda dapat memasukkan nama dosen dan mendapatkan saran topik penelitian yang relevan.

## Panduan Instalasi dan Penggunaan

### Persyaratan Awal

1. Pastikan Anda memiliki **Git** terinstall di komputer Anda. Jika belum, ikuti panduan berikut untuk menginstall Git:
   - **Windows**:
     1. Unduh installer Git dari [situs resmi Git](https://git-scm.com/).
     2. Jalankan installer dan ikuti petunjuk instalasi.
   - **Linux**:
     Jalankan perintah berikut di terminal:
     ```bash
     sudo apt update
     sudo apt install git
     ```
   - **MacOS**:
     Gunakan Homebrew untuk menginstall Git dengan perintah:
     ```bash
     brew install git
     ```

2. Pastikan Anda memiliki Python 3.x terinstall di sistem Anda.

### Langkah Instalasi

1. Clone repositori Script-SI ke komputer Anda:
   - Buka **File Explorer** dan pilih folder di mana Anda ingin menyimpan project ini.
   - Klik kanan di dalam folder tersebut dan pilih **Open in Terminal** atau buka **Command Prompt (cmd)** secara manual.
   - Jalankan perintah berikut di terminal:
     ```bash
     git clone https://github.com/zhillanarf/ProjectPPL.git
     ```

2. Tunggu hingga proses cloning selesai.

3. Setelah selesai, buka folder project Script-SI menggunakan teks editor seperti **Visual Studio Code (VSCode)**.

### Menjalankan Server Lokal

1. Masuk ke folder project yang berisi file `manage.py` dengan perintah berikut:
   ```bash
   cd mysite
   ```

2. Pastikan Anda memiliki Django terinstall. Jika belum, install Django dengan perintah:
   ```bash
   pip install django
   ```

3. Jalankan server lokal Django dengan perintah:
   ```bash
   python manage.py runserver
   ```

4. Setelah server berhasil dijalankan, Anda akan melihat URL lokal berupa:
   ```
   http://127.0.0.1:8000/
   ```
   Buka URL tersebut di browser dengan **Ctrl + klik** pada URL.

### Selamat Menggunakan Script-SI
Anda sekarang dapat menggunakan Script-SI untuk menghasilkan ide penelitian sesuai dengan kepakaran dosen yang diinputkan.

