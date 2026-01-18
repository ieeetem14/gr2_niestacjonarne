import streamlit as st
from supabase import create_client, Client

# Konfiguracja połączenia
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("Zarządzanie Asortymentem")

# --- SEKCJA KATEGORII ---
st.header("📂 Kategorie")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dodaj kategorię")
    kat_nazwa = st.text_input("Nazwa kategorii", key="new_kat_name")
    kat_opis = st.text_area("Opis kategorii")
    if st.button("Dodaj Kategorię"):
        data = {"nazwa": kat_nazwa, "opis": kat_opis}
        supabase.table("kategorie").insert(data).execute()
        st.success("Dodano kategorię!")
        st.rerun()

with col2:
    st.subheader("Usuń kategorię")
    try:
        kategorie = supabase.table("kategorie").select("id, nazwa").execute().data
        if kategorie:
            kat_to_del = st.selectbox("Wybierz kategorię", kategorie, format_func=lambda x: x['nazwa'], key="del_kat")
            if st.button("Usuń Kategorię"):
                supabase.table("kategorie").delete().eq("id", kat_to_del['id']).execute()
                st.warning(f"Usunięto {kat_to_del['nazwa']}")
                st.rerun()
    except Exception as e:
        st.error(f"Błąd: {e}")

st.divider()

# --- SEKCJA PRODUKTÓW ---
st.header("📦 Produkty")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Dodaj produkt")
    p_nazwa = st.text_input("Nazwa produktu")
    p_liczba = st.number_input("Liczba (szt.)", min_value=0, step=1)
    p_cena = st.number_input("Cena", min_value=0.0, step=0.01)
    
    # Pobranie kategorii do selectboxa
    kategorie_list = supabase.table("kategorie").select("id, nazwa").execute().data
    kat_options = {k['nazwa']: k['id'] for k in kategorie_list}
    
    p_kat = st.selectbox("Kategoria", options=list(kat_options.keys()))

    if st.button("Dodaj Produkt"):
        prod_data = {
            "nazwa": p_nazwa,
            "liczba": p_liczba,
            "cena": p_cena,
            "kategoria_id": kat_options[p_kat]
        }
        supabase.table("produkty").insert(prod_data).execute()
        st.success(f"Dodano produkt: {p_nazwa}")
        st.rerun()

with col4:
    st.subheader("Usuń produkt")
    produkty = supabase.table("produkty").select("id, nazwa").execute().data
    if produkty:
        prod_to_del = st.selectbox("Wybierz produkt", produkty, format_func=lambda x: x['nazwa'])
        if st.button("Usuń Produkt"):
            supabase.table("produkty").delete().eq("id", prod_to_del['id']).execute()
            st.warning("Produkt usunięty")
            st.rerun()

# --- PODGLĄD TABEL ---
st.divider()
st.subheader("Aktualny stan bazy")
if st.checkbox("Pokaż tabelę produktów"):
    res = supabase.table("produkty").select("id, nazwa, liczba, cena, kategorie(nazwa)").execute()
    st.table(res.data)
