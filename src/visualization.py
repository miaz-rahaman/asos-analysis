import matplotlib.pyplot as plt
import seaborn as sns

def plot_top_loss(df):
    top = df.sort_values(by='Lost_Revenue', ascending=False).head(10)

    sns.barplot(x='Lost_Revenue', y='brand', data=top)
    plt.title("Top Brands by Revenue Loss")
    plt.show()