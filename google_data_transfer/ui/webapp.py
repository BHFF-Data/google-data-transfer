import gin
import streamlit as st

from google_data_transfer.controller.webapp import WebApp


def main():
    webapp = WebApp()

    st.title("Mentoring Reports")

    form_url = st.text_input("Unesite 'edit' link Google forme:", key="form")
    if form_url:
        # webapp.init_form_from_credentials(form_url, st.secrets["credentials"])
        # webapp.init_form_from_acces_token(form_url, st.secrets["token"])
        webapp.init_form_from_service_account(form_url=form_url, service_account_creds=st.secrets["service_account"])
        # webapp.init_form(form_url)
        sheet_url = st.text_input("Unesite 'edit' link Google sheeta:")
        if sheet_url:
            # webapp.init_sheet_from_credentials(sheet_url, st.secrets["credentials"])
            # webapp.init_sheet_from_access_token(sheet_url, st.secrets["token"])
            webapp.init_sheet_from_service_account(sheet_url=sheet_url,
                                                   service_account_creds=st.secrets["service_account"])
            # webapp.init_sheet(sheet_url)
            subsheet_names = webapp.get_subsheet_names()
            sheet_name = st.selectbox(
                "Izaberite ime sheeta:", subsheet_names, index=None
            )
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
