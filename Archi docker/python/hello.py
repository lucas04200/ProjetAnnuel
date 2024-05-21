import psycopg2


try :
    conn = psycopg2.connect(
        user = "user",
        password = "root",
        host = "localhost",
        port = "54320",
        database = "timo"
    )
    
    cur = conn.cursor()
    
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Version : ", version,"\n")
    
    cur.execute("""
    INSERT INTO dimconversation (id_conversation, conversation) VALUES (%s, %s);""", (1, 'O'))
    conn.commit()
  
    #fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")
except (Exception, psycopg2.Error) as error :
    print ("Erreur lors de la connexion à PostgreSQL", error)