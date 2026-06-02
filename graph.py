import matplotlib.pyplot as plt
from analytics import weekly

def show_graph(user):
    data = weekly(user)

    if data.empty:
        print("No Data")
        return

    plt.figure()
    plt.plot(data.index, data.values, marker='o')
    plt.title("Weekly Calories")
    plt.xticks(rotation=45)
    plt.show()