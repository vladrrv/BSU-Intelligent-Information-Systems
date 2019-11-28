import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

SEED = 42
np.random.seed(SEED)


def generate_data(n=2, num_samples=10, num_classes=3):
    x = np.round(np.random.rand(num_samples, n)).astype(int)
    y = np.random.randint(0, num_classes, (num_samples, 1))
    return x, y


def load_data(path):
    df = pd.read_csv(path, index_col='id')
    cols = list(df)
    x = df[cols[1:-1]].values
    y = df[cols[-1]].values[..., np.newaxis]
    return x, y


def algorithm(x_train, y_train, x_test):
    num_samples, num_features = x_train.shape
    num_classes = y_train.max() + 1
    mask = np.arange(num_classes) == y_train.repeat(num_classes, 1)
    m = mask.sum(axis=0)

    # Training
    b = np.empty((num_classes, num_features))
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
    # x, y = generate_data(n=20, num_samples=100, num_classes=5)
    x, y = load_data('dataset.csv')

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=SEED)
    print('Train samples: ', x_train.shape[0])
    print('Test samples: ', x_test.shape[0])

    y_pred = algorithm(x_train, y_train, x_test)
    score = accuracy_score(y_test, y_pred)
    print('Accuracy: ', score)


if __name__ == "__main__":
    main()
