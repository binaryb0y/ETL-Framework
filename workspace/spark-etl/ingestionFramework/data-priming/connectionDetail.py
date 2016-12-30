'''
Created on 29 Dec 2016

@author: 611370417
'''

import cx_Oracle

# connect to master database to fetch entries
def make_Connection() :#
    try:
        conn = cx_Oracle.connect('sparkmaya/sparkmaya@127.0.0.1/XE')
        valid_connection(conn)
        get_metadata(conn)
        conn.close()
    except cx_Oracle.DatabaseError,exception:
        print("Failed to connect to SparkMaya Master Database")

def get_metadata(conn):
    cur = conn.cursor()
    connection = cur.execute("select column_name, data_type from all_tab_columns where table_name='DATABASE_TYPE'")
    for result in connection:
        print result
    
    print 'Complete'
# verify entries  
def valid_connection(conn):
    cur = conn.cursor()
    
    # Fetch entries
    connection = cur.execute('select * from connection_detail where valid_connection=0 and database_type=1')
    
    # Sample Entry : (1, 1, '127.0.0.1', 1521, 'SPARKMAYA', 'sparkmaya', 'SPARKMAYA', 'XE_Connection_Local', '0', 'XE')
    
    
    for result in connection:
        print 'Validating entry for connection ', result[7]      
        try:
            entryconn = cx_Oracle.connect(result[4],result[5],result[9])
            print "Connection Valid"
            entrycurr = entryconn.cursor()
            print "Updating %s with valid_conection=1" %(result[7])
            entrycurr.execute("update connection_detail set valid_connection=1 where database_type=1 and id=%s" %(result[0]))
            entryconn.commit()
            entryconn.close()
            
        except cx_Oracle.DatabaseError, exception:
            prinfException(exception)           
    
    cur.close()
    




if __name__ == '__main__':
    make_Connection()