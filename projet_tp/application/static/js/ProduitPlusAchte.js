new Chart(document.getElementById("chart").getContext("2d"), {
  type: "bar",
  data: {
    labels: [
      "Coca-Cola 1L",
      "Fanta 1L",
      "Jus Orange Naturel 1.5L",
      "Huile végétale 2L",
    ],
    datasets: [
      {
        label: "Produits Plus Achete",
        data: [40, 20, 40, 10, 0],
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 99, 132, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(75, 192, 192, 0.2)",
        ],
        borderColor: [
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
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
