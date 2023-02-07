new Chart(document.getElementById("chart").getContext("2d"), {
  type: "bar",
  data: {
    labels: ["Coca-Cola", "SIM", "Elegant Clothing", "Cevital"],
    datasets: [
      {
        label: "Top Fournisseurs",
        data: [5, 7, 3, 10, 0],
        backgroundColor: [
          "rgba(255, 159, 64, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(12, 205, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
        ],
        borderColor: [
          "rgb(255, 99, 132)",
          "rgb(153, 102, 255)",
          "rgb(201, 203, 207)",
          "rgb(89, 100, 207)",
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
