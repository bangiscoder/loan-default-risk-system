# ============================================
# Loan Default Risk Prediction System (Flask App)
# ============================================

from flask import Flask, render_template, request
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load saved model, scaler, and training columns
model = joblib.load("../models/loan_risk_model.pkl")
scaler = joblib.load("../models/scaler.pkl")
model_columns = joblib.load("../models/model_columns.pkl")


# ============================================
# Home Page
# ============================================
@app.route("/")
def home():
    return render_template("predict.html", prediction_text=None, explanation_text=None)


# ============================================
# Prediction Route
# ============================================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # ----------------------------------------
        # Step 1: Collect form input
        # ----------------------------------------
        form_data = request.form.to_dict()

        # ----------------------------------------
        # Step 2: Define ALL numeric fields used by model
        # ----------------------------------------
        numeric_fields = [
            "duration",
            "credit_amount",
            "installment_rate",
            "present_residence_since",
            "age",
            "existing_credits",
            "people_liable"
        ]

        # Convert numeric input values from string to float
        for key in numeric_fields:
            if key in form_data and form_data[key] != "":
                form_data[key] = float(form_data[key])

        # ----------------------------------------
        # Step 3: Build empty input row with all model columns
        # ----------------------------------------
        input_df = pd.DataFrame(columns=model_columns)
        input_df.loc[0] = 0

        # ----------------------------------------
        # Step 4: Fill numeric columns directly
        # ----------------------------------------
        for field in numeric_fields:
            if field in input_df.columns and field in form_data:
                input_df.at[0, field] = form_data[field]

        # ----------------------------------------
        # Step 5: Fill categorical one-hot encoded columns
        # ----------------------------------------
        for key, value in form_data.items():
            column_name = f"{key}_{value}"
            if column_name in input_df.columns:
                input_df.at[0, column_name] = 1

        # ----------------------------------------
        # Step 6: Scale input using saved scaler
        # ----------------------------------------
        input_scaled = scaler.transform(input_df)

        # ----------------------------------------
        # Step 7: Predict class and probability
        # ----------------------------------------
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]

        # Convert prediction to human-readable result
        if prediction == 1:
            result = "High Default Risk"
        else:
            result = "Low Default Risk"

        # ----------------------------------------
        # Step 8: Build a simple explanation
        # ----------------------------------------
        reasons = []

        if float(form_data.get("credit_amount", 0)) > 500000:
            reasons.append("the loan amount entered is relatively high")

        if float(form_data.get("duration", 0)) > 12:
            reasons.append("the repayment duration is relatively long")

        if float(form_data.get("age", 0)) < 25:
            reasons.append("the borrower is relatively young")

        if form_data.get("checking_account_status") == "A11":
            reasons.append("the checking account balance band is low")

        if form_data.get("savings_account") == "A61":
            reasons.append("the savings balance band is low")

        if form_data.get("employment_since") == "A71":
            reasons.append("the borrower is currently unemployed")

        if float(form_data.get("existing_credits", 0)) > 2:
            reasons.append("the borrower is already managing multiple credits")

        if float(form_data.get("people_liable", 0)) > 2:
            reasons.append("the borrower has many financial dependents")

        if form_data.get("housing") == "A152":
            reasons.append("the borrower is living in rented housing")

        if reasons:
            explanation = "The system reached this conclusion because " + ", ".join(reasons) + "."
        else:
            explanation = "The system reached this conclusion based on the full combination of borrower characteristics provided."

        # ----------------------------------------
        # Step 9: Return result to page
        # ----------------------------------------
        return render_template(
            "predict.html",
            prediction_text=f"{result} (Probability: {probability:.2%})",
            explanation_text=explanation
        )

    except Exception as e:
        return render_template(
            "predict.html",
            prediction_text=f"Error: {str(e)}",
            explanation_text="The system could not complete the prediction because of an internal processing error."
        )


# ============================================
# Run Development Server
# ============================================
if __name__ == "__main__":
    app.run(debug=True)