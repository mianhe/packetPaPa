_is_log_open = False

def log(log_str):
    pass
    global _is_log_open
    if _is_log_open:
        print log_str

def open_log():
    global _is_log_open
    _is_log_open = True
        
def close_log():
    global _is_log_open
    _is_log_open = False
