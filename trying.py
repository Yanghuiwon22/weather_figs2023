word = input(str('단어를 입력하세요'))

word_sorted = [i for i in word]
word_back = word_sorted.copy()
word_back.reverse()


if 100 >= len(word_sorted) >= 1:
    if word_sorted == word_back:
        print(1)
    else:
        print(0)