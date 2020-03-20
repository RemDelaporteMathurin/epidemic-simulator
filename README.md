# epidemic-simulator
Many countries in Europe and around the world are currently on lockdown. Yet many people still choose to go out in the street despite the control measures!
We'll first explain why applying **control measures and lockdown** during an epidemic are indeed **a good thing** and then we'll then try to use this model to do some predictions !
## Prerequisites
This project uses [matplotlib](https://matplotlib.org/) and [scipy](https://www.scipy.org/).
## Usage
```
python3 fit_any_country.py France
```
or

```
python3 fit_any_country.py China
```
will simulate the evolution of the epidemic in a specific country based on [pomber/covid19](https://github.com/pomber/covid19) dataset
## Mathematical model
Let's first try to create a **mathematical model** that represents the population and the way some get contaminated, some recover, and some people die.
We'll name <img src="https://render.githubusercontent.com/render/math?math=P_h"> the **h**ealthy population, <img src="https://render.githubusercontent.com/render/math?math=P_c"> the **c**ontaminated population, <img src="https://render.githubusercontent.com/render/math?math=P_r"> the population which has **r**ecovered from the disease and produced its own antibodies and <img src="https://render.githubusercontent.com/render/math?math=P_d"> the part of the population that has **d**ied.
The temporal evolution of each population can be modelled with the following system of equations:

<img src="https://render.githubusercontent.com/render/math?math=\left\{\begin{array}{l}\frac{\partial P_{h}}{\partial t}=-K_{c} P_{h} P_{c} \\ \\\frac{\partial P_{c}}{\partial t}=K_{c} P_{h} P_{c}-K_{r} P_{c}-K_{d} P_{c} \\ \\\frac{\partial P_{r}}{\partial t}=K_{r} P_{c} \\ \\\frac{\partial P_{d}}{\partial r}=K_{d} P_{c} \\ \\P_h = P_{h_0} \quad \mathrm{and}  \quad P_c = P_{c_0} \quad \mathrm{for} \quad t=0\end{array}\right.">

where <img src="https://render.githubusercontent.com/render/math?math=K_c"> is the contamination probability, <img src="https://render.githubusercontent.com/render/math?math=K_r"> is the recovery probability, <img src="https://render.githubusercontent.com/render/math?math=K_d"> is the death probability.

We'll assume the contamination probability increases with people's mobility <img src="https://render.githubusercontent.com/render/math?math=v">.
If people were 100% immobile that would mean <img src="https://render.githubusercontent.com/render/math?math=v = 0"> . We'll assume that usual people's mobility is <img src="https://render.githubusercontent.com/render/math?math=v = 1"> .

<img src="https://render.githubusercontent.com/render/math?math=K_c = 0.4 \cdot v">

Here <img src="https://render.githubusercontent.com/render/math?math=0.4"> is arbitrary.

## Effect of control measures

**How does this model behaves in time ?**

<p align="center">
    <img src="https://user-images.githubusercontent.com/40028739/76973966-e6380880-6930-11ea-8ec8-cf7c3003f69f.png" alt="drawing" width="500"/>
</p>

First, **more and more people get contaminated**. Then as people recover and developp antibodies, a **contamination peak** can be seen after which contaminated population **decreases until reaching zero**: the epidemic has ended.

By decreasing people's mobility, the contamination peak is **delayed** and is **less significant** in terms of contaminated people. Also the epidemic ends later.

Overall, **the curve has been flatted**!

**Great! But why would we care ?**

Well let's take a look at the ammount of dead people now...
<p align="center">
    <img src="https://user-images.githubusercontent.com/40028739/76974131-1ed7e200-6931-11ea-9654-324073f08d50.png" alt="drawing" width="500"/>
</p>
Here we start to see the importance of taking control measures! **As the mobility decreases, deaths decreases as well!**
That's because if less people get sick, then obviously less people a likely to die from the disease!

But that's not quite the way our health system works right ? People don't miraculously heal themselves (at least not all of them): some of them go to the hospital. And if there are too many patients then ... it is more likely that people will die and heal less rapidly.

In order to take this effect into account in our model, let's first assume a hospital capacity <img src="https://render.githubusercontent.com/render/math?math=C">. If the number of sick people is above this capacity, the recovering probability <img src="https://render.githubusercontent.com/render/math?math=K_r"> will decrease by 50% and the death probability <img src="https://render.githubusercontent.com/render/math?math=K_d"> will increase by 50%.
What will happen then ?

<img src="https://user-images.githubusercontent.com/40028739/76974014-f9e36f00-6930-11ea-8da8-2cf38e16fe74.png" alt="drawing" width="420"/><img src="https://user-images.githubusercontent.com/40028739/76974237-3fa03780-6931-11ea-9d15-87671ad77bbf.png" alt="drawing" width="420"/>

We added to the previous graphs dashed lines corresponding to the extended model with a hospital saturation limit.
If people's mobility is not reduced enough **the number of sick people increases by 12%!** But more important is that **the number of deaths almost doubled**!

That's pretty much it!
The simple code I used is available if you wish to play with it and tweak the parameters a little!

### Takeaway message: stay home!


## Model validation and predictions

Alright. Is this model actually representing what's **happening in reality** ?
One way to found out: try to **reproduce actual epidemics** that happened in the past!

Let's do it with the recent Covid-19 epidemic in China that is nearly ended by now.
The model's parameters (contamination, recovering and death rates) will be adjusted in order to fit actual data as best as we can.

<img src="https://user-images.githubusercontent.com/40028739/77149687-72ae0c80-6a92-11ea-831d-a09e8ad57611.png" alt="drawing" width="420"/><img src="https://user-images.githubusercontent.com/40028739/77149685-72ae0c80-6a92-11ea-90a3-173a5643ca19.png" alt="drawing" width="420"/>

Not that bad afterall!
We now know that **our model can reproduce actual epidemic behaviour** with more or less accuracy.
Could we use this fitting process to try and **predict the future** ?
I'd really like to know when I'll be authorised to go out again...so let's do it for France!

<img src="https://user-images.githubusercontent.com/40028739/77149693-76da2a00-6a92-11ea-963e-cfafe0ca5a15.png" alt="drawing" width="420"/><img src="https://user-images.githubusercontent.com/40028739/77149691-76da2a00-6a92-11ea-935f-cdb9d4a793be.png" alt="drawing" width="420"/>

Alright, so this is obviously not as accurate as the case for China cause we simply don't have enough data yet. This means that the predictions will gain in accuracy day by day!
But so far, all we can expect is that the epidemic in France (assuming there won't be any changes in the confinement measures) won't be over until the end of April!
We'll come back then and check if the results were okay!
