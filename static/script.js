document.addEventListener("DOMContentLoaded", async () => {
    const res = await fetch("/api/user");
    const data = await res.json();
    
    let linkLogowania = document.getElementById("zaloguj");
    let naglowekKonta = document.getElementById("zaloguj_konto");
    let miejsceNaEmail = document.getElementById("pokaz-email");

    if (!data.email) {
        if (naglowekKonta) {
            naglowekKonta.innerHTML = "Zaloguj";
        }
    } else {
        if (naglowekKonta) {
            naglowekKonta.innerText = data.email;
        }
        if (linkLogowania) {
            linkLogowania.href = "/konto"; 
        }
        if (miejsceNaEmail) {
            miejsceNaEmail.innerText = `Zalogowany jako: ${data.email}`;
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
                            <img src="${product.image || 'https://via.placeholder.com/200'}" alt="${product.name}">
                            <h3>${product.name}</h3>
                            <p>Ilość: <strong>${product.quantity}</strong></p>
                            <p>Cena: <strong>${product.price}</strong> zł</p>
                            <span class="status-completed" style="color: #10b981; font-weight: bold; margin-top: 10px;">Dostarczono</span>
                        </div>`;
                });
            } else {
                historyContainer.innerHTML = "<p class='pusty-koszyk' style='grid-column: 1/-1;'>Nie masz jeszcze żadnych zakupionych produktów w historii.</p>";
            }
        } catch (error) {
            console.error("Błąd podczas pobierania historii:", error);
            historyContainer.innerHTML = "<p style='grid-column: 1/-1;'>Nie udało się załadować historii zamówień.</p>";
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