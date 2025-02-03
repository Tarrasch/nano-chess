from position import Position, Move
import position
import math


def test_initial_position():
    pos = Position.new_startpos()

    assert pos.board.count("P") == 8
    assert pos.board.count("p") == 8


def test_white_up_by_pawn_after_latvian_gambit():
    pos = Position.new_startpos()
    pos = pos.move(Move.from_uci("e2e4"))
    pos = pos.move(Move.from_uci("f7f5").rotate())
    pos = pos.move(Move.from_uci("e4f5"))
    pos = pos.rotate()

    assert pos.board.count("P") == 8
    assert pos.board.count("p") == 7


inefficient_nn_cls = position.InefficientNeuralNetworkEvalPosition
nnue_cls = position.NeuralNetworkEvalPosition


def test_white_and_black_similar_score_startpos():
    pos_inefficient = inefficient_nn_cls.new_startpos()

    assert math.isclose(
        pos_inefficient.evaluation,
        -pos_inefficient.rotate().evaluation,
        abs_tol=10,
    )


def test_white_and_black_same_score_random_pos():
    pos_white_to_move = inefficient_nn_cls.from_fen(
        "r1b1kbnr/pppp1ppp/n7/4N3/1q1PP3/8/PPP2PPP/RNBQKB1R w KQkq - 1 5"
    )
    pos_black_to_move = inefficient_nn_cls.from_fen(
        "R1B1KBNR/PPPP1PPP/N7/4n3/1Q1pp3/8/ppp2ppp/rnbqkb1r b KQkq - 1 5"
    )

    assert math.isclose(
        pos_white_to_move.evaluation,
        -pos_black_to_move.evaluation,
        abs_tol=300,
    )


class TestNnueEfficientUpdates:
    start_fen = "r1b1kbnr/pppp1ppp/n7/4N3/1q1PP3/2P5/PP3PPP/RNBQKB1R b KQkq - 0 5"
    moves = [
        "d7d6",  # Just a move
        "c3b4",  # Pawn takes queen
        "a6b4",  # Knight takes pawn
        "d4d5",  # Just a move
        "c7c5",  # Allow en passant
        "d5c6",  # En passant
        "c8g4",  # Just a bishop move
        "c6c7",  # Just a move
        "g4d1",  # Bishop take queen
        "c7c8q",  # Pawn promotion to queen
        "a8c8",  # Take queen back
    ]

    def yield_all_positions_and_next_move(self):
        pos = nnue_cls.from_fen(self.start_fen)
        for next_move_ucistr in self.moves:
            next_move = Move.from_uci(next_move_ucistr)
            if pos.is_flipped_perspective:
                next_move = next_move.rotate()
            yield pos, next_move
            pos = pos.move(next_move)

    def test_nnue_efficient_updates_all_moves(self):
        for pos, move in self.yield_all_positions_and_next_move():
            pos_nnue = nnue_cls.from_fen(pos.to_fen())
            pos_inefficient = inefficient_nn_cls.from_fen(pos.to_fen())
            assert math.isclose(pos_nnue.evaluation, pos_inefficient.evaluation, abs_tol=0.1)
            pos_inefficient = pos_inefficient.move(move)
            pos_nnue = pos_nnue.move(move)
            assert math.isclose(pos_nnue.evaluation, pos_inefficient.evaluation, abs_tol=10)
