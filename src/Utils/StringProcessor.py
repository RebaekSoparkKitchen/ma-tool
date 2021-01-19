def str_process(col_name: str) -> str:
    """
    transfer the lower case staff to the first capital words
    :param col_name: eg. campaign_name
    :return: eg. Campaign Name
    """
    col_name = col_name.replace('_', ' ').title()
    col_name = col_name.replace('Id', 'ID')
    col_name = col_name.replace('Smc', 'SMC')
    col_name = col_name.replace('Mu', 'MU')
    return col_name
