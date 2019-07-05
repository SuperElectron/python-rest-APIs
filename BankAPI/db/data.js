db.users.insert(
    {
        "Username": "BANK",
        "Password": bcrypt.hashpw(bankPassword.encode('utf8'), bcrypt.gensalt()),
        "Own": 0,
        "Debt": 0}    
    
);