from bottle import default_app
from bottle import route, template, request, static_file
import db_functions as dbf

@route('/static/:filename#.*#')
def send_static(filename):
    return static_file(filename, root='./static/')

@route('/')
def index():
    index_dict = {'string': '', 'skipped': '', 'counter': dbf.get_counter(), 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}

    return template('/home/drewdavie/mysite/index.tpl', **index_dict)

@route('/new_string')
def new_string():

    if len(dbf.get_current_string()) > 0:
        index_dict = {'string': dbf.get_current_string() + '- Solve the current clue!', 'skipped': dbf.get_skipped_string(), 'counter': dbf.get_counter(), 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}
        return (template('/home/drewdavie/mysite/index.tpl', **index_dict))

    index_dict = {'string': dbf.get_new_string(), 'skipped': dbf.get_skipped_string(), 'counter': dbf.get_counter(), 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}

    return (template('/home/drewdavie/mysite/index.tpl', **index_dict))

@route('/skip_string')
def skip_string():

    if len(dbf.get_skipped_string()) > 0:
        index_dict = {'string': dbf.get_current_string(), 'skipped': dbf.get_skipped_string() + ' STOP TRYING TO SKIP TWICE.', 'counter': dbf.get_counter(), 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}
        return (template('/home/drewdavie/mysite/index.tpl', **index_dict))

    dbf.set_skipped_string()
    index_dict = {'string': dbf.get_current_string(), 'skipped': dbf.get_skipped_string(), 'counter': dbf.get_counter(), 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}

    return (template('/home/drewdavie/mysite/index.tpl', **index_dict))

@route('/guessed_string')
def guessed_string():

    if dbf.get_current_string == '':
        index_dict = {'string': '', 'skipped': dbf.get_skipped_string(), 'counter': dbf.get_counter(), 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}
        return (template('/home/drewdavie/mysite/index.tpl', **index_dict))

    dbf.set_guessed_string()
    index_dict = {'string': '', 'skipped': dbf.get_skipped_string(), 'counter': dbf.update_counter(), 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}

    return (template('/home/drewdavie/mysite/index.tpl', **index_dict))

@route('/guessed_skipped')
def guessed_skipped():

    if dbf.get_skipped_string() == '':
        index_dict = {'string': dbf.get_current_string(), 'skipped': '', 'counter': dbf.get_counter(), 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}
        return (template('/home/drewdavie/mysite/index.tpl', **index_dict))

    dbf.set_guessed_skipped_string()
    index_dict = {'string': dbf.get_current_string(), 'skipped': '', 'counter': dbf.update_counter(), 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}

    return (template('/home/drewdavie/mysite/index.tpl', **index_dict))

@route('/end_turn')
def end_turn():

    dbf.reset_clues()
    dbf.end_player_turn()
    dbf.reset_counter()
    index_dict = {'string': '', 'skipped': '', 'counter': '0', 'current_player': dbf.get_player()[0][1], 'score_table': dbf.get_scores()}

    return (template('/home/drewdavie/mysite/index.tpl', **index_dict))


@route('/admin')
def admin():
    return template('/home/drewdavie/mysite/admin.tpl')

@route('/admin/create_DB')
def create_db():
    dbf.create_db()
    return template('/home/drewdavie/mysite/admin.tpl')

@route('/admin/clean_DB')
def clean_db():
    dbf.clean_db()
    return template('/home/drewdavie/mysite/admin.tpl')

@route('/admin/delete_DB')
def delete_db():
    dbf.delete_db()

    return template('/home/drewdavie/mysite/admin.tpl')

@route('/admin/print_DB')
def print_db():
    dbf.print_db()

    return template('/home/drewdavie/mysite/admin.tpl')

@route('/submit')
def submit():
    return template('/home/drewdavie/mysite/submit.tpl', message='', player_message="")

@route('/submit_clue', method='POST')
def submit_string():

    if request.forms.get('string') == '':
        return template ('/home/drewdavie/mysite/submit.tpl', message="Clue cannot be blank.", player_message="")

    count_strings = dbf.count_strings()
    dbf.submit_string(request.forms.get('string'))

    return template('/home/drewdavie/mysite/submit.tpl', message="Clue submitted successfully. There are currently " + str(count_strings) + " clues.", player_message="")

@route('/submit_player', method='POST')
def submit_player():

    if request.forms.get('player') == '':
        return template ('/home/drewdavie/mysite/submit.tpl', message="", player_message="Player cannot be blank.")

    dbf.submit_player(request.forms.get('player'), request.forms.get('team'))

    return template('/home/drewdavie/mysite/submit.tpl', message="", player_message="Player submitted successfully.")

application = default_app()

