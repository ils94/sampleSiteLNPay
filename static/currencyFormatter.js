document.getElementById("amount_fiat").addEventListener("input", function(event) {
    let value = event.target.value.replace(/[^0-9]/g, "");

    if (value.length > 2) {
        value = value.slice(0, -2) + "." + value.slice(-2);
    }

    event.target.value = value;
});
