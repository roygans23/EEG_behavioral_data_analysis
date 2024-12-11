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
    def plot_bar_chart(x: list, y: list, yerr: list, x_name: str, y_name: str, colors: list[str], label: str, save_file_name: str, width = 0.5, capsize: int = 5):
        plt.bar(x, y, color=colors, label=label, yerr=yerr, width=width, capsize=capsize)

        # Annotate each point with its value
        for i, value in enumerate(y):
            plt.text(x[i], y[i], f'{value:.3f}', ha='right', fontsize=8)

        plt.xlabel(x_name)
        plt.ylabel(y_name)
        # plt.legend()
        # plt.show()

        plt.savefig(f'data/graphs/{save_file_name}')
        plt.close()

    @staticmethod
    def plot_subplots(x: list[list], y: list[list], x_name: str, y_name: str, color: str, label_prefix: str, title_prefix: str, save_file_name: str):
        # Number of subplots needed
        num_plots = len(x)

        # Determine the grid size (e.g., 2x2, 3x3, etc. based on the number of plots)
        cols = 2
        rows = (num_plots // cols) + (num_plots % cols)

        # Create a grid of subplots
        fig, axs = plt.subplots(rows, cols, figsize=(10, 8))

        # Flatten axs to easily iterate if there's more than one row
        axs = axs.flatten()

        # Plot each dataset
        for i in range(num_plots):
            axs[i].plot(x[i], y[i], label=f'{label_prefix} {i+1}')
            axs[i].set_title(f'{title_prefix} {i+1}')
            axs[i].set_xlabel(x_name)
            axs[i].set_ylabel(y_name)
            axs[i].legend()

        # Adjust the layout to avoid overlap
        fig.tight_layout()

        # Show the plot
        # plt.show()

        plt.savefig(f'data/graphs/{save_file_name}')
        plt.close()