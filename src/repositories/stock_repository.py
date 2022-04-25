from database_connection import get_database_connection


class StockRepository:
    """Stocks tietokannan hallinnasta vastaava luokka.

    Attributes:
        connection: Tietokantayhteys.
    """
    def __init__(self, connection):
        """Luokan konstruktori.

        Args:
            connection (object): Tietokantayhteyden connection-olio.
        """
        self.connection = connection

    
    def add_to_portfolio(self, user, stock, price, amount):
        """Lisää osakkeen tietokantaan. Tarkistaa ensin löytyykö osake jo käyttäjän
        tietokannasta. Jos osake löytyy, hinta päivitetään uuden ja vanhan hinnan
        keskiarvoon per osake, sekä osakkeiden määrään lisätään uudet osakkeet.

        Args:
            user (string): Käyttäjän tunnus
            stock (string): Osakkeen symboli
            price (float): Osakkeen hinta
            amount (integer): Osakkeiden määrä

        """
        stocks_database = self.connection.cursor()

        stocks_database.execute(
            """SELECT avg_price,
            amount FROM Stocks WHERE user = ? and content = ?""",
            [user, stock]
            )

        data = stocks_database.fetchall()

        if len(data) == 0: # Osake ei löytynyt tietokannasta
            stocks_database.execute(
                """INSERT INTO Stocks (
                    user, 
                    content, 
                    avg_price, 
                    amount)
                    values (?,?,?,?)""",
                    [user, stock, price, amount]
                )
        else: # Osake löytyi tietokannasta
            old_amount = data[0][1]
            new_amount = old_amount+amount
            old_total_value = data[0][0]*data[0][1]
            new_total_value = amount*price
            new_avg_price = (old_total_value+new_total_value)/new_amount
        
            stocks_database.execute(
                """UPDATE Stocks
                    SET avg_price = ?, amount = ?
                    WHERE user = ?
                    AND content = ?""",
                    [float(f"{new_avg_price:.2f}"),new_amount, user, stock]
                )

    
    def remove_stock_from_portfolio(self, user, stock, amount):
        """Poistaa osakkeen tietokannasta, joko kokonaan, tai vähentää sitä
            annetun määrän verran.
        
        Args: 
            user (string): Käyttäjän tunnus
            stock (string): Osakkeen symboli
            amount (integer): Osakkeiden määrä

        """
        stocks_database = self.connection.cursor()

        stocks_database.execute(
            """SELECT avg_price,
                amount
                FROM Stocks
                WHERE user = ?
                AND content=?""",
                [user, stock]
            )

        data = stocks_database.fetchall()

        if len(data) > 0: #osake löytyi tietokannasta
            old_amount = data[0][1]
            if amount == old_amount:
                stocks_database.execute(
                    """DELETE FROM 
                        Stocks WHERE 
                        user = ?
                        AND content = ?""",
                        [user, stock]
                    )

            if amount < old_amount:
                new_amount = old_amount - amount
                stocks_database.execute(
                    """UPDATE Stocks 
                        SET amount = ?
                        WHERE user = ? 
                        AND content = ?""",
                        [new_amount, user, stock]
                )

    
    def get_portfolio_from_database(self, user):
        """ Palauttaa tietokannasta käyttäjän portfolion.
        
        Args:
            user (string): Käyttäjän tunnus jonka portfolio palautetaan.
            
        Returns:
            list: Palautta listan käytäjän osakkeista, niiden määrän ja 
            keskimääräisen hankintahinnan. 
        """
        stocks_database = self.connection.cursor()

        stocks_database.execute(
            """SELECT content,
                avg_price,
                amount 
                FROM Stocks 
                WHERE user = ?""",
                [user]
            )

        results = stocks_database.fetchall()
        print(type(results))
        return results

    
    def get_stock_from_portfolio(self, user, stock):
        """ Hakee osakkeen tietokannasta.

        Args:
            user (string): Käyttäjän tunnus, jonka portfoliosta osake palautetaan.
            stock (string): Osakkeen symboli, joka palautetaan

        Returns:
            list: Palauttaa osakkeen, sen määrän ja keskimääräisen
            hankintahinnan.
        """
        stock_database = self.connection.cursor()

        stock_database.execute(
            """SELECT * 
                FROM Stocks 
                WHERE user = ?
                AND content=?""",
                [user, stock]
            )
        
        result = stock_database.fetchone()

        return result

    
    def delete_all(self):
        """ Poistaa tietokannasta kaikki osakkeet.
        """
        cursor = self.connection.cursor()

        cursor.execute("DELETE FROM Stocks")

        self.connection.commit()


stock_repository = StockRepository(get_database_connection())
