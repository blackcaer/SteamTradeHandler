from steampy.client import SteamClient, TradeOfferState


class TradeOffer():

    def __init__(self, steam_client: SteamClient, offer_data) -> None:
        self.steam_client = steam_client

        self.tradeid = offer_data["tradeofferid"]
        self.message = offer_data["message"]
        self.trade_state = offer_data["trade_offer_state"]
        self.is_our_offer = offer_data["is_our_offer"]
        self.time_created = offer_data["time_created"]
        self.steamid64 = TradeOffer.trade_partner_id_to_steamid64(offer_data["accountid_other"])

        self.items_to_give = offer_data["items_to_give"]
        self.items_to_receive = offer_data["items_to_receive"]

    @staticmethod
    def trade_partner_id_to_steamid64(trade_partner_id):
        return int(trade_partner_id) + 76561197960265728    # It just works like that, do not argue

    def accept(self, verbose=False):
        if verbose:
            print(
                f'Accepting trade (id:{self.tradeid}) with msg: "{self.message}". Reciving {len(self.items_to_receive)} items, giving {len(self.items_to_give)} items')

        self.steam_client.accept_trade_offer(self.tradeid)

    def decline(self, verbose=False):
        if verbose:
            print(f'Declining trade (id:{self.tradeid}) with msg: "{self.message}".')

        self.steam_client.decline_trade_offer(self.tradeid)

    def get_items_to_receive(self):
        pass

    def get_items_to_give(self):
        pass

    def is_gift(self):
        return (
                self.items_to_receive
                and not self.items_to_give
                and self.trade_state == TradeOfferState.Active
                and not self.is_our_offer
        )
