def str_process(col_name: str) -> str:
    """
    transfer the lower case staff to the first capital words
    :param col_name: eg. campaign_name
    :return: eg. Campaign Name
    """
    if col_name == 'id':
        return col_name.upper()
    return col_name.replace('_', ' ').title()