# импортируем необходимые библиотеки
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# загружаем данные из файла
data = pd.read_csv("experiment_data.csv")

# разбиваем данные на две группы: контрольную и экспериментальную
control = data[data["group"] == "control"]
experiment = data[data["group"] == "experiment"]

# смотрим на основные статистики по каждой группе
control.describe()
experiment.describe()

# строим гистограммы распределения значений по каждой группе
plt.hist(control["value"], bins=20, alpha=0.5, label="control")
plt.hist(experiment["value"], bins=20, alpha=0.5, label="experiment")
plt.legend()
plt.show()

# проверяем нормальность распределений с помощью теста Шапиро-Уилка
control_shapiro = stats.shapiro(control["value"])
experiment_shapiro = stats.shapiro(experiment["value"])
print(f"p-value for control group: {control_shapiro[1]}")
print(f"p-value for experiment group: {experiment_shapiro[1]}")

# если p-value меньше 0.05, то отвергаем нулевую гипотезу о нормальности распределения
if control_shapiro[1] < 0.05:
    print("Control group is not normally distributed")
else:
    print("Control group is normally distributed")

if experiment_shapiro[1] < 0.05:
    print("Experiment group is not normally distributed")
else:
    print("Experiment group is normally distributed")

# выбираем подходящий статистический тест в зависимости от нормальности распределений
# если обе группы нормально распределены, то используем t-тест
# если хотя бы одна группа не нормально распределена, то используем U-тест Манна-Уитни
if control_shapiro[1] >= 0.05 and experiment_shapiro[1] >= 0.05:
    # используем t-тест
    ttest = stats.ttest_ind(control["value"], experiment["value"])
    print(f"p-value for t-test: {ttest[1]}")
    # если p-value меньше 0.05, то отвергаем нулевую гипотезу о равенстве средних
    if ttest[1] < 0.05:
        print("There is a significant difference between the means of the two groups")
    else:
        print("There is no significant difference between the means of the two groups")
else:
    # используем U-тест Манна-Уитни
    utest = stats.mannwhitneyu(control["value"], experiment["value"])
    print(f"p-value for U-test: {utest[1]}")
    # если p-value меньше 0.05, то отвергаем нулевую гипотезу о равенстве медиан
    if utest[1] < 0.05:
        print("There is a significant difference between the medians of the two groups")
    else:
        print("There is no significant difference between the medians of the two groups")