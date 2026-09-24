from flask import Flask, render_template, request

app = Flask(__name__)


digits = "0123456789ABCDEF"


def convert_to_decimal(number, base):

    decimal = 0

    for digit in number.upper():

        value = digits.index(digit)

        decimal = decimal * base + value

    return decimal


def convert_from_decimal(decimal, base):

    if decimal == 0:
        return "0"

    result = ""

    while decimal > 0:

        remainder = decimal % base

        result = digits[remainder] + result

        decimal = decimal // base

    return result


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    solution = ""

    if request.method == "POST":

        number = request.form["number"].upper()

        from_base = int(request.form["from_base"])
        to_base = int(request.form["to_base"])

        # Convert to decimal first
        decimal_number = convert_to_decimal(number, from_base)

        # Convert decimal to target base
        result = convert_from_decimal(decimal_number, to_base)

        # Basic solution
        solution = f"""
        <p><b>Step 1:</b> Convert Base {from_base} to decimal.</p>

        <p>
        {number}<sub>{from_base}</sub>
        =
        {decimal_number}<sub>10</sub>
        </p>

        <p><b>Step 2:</b> Convert decimal to Base {to_base}.</p>

        <p>
        {decimal_number}<sub>10</sub>
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