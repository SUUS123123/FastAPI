import math
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# Задача 1
def predict_logistic(x1, x2, w1, w2, b, threshold=0.5):
    z = w1 * x1 + w2 * x2 + b
    p = 1 / (1 + math.exp(-z))
    answer = 1 if p >= threshold else 0
    return z, p, answer


def task_1():
    print("Задача 1. Логистическая регрессия")
    objects = [(1, 1), (2, 1), (0, 2), (3, 0)]

    for x1, x2 in objects:
        z, p, answer_05 = predict_logistic(x1, x2, 1.2, -0.8, -0.5)
        answer_07 = predict_logistic(x1, x2, 1.2, -0.8, -0.5, 0.7)[2]
        print(
            f"Объект ({x1}, {x2}): z={z:.4f}, p={p:.4f}, "
            f"класс при t=0.5: {answer_05}, при t=0.7: {answer_07}"
        )

    print("При смене порога меняется граница класса. В этих данных ответы не изменились.")


# Задача 2
def gini(labels):
    if len(labels) == 0:
        return 0

    p0 = labels.count(0) / len(labels)
    p1 = labels.count(1) / len(labels)
    return 1 - p0**2 - p1**2


def task_2():
    print("Задача 2. Индекс Джини")
    data = [
        {"age": 20, "class": 0},
        {"age": 22, "class": 0},
        {"age": 25, "class": 1},
        {"age": 28, "class": 1},
        {"age": 30, "class": 1},
        {"age": 35, "class": 0},
    ]

    all_classes = [item["class"] for item in data]
    left = [item["class"] for item in data if item["age"] <= 26]
    right = [item["class"] for item in data if item["age"] > 26]
    split_gini = len(left) / len(data) * gini(left) + len(right) / len(data) * gini(right)

    print("Gini до разделения:", round(gini(all_classes), 4))
    print("Gini левого узла:", round(gini(left), 4))
    print("Gini правого узла:", round(gini(right), 4))
    print("Взвешенный Gini:", round(split_gini, 4))
    print("Узлы нужно взвешивать по количеству объектов, потому что их размеры могут отличаться.")


# Задача 3
def average(numbers):
    return sum(numbers) / len(numbers)


def sse(numbers):
    middle = average(numbers)
    total = 0
    for number in numbers:
        total += (number - middle) ** 2
    return total


def task_3():
    print("Задача 3. Дерево регрессии")
    data = [(20, 4), (25, 5), (30, 6), (50, 12), (55, 13), (60, 14)]

    for threshold in [40, 52.5]:
        left = [price for area, price in data if area <= threshold]
        right = [price for area, price in data if area > threshold]
        error = sse(left) + sse(right)
        print(
            f"Порог {threshold}: среднее слева {average(left):.2f}, "
            f"среднее справа {average(right):.2f}, SSE={error:.2f}"
        )

    print("Лучший порог — 40. Среднее используется, потому что оно дает наименьшую SSE.")


# Задача 4
def majority_vote(votes):
    ones = votes.count(1)
    zeros = votes.count(0)

    if ones > zeros:
        return 1
    if zeros > ones:
        return 0
    return None


def get_ensemble(models):
    result = []
    for object_number in range(len(models[0])):
        votes = [model[object_number] for model in models]
        result.append(majority_vote(votes))
    return result


def task_4():
    print("Задача 4. Bagging")
    predictions = [
        [1, 0, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0],
        [1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0],
    ]

    result = get_ensemble(predictions)
    print("Ответы ансамбля:", result)

    changed_predictions = [row.copy() for row in predictions]
    changed_predictions[0][3] = 0
    new_result = get_ensemble(changed_predictions)
    changed = []
    for i in range(len(result)):
        if result[i] != new_result[i]:
            changed.append(i + 1)
    print("После изменения одного ответа поменялись объекты:", changed)


# Задача 5
def get_classes(probabilities, threshold):
    answers = []
    for probability in probabilities:
        answers.append(1 if probability >= threshold else 0)
    return answers


def get_metrics(y_true, y_pred):
    tp = tn = fp = fn = 0

    for actual, predicted in zip(y_true, y_pred):
        if actual == 1 and predicted == 1:
            tp += 1
        elif actual == 0 and predicted == 0:
            tn += 1
        elif actual == 0 and predicted == 1:
            fp += 1
        else:
            fn += 1

    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    return tp, tn, fp, fn, accuracy, precision, recall


def task_5():
    print("Задача 5. Как порог влияет на классификацию")
    probabilities = [0.12, 0.28, 0.41, 0.49, 0.52, 0.67, 0.73, 0.91]
    y_true = [0, 0, 1, 0, 1, 1, 0, 1]

    for threshold in [0.3, 0.5, 0.7]:
        y_pred = get_classes(probabilities, threshold)
        tp, tn, fp, fn, accuracy, precision, recall = get_metrics(y_true, y_pred)
        print("\nПорог:", threshold)
        print("Предсказания:", y_pred)
        print(f"TP={tp}, TN={tn}, FP={fp}, FN={fn}")
        print(f"Accuracy={accuracy:.2f}, Precision={precision:.2f}, Recall={recall:.2f}")

    print("При увеличении порога положительных ответов становится меньше.")


# Задача 6
def task_6():
    print("Задача 6. Лучшее разделение дерева классификации")
    data = [(2, 0), (3, 0), (4, 1), (5, 0), (6, 1), (7, 1), (8, 1), (9, 0)]
    results = []

    for threshold in [3.5, 4.5, 5.5, 6.5, 7.5, 8.5]:
        left = [label for x, label in data if x <= threshold]
        right = [label for x, label in data if x > threshold]
        split_gini = len(left) / len(data) * gini(left) + len(right) / len(data) * gini(right)
        results.append((threshold, split_gini))
        print(f"Порог {threshold}: взвешенный Gini={split_gini:.4f}")

    best = min(results, key=lambda item: item[1])
    print(f"Лучший порог: {best[0]}, Gini={best[1]:.4f}")


# Задача 7
def task_7():
    print("Задача 7. Регуляризация дерева")
    models = [
        {"depth": 1, "train_error": 0.22, "validation_error": 0.25},
        {"depth": 2, "train_error": 0.14, "validation_error": 0.17},
        {"depth": 4, "train_error": 0.05, "validation_error": 0.13},
        {"depth": 8, "train_error": 0.00, "validation_error": 0.21},
    ]

    best = min(models, key=lambda item: item["validation_error"])
    print("Данные моделей:", models)
    print("Лучшая глубина:", best["depth"])

    for model in models:
        if model["train_error"] == 0:
            print("Ошибка на обучении равна нулю при глубине:", model["depth"])


# Задача 8
def task_8():
    print("Задача 8. Сравнение Bagging и одной модели")
    y_true = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    single_model = [1, 1, 1, 0, 0, 0, 1, 0, 0, 0]
    models = [
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
    ]

    ensemble = get_ensemble(models)
    single_right = 0
    ensemble_right = 0
    improved = []
    worsened = []

    for i in range(len(y_true)):
        single_is_right = single_model[i] == y_true[i]
        ensemble_is_right = ensemble[i] == y_true[i]
        single_right += single_is_right
        ensemble_right += ensemble_is_right

        if not single_is_right and ensemble_is_right:
            improved.append(i + 1)
        elif single_is_right and not ensemble_is_right:
            worsened.append(i + 1)

    print("Ответы ансамбля (None — ничья):", ensemble)
    print(f"Accuracy одной модели: {single_right / len(y_true):.2f}")
    print(f"Accuracy ансамбля: {ensemble_right / len(y_true):.2f}")
    print("Ансамбль улучшил объекты:", improved)
    print("Ансамбль ухудшил объекты:", worsened)


# Задача 9
def task_9():
    print("Задача 9. Логистическая регрессия и дерево решений")
    clients = [(1, 5), (4, 20), (2, 15), (5, 3), (3, 30)]
    different = []

    for number, (x1, x2) in enumerate(clients, start=1):
        _, probability, logistic_class = predict_logistic(x1, x2, 0.8, -0.05, -1)

        if x1 >= 3:
            tree_class = 1
        elif x2 <= 10:
            tree_class = 1
        else:
            tree_class = 0

        print(
            f"Клиент {number}: вероятность={probability:.4f}, "
            f"логистическая регрессия={logistic_class}, дерево={tree_class}"
        )
        if logistic_class != tree_class:
            different.append(number)

    print("Ответы отличаются для клиентов:", different)


if __name__ == "__main__":
    task_1()
    # task_2()
    # task_3()
    # task_4()
    # task_5()
    # task_6()
    # task_7()
    # task_8()
    # task_9()
