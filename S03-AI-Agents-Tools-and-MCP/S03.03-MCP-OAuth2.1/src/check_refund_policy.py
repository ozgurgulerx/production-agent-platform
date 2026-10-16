



def check_refund_policy(principal, ticket, amount):
    if amount > 500:
        raise ValueError("execution_limit_exceeded")
   
    return 

check_refund_policy(None, None, 500)