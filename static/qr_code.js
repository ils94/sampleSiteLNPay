function checkPaymentStatus() {
    let invoice = document.getElementById("invoice").innerText.trim();
    console.log("Checking invoice:", invoice); // Debug

    $.ajax({
        url: `/check_payment_status?invoice=${invoice}`,
        type: "GET",
        success: function(response) {
            console.log("Payment check response:", response); // Debug
            if (response.success) {
                console.log("Redirecting to success page...");
                window.location.href = `/payment_success?invoice=${invoice}`;
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX Error:", status, error);
        }
    });
}

setInterval(checkPaymentStatus, 3000);