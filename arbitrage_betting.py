# Παράδειγμα κώδικα για τον υπολογισμό του σίγουρου κέρδους σε μια περίπτωση arbitrage betting

def calculate_arbitrage(op1, op2, total_amount):
    # Υπολογισμός των ποσών που πρέπει να πονταριστούν σε κάθε πιθανότητα
    sum_of_inverses = 1 / op1 + 1 / op2
    if sum_of_inverses < 1:
        # Υπάρχει σίγουρο κέρδος
        bet1 = total_amount / sum_of_inverses * (1 / op1)
        bet2 = total_amount / sum_of_inverses * (1 / op2)
        return bet1, bet2
    else:
        # Δεν υπάρχει σίγουρο κέρδος
        return None

# Αποδόσεις
odds1 = 6.10
# Αν θα το ζητά απο το χρήστη ή απο κάπω api των στοιχηματικών εταιριών μετέπειτα
#float(input("Εισάγετε την απόδοση του πρώτου στοιχήματος: "))
odds2 = 1.86
#float(input("Εισάγετε την απόδοση του δεύτερου στοιχήματος: "))

# Συνολικό ποσό που θέλουμε να ποντάρουμε
total_amount = 200
#float(input("Εισάγετε το συνολικό ποσό που θέλετε να ποντάρετε: "))

# Υπολογισμός των ποσών που πρέπει να πονταριστούν
bets = calculate_arbitrage(odds1, odds2, total_amount)

if bets:
    # Υπολογίζουμε τα κέρδη που θα προκύψουν από κάθε στοίχημα
    amount1 = round(bets[0], 2)
    amount2 = round(bets[1], 2)

    profit1 = amount1 * odds1 - total_amount
    profit2 = amount2 * odds2 - total_amount

    print("odds1: €%.2f" %odds1)
    print("Bet1: €%.2f" % amount1)
    print("Profit1: €%.2f" % profit1)

    print("odds2: €%.2f" %odds2)
    print("Bet2: €%.2f" % amount2)
    print("Profit2: €%.2f" % profit2)
    
else:
    print("No arbitrage opportunity.")
