<div align="center">
  <img src="https://github.com/quick-trade/xoney_py/blob/dev/img/logo.png?raw=true" width="340" height="340">

# Xoney
</div>

[![CircleCI](https://circleci.com/gh/quick-trade/xoney_py.svg?style=svg)](https://circleci.com/gh/quick-trade/xoney_py)
[![codecov](https://codecov.io/gh/quick-trade/xoney/branch/dev/graph/badge.svg)](https://codecov.io/gh/quick-trade/xoney)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/77c2d40203e847f2b028d456562cc8cf)](https://www.codacy.com/gh/quick-trade/xoney/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=quick-trade/xoney&amp;utm_campaign=Badge_Grade)


Xoney is a flexible Python framework for creating and testing trading systems based on statistical hypothesis testing.

## Key Features

- Strategy creation and backtesting
- Parameter optimization
- Live trading support
- Event-driven architecture
- Extensive metrics and analysis tools

## Installation

```bash
pip install git+https://github.com/quick-trade/xoney_py.git
```

## Quick Start

### Creating a Strategy

```python
from xoney.strategy import Strategy
from xoney.generic.events import Event, OpenTrade
from xoney.generic.trades import Trade, TradeMetaInfo
from xoney.generic.trades.levels import LevelHeap, SimpleEntry

class MyStrategy(Strategy):
    def run(self, chart):
        # Your trading logic here
        self.signal = "long" if some_condition else "short"
        
    def fetch_events(self) -> list[Event]:
        if self.signal == "long":
            return [
                OpenTrade(
                    Trade(
                        side=TradeSide.LONG,
                        entries=LevelHeap([SimpleEntry(price=self.current_price, trade_part=1)]),
                        breakouts=LevelHeap(),
                        meta_info=TradeMetaInfo(strategy_id=self._id)
                    )
                )
            ]
        return []
```

### Backtesting

```python
from xoney import Backtester, TradingSystem, Instrument
from xoney.generic.timeframes import DAY_1

system = TradingSystem({
    MyStrategy(): [Instrument("BTC/USD", DAY_1)]
})

backtester = Backtester(initial_depo=10000)
equity = backtester.run(charts=charts, trading_system=system)
```

### Parameter Optimization

```python
from xoney.optimization import DefaultOptimizer
from xoney.analysis.metrics import SharpeRatio
from xoney.strategy import IntParameter, FloatParameter

class MyStrategy(Strategy):
    @property
    def parameters(self):
        return {
            "window": IntParameter(min=10, max=100),
            "threshold": FloatParameter(min=0.1, max=5.0)
        }

optimizer = DefaultOptimizer(
    backtester=Backtester(),
    metric=SharpeRatio,
    n_trials=100
)

best_system = optimizer.run(system, charts)
```

### Custom Events

```python
from xoney.generic.events import Event
from xoney.generic.trades import TradeHeap

class MyCustomEvent(Event):
    def __init__(self, some_param):
        self.some_param = some_param
        
    def handle_trades(self, trades: TradeHeap) -> None:
        # Implement your event logic here
        pass
```

## Features Under Development

The following features are currently incomplete or need implementation:

1. Trade Volume Management
```python
# TODO implementation needed in BaseBreakout._update_trade_volume()
```

2. Real-time Trading Support
```python
# TODO: support real-time trading in BalanceBaseEvent._handle_free_balance()
```

3. Strategy Testing Accuracy
```markdown
## Bugs
- Unknown strategy testing accuracy
```

## Advanced Features

### Walk-Forward Analysis

```python
from xoney.optimization.validation.walkforward import WFSampler
from xoney.optimization.validation.validator import Validator

sampler = WFSampler(
    train_period=timeframes.DAY_1 * 100,
    test_period=timeframes.DAY_1 * 20,
    optimizer=optimizer
)

validator = Validator(charts=charts, sampler=sampler)
results = validator.test(system)
```

### Custom Stop Conditions

```python
from xoney.live.stopping import StopCondition

class MyStopCondition(StopCondition):
    def should_stop(self) -> bool:
        # Implement your stop logic
        return some_condition
```

###### Project licensed under Apache-2
