import cbpro
import config

BUY = 'buy'
SELL = 'sell'


class TradingBot:

    def __init__(self, cb_pro_client):
        self.cb_pro_client = cb_pro_client

    def limitTrade(self, action, limitPrice, quantity, orderType, productID, ):
        if action == BUY:
            response = self.cb_pro_client.buy(price=limitPrice,
                                              size=quantity,
                                              order_type=orderType,
                                              product_id=productID,
                                              overdraft_enabled=False
                                              )
        elif action == SELL:
            response = self.cb_pro_client.sell(price=limitPrice,
                                               size=quantity,
                                               order_type=orderType,
                                               product_id=productID,
                                               overdraft_enabled=False
                                               )

        print(response)

    def viewAccounts(self, asset):
        # grabs portfolio information for the assets owned
        accounts = self.cb_pro_client.get_accounts()
        account = list(filter(lambda x: x['currency'] == asset, accounts))[0]
        return account

    def viewOrder(self, order_id):
        order = self.cb_pro_client.get_order(order_id)
        return order

    def getCurrentBitcoinPrice(self):
        ticker = self.cb_pro_client.get_product_ticker(product_id='BTC-USD')
        return ticker['bid']

    def marketOrderByFunds(self, productId, action, funds):
        marketOrder = self.cb_pro_client.place_market_order(product_id=productId,
                                                            side=action,
                                                            funds=funds)
        print(marketOrder)
        return marketOrder

    def marketOrderByQuantity(self, productId, action, size):
        marketOrder = self.cb_pro_client.place_market_order(product_id=productId,
                                                            side=action,
                                                            size=size)
        print(marketOrder)
        return marketOrder


if __name__ == '__main__':
    auth_client = cbpro.AuthenticatedClient(config.CB_KEY,
                                            config.CB_SECRET,
                                            config.CB_PASSPHRASE,
                                            api_url=config.CB_URL)

    tradingBot = TradingBot(auth_client)

    currentBTCPrice = tradingBot.getCurrentBitcoinPrice()
    print('Current BTC Price: ' + currentBTCPrice)

    accountUSDBalance = tradingBot.viewAccounts('USD')['balance']
    print(accountUSDBalance)
    # tradingBot.limitTrade(BUY,
    #                  limitPrice='30000',
    #                  quantity='1',
    #                  orderType='market',
    #                  productID='BTC-USD')

    lastOrderInfo = tradingBot.viewOrder('05ac7b74-8b4a-4d5f-bcf0-a3d6729afc84')
    print(lastOrderInfo)

    # tradingBot.marketOrderByFunds(productId='BTC-USD',
    #                               action=BUY,
    #                               funds='10000.00')
    #
    # tradingBot.marketOrderByQuantity(productId='ETH-BTC',
    #                                  action=BUY,
    #                                  size='1')

    print(tradingBot.viewAccounts('BTC')['balance'])
    print(tradingBot.viewAccounts('ETH')['balance'])
