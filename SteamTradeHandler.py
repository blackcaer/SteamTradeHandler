import json

from fernet_wrapper import Wrapper as fernet_wrapper
from steampy.client import SteamClient

from steampy.models import TradeOfferState
from TradeOffer import TradeOffer


class SteamTradeHandler:

    def __init__(self, username, steamid, api_key, password, identity_secret, shared_secret, trade_whitelist: list):
        self.username = username
        self.steamid = steamid
        steam_guard_dict = {"steamid": str(self.steamid), "identity_secret": identity_secret,
                            "shared_secret": shared_secret}
        steam_guard_string = json.dumps(steam_guard_dict)

        self.trade_whitelist = trade_whitelist

        self.login_success = False
        self._login(password, api_key, steam_guard_string)

    @classmethod  # Factory method
    def create_account_from_encrypted_file(cls, key, path, trade_whitelist, key_not_password=True):
        # TODO: end that, document it
        def load_file(path):
            f = open(path, "r")
            return json.loads(f.read())

        loaded_data = load_file(path)
        return SteamTradeHandler.create_account_from_encrypted_data(key, loaded_data, trade_whitelist,
                                                                    key_not_password)

    @classmethod  # Factory method
    def create_account_from_encrypted_data(cls, key, accdata, trade_whitelist, key_not_password=True):
        """ Factory method. """

        if not key_not_password:
            key = fernet_wrapper.key_from_pass(key)

        def decrypt(cipher, key):
            return fernet_wrapper.decrypt(cipher, key)

        username = accdata["username"]
        steamid = accdata["steamid"]

        password = decrypt(accdata["encrypted_password"], key)
        api_key = decrypt(accdata["encrypted_api_key"], key)
        identity_secret = decrypt(accdata["encrypted_identity_secret"], key)
        shared_secret = decrypt(accdata["encrypted_shared_secret"], key)

        account = SteamTradeHandler(username=username,
                                    steamid=steamid,
                                    api_key=api_key,
                                    password=password,
                                    identity_secret=identity_secret,
                                    shared_secret=shared_secret,
                                    trade_whitelist=trade_whitelist)
        return account

    @staticmethod  # I'll just leave it like that
    def encrypt_account_data_to_dict(key, username, steamid, password, api_key, identity_secret, shared_secret):
        def encrypt(text, key):
            return fernet_wrapper.encrypt(text, key).decode("utf-8")

        encrypted_api_key = encrypt(api_key, key)
        encrypted_password = encrypt(password, key)
        encrypted_identity_secret = encrypt(identity_secret, key)
        encrypted_shared_secret = encrypt(shared_secret, key)

        encrypted = {"username": username,
                     "steamid": steamid,
                     "encrypted_password": encrypted_password,
                     "encrypted_api_key": encrypted_api_key,
                     "encrypted_identity_secret": encrypted_identity_secret,
                     "encrypted_shared_secret": encrypted_shared_secret
                     }

        return encrypted

    def _login(self, password, api_key, steam_guard_string):
        self.steam_client = SteamClient(username=self.username,
                                        password=password,
                                        api_key=api_key,
                                        steam_guard=steam_guard_string
                                        )
        self.steam_client.login()
        print(f"Login status: {self.steam_client.was_login_executed}")
        # print(f"is_session_alive: {self.steam_client.is_session_alive()}")

        if self.steam_client.was_login_executed and self.steam_client.is_session_alive():
            self.login_success = True

    def get_trade_offers(self):
        """ Get trade offers received and sent as TradeOffer objects.
        Returns:
            Tuple with trade_offers_received and trade_offers_sent. Both are lists of TradeOffer objects.
        """

        resp = self.steam_client.get_trade_offers()["response"]
        to_received_data = resp["trade_offers_received"]
        to_sent_data = resp["trade_offers_sent"]

        to_received = []
        to_sent = []

        for offer_data in to_received_data:
            to_received.append(TradeOffer(self.steam_client, offer_data))

        for offer_data in to_sent_data:
            to_sent.append(TradeOffer(offer_data))

        return to_received, to_sent

    def accept_all_offers(self, gifts_only=False):
        trade_offers_received, trade_offers_sent = self.get_trade_offers()
        responses = []

        if len(trade_offers_sent) != 0:
            print("==trade_offers_sent = ", trade_offers_sent)
            raise NotImplementedError("Not implemented handlind accepting sent offers")

        if len(trade_offers_received) == 0:
            print("No trade offers recived\n")
            return

        for offer in trade_offers_received:
            offer: TradeOffer
            if offer.trade_state not in (TradeOfferState.Active,TradeOfferState.ConfirmationNeed):
                print("Wrong state of offer: ",str(TradeOfferState(offer.trade_state)))
            if gifts_only and not offer.is_gift():
                continue
            try:
                responses.append(offer.accept(verbose=True))
            except KeyError as e:
                if e.args[0] == 'identity_secret':
                    print('You have to accept that offer via Steam Guard\n')
                else:
                    raise e
        return responses
