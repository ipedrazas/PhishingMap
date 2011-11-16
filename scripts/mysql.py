import MySQLdb
import sys
import socket

def isValidIP(ip):
    
    try:
        socket.inet_aton(ip)
        res = True
        # legal
    except socket.error:
        # Not legal
        res = False
    return res

try:
    
    txtFile = 'ips.txt'    
    
    
    fd = open(txtFile)
    content = fd.readline().strip()
    
    conn = MySQLdb.connect('localhost','section9', 'section9', 'section9');
    cursor = conn.cursor()
    
    while(content != ""):
        
            if(content=='##EOF##'):
                break
            else:
                if(isValidIP(content)):
                    cursor.execute("""SELECT ip FROM geoipdata WHERE ip= %s""",content)
                    rows = cursor.fetchall()
                    flag = True
                    for row in rows:
                        flag = False
                    if(flag):
                        cursor.execute("""
                            INSERT IGNORE INTO geoipdata SET ip = %s
                                       """, content)
            content = fd.readline().strip()
    
    cursor.close()
    conn.commit()
    conn.close()
    cursor = conn.cursor()
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
