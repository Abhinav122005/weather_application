import bcrypt

def hash_pass(ip_password):
    return bcrypt.hashpw(ip_password.encode('utf-8'),bcrypt.gensalt(rounds=12)).decode('utf-8')

def check_pass(ip_password,db_password):
    return bcrypt.checkpw(ip_password.encode('utf-8'),db_password.encode('utf-8'))