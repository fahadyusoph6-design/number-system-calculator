from flask import Flask, render_template, request

app = Flask(__name__)

digits = "0123456789ABCDEF"


# =========================
# BASE CONVERSION
# =========================

def convert_to_decimal(number, base):
    number = number.upper()

    if "." in number:
        whole_part, fractional_part = number.split(".")
    else:
        whole_part = number
        fractional_part = ""

    decimal = 0

    # Whole part
    for digit in whole_part:
        value = digits.index(digit)

        if value >= base:
            raise ValueError("Invalid digit for selected base.")

        decimal = decimal * base + value

    # Fractional part
    fraction = 0
    power = 1

    for digit in fractional_part:
        value = digits.index(digit)

        if value >= base:
            raise ValueError("Invalid digit for selected base.")

        power *= base
        fraction += value / power

    return decimal + fraction


def convert_from_decimal(decimal, base):
    whole = int(decimal)
    fraction = decimal - whole

    # Whole number
    if whole == 0:
        whole_result = "0"
    else:
        whole_result = ""

        while whole > 0:
            remainder = whole % base
            whole_result = digits[remainder] + whole_result
            whole //= base

    # No fraction
    if abs(fraction) < 1e-12:
        return whole_result

    # Fraction
    fraction_result = ""

    for _ in range(12):
        fraction *= base
        digit = int(fraction)

        fraction_result += digits[digit]

        fraction -= digit

        if abs(fraction) < 1e-12:
            break

    return whole_result + "." + fraction_result


# =========================
# MAIN PAGE
# =========================

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    solution = ""
    error = ""

    operation = "convert"

    if request.method == "POST":

        try:

            operation = request.form.get("operation", "convert")

            # =================================
            # CONVERT
            # =================================

            if operation == "convert":

                number = request.form["number"].upper()
                from_base = int(request.form["from_base"])
                to_base = int(request.form["to_base"])

                decimal_number = convert_to_decimal(number, from_base)

                result = convert_from_decimal(decimal_number, to_base)

                if decimal_number.is_integer():
                    decimal_display = str(int(decimal_number))
                else:
                    decimal_display = str(decimal_number)

                solution = f"""
                <p><b>Step 1:</b> Convert Base {from_base} to decimal.</p>

                <p>
                    {number}<sub>{from_base}</sub>
                    =
                    {decimal_display}<sub>10</sub>
                </p>

                <p><b>Step 2:</b> Convert decimal to Base {to_base}.</p>

                <p>
                    {decimal_display}<sub>10</sub>
                    =
                    {result}<sub>{to_base}</sub>
                </p>

                <p><b>Final Answer:</b></p>

                <p>
                    {number}<sub>{from_base}</sub>
                    =
                    <strong>{result}<sub>{to_base}</sub></strong>
                </p>
                """

            # =================================
            # ADD / SUBTRACT / MULTIPLY
            # =================================

            else:

                number1 = request.form["number1"].upper()
                number2 = request.form["number2"].upper()

                base = int(request.form["base"])

                decimal1 = convert_to_decimal(number1, base)
                decimal2 = convert_to_decimal(number2, base)

                if operation == "add":

                    decimal_answer = decimal1 + decimal2
                    symbol = "+"

                elif operation == "subtract":

                    decimal_answer = decimal1 - decimal2
                    symbol = "-"

                elif operation == "multiply":

                    decimal_answer = decimal1 * decimal2
                    symbol = "×"

                else:
                    raise ValueError("Invalid operation.")

                # Convert answer back to selected base
                if decimal_answer >= 0:
                    result = convert_from_decimal(decimal_answer, base)

                else:
                    positive_answer = convert_from_decimal(
                        abs(decimal_answer), base
                    )

                    result = "-" + positive_answer

                solution = f"""
                <p><b>Step 1:</b> Convert the numbers to decimal.</p>

                <p>
                    {number1}<sub>{base}</sub>
                    =
                    {decimal1}<sub>10</sub>
                </p>

                <p>
                    {number2}<sub>{base}</sub>
                    =
                    {decimal2}<sub>10</sub>
                </p>

                <p><b>Step 2:</b> Perform the operation.</p>

                <p>
                    {decimal1} {symbol} {decimal2}
                    =
                    {decimal_answer}
                </p>

                <p><b>Step 3:</b> Convert the decimal answer back to Base {base}.</p>

                <p>
                    {decimal_answer}<sub>10</sub>
                    =
                    {result}<sub>{base}</sub>
                </p>

                <p><b>Final Answer:</b></p>

                <p>
                    <strong>
                        {number1}<sub>{base}</sub>
                        {symbol}
                        {number2}<sub>{base}</sub>
                        =
                        {result}<sub>{base}</sub>
                    </strong>
                </p>
                """

        except Exception as e:

            error = "Invalid number or digit for the selected base."

    return render_template(
        "index.html",
        result=result,
        solution=solution,
        error=error,
        operation=operation
    )


if __name__ == "__main__":
    app.run(debug=True)