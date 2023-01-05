# sotcks-support-resistance-finder
Identify support and resistance zones of stocks price using python!
<h1>
What is support and resistance zones and how we can find them?
</h1>
When price gose down once or more than once to an specific price and then turns up again, we call that area "Support zone".
<br>
When price gose up once or more than once to an specific price and then turns down again, we call that area "Resistance zone".
<h1>
What is usage of this zones?
</h1>
I gonna say an example, Suppose you bought a car for $9,700. Two months later, you decide to buy another one for your daughter, but suddenly you realize that the price of that car has gone up and a friend tells you that the price is going to go down again. Since you bought this car last time for 9700 dollars, if the price reaches there, you are ready to buy it again and you actually support that price. Various other examples can be found.
<br>
So now we know that these support and resistance areas play an important role in determining the continuation of the price trend. So we expect the price reaction to these areas!
<br>
Lets go on python!
<h1>
How to install requirements
</h1>
Simply use this command in terminal:

```shell

pip3 install -r requirement.txt

```

<h1>
How to use script
</h1>
You can customize this script for your porpose, but by default this script runs from CLI.
<br>
Simply use this command in terminal:

```shell

python3 main.py btcusdt 1hour 1000 n

```

<br>
There is 4 argumans:
<br>
<ul>
<li>1- Symbol pair name like: BTCUSDT TRXUSDT ...</li>
<li>2- K-line information category, supports the following parameters: 1min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 12hour, 1day, 3day, 1week</li>
<li>3- Last N K-line(candles) to calculate and display resistance and support areas: N must be lower than 1,001</li>
<li>4- When pass "n": script will calculates most important support and resistance zones. When pass "y": script will calculates all support and resistance zones.</li>
</ul>
<br>
And there is no more explanation remained, if you had any question contact me by email: pooriyamadandar@gmail.com
