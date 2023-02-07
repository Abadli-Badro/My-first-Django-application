new Chart(document.getElementById("chart").getContext("2d"), {
  type: "bar",
  data: {
    labels: [
      "Huile végétale 2L",
      "Fanta 1L",
      "Coca-Cola 1L",
      "Jus Orange Naturel 1.5L",
      "Couscous Sim 1Kg",
      "Tomate 1Kg",
    ],
    datasets: [
      {
        label: "Top Products",
        data: [65, 59, 80, 81, 90, 15],
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 159, 64, 0.2)",
          "rgba(255, 159, 64, 0.2)",
          "rgba(255, 205, 86, 0.2)",
          "rgba(255, 205, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
        ],
        borderColor: [
          "rgb(255, 99, 132)",
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
          "rgb(153, 102, 255)",
          "rgb(153, 102, 255)",
          "rgb(201, 203, 207)",
        ],
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: false,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  },
});
