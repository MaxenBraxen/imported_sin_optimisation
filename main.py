from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import matplotlib.pyplot as plt
from math import sin, radians
from random import randint

X = np.arange(1,361)
poly = PolynomialFeatures(degree = 5, include_bias = False)
poly_features = poly.fit_transform(X.reshape(-1,1))
Y = [sin(radians(x)) for x in X]
reg = LinearRegression()
reg.fit(poly_features,Y)
y_predicted = reg.predict(poly_features)

plt.plot(X, y_predicted)
plt.plot(X,Y)
plt.show()
x_new = X.view(dtype = float)


def funktion(reg, x = None):
    mat_func = 0
    print_func = ""
    for i in range(len(reg.coef_)):
        if x:
            mat_func += reg.coef_[i] * x ** (i+1)
        else:
            print_func += f"{reg.coef_[i]}x^{i+1} "
    if x:
        mat_func += reg.intercept_
        return mat_func
    else:
        print_func += str(reg.intercept_)
        return print_func


def genomsnittligt_fel():
    fel = 0
    for x in range(1,361):
        fel += abs(funktion(reg, x) - sin(radians(x)))
    fel /= 360
    return fel

def genomsnittligt_fel_random():
    fel = 0
    random_list = [randint(1, 360) for _ in range(360)]
    for x in random_list:
        fel += abs(funktion(reg, x) - sin(radians(x)))
    fel /= 360
    return fel

print (funktion(reg))
print (genomsnittligt_fel())
print (genomsnittligt_fel_random())



#Jag märkte när jag skrev det här programmet att det var en mycket dålig idé att skriva ut felprocent
#Den blev nämligen mycket hög, för tredjegradsfunktionen blev den 228 * 10^12 % och för 5:gradsfunktionen blev den 175 * 10^11%
#Anledningen till att det blir så högt är att man dividerar med nästan noll. När man skriver 1/sin(radians(360)) så blir det inte odefinerat, utan det blir ett
#mycket stort tal, 80 * 10^14, det är för att det finns en osäkerhet i omvandlingen mellan radianer och grader
#Jag märkte inte det här när jag skrev looked_sin_optimisation programmet eftersom då var funktionen såpass bra anpassad i de punkterna där sin(x) = 0
#Skillnaden mellan mitt värde och sin värdet var då 10^-16. Men när jag dividerade med programmets version av sin(180) så blev det 1,
#alltså 100 felprocent. Det försvann i statistiken, därför är nog felprocenten som skrevs ut där(18.7 och 7.3 %)inte jättepålitliga att kolla på.
#Det är bättre att kolla på genomsnittlig avvikelse, och den var där 0.08 för 3:gradaren
#och här utan låsta nollställen 0.058. Alltså bättre. Sen märkte jag också när jag anpassade med den här modellen att den inte tar så jättemycket hänsyn till
#vad som händer i slutet av intervallet, vid 0 och 360 grader. Skillnaden blev 0.2 där för tredjegradaren. Det gör att jag inte kan anpassa
#polynomfunktioner av jättehög grad här. 5 är egentligen det som funkar bäst. Där får jag en genomsnittlig avvikelse på endast 0.004 alltså bara 4 % av felet hos 3:gradare med låsta punkter.
#3,4 och 6 funkar också bra här. Anledningen till att jag inte kan anpassa polynom av högra grad (tror jag) inte är på grund av
#att det inte går utan snarare att programmet tar hänsyn till olika saker som påverkar hur funktionen ser ut.


#En slutgiltig sak som jag har tänkt på är hur man ska bestämma fel. Ska man välja själv ett antal punkter med ekvivalent avstånd
#eller ska man slumpmässigt välja vilka punkter som ska kontrolleras. Jag gjorde båda metoderna nedan eftersom jag inte vet vilket som är mer korrekt
#En människa som väljer kan anses ha tendens, men samtidigt risken när en robot väljer är att varje del av kurvan inte får lika mycket utrymme










def felprocent():
    fel_procent = 0
    for x in range(1, 361):
        skillnad = abs(funktion(reg,x) - sin(radians(x)))
        fel_procent += abs(float(funktion(reg, x)) - sin(radians(x))) / abs(sin(radians(x)))
        print (skillnad, skillnad / abs(sin(radians(x))))
    fel_procent /= 360
    fel_procent *= 100
    return fel_procent

def typ_felprocent(): # En typ av felprocent som jag definerade, dividerar genomsnittligt fel med abs(genomsnittligt sin-värde)
    sum = 0
    for i in range(1, 361):
        sum += abs(sin(radians(i)))
    sum /= 360
    return 100 * genomsnittligt_fel() / sum

print (typ_felprocent())
