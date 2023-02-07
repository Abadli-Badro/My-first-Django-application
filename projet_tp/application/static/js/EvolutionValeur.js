var ctx = document.getElementById("chart").getContext("2d");
var chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [0, 1, 2, 3, 4, 5, 6],
    datasets: [
      {
        label: "Evolution des valeurs",
        data: [15, 20, 30, 40, 50, 80, 75],
        backgroundColor: "rgba(100, 100, 180, 0.2)",
        borderColor: "rgba(100, 100, 180, 1)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});
