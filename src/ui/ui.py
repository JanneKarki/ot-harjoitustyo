from ui.login_view import LoginView
from ui.create_user_view import CreateUserView
from ui.action_view import ActionView
from ui.portfolio_view import PortfolioView


class UI:
    def __init__(self, root):
        """_summary_

        Args:
            root (_type_): _description_
        """
        
        self._root = root
        self._entry = None
        self._current_view = None

    def start(self):
        self._show_login_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _handle_action(self, stock_actions, portfolio):
        self._show_action_view(stock_actions, portfolio)

    def _handle_portfolio(self, stock_actions, portfolio):
        self._show_portfolio_view(stock_actions, portfolio)

    def _handle_start(self):
        self._show_login_view()

    def _handle_create_user(self):
        self._show_create_user_view()

    def _show_login_view(self):
        self._hide_current_view()

        self._current_view = LoginView(
            self._root,
            self._handle_create_user,
            self._handle_action
        )
        self._current_view.pack()

    def _show_create_user_view(self):
        self._hide_current_view()

        self._current_view = CreateUserView(
            self._root,
            self._handle_start
        )
        self._current_view.pack()

    def _show_action_view(self, stock_actions, portfolio_services):
        self._hide_current_view()

        self._current_view = ActionView(
            self._root,
            self._handle_start,
            self._handle_portfolio,
            stock_actions,
            portfolio_services

        )
        self._current_view.pack()

    def _show_portfolio_view(self, stock_actions, portfolio):
        self._hide_current_view()
        try:
            self._current_view = PortfolioView(
                self._root,
                self._handle_action,
                stock_actions,
                portfolio
            )
            self._current_view.pack()
        except:
            self._handle_action(stock_actions, portfolio)
            print(
                "Connection problem in yfinance-module. Check your internet connection and try again.")
