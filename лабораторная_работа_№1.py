# -*- coding: utf-8 -*-
"""Лабораторная работа №1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10RXK3UmpN_f3-o1jR751IBARkDhFGg7L
"""

import numpy as np
from sklearn.datasets import load_iris # загружаем датасет с информацией о 150 Ирисах
from sklearn.model_selection import train_test_split # импорт библиотеки, которая разделяет датасет на
# два набора данных: тренировочный для обучения алгоритма и тестовый для проверки точности его работы
from sklearn.preprocessing import StandardScaler # импорт класса для стандартизации данных,
# приводя их к нормальному распределению с средним 0 и стандартным отклонением 1

class OneLayerPerceptron: # Создаем класс Однослойного персептрона
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        # Инициализация гиперпараметров
        self.learning_rate = learning_rate # коэффициент обучения = 0.01
        self.n_iterations = n_iterations # количество итераций обучения = 1000
        self.weights = None # вес
        self.bias = None # смещение

    def activation_function(self, x): #сигмоидная функция активации
        return 1 / (1 + np.exp(-x))

    def predict(self, X): #предсказание на основе обученных весов и смещения выходных значений
        linear_output = np.dot(X, self.weights) + self.bias
        return self.activation_function(linear_output)

    def train(self, X, y): #инициализация весов и смещения
        n_samples, n_features = X.shape #извлекает количество образцов и количество признаков
        self.weights = np.zeros(n_features) #инициализирует веса как массив нулей с размерностью, равной количеству признаков
        self.bias = 0 # смещение = 0

        #обучение с помощью градиентного спуска
        for _ in range(self.n_iterations):
            model_output = self.predict(X)
            #вычисление градиентов весов
            dw = (1 / n_samples) * np.dot(X.T, (model_output - y)) #вычисляет градиент весов `dw`, используя производную функции потерь
            # (model_output - y) – разность между предсказанными значениями и истинными метками и нормализуя его по количеству образцов
            # градиент по смещению (db) вычисляется как среднее значение ошибок
            db = (1 / n_samples) * np.sum(model_output - y)
            #обновление весов и смещения
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def binary_predict(self, X):
        #получение бинарных предсказаний (0 или 1)
        predicted_probs = self.predict(X)
        return [1 if prob > 0.5 else 0 for prob in predicted_probs]

def load_data():
    #загрузка данных
    data = load_iris()
    X = data.data #массив, содержащий дату
    y = data.target #массив, содержащий сорта уже измеренных цветов

    #бинаризация задачи
    y = np.where(y == 2, 1, 0)

    #разделение на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #масштабирование признаков
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

def calculate_accuracy(y_true, y_pred):
    #подсчет точности
    return np.mean(y_true == y_pred)

if __name__ == '__main__':
    #загрузка данных
    X_train, X_test, y_train, y_test = load_data()

    #создание экземпляра персептрона
    ppn = OneLayerPerceptron(learning_rate=0.01, n_iterations=1000)

    #обучение персептрона
    ppn.train(X_train, y_train)

    #подсчет предсказаний
    predictions = ppn.binary_predict(X_test)
    print("Predictions:", predictions)

    #подсчет точности
    accuracy = calculate_accuracy(y_test, predictions)
    print(f'Accuracy: {accuracy * 100:.2f}%')