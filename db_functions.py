import sqlite3 as sq

def get_current_string():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('SELECT string FROM tbl_strings WHERE isCurrent = ?', ('Y'))
    record = cur.fetchall()

    if record:
        current_string = record[0][0]
    else:
        current_string = ''
		
	conn.commit()
    conn.close()
    return current_string

def get_skipped_string():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('SELECT string FROM tbl_strings WHERE skipped = ?', ('Y'))
    record = cur.fetchall()

    if record:
        skipped_string = record[0][0]
    else:
        skipped_string = ''
		
	conn.commit()
    conn.close()
    return skipped_string

def get_new_string():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('SELECT stringID, string FROM tbl_strings WHERE skipped = ? AND r1 = ? ORDER BY random() LIMIT 1 ', ('N', 'N'))
    record = cur.fetchall()

    if record:
        stringID = record[0][0]
        new_string = record[0][1]
        cur.execute('UPDATE tbl_strings SET isCurrent = ? WHERE stringID = ?', ('Y', stringID))
    else:
        new_string = 'Round Complete!'

    conn.commit()
    conn.close()
    return new_string

def set_skipped_string():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('UPDATE tbl_strings SET skipped = ?, isCurrent = ? WHERE isCurrent = ?', ('Y', 'N', 'Y'))
    conn.commit()
    conn.close()
    return

def set_guessed_string():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('UPDATE tbl_strings SET r1 = ?, isCurrent = ? WHERE isCurrent = ?', ('Y', 'N', 'Y'))
    conn.commit()
    conn.close()
    return

def set_guessed_skipped_string():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('UPDATE tbl_strings SET r1 = ?, skipped = ? WHERE skipped = ?', ('Y', 'N', 'Y'))
    conn.commit()
    conn.close()
    return

def update_counter():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('SELECT count FROM tbl_turns')
    record = cur.fetchall()
    
	counter = record[0][0]
    counter = counter + 1
    cur.execute('UPDATE tbl_turns SET count = ?', (counter,))
	
    conn.commit()
    conn.close()
    return counter

def get_counter():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()

    cur.execute('SELECT count FROM tbl_turns')
    record = cur.fetchall()
    counter = record[0][0]

    conn.commit()
    conn.close()
    return counter

def reset_counter():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('UPDATE tbl_turns SET count = ?', (0,))
    conn.commit()
    conn.close()

def reset_clues():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('UPDATE tbl_strings SET isCurrent = ?, skipped = ? WHERE isCurrent = ? or skipped = ?', ('N', 'N', 'Y', 'Y'))
    conn.commit()
    conn.close()

def create_db():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS tbl_strings (stringID INTEGER PRIMARY KEY, string TEXT, r1 TEXT, r2 TEXT, r3 TEXT, skipped TEXT, isCurrent TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS tbl_players (stringID INTEGER PRIMARY KEY, name TEXT, team TEXT, score INTEGER, turns INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS tbl_turns (stringID INTEGER PRIMARY KEY, count INTEGER)')
    cur.execute('INSERT INTO tbl_turns (count) VALUES (?)', (0,))
    conn.commit()
    conn.close()

def clean_db():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('UPDATE tbl_strings SET skipped = ?, isCurrent = ?, r1 = ?', ('N', 'N', 'N'))
    conn.commit()
    conn.close()

def delete_db():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM tbl_strings')
    cur.execute('DELETE FROM tbl_players')
    cur.execute('DELETE FROM tbl_turns')
    conn.commit()
    conn.close()

def submit_string(string):

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO tbl_strings (string, r1, r2, r3, skipped, isCurrent) VALUES (?,?,?,?,?,?)', (string, 'N', 'N', 'N', 'N', 'N'))
    conn.commit()
    conn.close()

def count_strings():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT() FROM tbl_strings')
    count_strings = cur.fetchone()[0]

    conn.commit()
    conn.close()
    return count_strings

def submit_player(player, team):

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO tbl_players (name, team, score, turns) VALUES (?,?,?,?)', (player,team, 0, 0))
    conn.commit()
    conn.close()

def get_player():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    # select the next player by selecting the player with the fewest turns from the team with the fewest cumulative teams
    cur.execute('SELECT stringID, name, turns, score FROM tbl_players WHERE team IN (SELECT team FROM tbl_players GROUP BY team ORDER BY SUM(turns) ASC LIMIT 1) GROUP BY turns ORDER BY turns ASC LIMIT 1')
    record = cur.fetchall()

    conn.commit()
    conn.close()
    return record

def end_player_turn():

    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
    current_player = get_player()
    current_player_turns = current_player[0][2] + 1
    current_player_score = current_player[0][3] + get_counter()
    cur.execute('UPDATE tbl_players SET turns = ?, score = ? WHERE stringID = ?', (current_player_turns, current_player_score, current_player[0][0]))

    conn.commit()
    conn.close()

def get_scores():

    # get the scores of teams and individuals and format into an HTML table returned on the index page
    conn = sq.connect('/home/drewdavie/mysite/strings.db')
    cur = conn.cursor()
	
    cur.execute('SELECT name, turns, score, team from tbl_players ORDER BY team')
    individual_scores = cur.fetchall()
    cur.execute('SELECT SUM(score), team FROM tbl_players GROUP BY score')
    team_scores = cur.fetchall()

    conn.commit()
    conn.close()

    table = []
    table_header = '<table><tr><td>Player</td><td>Turns</td><td>Score</td><td>Team</td></tr>'
    table.append(table_header)

    for team_score in team_scores:
        table_row = '<tr><td></td><td></td><td>' + str(team_score[0]) + '</td><td>' + str(team_score[1]) + '</td></tr>'
        table.append(table_row)

    for individual_score in individual_scores:
        table_row = '<tr><td>' + str(individual_score[0]) + '</td><td>' + str(individual_score[1]) + '</td><td>' + str(individual_score[2]) + '</td><td>' + str(individual_score[3]) + '</td></tr>'
        table.append(table_row)

    table_end = '</table>'
    table.append(table_end)
    table = ''.join(map(str, table))
    return table

