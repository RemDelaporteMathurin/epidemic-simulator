# epidemic-simulator


Let's name $$P_h$$ the healthy population, $$P_c$$ the contaminated population, $$P_r$$ the population which has recovered from the disease and produced its own antibodies and $$P_d$$ the population that has died.
The temporal evolution of each population can be modelled with the following system of equations:
$$\left\{\begin{array}{l}
\frac{\partial P_{h}}{\partial t}=-K_{c} P_{h} P_{c} \\ \\
\frac{\partial P_{c}}{\partial t}=K_{c} P_{h} P_{c}-K_{r} P_{c}-K_{d} P_{c} \\ \\
\frac{\partial P_{r}}{\partial t}=K_{r} P_{c} \\ \\
\frac{\partial P_{d}}{\partial r}=K_{d} P_{c} \\ \\
P_h = P_{h_0} \quad \mathrm{and}  \quad P_c = P_{c_0} \quad \mathrm{for} \quad t=0
\end{array}\right.$$
where $$K_c$$ is the contamination probability, $$K_r$$ is the recovery probability, $$K_d$$ is the death probability.

We'll assume the contamination probability increases with people's mobility $$v$$.
$$v=0$$ would mean that people are 100% immobile.
$$K_c = 0.4*v$$

Here $$0.4$$ is arbitrary.

How does it look like ?

![sick_people_simple](https://user-images.githubusercontent.com/40028739/76973966-e6380880-6930-11ea-8ec8-cf7c3003f69f.png)

First, more and more people get contaminated. Then as people recover and developp antibodies, a contamination peak can be seen after which contaminated population decreases until reaching zero: the epidemic has ended.
By decreasing people's mobility, the contamination peak is delayed and is less significant in terms of contaminated people. Also the epidemic ends later. Overall, **the curve has been flatten** !

**Great! But why would we care ?**

Well let's take a look at the ammount of dead people now...

![dead_people_simple](https://user-images.githubusercontent.com/40028739/76974131-1ed7e200-6931-11ea-9654-324073f08d50.png)

Here we start to see the importance of taking control measures! As the mobility $$v$$ decreases, the number of dead people decreases as well !
That's because if less people are sick, then obviously less people a likely to die from the disease!

But that's not quite the way our health system works right ? People don't miraculously heal themselves (at least not all of them): some of them go to the hospital. And if there are too many patients then ... it is more likely that people will die and heal less rapidly.

In order to take this effect into account in our model, let's first assume a hospital capacity $$C$$. If the number of sick people is above this capacity, the recovering probability $$K_r$$ will decrease by 50% and the death probability $$K_d$$ will increase by 50%.
What will happen then ?

<img src="https://user-images.githubusercontent.com/40028739/76974014-f9e36f00-6930-11ea-8da8-2cf38e16fe74.png" alt="drawing" width="400"/><img src="https://user-images.githubusercontent.com/40028739/76974237-3fa03780-6931-11ea-9d15-87671ad77bbf.png" alt="drawing" width="400"/>

We added to the previous graphs dashed lines corresponding to the extended model with a hospital saturation limit.
If people's mobility is not reduced enough the number of sick people increases by 12%! But more important is that **the number of deaths almost doubled** !