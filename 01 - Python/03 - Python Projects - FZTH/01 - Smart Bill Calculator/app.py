def is_non_negative(value):
    if value < 0:
        return False
    else:
        return True


def calculate_discount(original_price, discount_rate):
    discount_amount = original_price * discount_rate / 100
    discounted_price = original_price - discount_amount
    return [discounted_price, discount_amount]


def calculate_vat(discounted_price, vat_rate):
    vat_amount = discounted_price * vat_rate / 100
    subtotal_with_vat = discounted_price + vat_amount
    return [subtotal_with_vat, vat_amount]


def calculate_tip(subtotal_with_vat, tip_rate):
    tip_amount = subtotal_with_vat * tip_rate / 100
    final_total = subtotal_with_vat + tip_amount
    return [final_total, tip_amount]


def display_summary(
    original_price,
    discount_rate,
    vat_rate,
    tip_rate,
    discounted_price,
    discount_amount,
    subtotal_with_vat,
    vat_amount,
    final_total,
    tip_amount,
):
    print("Base price: ", original_price)
    print("Discount percentage: ", discount_rate)
    print("VAT percentage: ", vat_rate)
    print("Tip percentage: ", tip_rate)
    print("Discount amount: ", discount_amount)
    print("Price after discount: ", discounted_price)
    print("VAT amount: ", vat_amount)
    print("Price with VAT: ", subtotal_with_vat)
    print("Tip amount: ", tip_amount)
    print("Final total: ", final_total)


def main():
    original_price = float(input("Insert the base price of the product: "))

    if is_non_negative(original_price):
        discount_rate = float(input("Insert the discount percentage of the product: "))

        if is_non_negative(discount_rate):
            vat_rate = float(input("Insert the VAT percentage of the product: "))

            if is_non_negative(vat_rate):
                tip_rate = float(input("Insert the tip percentage of the product: "))

                if is_non_negative(tip_rate):
                    discounted_price, discount_amount = calculate_discount(
                        original_price, discount_rate
                    )

                    subtotal_with_vat, vat_amount = calculate_vat(
                        discounted_price, vat_rate
                    )

                    final_total, tip_amount = calculate_tip(
                        subtotal_with_vat, tip_rate
                    )

                    display_summary(
                        original_price,
                        discount_rate,
                        vat_rate,
                        tip_rate,
                        discounted_price,
                        discount_amount,
                        subtotal_with_vat,
                        vat_amount,
                        final_total,
                        tip_amount,
                    )
                else:
                    print("The tip cannot be less than zero. Bye Bye")
            else:
                print("The VAT cannot be less than zero. Bye Bye")
        else:
            print("The discount cannot be less than zero. Bye Bye")
    else:
        print("The price cannot be less than zero. Bye Bye")


if __name__ == "__main__":
    main()