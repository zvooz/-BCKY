## caveats

My code stinks. Don’t blindly trust it. 

I haven't figured out how to take market holidays off the x-axis. Please help me if you know how. 

The stocks for MC and OR I use in the portfolios are $LVMHF and $LRLCF instead of $MC.PA and $OR.PA because I'm too lazy to do currency conversions, although it is quite simple to get the exchange reate from IEX. 

This thing doesn't handle stock splits and portfolio rebalances, yet. I have some sort of an idea of how it might be done, but I'm too lazy to do it for now. Luckily none of the companies in the portfolios have splits scheduled, as far as I know.

For all the candlestick charts, the open and close quotes are accurates, but the highs and lows are likely not. The highs and lows are the sum of an index’s components’ highs and lows. To get accurate highs and lows, I would need tick data, but that would exhaust my free IEX accoun's message quota quite quickly. I don't even know if I have enough quota for one day's worth of tick data.

## weighting

Throw $1000 into each ticker at the epoch (2019-01-01), then round the number of shares to the nearest integer.

### build/play with the code

Just clone it and run ./update

```bash
git clone https://github.com/zvooz/-BCKY.git
cd -BCKY
./update
```

`./update -h` for more information


<p>
	Data provided for free by <a href="https://iextrading.com/developer">IEX Cloud</a>. View <a href="https://iextrading.com/api-exhibit-a/">IEX’s Terms of Use</a>
	<sub>
		<a href="https://www.iexcloud.io">
			<img src="docs/assets/IEX/logo-color.svg" height="25"/>
		</a>
	</sub>
</p>

<a href="http://www.wtfpl.net/">
	<img src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-1.png" height="30" alt="WTFPL" />
</a>

<script type="text/javascript">
    function AdjustIframeHeightOnLoad() { document.getElementById("chart-iframe").style.height = document.getElementById("chart-iframe").contentWindow.document.body.scrollHeight + "px"; }
    function AdjustIframeHeight(i) { document.getElementById("chart-iframe").style.height = parseInt(i) + "px"; }
</script>


