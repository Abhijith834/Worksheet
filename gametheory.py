def minimax( node , depth , maximizing_player ) :
    if depth == 0 or not node [ 'children'] :
        return node [ 'value']
    if maximizing_player :
        max_eval = float ( '-inf')
        for child in node [ 'children'] :
            eval = minimax ( child , depth - 1 , False )
            max_eval = max ( max_eval , eval )
        return max_eval
    else :
        min_eval = float ( 'inf')
        for child in node [ 'children'] :
            eval = minimax ( child , depth - 1 , True )
            min_eval = min ( min_eval , eval )
        return min_eval


def alpha_beta (node , depth , alpha , beta , maximizing_player) :
    if depth == 0 or not node [ 'children'] :
        return node [ 'value']
    if maximizing_player :
        max_eval = float ( '-inf')
        for child in node [ 'children'] :
            eval = alpha_beta ( child , depth - 1 , alpha , beta , False )
            max_eval = max ( max_eval , eval )
            alpha = max ( alpha , eval )
            if beta <= alpha :
                break # Beta cut - off
        return max_eval
    else :
        min_eval = float ( 'inf')
        for child in node [ 'children'] :
            eval = alpha_beta ( child , depth - 1 , alpha , beta , True )
            min_eval = min ( min_eval , eval )
            beta = min ( beta , eval )
            if beta <= alpha :
                break # Alpha cut - off
        return min_eval


# Define the game tree
tree = {
    'value': None , 'children': [
        { 'value': None , 'children': [
            { 'value': 5 , 'children': [ ] } ,
            { 'value': 3 , 'children': [ ] }
        ] } ,
        { 'value': None , 'children': [
            { 'value': 5 , 'children': [ ] } ,
            { 'value': 9 , 'children': [ ] }
        ] },
        { 'value': None , 'children': [
            { 'value': 11 , 'children': [ ] } ,
            { 'value': 9 , 'children': [ ] }
        ] }
    ]
}
# C a l c u l a t e the optimal value at the root
print(f"Optimal value at the root : { minimax ( tree , 2 , True ) } " )

print(f"Optimal value at the root with alpha-beta pruning: {alpha_beta(tree, 2, float('-inf'), float('inf'), True)}")


import random
def count_pi ( n ) :
    i = 0
    count = 0
    while i < n :
        x = random . random ()
        y = random . random ()
        if ( pow (x , 2 ) + pow (y , 2 ) ) < 1 :
            count += 1
        i += 1
    return 4 * ( count / n )
pi = count_pi ( 10000000 )
print (pi)
