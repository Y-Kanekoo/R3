// 検索機能の実装
document.getElementById("search-button").addEventListener("click", function() {
    const searchText = document.getElementById("search").value.toLowerCase();
    const tableRows = document.querySelectorAll(".table-container tbody tr");

    tableRows.forEach(row => {
        const rowText = row.innerText.toLowerCase();
        if (rowText.includes(searchText)) {
            row.style.display = ""; // 一致する場合は表示
        } else {
            row.style.display = "none"; // 一致しない場合は非表示
        }
    });
});

