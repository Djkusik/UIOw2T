from db import Database


class PlayerRankingRepository:
    def __init__(self, database: Database) -> None:
        self._database = database
        conn = self._database.get_conn()

        conn.execute("CREATE TABLE IF NOT EXISTS player_ranking(nick varchar(255) PRIMARY KEY UNIQUE,elo BIGINT)")

        conn.commit()

    def create_or_update(self, nick: str, elo: int):
        conn = self._database.get_conn()
        existing = self.read(nick,None)
        if existing:
            conn.execute("UPDATE player_ranking set elo = (?) where nick = (?)",
                      [elo, nick])
        else:
            conn.execute("INSERT INTO player_ranking(nick,elo) VALUES (?,?)",
                      [nick, elo])
        conn.commit()

    def read_all(self):
        conn = self._database.get_conn()
        cur = conn.cursor()
        cur.execute("select nick,elo from player_ranking")
        return cur.fetchall()

    def read(self, nick,default_points):
        conn = self._database.get_conn()
        cur = conn.cursor()
        cur.execute("select elo from player_ranking where nick = (?)", [nick])
        result = cur.fetchone()
        if result:
            return result[0]
        elif default_points:
            return default_points

