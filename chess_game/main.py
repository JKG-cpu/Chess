from game import Board

def main():
    board = Board()
    board.main()

def test_run():
    board = Board()
    board.check_if_king_checked()

if __name__ == '__main__':
    main()