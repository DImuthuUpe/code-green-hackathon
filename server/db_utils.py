""" Implements the data access layer methods. """

from sqlalchemy import text
from decimal import Decimal

def decimal_default(obj):
  """ Prepares decimal properties for serialization. """
  if isinstance(obj, Decimal):
      return float(obj)
  raise TypeError

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
  
  print result
  
  return result