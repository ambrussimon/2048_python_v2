import time
from app import app, db, database_2048
from app.models import Game_obj
from game import *
from flask import request, render_template, jsonify
from datetime import datetime, timedelta


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/api/new_game')
def new_game():
    now = datetime.now()
    expires_at = now + timedelta(hours=3)
    b = Game(board=None, c_score=0)
    uId = str(time.time())
    b.add_number()
    board = b.x
    c_score = b.c_score
    game_obj = Game_obj(uId=uId, c_score=c_score, board=board, expires_at=expires_at)
    game_data = {"board": board, "c_score": c_score, "uId": uId}
    game_dict = jsonify(game_data)
    db.session.add(game_obj)
    db.session.commit()
    return game_dict


@app.route('/api/play_the_game', methods=['POST', 'GET'])
def play_the_game():
    resp = request.get_json()
    uId = str(resp['uId'])
    direction = resp['direction']
    z = Game_obj.query.filter_by(uId=uId).first()
    b = Game(board=z.board, c_score=z.c_score)
    board = b.x
    moved = b.process_move(direction)
    legit = b.next_step_check()
    c_score = b.c_score
    if legit:
        if moved and b.count_zeroes() != 0:
            b.add_number()
            Game_obj.query.filter_by(uId=uId).update(dict(board=board))
            Game_obj.query.filter_by(uId=uId).update({"c_score": c_score})
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            db.session.commit()
            return game_dict
        elif moved:
            Game_obj.query.filter_by(uId=uId).update(dict(board=board))
            Game_obj.query.filter_by(uId=uId).update({"c_score": c_score})
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            db.session.commit()
            return game_dict
        else:
            Game_obj.query.filter_by(uId=uId).update(dict(board=board))
            Game_obj.query.filter_by(uId=uId).update({"c_score": c_score})
            game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": False}
            game_dict = jsonify(game_data)
            db.session.commit()
            return game_dict
    game_data = {"board": board, "c_score": c_score, "uId": uId, "game_over": True}
    game_dict = jsonify(game_data)
    return game_dict


@app.route('/save_user_highscore', methods=['POST', 'GET'])
def save_user_highscore():
    resp = request.get_json()
    u_name = resp['u_name']
    c_score = resp['c_score']
    database_2048.save_to_scores_db(u_name, c_score)
    msg = "Saved!"
    return msg


@app.route('/api/high_scores')
def games():
    scores = database_2048.get_high_scores_from_db()
    return jsonify(scores)
