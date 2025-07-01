# class SyncBinanceOrderStatusChangeHandler(SocketEventHandler):
#     def __init__(
#         self,
#         wallet: Wallet,
#         logger: logging.Logger,
#         socket_sectretary: UserSocketSecretary,
#         # mq_helper: PushOrderExecuteMQHelper,
#         testnet: bool = False,
#     ) -> None:
#         self.id = str(uuid.uuid4())
#         self.__running = True
#         self.__storage = socket_sectretary
#         self.__logger = logger
#         # self.__helper = mq_helper
#         self.__base_url = "https://api.binance.com"
#         self.__base_ws_url = "wss://stream.binance.com:9443"

#         if testnet:
#             self.__base_url = "https://testnet.binance.vision"
#             self.__base_ws_url = "wss://stream.testnet.binance.vision/ws"

#         self.__client = Spot(
#             base_url=self.__base_url,
#             api_key=wallet.api_key,
#             api_secret=wallet.api_secret,
#         )
#         self.socket_manager = BinanceWebsocketManager(
#             self.__base_ws_url,
#             asyncio.get_event_loop(),
#             True,
#             self.on_message(),
#             self.on_open(),
#             self.on_close(),
#             self.on_error(),
#             self.on_ping(),
#             None,
#             self.__logger,
#             None,
#         )

#     @staticmethod
#     async def make(
#         wallet: Wallet,
#         logger: logging.Logger,
#         socket_sectretary: UserSocketSecretary,
#         # mq_helper: PushOrderExecuteMQHelper,
#         testnet: bool = False,
#     ) -> "SyncBinanceOrderStatusChangeHandler":
#         socket = SyncBinanceOrderStatusChangeHandler(
#             wallet=wallet,
#             logger=logger,
#             socket_sectretary=socket_sectretary,
#             # mq_helper=mq_helper,
#             testnet=testnet,
#         )
#         await socket_sectretary.save_socket(
#             socket_id=socket.id, user_id=wallet.user_id, wallet_id=wallet.id
#         )
#         return socket

#     def start(self):
#         self.listen_key = self.create_listen_key()
#         self.socket_manager.start()

#     # Остановка пользовательского сокета
#     def stop(self) -> None:
#         self.__running = False
#         self.socket_manager.close()

#     def create_listen_key(self):
#         listen_key = self.__client.new_listen_key().get("listenKey")

#         if listen_key is None:
#             raise ValueError("listenKey is None")

#         return listen_key

#     def update_listen_key(self):
#         self.__client.renew_listen_key(self.listen_key)

#     # Метод возврашает обработчик закрытия вебсокета
#     def on_close(self) -> Callable:
#         async def callback(_):
#             if self.__running:
#                 await self.__storage.update_status(self.id, Status.ERROR.value)
#                 return True
#             else:
#                 await self.__storage.update_status(self.id, Status.STOP.value)
#                 return

#         return callback

#     # Метод возврашает обработчик открытия вебсокета
#     def on_open(self) -> Callable:
#         async def callback(_):
#             self.__logger.info("Socket opened.")
#             await self.socket_manager.user_data(listen_key=self.listen_key)
#             await self.__storage.update_status(self.id, Status.RUNING.value)

#         return callback

#     # Метод возврашает обработчик ошибок вебсокета
#     def on_error(self) -> Callable:
#         async def callback(_, error):
#             self.__logger.info("Event: Socket error: {}".format(error))
#             await self.__storage.update_status(self.id, Status.ERROR.value)

#         return callback

#     def on_ping(self) -> Callable:
#         async def callback(_):
#             self.__storage.set_ping_time(self.id)
#             self.__logger.info("Event: Socket ping.")

#         return callback

#     # Метод возврашает обработчик сообщений
#     def on_message(self) -> Callable:
#         async def callback(_, mes):
#             mes = json.loads(mes)
#             if "e" not in mes:
#                 return

#             if mes["e"] == "executionReport" and mes["X"] == "FILLED":
#                 await self._is_execution_report(mes)
#             elif mes["e"] == "outboundAccountPosition":
#                 self._is_outbound_account_position(mes)
#             elif mes["e"] == "balanceUpdate":
#                 self._is_balance_update(mes)

#         return callback

#     # Метод исполения ордеров
#     async def _is_execution_report(self, mes) -> None:
#         (
#             self.__helper.push_did_execute(
#                 await self.__storage.get_bot_id(mes["c"]),
#                 mes["c"],
#                 datetime.fromtimestamp(mes["E"] / 1000),
#                 decimal_from_json(mes["L"]),
#             ),
#         )

#         self.__logger.info(f"Event: Order executed: {mes}")

#     # Метод обновления баланса при исполнении ордера
#     def _is_outbound_account_position(self, mes) -> None:
#         self.__logger.info(f"Event: Balance update: {mes}")

#     # Метод обновления баланса при выводе средств с баланса
#     def _is_balance_update(self, mes) -> None:
#         self.__logger.info(f"Event: Balance update: {mes}")

#  _entry_capital = None
#             if isinstance(settings.bot.entry, FromWalletEntryCapitalSchemas):
#                 _entry_capital = FromWalletEntryCapital(
#                     decimal_from_json(settings.bot.entry.volume),
#                     decimal_from_json(settings.bot.entry.price),
#                 )

#             if isinstance(settings.bot.entry, BuyingEntryCapitalSchemas):
#                 _entry_capital = BuyingEntryCapital(
#                     decimal_from_json(settings.bot.entry.volume),
#                     Order.TypeMarket()
#                     if settings.bot.entry.order_type == EntryOrderType.MARKET
#                     else Order.TypeLimit(decimal_from_json(settings.bot.entry.price)),
#                 )


# TakeProfitBot.Settings(
#                     _entry_capital,
#                     TakeProfit(
#                         [
#                             TakeProfit.Step(
#                                 decimal_from_json(tp_step.take_profit),
#                                 decimal_from_json(tp_step.volume_in_percent),
#                             )
#                             for tp_step in settings.bot.take_profit.steps
#                         ]
#                     ),
#                     depends=StopLoss(
#                         decimal_from_json(decimal_from_json(settings.bot.depends.reduction))
#                     )
#                     if isinstance(settings.bot.depends, StopLossSchemas)
#                     else Insurance(
#                         [
#                             Insurance.Step(
#                                 decimal_from_json(step.reduction),
#                                 decimal_from_json(step.amount),
#                             )
#                             for step in settings.bot.depends.steps
#                         ]
#                     )
#                     if settings.bot.depends is not None
#                     else None,
#                 ),


# from api.endpoints.bot.schemas import (
#     AutomaticTakeProfitSchemas,
#     InsuranceSettingsSchemas,
#     InsuranceType,
#     InsuranceSchemas,
# )
# from api.services.bot import CalculateOrders


# test = CalculateOrders(volume=1000)
# # test.calculate_insurance(InsuranceSchemas(
# #     insurance=InsuranceSettingsSchemas(
# #         type=InsuranceType.FROM_AVERAGE,
# #         count=3,
# #         step=5,
# #         mrt=1.5,
# #         price_step=1.5
# #     )
# # )

# val = test.calculate_take_profit_steps(
#     AutomaticTakeProfitSchemas(
#         take_profit=15,
#         take_amount=15,
#         step=1,
#         mrt=1.5,
#         amount_limit=100,
#     )
# )
# for i in val:
#     print(i.__dict__)


# from dataclasses import dataclass
# from pydantic import Field
# from pydantic_settings import BaseSettings


# @dataclass
# class APIConfig:
#     host: str 
#     port: int = 8000
#     debug: bool = __debug__


# class Config(BaseSettings):
#     api: APIConfig 


# config = Config()

# print(config)

from eth_account import Account
from eth_account.messages import encode_defunct

# Приватный ключ пользователя (никогда не логируй, не храни в коде)
private_key = "0xabc123..."  # Пример, замени на реальный

# Сообщение для подписи (например, nonce)
nonce = "my-nonce-string"

# Кодируем сообщение в формат EIP-191
message = encode_defunct(text=nonce)

# Подписываем сообщение
signed_message = Account.sign_message(message, private_key=private_key)

# Получаем сигнатуру
signature = signed_message.signature.hex()

print(f"Signature: {signature}")
