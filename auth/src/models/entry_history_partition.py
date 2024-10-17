from sqlalchemy import text


def create_partition(target, connection, **kwargs) -> None:
    '''
        Creating table partition by user sign in device:
        console, mobile, tablet, smarttv, wearable, embedded
    '''
    connection.execute(
        text(
            '''
                CREATE TABLE IF NOT EXISTS 'entry_histories_console'
                PARTITION OF 'entry_histories'
                FOR VALUES IN ('console')
            '''
        ),
    )
    connection.execute(
        text(
            '''
                CREATE TABLE IF NOT EXISTS 'entry_histories_mobile'
                PARTITION OF 'entry_histories'
                FOR VALUES IN ('mobile')
            '''
        ),
    )
    connection.execute(
        text(
            '''
                CREATE TABLE IF NOT EXISTS 'entry_histories_tablet'
                PARTITION OF 'entry_histories'
                FOR VALUES IN ('tablet')
            '''
        ),
    )
    connection.execute(
        text(
            '''
                CREATE TABLE IF NOT EXISTS 'entry_histories_smarttv'
                PARTITION OF 'entry_histories'
                FOR VALUES IN ('smarttv')
            '''
        ),
    )
    connection.execute(
        text(
            '''
                CREATE TABLE IF NOT EXISTS 'entry_histories_wearable'
                PARTITION OF 'entry_histories'
                FOR VALUES IN ('wearable')
            '''
        ),
    )
    connection.execute(
        text(
            '''
                CREATE TABLE IF NOT EXISTS 'entry_histories_embedded'
                PARTITION OF 'entry_histories'
                FOR VALUES IN ('embedded')
            '''
        ),
    )
    connection.execute(
        text(
            '''
                CREATE TABLE IF NOT EXISTS 'entry_histories_undefined'
                PARTITION OF 'entry_histories'
                FOR VALUES IN ('undefined')
            '''
        ),
    )
