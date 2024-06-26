import pygame
from draw_chessboard import *
from pieces import *
from create_pieces import *
from copy import deepcopy as dc
from game_functions import *
pygame.init()



sc = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()
FPS = 30

WHITE = (250, 250, 250)
GREEN = (0, 128, 0)

chessboard(sc, WHITE, GREEN)

selected_piece = None
move_color = 'white'

all_pawns = create_pawns()
all_knights = create_knights()
all_bishops = create_bishops()
all_rooks = create_rooks()
all_queens = create_queens()
all_kings = create_kings()
all_pieces = all_pawns + all_knights + all_bishops + all_rooks + all_queens + all_kings

def draw_figures(all_pieces):
    chessboard(sc, WHITE, GREEN)
    for i in all_pieces:
        sc.blit(i.image, i.rect)
        pygame.display.flip()
draw_figures(all_pieces)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            figures_coordinates = [(i.x, i.y) for i in all_pieces]
            #print(check_mate(all_pieces, move_color, figures_coordinates)) 
            if selected_piece == None:
                for piece in all_pieces:
                    if piece.rect.collidepoint(pos):
                        selected_piece = piece if move_color == piece.color else None

            else:
                captured_piece = None
                new_x = pos[0] // 50
                new_y = pos[1] // 50
                if isinstance(selected_piece, Pawn):
                    for piece in all_pieces:
                        if isinstance(piece, Pawn):
                            if (piece.x == new_x and piece.y == new_y and piece.color != selected_piece.color) or (piece.get_enpassant() and piece.x == new_x and ((piece.y == new_y+1 and piece.color == 'black') or (piece.y == new_y-1 and piece.color == 'white'))):
                                captured_piece = piece
                        else:
                            if (piece.x == new_x and piece.y == new_y and piece.color != selected_piece.color):
                                captured_piece = piece
                    if simulate_move_and_check_king(selected_piece, new_x, new_y, all_pieces, figures_coordinates, captured_piece):
                        print('check')
                        selected_piece = None
                        continue                   
                    if not selected_piece.move(new_x, new_y, bool(captured_piece), figures_coordinates):
                        selected_piece = None
                        continue
                    if (selected_piece.color == 'black' and new_y == 7) or (selected_piece.color == 'white' and new_y == 0):
                        figure = promote_pawn_dialog(sc)
                        match figure:
                            case 'Queen':
                                all_pieces.append(Queen(new_x, selected_piece.color, y = new_y))
                            case 'Rook':
                                all_pieces.append(Rook(new_x, selected_piece.color, y = new_y))
                            case 'Bishop':
                                all_pieces.append(Bishop(new_x, selected_piece.color, y = new_y))
                            case 'Knight':
                                all_pieces.append(Knight(new_x, selected_piece.color, y = new_y))
                        all_pieces.remove(selected_piece)
                        all_pawns.remove(selected_piece)
                    if captured_piece:
                        all_pieces.remove(captured_piece)
                        if isinstance(captured_piece, Pawn): all_pawns.remove(captured_piece)
                        #if isinstance(captured_piece, Knight): all_knights.remove(captured_piece)
                    move_color = 'white' if move_color == 'black' else 'black'
                    selected_piece = None
                    draw_figures(all_pieces)
                    for pawn in all_pawns:
                        pawn.subbstract_enpassant()
                    continue
                elif isinstance(selected_piece, King):
                    coordinates = figures_coordinates
                    pieces = all_pieces
                    for piece in all_pieces:
                        if (piece.x == new_x and piece.y == new_y and piece.color != selected_piece.color):
                            is_defended = is_piece_defended(piece, all_pieces, figures_coordinates)
                            if not is_defended:
                                captured_piece = piece
                                coordinates = [i for i in figures_coordinates if i != (captured_piece.x, captured_piece.y)]
                                pieces = [i for i in all_pieces if i != captured_piece]

                    move_result = selected_piece.move(new_x, new_y, bool(captured_piece), coordinates, pieces)
                    if not move_result:
                        selected_piece = None
                        continue
                    if isinstance(move_result, str):
                        if move_result == 'short':
                            rook = [i for i in all_pieces if i.x == 7 and isinstance(i, Rook) and i.color == selected_piece.color][0]
                            rook.x = 5
                            rook.rect.topleft = (5 * 50, new_y * 50)
                        elif move_result == 'long':
                            rook = [i for i in all_pieces if i.x == 0 and isinstance(i, Rook) and i.color == selected_piece.color][0]
                            rook.x = 3
                            rook.rect.topleft = (3 * 50, new_y * 50)
                        move_color = 'white' if move_color == 'black' else 'black'
                        selected_piece = None
                        draw_figures(all_pieces)
                        for pawn in all_pawns:
                            pawn.subbstract_enpassant()
                        continue

                    move_color = 'white' if move_color == 'black' else 'black'
                    if captured_piece:
                        all_pieces.remove(captured_piece)
                    selected_piece = None
                    draw_figures(all_pieces)
                    for pawn in all_pawns:
                        pawn.subbstract_enpassant()
                    continue
                for piece in all_pieces:
                    if (piece.x == new_x and piece.y == new_y and piece.color != selected_piece.color):
                        captured_piece = piece
                        figures_coordinates.remove((captured_piece.x, captured_piece.y))


                if simulate_move_and_check_king(selected_piece, new_x, new_y, all_pieces, figures_coordinates, captured_piece):
                    print('check')
                    selected_piece = None
                    continue                   

                if not selected_piece.move(new_x, new_y, bool(captured_piece), figures_coordinates):
                    selected_piece = None
                    continue
                if isinstance(selected_piece, Rook):
                    king = [i for i in all_pieces if isinstance(i, King) and i.color == selected_piece.color][0]
                    if selected_piece.x == 0: king.long_castle = False
                    if selected_piece.x == 7: king.short_castle = False
                if captured_piece:
                    all_pieces.remove(captured_piece)
                    if isinstance(captured_piece, Pawn): all_pawns.remove(captured_piece)
                    #if isinstance(captured_piece, Knight): all_knights.remove(captured_piece)
                    #if isinstance(captured_piece, Bishop): all_bishops.remove(captured_piece)
                    #if isinstance(captured_piece, Rook): all_rooks.remove(captured_piece)
                move_color = 'white' if move_color == 'black' else 'black'
                selected_piece = None
                draw_figures(all_pieces)

    sc.fill((0, 0, 0))
    clock.tick(FPS)
