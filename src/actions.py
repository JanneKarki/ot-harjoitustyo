import yfinance as yf
from user import User
from user_repository import (user_repository as default_user_repository)
from stock_repository import (stock_repository as default_stock_repository)
from services.user_services import user_services

class InvalidCredentialsError(Exception):
    pass



class Actions:

    '''Sovelluslogiikasta vastaava luokka''' 

    def __init__(self, user_services, user_repository=default_user_repository,
                 stock_repository=default_stock_repository,
                 ):
        """Konstruktori, joka luo sovelluslogiikan palvelun
        
        
        Args:
            stock_repository:

                Olio, jolla on StockRepository-luokkaa vastaavat metodit.
            user_repository:
                Olio, jolla on UserRepository-luokkaa vastaavat metodit.
        """
        
        self._user_services = user_services
        self._logged_user = None
        self._stock_repository = stock_repository
        self._user_repository = user_repository

    def get_latest_price(self, stock):
        """Palauttaa haettavan osakkeen sen hetkisen hinnan
        
        Args:
            stock: Merkkijono joka kertoo osakkeen symbolin.
        
        Returns:
            Paluttaa osakkeen hinnan yfinance moduulista 
            kahden desimaalin tarkkuudella
        
        """
        share = yf.Ticker(stock)
        dataframe = share.history(period="1d", interval="1d")
        return float("%.2f" % dataframe.iat[0, 3])

    def buy_stock(self, stock, amount):

        """Ostaa osaketta annetun määrän ja lisää ne käyttäjän 
        portfolioon, sekä vähentää niiden hinnan käyttäjän pääomasta
        
        Args:
            stock:
            amount:
        
        Returns
        """

        buy_price = self.get_latest_price(stock)
        self._user_repository.adjust_capital(
            self._logged_user, -abs(buy_price*amount))
        self._stock_repository.add_to_portfolio(
            self._logged_user, stock, buy_price, amount)
        return buy_price

    def sell_stock(self, stock, amount):

        """Myy osaketta annetun määrän ja vähentää ne käyttäjän, 
        sekä lisää niiden hinnan käyttäjän pääomaan
        
        Args:
            stock:
            amount: 
            
        Returns:
        """
        sell_price = self.get_latest_price(stock)
        self._user_repository.adjust_capital(
            self._logged_user, sell_price*amount)
        self._stock_repository.remove_stock_from_portfolio(
            self._logged_user, stock, amount)
        return sell_price

    def get_stock_info(self, stock):
        """Hakee ja tulostaa osakkeen yritystiedot yfinance moduulista
        
        Args:
            stock:"""
        share = yf.Ticker(stock)
        print(share.info['longBusinessSummary'])


    def get_capital(self):
        """Palauttaa kirjautuneen käyttäjän pääoman"""

        return self._user_repository.get_user_capital(self._logged_user)

    """ def create_user(self, username, password, capital):
        """"""Luo uuden käyttäjän
        
        Args:
            username:
            password:
            capital:
            
        Returns:
        
        """"""
        user = self._user_repository.new_user(
            User(username, password, capital))
        self._logged_user = username
        return user
    """
    def get_portfolio(self):
        """Palauttaa kirjautuneen käyttäjän portfolion"""
        return self._stock_repository.get_portfolio_from_database(self._logged_user)

    def get_all_users(self):
        """Palauttaa tulosteena kaikki luodut käyttäjät"""
        return self._user_repository.print_all_users()

  #  def get_user(self):
   #     return self._user_repository.find_user(self._logged_user)

   # def find_user(self, username):
   #     row = self._user_repository.find_user(username)
   #     if row:
   #         return True
   #     return False

    def get_logged_user(self):
        #print(user_services.get_logged_user(), "logged user from user_services")
        return self._logged_user

    def find_stock_from_portfolio(self,stock):
        return self._stock_repository.get_stock_from_portfolio(self._logged_user,stock)

    def login(self, username):
        """Kirjaa käyttäjän sisään sovellukseen
        
        Args:
            username:
            password:

        
        """
        """
        user = self._user_repository.find_user(username)
        result = None,None
        if user:
            result = user
        if result[1] != password:
            raise InvalidCredentialsError('Väärä käyttäjätunnus tai salasana')
        self._user = result[0]
        """
        self._logged_user = username

    def logout(self):
        """Kirjaa käyttäjän ulos sovelluksesta"""
        self._logged_user = None    

    def rank_investments(self):
        """Lasekee ja järjestää sijoitukset listaan tuoton/tappion perusteella"""
        
        rank_list = []
        portfolio = self.get_portfolio()
        for item in portfolio:
            latest_price = self.get_latest_price(item[0])
            entry_price = item[1]*item[2]
            end_price = latest_price*item[2]
            profit = end_price-entry_price
            rank_list.append((item[0], "%.3f" % profit))
        rank_list.sort(key=lambda y: y[1])
        return rank_list

    def total_win_loss(self):
        total = 0
        portfolio = self.get_portfolio()
        for item in portfolio:
            latest_price = self.get_latest_price(item[0])
            entry_price = item[1]*item[2]
            end_price = latest_price*item[2]
            profit = end_price-entry_price
            total += profit
        return total

    def total_portfolio_worth(self):
        portfolio = self._stock_repository.get_portfolio_from_database(self._logged_user)
        total_worth = 0
        for i in portfolio:
            stock_amount = i[2]
            present_price = self.get_latest_price(i[0]) 
            total_worth += (stock_amount*present_price)
        return total_worth


    def total_capital(self):
        if self._logged_user:
            net_capital = self.get_capital()
            return net_capital+self.total_portfolio_worth()
        return None

    def print_total_win_loss(self):
        total = self.total_win_loss()
        print("Net profit " "%.3f" % total)

actions = Actions(user_services)