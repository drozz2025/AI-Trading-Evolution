import time

def _db():
 from .auth import _db as db
 return db()
def init_audit():
 c=_db(); c.execute("CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, user_id INTEGER, action TEXT NOT NULL, detail TEXT, created_at INTEGER NOT NULL)"); c.commit(); c.close()
def log(user_id,action,detail=''):
 init_audit(); c=_db(); c.execute("INSERT INTO audit(user_id,action,detail,created_at) VALUES(?,?,?,?)",(user_id,action,detail,int(time.time()))); c.commit(); c.close()
def recent(limit=100):
 init_audit(); c=_db(); rows=c.execute("SELECT a.id,a.user_id,u.email,a.action,a.detail,a.created_at FROM audit a LEFT JOIN users u ON u.id=a.user_id ORDER BY a.id DESC LIMIT ?",(limit,)).fetchall(); c.close(); return [{"id":r[0],"user_id":r[1],"email":r[2],"action":r[3],"detail":r[4],"created_at":r[5]} for r in rows]
