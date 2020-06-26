from django.shortcuts import render, redirect
from django.http import HttpResponse

import json
import pickle
import random

import chess

from main.models import ChessBoard


def index(request):
    chess_boards = {'ChessBoards': [(x.id, pickle.loads(x.board)) for x in ChessBoard.objects.all()]}
    return render(request, 'index.html', chess_boards)


def make_random_move(request):
    chess_board_obj = ChessBoard.objects.get(id=request.POST.get('id'))
    chess_board = pickle.loads(chess_board_obj.board)
    legal_moves = list(chess_board.legal_moves)
    if chess_board.is_game_over():
        ChessBoard.objects.filter(id=request.POST.get('id')).delete()
        return redirect(index)
    random_index = random.randint(0, len(legal_moves)-1)
    chess_board.push(legal_moves[random_index])
    chess_board_obj.board = pickle.dumps(chess_board)
    chess_board_obj.save()
    response = {'FEN': chess_board.fen()}
    return HttpResponse(json.dumps(response), content_type='application/json')


def add_board(request):
    board = pickle.dumps(chess.Board())
    ChessBoard.objects.create(board=board)
    chess_boards = {'ChessBoards': [(x.id, pickle.loads(x.board)) for x in ChessBoard.objects.all()]}
    return redirect(index)
