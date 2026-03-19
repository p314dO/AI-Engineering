
def validate_values(value):
    if value < 0:
        return False
    else:
        return True
    
def calculate_discount(price, discount):
    discount_amount = price * discount / 100
    final_price = price - discount_amount
    return [final_price , discount_amount]

def calculate_vat(price, vat):
    vat_amount = price * vat / 100
    price_with_vat = price + vat_amount
    return [price_with_vat , vat_amount]

def calculate_tip(price_with_vat, tip_percentage):
    tip = price_with_vat * tip_percentage / 100
    final_total = price_with_vat + tip
    return [final_total, tip]

def show_summary(base_price,vat_percentage,tip_percentage, discount_percentage, price_after_discount, discount_amount, price_with_vat, vat_amount,final_total, tip):
    print("Base price: ", base_price)
    print("Discount percentage: ", discount_percentage)
    print("VAT percentage: ", vat_percentage)
    print("Tip percentage: ", tip_percentage)
    print("Discount amount", discount_amount)
    print("Price after discount", price_after_discount)
    print("VAT Amount:" , vat_amount)
    print("Price with VAT: ", price_with_vat)
    print("Tip: ", tip)
    print("Price with TIP: ", final_total)
    
    

def main():
    base_price = float(input("Insert the base price of the product: "))
    
    if(validate_values(base_price)):
        discount_percentage = float(input("Insert the discount percentage of the product: "))
        
        if(validate_values(discount_percentage)):
            vat_percentage = float(input("Insert the VAT percentage of the product: "))
            
            if(validate_values(vat_percentage)):
                tip_percentage = float(input("Insert the tip percentage of the product: "))
                
                if(validate_values(tip_percentage)):
                    # TODO Logic Business Here 
                    
                    price_after_discount, discount_amount = calculate_discount(base_price, discount_percentage)
                    
                    price_with_vat, vat_amount = calculate_vat(price_after_discount, vat_percentage)
                    
                    final_total, tip = calculate_tip(price_with_vat, tip_percentage)
                    
                    show_summary(base_price,vat_percentage, tip_percentage,discount_percentage, price_after_discount, discount_amount,price_with_vat, vat_amount,final_total, tip )
                    
                else:
                    print("The tip cannot be less than zero. Bye Bye")
            else:
                print("The vat cannot be less than zero. Bye Bye")
        else:
            print("The discount cannot be less than zero. Bye Bye")
    else:
        print("The price cannot be less than zero. Bye Bye")


if __name__ == "__main__":
    main()


