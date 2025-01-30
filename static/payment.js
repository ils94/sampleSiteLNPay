$(document).ready(function () {
    $("#payment-form").submit(function (event) {
        event.preventDefault();  // Prevent page reload

        let amount = $("#amount").val();
        let ln_address = $("#ln_address").val();

        if (!amount || !ln_address) {
            alert("Please fill in both fields.");
            return;  // Stop execution if any field is missing
        }

        // Make the AJAX request to the backend
        $.ajax({
            url: "/submit",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                amount: amount,
                ln_address: ln_address
            }),
            success: function (response) {
                const queryParams = new URLSearchParams({
                    amount_sats: response.amount_sats,
                    time: response.time,
                    qr_code: response.qr_code,
                    invoice: response.invoice
                }).toString();

                window.location.href = "qr_code.html?" + queryParams;
            },
            error: function (xhr) {
                console.log('Error:', xhr);
                alert("Error: " + xhr.responseJSON.message);
            }
        });
    });
});
