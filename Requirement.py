class Requirement:
  def __init__(self):
    self.t_postyp = -1
    self.t_start_service = -1
    self.t_end_service = -1

  def set_t_postyp(self, t):
    self.t_postyp = t

  def set_t_start(self, t):
    self.t_start_service = t

  def set_t_end(self, t):
    self.t_end_service = t

  def get_t_postyp(self):
    return self.t_postyp

  def get_t_start(self):
    return self.t_start_service

  def get_t_end(self):
    return self.t_end_service