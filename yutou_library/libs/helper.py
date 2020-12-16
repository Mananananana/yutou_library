def get_legal_isbn(isbn):
    if len(isbn) == 10:
        return cal_10bit_isbn(isbn)
    elif len(isbn) == 13:
        return cal_13bit_isbn(isbn)
    return False


def cal_10bit_isbn(isbn):
    sum = 0
    for i in range(9):
        sum += (10 - i) * (ord(isbn[i]) - ord('0'))
    n = sum % 11
    if n == 10:
        end = 'X'
    elif n == 11:
        end = '0'
    else:
        end = str(n)
    return isbn[:9] + end


def cal_13bit_isbn(isbn):
    sum = 0
    for i in range(0, 11, 2):
        sum += ord(isbn[i]) - ord('0')
    for i in range(1, 13, 2):
        sum += 3 * (ord(isbn[i]) - ord('0'))
    return isbn[:12] + str(10 - sum % 10)


if __name__ == "__main__":
    print(get_legal_isbn("9787302555541"))
