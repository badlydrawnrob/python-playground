#
# Discount script
#
# Author: @badlydrawnrob
# Source: https://youtu.be/Kh1Tr1eYghA

def discount(original,sale):
    # First calulate the difference in price
    difference = original - sale
    # Next, divide the difference by original
    # to get the percent of change as a decimal
    # - As we're calculating a decimal point here,
    #   we need to convert integer to a float.
    discountDecimal = float(difference) / float(original)
    # Finally, we need to multiply by 100
    # to get the final percentage amount of discount.
    # You can't use % or \%: instead use %%
    discountPercent = discountDecimal * 100
    print "%d%% discount" % (discountPercent)
    

# discount(30,10)