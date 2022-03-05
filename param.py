from mysql.connector.constants import ClientFlag

config = {
    'user': 'users',
    'password': '#Stocks@007#',
    'host': '34.79.163.70',
    'database': 'stocksdb',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}
