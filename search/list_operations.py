import sys


# リストの二項演算 (仮)
# 今のところ集合演算による実装なので, 以下のことが許される場合しか使えない. 
#  1. リストに同一の要素が複数あり重複するときはただ1つの要素になる. 
#  2. リストの要素の順序は一般に保存されない. 

def l_or(l0, l1):
    # リストの和 (和集合から)
    return list(set(l0) | set(l1))

def l_and(l0, l1):
    # リストの積 (積集合から)
    return list(set(l0) & set(l1))

def l_diff(l0, l1):
    # リストの差 (差集合から)
    return list(set(l0) - set(l1))


# テスト実行例
if __name__ == '__main__':
    A = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    B = [2, 3, 5, 7, 11, 13, 17, 19]
    print('A = ' + str(A))
    print('B = ' + str(B) + '\n')
    
    print('l_or(A, B)  = ' + str(l_or(A, B)))
    print('l_and(A, B) = ' + str(l_and(A, B)) + '\n')
    
    print('l_diff(A, B) = ' + str(l_diff(A, B)))
    print('l_diff(B, A) = ' + str(l_diff(B, A)) + '\n')
