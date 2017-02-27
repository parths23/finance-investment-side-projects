from datetime import datetime, timedelta


def _string_to_date(date_string):
    """
    Convert a string to a python datetime object.
    Will attempt to match date format with commonly used string representations.
    :param date_string: string representation of date
    :rtype: string of date in "Y-m-d" format
    """
    if date_string == '':
        return ''
    formats = (
        '%d-%b-%Y', '%Y-%m-%d',
    )
    for fmt in formats:
        try:
            result = datetime.strptime(date_string, fmt)
            return result.strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError('Unknown date format: {0}'.format(date_string))


def prior_date(date_string, days=1):
    result = datetime.strptime(date_string, '%Y-%m-%d')
    day = result - timedelta(days=days)
    return day.strftime('%Y-%m-%d')
