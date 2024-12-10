from matplotlib import pyplot as plt

class GraphGenerator:
    def __init__(self):
        pass

    @staticmethod
    def plot_distribution(x: list, y: list, x_name: str, y_name: str, color: str, alpha: float, label: str):
        plt.scatter(x, y, color=color, alpha=alpha, label=label)

        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.legend()
        plt.show()

    @staticmethod
    def plot_trend_line(x: list, y: list, x_name: str, y_name: str, color: str, label: str):
        plt.plot(x, y, color=color, label=label)

        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.legend()
        plt.show()

    @staticmethod
    def plot_bar_chart(x: list, y: list, yerr: list, x_name: str, y_name: str, color: str, label: str, capsize: int = 5):
        plt.bar(x, y, color=color, label=label, yerr=yerr, capsize=capsize)

        # Annotate each point with its value
        for i, value in enumerate(y):
            plt.text(x[i], y[i], f'{value:.3f}', ha='right', fontsize=8)

        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.legend()
        plt.show()
