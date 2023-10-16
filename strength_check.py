import re
import time

def pass_strength(password):
  
  strong_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_@$]).{8,}$"
  medium_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{5,}$"
  weak_pattern = r"^(?=.*[a-z]).{1,}$"

  strong_match = re.match(strong_pattern, password)
  medium_match = re.match(medium_pattern, password)
  weak_match = re.match(weak_pattern, password)

  if strong_match:
    return "Strong"
  elif medium_match:
    return "Intermediate"
  elif weak_match:
    return "Weak"
  else:
    return "Invalid"

def crack_time(password,cracking_speed):
  
  total_characters = len(set(password))
  estimated_time = (total_characters ** 8) / (cracking_speed / 60)
  days=estimated_time/1440
  
  return f"{round(days)} days"

