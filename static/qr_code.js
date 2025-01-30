function checkPaymentStatus() {
    let invoiceId = document.getElementById("invoice").innerText.trim();
    console.log("Checking invoice:", invoiceId); // Debug

    $.ajax({
        url: `/check_payment_status?invoice_id=${invoiceId}`,
        type: "GET",
        success: function(response) {
            console.log("Payment check response:", response); // Debug
            if (response.success) {
                console.log("Redirecting to success page...");
                window.location.href = `/payment_success?invoice_id=${invoiceId}`;
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", status, error);
        }
    });
}

setInterval(checkPaymentStatus, 5000);