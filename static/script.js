document.addEventListener("DOMContentLoaded", async () => {

  
    const res = await fetch("/api/user");
    const data = await res.json();
    let link = document.getElementById("zaloguj");

    if (!data.email) {
        if (document.getElementById('zaloguj_konto')) {
            document.getElementById('zaloguj_konto').innerHTML = "Zaloguj";
        }
    } else {
        if (document.getElementById("zaloguj_konto")) {
            document.getElementById("zaloguj_konto").innerText = data.email;
        }
        if (link) {
            link.href = "/konto"; 
        }
    }

    const historyContainer = document.getElementById('history-container');
    
    if (historyContainer) {
        try {
            const response = await fetch("/api/user/history");
            const historyData = await response.json();
            
            historyContainer.innerHTML = ''; 

            if (historyData.products && historyData.products.length > 0) {
                historyData.products.forEach(product => {
                    historyContainer.innerHTML += `
                        <div class="pos1">
                            <img src="${product.image || 'https://via.placeholder.com/200'}" alt="${product.name}" height="200px">
                            <h3>${product.name}</h3>
                            <p>Ilość: <strong>${product.quantity}</strong></p>
                            <p>Cena: <strong>${product.price}</strong> zł</p>
                            <span class="status-completed" style="color: green; font-weight: bold;">Dostarczono (Completed)</span>
                        </div>`;
                });
            } else {
                historyContainer.innerHTML = "<p>Nie masz jeszcze żadnych zakupionych produktów w historii.</p>";
            }
        } catch (error) {
            console.error("Błąd podczas pobierania historii:", error);
            historyContainer.innerHTML = "<p>Nie udało się załadować historii zamówień.</p>";
        }
    }
});


async function usunZKoszyka(productName) {
    if (confirm(`Czy chcesz usunąć ${productName} z koszyka?`)) {
        const response = await fetch("/api/koszyk/usun", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: productName })
        });
        
        if (response.ok) {
            window.location.reload();
        } else {
            alert("Wystąpił błąd podczas usuwania produktu.");
        }
    }
}

async function zmienIlosc(productName, newQuantity) {
    if (parseInt(newQuantity) < 1) {
        alert("Ilość nie może być mniejsza niż 1.");
        window.location.reload();
        return;
    }

    const response = await fetch("/api/koszyk/zmien_ilosc", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            name: productName, 
            quantity: parseInt(newQuantity) 
        })
    });

    if (response.ok) {
        window.location.reload();
    } else {
        alert("Wystąpił błąd podczas zmiany ilości produktu.");
    }
}