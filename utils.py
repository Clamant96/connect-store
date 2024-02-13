def converteDictEmJsonAll(cursor):
    lista = cursor.fetchall()

    if lista:
        return [dict(dict_factory(cursor, row)) for row in lista]
    else:
        return []

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d