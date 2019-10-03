from GameState import GameState
from copy import deepcopy

class Engine:
  # Constant
  INF = float('inf')
  WEIGHTS = [
      [ 4, -3,  2,  2,  2,  2, -3,  4],
      [-3, -4, -1, -1, -1, -1, -4, -3],
      [ 2, -1,  1,  0,  0,  1, -1,  2],
      [ 2, -1,  0,  1,  1,  0, -1,  2],
      [ 2, -1,  0,  1,  1,  0, -1,  2],
      [ 2, -1,  1,  0,  0,  1, -1,  2],
      [-3, -4, -1, -1, -1, -1, -4, -3],
      [ 4, -3,  2,  2,  2,  2, -3,  4]
  ]
  DEBUG_MODE = False

  # Depth Variable (default = 1)
  PLY_AB = 1

  def debug_message(self, ply, value):
    if (self.DEBUG_MODE):
      message = ""
      for x in range(self.PLY_AB-ply): message += "    "
      message += str(value)
      print(message)

  def get_move(self, state, color):
    score, move = self.mini_max_with_alpha_beta(self, state, color, self.PLY_AB)
    return move

  def get_cost(state, color):
    op_piece_count = state.count(not color)
    my_piece_count = state.count(color)

    return my_piece_count - op_piece_count

  def corner_weight(self, state, color):
    total_weight = 0
    for i in range(8):
      for j in range(8):
        weight = self.WEIGHTS[i][j]
        if (not color): weight = -weight
        total_weight += weight
    return total_weight

  def heuristics(self, state, color):
    return self.corner_weight(self, state, color) + self.get_cost(state, color)

  def mini_max_with_alpha_beta(self, state, color, ply):
    # Initialization
    best_move = state.moves[int(color)][0]
    best_score = -self.INF

    # Algorithm
    for move in state.moves[int(color)]:
      new_state = deepcopy(state)
      new_state.putpiece(move[0], move[1])
      score = self.min_alpha_beta(self, new_state, not color, ply-1, -self.INF, self.INF)
      if score > best_score:
        best_score = score
        best_move = move

    self.debug_message(self, ply, best_score)
    return (best_score, best_move)

  def max_alpha_beta(self, state, color, ply, alpha, beta):
    if ply == 0:
      self.debug_message(self, ply, self.heuristics(self, state, color))
      return self.heuristics(self, state, color)
    else:
      best_score = -self.INF
      for move in state.moves[int(color)]:
        new_state = deepcopy(state)
        new_state.putpiece(move[0], move[1])
        score = self.min_alpha_beta(self, new_state, not color, ply-1, alpha, beta)
        if score > best_score:
          best_score = score
        # break because only there's only one possible score of possible moves
        if best_score >= beta:
          self.debug_message(self, ply, best_score)
          return best_score
        alpha = max(alpha, best_score)
      self.debug_message(self, ply, best_score)
      return best_score

  def min_alpha_beta(self, state, color, ply, alpha, beta):
    if ply == 0:
      self.debug_message(self, ply, self.heuristics(self, state, color))
      return self.heuristics(self, state, color)
    else:
      best_score = self.INF
      for move in state.moves[int(color)]:
        new_state = deepcopy(state)
        new_state.putpiece(move[0], move[1])
        score = self.max_alpha_beta(self, new_state, not color, ply-1, alpha, beta)
        if score < best_score:
          best_score = score
        # break because only there's only one possible score of possible moves
        if best_score <= alpha:
          self.debug_message(self, ply, best_score)
          return best_score
        beta = min(beta, best_score)
      self.debug_message(self, ply, best_score)
      return best_score