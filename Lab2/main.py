import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

np.random.seed(42)


def generate_data(n=2, num_samples=10, num_classes=3):
    x = np.round(np.random.rand(num_samples, n)).astype(int)
    y = np.random.randint(0, num_classes, (num_samples, 1))
    return x, y


def algorithm(x_train, y_train, x_test):
    num_samples, n = x_train.shape
    num_classes = y_train.max() + 1
    mask = np.arange(num_classes) == y_train.repeat(num_classes, 1)
    m = mask.sum(axis=0)

    # Training
    b = np.empty((num_classes, n))
    for i in range(num_classes):
        b[i] = x_train[mask[:, i]].sum(axis=0) / m[i]
    a = np.abs(b - b.mean(axis=0))

    # Evaluation
    mu = np.empty((len(x_test), num_classes))
    for k, x_t in enumerate(x_test):
        for i in range(num_classes):
            mu[k, i] = np.max(
                np.maximum(
                    0,
                    np.sum(((x_train[mask[:, i]] == x_t) * 2 - 1) * a[i], axis=1) / np.sum(a[i])
                )
            )
    predicted = np.argmax(mu, axis=1)
    return predicted


def main():
    x, y = generate_data(n=20, num_samples=100, num_classes=4)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)
    y_pred = algorithm(x_train, y_train, x_test)
    score = accuracy_score(y_test, y_pred)
    print(score)


if __name__ == "__main__":
    main()

