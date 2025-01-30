document.getElementById("generate_correlation").addEventListener("click", function() {
    let length = 20; // Define o tamanho do ID
    let chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let randomString = "";
    for (let i = 0; i < length; i++) {
        randomString += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    document.getElementById("correlation_id").value = randomString;
});
