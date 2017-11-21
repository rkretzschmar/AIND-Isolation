"""
    Finish all TODO items in this file to complete the isolation project, then
    test your agent's strength against a set of known agents using tournament.py
    and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def look_ahead_moves(game, moves):
    """
        Extends each move from the passed moves in each direction, filters the
        resulting list and returns only legal moves

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        moves : list<(int, int)>
            A list of moves

        Returns
        -------
        list<(int, int)>
            A list of legal look ahead moves.
    """
    move_directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                     (1, -2), (1, 2), (2, -1), (2, 1)]
    
    return [(r + dr, c + dc)
            for r, c in moves
            for dr, dc in move_directions
            if game.move_is_legal((r + dr, c + dc))]


def opponent_distance(location, other_location):
    """
        Calculates the distances between the a location and another location.

        Parameters
        ----------
        location : (int, int)
            A location
        other_location: (int, int)
            Another location

        Returns
        -------
        float
            The distance between a location and anoter location 
    """
    h, w = location
    ho, wo = other_location
    return float((h - ho)**2 + (w - wo)**2)

def blocking_moves(own_moves, opp_moves):
    """
        From two lists of moves it calculates a new list with identicsal moves

        Parameters
        ----------
        location : list<(int, int)>
            A list of moves
        other_location: list<(int,int)>
            Another list of moves

        Returns
        -------
        list<(int, int)>
            A list of the moves that are in both lists.
    """
    return set(own_moves) & set(opp_moves)

def occupation(game):
    """
        Calculates the relation between occupied spaces and all spaces
        
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        Returns
        -------
        float
            The occupation rate
    """
    all_spaces = game.width * game.height
    occupied_spaces = all_spaces - len(game.get_blank_spaces())
    return float(occupied_spaces / all_spaces)


def custom_score(game, player):
    """
        Calculate the heuristic value of a game state from the point of view
        of the given player.

        This should be the best heuristic function for your project submission.

        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)

    own_la_moves = look_ahead_moves(game, own_moves)
    opp_la_moves = look_ahead_moves(game, opp_moves)

    own_blocking_moves = blocking_moves(own_moves, opp_moves)
    opp_blocking_moves = blocking_moves(opp_moves, own_la_moves)    

    o = occupation(game)

    return float(len(own_la_moves) - len(opp_la_moves) 
                    + (len(own_blocking_moves) - len(opp_blocking_moves)) * o)


def custom_score_2(game, player):
    """
        Calculate the heuristic value of a game state from the point of view
        of the given player.

        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)

    own_blocking_moves = blocking_moves(own_moves, opp_moves)
    o = occupation(game)

    return float(len(own_moves) - len(opp_moves) + len(own_blocking_moves) * o)


def custom_score_3(game, player):
    """
        Calculate the heuristic value of a game state from the point of view
        of the given player.

        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    yo, xo = game.get_player_location(player)
    own_center_distance = float((h - y)**2 + (w - x)**2)
    opp_center_distance = float((h - y)**2 + (w - x)**2)

    o = occupation(game)

    return float(len(own_moves) - len(opp_moves) + (own_center_distance - opp_center_distance) / o)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """
            Implement depth-limited minimax search algorithm as described in
            the lectures.

            This should be a modified version of MINIMAX-DECISION in the AIMA text.
            https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

            **********************************************************************
                You MAY add additional methods to this class, or define helper
                    functions to implement the required functionality.
            **********************************************************************

            Parameters
            ----------
            game : isolation.Board
                An instance of the Isolation game `Board` class representing the
                current game state

            depth : int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting

            Returns
            -------
            (int, int)
                The board coordinates of the best move found in the current search;
                (-1, -1) if there are no legal moves

            Notes
            -----
                (1) You MUST use the `self.score()` method for board evaluation
                    to pass the project tests; you cannot call any other evaluation
                    function directly.

                (2) If you use any helper functions (e.g., as shown in the AIMA
                    pseudocode) then you must copy the timer check into the top of
                    each helper function or else your agent will timeout during
                    testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float('-inf')
        best_move = (-1, -1)

        for move in game.get_legal_moves():
            moved_game = game.forecast_move(move)
            move_score = self.min_value(moved_game, depth - 1)
            if move_score > best_score:
                best_move = move
                best_score = move_score

        return best_move

    def max_value(self, game, depth):
        """
            Calculates the game state's best value from the players perspective.

            Parameters
            ----------
            game : isolation.Board
                An instance of the Isolation game `Board` class representing the
                current game state

            depth : int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting

            Returns
            -------
            float
                The game state's best value from the players perspective.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if len(legal_moves) == 0 or depth == 0:
            return self.score(game, self)

        best_value = float('-inf')

        for move in legal_moves:
            moved_game = game.forecast_move(move)
            best_value = max(best_value, self.min_value(moved_game, depth - 1))

        return best_value

    def min_value(self, game, depth):
        """
            Calculates the game state's best value from the opponents perspective.

            Parameters
            ----------
            game : isolation.Board
                An instance of the Isolation game `Board` class representing the
                current game state

            depth : int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting

            Returns
            -------
            float
                The game state's best value from the opponents perspective.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if len(legal_moves) == 0 or depth == 0:
            return self.score(game, self)

        best_value = float('inf')
        for move in legal_moves:
            moved_game = game.forecast_move(move)
            best_value = min(best_value, self.max_value(moved_game, depth - 1))

        return best_value


class AlphaBetaPlayer(IsolationPlayer):
    """
        Game-playing agent that chooses a move using iterative deepening minimax
        search with alpha-beta pruning. You must finish and test this player to
        make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """
            Search for the best move from the available legal moves and return a
            result before the time limit expires.

            Modify the get_move() method from the MinimaxPlayer class to implement
            iterative deepening search instead of fixed-depth search.

            **********************************************************************
            NOTE: If time_left() < 0 when this function returns, the agent will
                forfeit the game due to timeout. You must return _before_ the
                timer reaches 0.
            **********************************************************************

            Parameters
            ----------
            game : `isolation.Board`
                An instance of `isolation.Board` encoding the current state of the
                game (e.g., player locations and blocked cells).

            time_left : callable
                A function that returns the number of milliseconds left in the
                current turn. Returning with any less than 0 ms remaining forfeits
                the game.

            Returns
            -------
            (int, int)
                Board coordinates corresponding to a legal move; may return
                (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        depth = self.search_depth

        # Increase the search depth by 1 until the search times out
        try:
            while(True):
                best_move = self.alphabeta(game, depth)
                depth += 1
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """
            Implement depth-limited minimax search with alpha-beta pruning as
            described in the lectures.

            This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
            https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

            **********************************************************************
                You MAY add additional methods to this class, or define helper
                    functions to implement the required functionality.
            **********************************************************************

            Parameters
            ----------
            game : isolation.Board
                An instance of the Isolation game `Board` class representing the
                current game state

            depth : int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting

            alpha : float
                Alpha limits the lower bound of search on minimizing layers

            beta : float
                Beta limits the upper bound of search on maximizing layers

            Returns
            -------
            (int, int)
                The board coordinates of the best move found in the current search;
                (-1, -1) if there are no legal moves

            Notes
            -----
                (1) You MUST use the `self.score()` method for board evaluation
                    to pass the project tests; you cannot call any other evaluation
                    function directly.

                (2) If you use any helper functions (e.g., as shown in the AIMA
                    pseudocode) then you must copy the timer check into the top of
                    each helper function or else your agent will timeout during
                    testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_value = float('-inf')
        new_alpha = alpha

        best_move = (-1, -1)

        for move in game.get_legal_moves():
            moved_game = game.forecast_move(move)
            move_score = self.min_value(
                moved_game, depth - 1, new_alpha, beta)
            if move_score > best_value:
                best_move = move
                best_value = move_score

            if best_value >= beta:
                break

            new_alpha = max(new_alpha, best_value)

        return best_move

    def max_value(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """
            Calculates the game state's best value from the players perspective.

            Parameters
            ----------
            game : isolation.Board
                An instance of the Isolation game `Board` class representing the
                current game state

            depth : int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting
            
            alpha : float
                The minimum score the player is assured of

            beta : float
                The maximum score the opponent is assured of

            Returns
            -------
            float
                The game state's best value from the players perspective.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        # if TERMINAL-TEST(state) then return UTILITY(state)
        if len(legal_moves) == 0 or depth == 0:
            return self.score(game, self)

        # v ← −∞
        best_value = float('-inf')

        new_alpha = alpha

        # for each a in ACTIONS(state) do
        for move in legal_moves:
            moved_game = game.forecast_move(move)

            # v ← MAX(v, MIN-VALUE(RESULT(state, a), α, β))
            best_value = max(best_value, self.min_value(
                moved_game, depth - 1, new_alpha, beta))

            # if v ≥ β then return v
            if best_value >= beta:
                break

            # α ← MAX(α, v)
            new_alpha = max(new_alpha, best_value)

        # return v
        return best_value

    def min_value(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """
            Calculates the game state's best value from the opponents perspective.

            Parameters
            ----------
            game : isolation.Board
                An instance of the Isolation game `Board` class representing the
                current game state

            depth : int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting

            alpha : float
                The minimum score the player is assured of

            beta : float
                The maximum score the opponent is assured of                

            Returns
            -------
            float
                The game state's best value from the opponents perspective.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        # if TERMINAL-TEST(state) then return UTILITY(state)
        if len(legal_moves) == 0 or depth == 0:
            return self.score(game, self)
        
        # v ← +∞
        best_value = float('inf')

        new_beta = beta

        # for each a in ACTIONS(state) do
        for move in legal_moves:
            moved_game = game.forecast_move(move)
            # v ← MIN(v, MAX-VALUE(RESULT(state, a), α, β))
            best_value = min(best_value, self.max_value(
                moved_game, depth - 1, alpha, new_beta))
            # if v ≤ α then return v
            if best_value <= alpha:
                break

            # β ← MIN(β, v)
            new_beta = min(new_beta, best_value)

        # return v
        return best_value
