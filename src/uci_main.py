# Advanced UCI interface

import time
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from functools import partial
from position import Position, Move
from search import search_indefinetly


print = partial(print, flush=True)

current_pos: Position = Position.from_fen(
    fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)


def go_loop(position: Position, stop_event, max_movetime=0, max_depth=0, debug=False):
    if debug:
        print(f"Going movetime={max_movetime}, depth={max_depth}")

    start = time.time()
    for search_result in search_indefinetly(position):
        elapsed = time.time() - start
        move = search_result.move
        if position.is_flipped_perspective:
            move = move.rotate()
        fields = {
            "depth": search_result.depth,
            "time": round(1000 * elapsed),
            "nodes": search_result.nodes_visited,
            "nps": round(search_result.nodes_visited / elapsed),
            "score cp": f"{search_result.score} lowerbound",
            "pv": move.to_uci(),
        }
        print("info", " ".join(f"{k} {v}" for k, v in fields.items()))
        if search_result.depth >= max_depth:
            break

        # We may not have a move yet at depth = 1  # Arash: Not sure if its true for this engine flavor.
        if search_result.depth > 1:
            if elapsed > max_movetime * 0.15:
                break
            if stop_event.is_set():
                break

    print(f"bestmove {move.to_uci()}")


debug = False


def apply_uci_moves(position: Position, remaining_args) -> Position:
    if remaining_args:
        assert args[2] == "moves"
        for move_in_uci in args[3:]:
            move = Move.from_uci(move_in_uci)
            if position.is_flipped_perspective:
                move = move.rotate()
            position = position.move(move)

    return position


with ThreadPoolExecutor(max_workers=1) as executor:
    # Noop future to get started
    go_future = executor.submit(lambda: None)
    do_stop_event = Event()
    current_pos: Position = Position.new_startpos()

    while True:
        try:
            args = input().split()
            if not args:
                continue

            elif args[0] in ("stop", "quit"):
                if go_future.running():
                    if debug:
                        print("Stopping go loop...")
                    do_stop_event.set()
                    go_future.result()
                else:
                    if debug:
                        print("Go loop not running...")
                if args[0] == "quit":
                    break

            elif not go_future.done():
                print(f"Ignoring input {args}. Please call 'stop' first.")
                continue

            # Make sure we are really done, and throw any errors that may have
            # happened in the go loop.
            go_future.result(timeout=0)

            if args[0] == "uci":
                print("id name arre90-bot 0.0")  ## Parametrize
                print("uciok")

            elif args[0] == "isready":
                print("readyok")

            elif args[:2] == ["position", "startpos"]:
                current_pos = Position.new_startpos()
                current_pos = apply_uci_moves(current_pos, args[2:])

            elif args[:2] == ["position", "fen"]:
                current_pos = Position.from_fen(*args[2:8])
                current_pos = apply_uci_moves(current_pos, args[8:])

            elif args[0] == "go":
                think = 10**6
                max_depth = 100
                loop = go_loop

                if args[1:] == [] or args[1] == "infinite":
                    pass

                elif args[1] == "movetime":
                    movetime = args[2]
                    think = int(movetime) / 1000

                elif args[1] == "wtime":
                    wtime, btime, winc, binc = [int(a) / 1000 for a in args[2::2]]
                    # we always consider ourselves white, but uci doesn't
                    if current_pos.is_flipped_perspective:
                        wtime, winc = btime, binc
                    think = min(wtime / 40 + winc, wtime / 2 - 1)

                elif args[1] == "depth":
                    max_depth = int(args[2])

                do_stop_event.clear()
                go_future = executor.submit(
                    loop,
                    current_pos,
                    do_stop_event,
                    think,
                    max_depth,
                    debug=debug,
                )

                # Make sure we get informed if the job fails
                def callback(fut):
                    fut.result(timeout=0)

                go_future.add_done_callback(callback)

        except (KeyboardInterrupt, EOFError):
            if go_future.running():
                if debug:
                    print("Stopping go loop...")
                do_stop_event.set()
                go_future.result()
            break
