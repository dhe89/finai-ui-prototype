# FinAI Streamlit UI Prototype

Prototype UI untuk FinAI — Financial Intelligence.

## Isi

- `app.py` — Streamlit prototype, tanpa LLM/backend.
- `requirements.txt` — dependency minimal.

## Jalankan lokal

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy ke Streamlit Community Cloud

1. Buat repository GitHub baru.
2. Upload `app.py` dan `requirements.txt`.
3. Di Streamlit Community Cloud pilih repository tersebut.
4. Main file: `app.py`.
5. Deploy.

Prototype ini sengaja menggunakan HTML/CSS/JavaScript di dalam Streamlit Component agar layout responsive bisa dibuat lebih bebas daripada memakai widget Streamlit biasa.

## Responsive behavior

- Desktop: Sidebar kiri + dashboard + AI Assistant kanan.
- Tablet: AI Assistant dapat menjadi drawer.
- Mobile: dashboard full-width, menu menjadi drawer kiri, AI menjadi drawer kanan.
- Tidak menggunakan LLM; chat hanya simulasi UI.
