height_cm = float(input("키를 입력하세요(m)."))
weight = int(input("몸무게를 입력하세요(kg)."))

bmi = weight / (height_cm ** 2)
print("키가 {}m, 몸무게가{}kg이면, BMI는 {}입니다.".format(height_cm, weight, bmi))