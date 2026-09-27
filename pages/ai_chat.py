import streamlit as st
from ai_advisor import (
    get_gemini_model,
    init_chat_session,
    format_financial_context,
    get_ai_response
)


def show():
    st.header("🤖 FinanSaku AI Advisor")
    st.caption("Asisten keuangan pribadi berbasis AI — tanyakan apa saja tentang keuanganmu!")

    fm = st.session_state.finance_manager

    # ── Initialize AI Model ──
    model = get_gemini_model()

    if model is None:
        st.warning("""
        ⚠️ **API Key Gemini belum dikonfigurasi.**

        Untuk menggunakan AI Advisor, silakan:
        1. Dapatkan API key gratis di [Google AI Studio](https://aistudio.google.com/apikey)
        2. Buat file `.streamlit/secrets.toml` dengan isi:
           ```
           GEMINI_API_KEY = "your_api_key_here"
           ```
        3. Atau set di Streamlit Cloud: Settings → Secrets
        """)
        return

    # ── Initialize Chat Session ──
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "chat_session" not in st.session_state:
        ringkasan = fm.ringkasan_keuangan()
        context = format_financial_context(ringkasan)
        st.session_state.chat_session = init_chat_session(model, context)
        # Add welcome message
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": "Halo! 👋 Saya **FinanSaku AI**, asisten keuangan pribadi Anda.\n\n"
                       "Saya bisa membantu Anda:\n"
                       "- 📊 Menganalisis pola pengeluaran\n"
                       "- 💡 Memberikan saran penghematan\n"
                       "- 📋 Membantu membuat budget\n"
                       "- 🎯 Tips tabungan & investasi\n\n"
                       "Silakan tanyakan apa saja tentang keuangan Anda! 😊"
        })

    # ── Sidebar Quick Actions ──
    with st.sidebar:
        st.markdown("---")
        st.subheader("⚡ Pertanyaan Cepat")
        quick_prompts = [
            "📊 Analisis keuangan saya",
            "💡 Tips menghemat pengeluaran",
            "📋 Buatkan budget bulanan",
            "🎯 Saran tabungan untuk pemula",
            "💰 Cara mengatur gaji bulanan"
        ]

        for qp in quick_prompts:
            if st.button(qp, key=f"quick_{qp}", use_container_width=True):
                st.session_state.quick_prompt = qp

        if st.button("🔄 Reset Chat", use_container_width=True, type="secondary"):
            st.session_state.chat_messages = []
            ringkasan = fm.ringkasan_keuangan()
            context = format_financial_context(ringkasan)
            st.session_state.chat_session = init_chat_session(model, context)
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": "Chat direset! 🔄 Ada yang bisa saya bantu?"
            })
            st.rerun()

    # ── Display Chat History ──
    for msg in st.session_state.chat_messages:
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # ── Handle Quick Prompt ──
    prompt = None
    if "quick_prompt" in st.session_state:
        prompt = st.session_state.quick_prompt
        del st.session_state.quick_prompt

    # ── Handle User Input ──
    if user_input := st.chat_input("Tanyakan tentang keuangan Anda..."):
        prompt = user_input

    if prompt:
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        # Generate AI response with streaming
        with st.chat_message("assistant", avatar="🤖"):
            try:
                response = get_ai_response(st.session_state.chat_session, prompt)
                if isinstance(response, str):
                    st.markdown(response)
                    full_response = response
                else:
                    # Streaming response
                    def stream_generator():
                        for chunk in response:
                            if chunk.text:
                                yield chunk.text

                    full_response = st.write_stream(stream_generator())

            except Exception as e:
                full_response = f"Maaf, terjadi kesalahan: {str(e)}"
                st.error(full_response)

        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": full_response
        })
        st.rerun()


show()
