import hmac
import os
import gin
import streamlit as st

from google_data_transfer.controller.webapp import WebApp

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


def main():
    webapp = WebApp()

    st.title("Mentoring Reports")

    # Provjeri lozinku
    if not check_password():
        st.stop()  # Do not continue if check_password is not True.

    form_url = st.text_input("Unesite 'edit' link Google forme:", key="form")
    if form_url:
        webapp.init_form(form_url)
        sheet_url = st.text_input("Unesite 'edit' link Google sheeta:")
        if sheet_url:
            webapp.init_sheet(sheet_url)
            subsheet_names = webapp.get_subsheet_names()
            sheet_name = st.selectbox("Unesite ime sheeta:", subsheet_names, index=None)
            if sheet_name:
                webapp.init_subsheet(sheet_name)
                cols = webapp.get_sheet_cols()
                target_col = st.selectbox(
                    "Izaberite u koju kolonu želite upisati rezultat:", cols, index=None
                )
                if target_col:
                    with st.spinner(text="Transfer u toku..."):
                        webapp.transfer(target_col)
                    st.success("Transfer uspješan!")

if __name__ == "__main__":
    gin.parse_config_file("config/local.gin")
    main()