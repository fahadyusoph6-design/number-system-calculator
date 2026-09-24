from flask import Flask, render_template, request

app = Flask(__name__)

digits = "0123456789ABCDEF"


# Convert a number from any base (2-16) to decimal
def convert_to_decimal(number, base):
    number = number.upper()

    # Separate whole and fractional parts
    if "." in number:
        whole_part, fractional_part = number.split(".")
    else:
        whole_part = number
        fractional_part = ""

    # Convert whole-number part
    decimal = 0

    for digit in whole_part:
        value = digits.index(digit)
        decimal = decimal * base + value

    # Convert fractional part
    fraction = 0
    power = 1

    for digit in fractional_part:
        value = digits.index(digit)
        power *= base
        fraction += value / power

    return decimal + fraction


# Convert decimal to any base (2-16)
def convert_from_decimal(decimal, base):
    # Whole part
    whole = int(decimal)
    fraction = decimal - whole

    if whole == 0:
        whole_result = "0"
    else:
        whole_result = ""

        while whole > 0:
            remainder = whole % base
            whole_result = digits[remainder] + whole_result
            whole //= base

    # Fractional part
    if fraction == 0:
        return whole_result

    fraction_result = ""

    # Limit fractional digits to prevent infinite calculations
    for _ in range(12):
        fraction *= base
        digit = int(fraction)

        fraction_result += digits[digit]

        fraction -= digit

        if fraction == 0:
            break

    return whole_result + "." + fraction_result


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    solution = ""

    if request.method == "POST":

        number = request.form["number"].upper()
        from_base = int(request.form["from_base"])
        to_base = int(request.form["to_base"])

        decimal_number = convert_to_decimal(number, from_base)

        result = convert_from_decimal(decimal_number, to_base)

        # Remove unnecessary decimal .0
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

    return render_template(
        "index.html",
        result=result,
        solution=solution
    )


if __name__ == "__main__":
    app.run(debug=True)