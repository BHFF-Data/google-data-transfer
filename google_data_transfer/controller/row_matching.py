from fuzzywuzzy import fuzz

def match_sheet_with_form_fuzzy(name, form_data, mapping):
    """
    Match a name from the sheet with corresponding data in the form using fuzzy matching.

    Args:
        name (str): The name to be matched.
        form_data (pd.DataFrame): Data from the form.
        mapping (dict): Mapping of form columns to sheet columns.

    Returns:
        Optional[str]: The matched email or None if no match is found.
    """
    sheet_column = mapping.get('Mentee')  # Adjust based on your actual google sheet
    form_column = mapping.get('Scholar email:')  # Adjust based on your actual google form

    if sheet_column is None or form_column is None:
        raise ValueError("Invalid column mapping")

    for _, row in form_data.iterrows():
        form_name = row[form_column]

        # Use fuzzy matching to determine similarity
        if fuzz.token_sort_ratio(name, form_name) > 80:  # Adjust the ratio as needed
            return row['Email']  # Adjust based on your actual column names

    return None
