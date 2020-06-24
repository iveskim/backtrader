# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
from vitu import ai, log

# 配置账户初始持仓信息
ai.create_account(name='account1', exchange='binance', account_type='digital.spot',
                  position_base=[{'asset': 'BTC', 'qty': 10}, {'asset': 'USDT', 'qty': 200000}])


# 在这个方法中编写任何的初始化逻辑，context对象将会在你的算法策略的任何方法之间做传递
def initialize(context):
    # 设置这个策略当中会用到的参数，在策略中可以随时调用
    context.account = context.get_account('account1')


# 你选择的universe crypto的数据更新将会触发此段逻辑，例如日线历史数据或者是实时数据更新
def handle_data(context):
    # 开始编写你的主要的算法逻辑

    # 获取最新价格
    current_price = context.get_price("BTC/USDT.binance")
    context.account.buy("BTC/USDT.binance", current_price, 0.2)

# 可以直接指定universe，或者通过筛选条件选择universe池
universe = ai.create_universe(['BTC/USDT.binance'])

# 配置策略参数如：基准、回测数据级别等
my_strategy = ai.create_strategy(
    initialize,
    handle_data,
    universe=universe,
    benchmark='csi5',
    freq='d',
    refresh_rate=1,
)

# 配置回测参数如：回测日期、手续费率
ai.backtest(
    strategy=my_strategy,
    start='2018-10-10',
    end='2019-08-10',
    commission={'taker': 0.0002, 'maker': 0.0002}
)