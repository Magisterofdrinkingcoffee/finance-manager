const ctx = document.getElementById('financeChart').getContext('2d');
const financeChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: chartMonths,
        datasets: [
            {
                label: 'Expenses',
                data: chartExpenses,
                backgroundColor: 'rgba(255, 99, 132, 0.6)'
            },
            {
                label: 'Incomes',
                data: chartIncomes,
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Monthly Expenses vs Incomes'
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Бар-чарт уже должен быть сверху (financeChart)

// Теперь создаем Pie Chart
const pieCtx = document.getElementById('pieChart').getContext('2d');
const pieChart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: pieLabels,
        datasets: [{
            data: pieData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)',
                'rgba(199, 199, 199, 0.6)',
                'rgba(83, 102, 255, 0.6)',
                'rgba(255, 180, 50, 0.6)',
                'rgba(0, 191, 255, 0.6)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Expenses by Category'
            }
        }
    }
});
