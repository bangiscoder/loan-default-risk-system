document.addEventListener("DOMContentLoaded", function () {
    console.log("Loan Default Risk Prediction app loaded successfully.");
});

// =========================================
// Loan Default Risk Predictor - Frontend JS
// =========================================

document.addEventListener("DOMContentLoaded", function () {
    // Get important form fields
    const creditAmountInput = document.getElementById("credit_amount");
    const durationInput = document.getElementById("duration");
    const monthlyRepaymentInput = document.getElementById("monthly_repayment");

    // Function to calculate monthly repayment automatically
    function calculateMonthlyRepayment() {
        const creditAmount = parseFloat(creditAmountInput.value) || 0;
        const duration = parseFloat(durationInput.value) || 0;

        if (creditAmount > 0 && duration > 0) {
            const monthlyRepayment = creditAmount / duration;

            monthlyRepaymentInput.value = "₦" + monthlyRepayment.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        } else {
            monthlyRepaymentInput.value = "";
        }
    }

    // Recalculate whenever amount or duration changes
    if (creditAmountInput && durationInput && monthlyRepaymentInput) {
        creditAmountInput.addEventListener("input", calculateMonthlyRepayment);
        durationInput.addEventListener("input", calculateMonthlyRepayment);
    }
});