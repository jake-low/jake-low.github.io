class memoize:
  """Decorator for adding memoization to functions.

  Just stick @memoize in front of function definitions,
  and you're good to go.
  """
  def __init__(self, function):
    self.function = function
    self.store = {}

  def __call__(self, *args):
    key = (args)

    # call function to store value
    if not key in self.store:
      self.store[key] = self.function(*args)

    # return stored value
    return self.store[key]
