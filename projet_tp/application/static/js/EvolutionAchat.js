var ctx = document.getElementById("chart").getContext("2d");
var chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [0, 1, 2, 3, 4, 5, 6],
    datasets: [
      {
        label: "Evolution des achat",
        data: [8, 16, 90, 81, 56, 40, 56],
        backgroundColor: "rgba(255, 200, 50, 0.2)",
        borderColor: "rgba(180, 200, 100, 1)",
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
