import gin
import streamlit as st

from google_data_transfer.controller.webapp import WebApp


def main():
    webapp = WebApp()

    st.title("Mentoring Reports")

    form_url = st.text_input("Unesite 'edit' link Google forme:", key="form")
    if form_url:
        webapp.init_form(form_url)
        sheet_url = st.text_input("Unesite 'edit' link Google sheeta:")
        if sheet_url:
            webapp.init_sheet(sheet_url)
            worksheet_names = webapp.get_worksheet_names()
            sheet_name = st.selectbox(
                "Izaberite ime sheeta:", worksheet_names, index=None
            )
            if sheet_name:
                webapp.init_worksheet(sheet_name)
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
