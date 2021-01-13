from src.Models.TableData import data_producer


def future_work():
    cols = ['blast_date', 'campaign_name', 'wave', 'owner_full_name', 'event_date']
    sql = f"SELECT {','.join(cols)} FROM Request " \
          "WHERE DATE(blast_date) > DATE('now', 'localtime') " \
          "ORDER BY DATE(blast_date)"
    title = "未来的工作"
    return data_producer(title=title, cols=cols, sql=sql)


def tbd_work():
    cols = ['id', 'creation_time', 'campaign_name', 'owner_full_name']
    sql = f"SELECT {','.join(cols)} FROM Request " \
          f"WHERE blast_date IS NULL " \
          f"ORDER BY request_id DESC " \
          f"LIMIT 10"
    title = "待定的工作"
    return data_producer(title=title, cols=cols, sql=sql)


def report_work():
    cols = ['request_id', 'blast_date', 'campaign_name', 'wave', 'owner_full_name', 'smc_campaign_id']
    sql = f"SELECT {','.join(cols)} FROM Request LEFT OUTER JOIN BasicPerformance USING (smc_campaign_id)" \
          f"WHERE DATE(report_date) = DATE('now', 'localtime') OR (sent IS NULL AND DATE(report_date) BETWEEN DATE(" \
          f"'2020-01-01') AND DATE('now', 'localtime')) " \
          f"ORDER BY blast_date DESC"
    title = '今日需发送报告'
    return data_producer(title=title, cols=cols, sql=sql)


def campaign_id_work():
    cols = ['id', 'blast_date', 'campaign_name', 'wave', 'owner_full_name']
    sql = f"SELECT {','.join(cols)} FROM Request " \
          "WHERE (smc_campaign_id IS NULL OR smc_campaign_id = '') AND DATE(blast_date) BETWEEN DATE('2020-01-01') " \
          "AND DATE('now', 'localtime') " \
          "ORDER BY DATE(blast_date) DESC"
    title = "需要填写smc campaign id的request"
    return data_producer(title=title, cols=cols, sql=sql)


def communication_limit_work():
    cols = ['id', 'blast_date', 'campaign_name', 'owner_full_name']
    sql = f"SELECT {','.join(cols)} FROM Request " \
          "WHERE DATE(blast_date) = DATE('now', '-4 day', 'localtime')" \
          "ORDER BY DATE(blast_date)"
    title = "明日需注意避让的campaign"
    return data_producer(title=title, cols=cols, sql=sql)


if __name__ == '__main__':
    from src.Connector.MA import MA

    a = MA().query('select campaign_name, sent from request left outer join basicperformance using (smc_campaign_id) '
                   'where sent is null limit 10;')
    print(a)
