var ctx = document.getElementById("chart").getContext("2d");
var chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [0, 1, 2, 3, 4, 5, 6],
    datasets: [
      {
        label: "Evolution du benefice",
        data: [65, 59, 80, 81, 56, 55, 40],
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
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
