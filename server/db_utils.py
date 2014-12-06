""" Implements the data access layer methods. """

from sqlalchemy import text

def run_query(db, query, multi=False):
  """ Executes a query passed in as a string. 
  Args:
    multi: Append row items if True, entire row otherwise.
    
  Returns:
    A list of results.
  """
  result = []
  connection = db.engine.connect()
  rows = connection.execute(text(query))
  for c in rows:
    if multi:
      result.append(dict(c.items()))
    else:
      result.append(dict(c))
  connection.close()
  
  return result