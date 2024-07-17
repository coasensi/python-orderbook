_Alexandre_ LAURENT  
_Charles_ ODEND'HAL  

**PROJECT : Creating an Order Book Simulator**

In this project, we developed an order book starting from a generic financial product, tradable on a financial market in general. We implemented several class methods to differentiate between takers, makers, buyers, and sellers. Then, we set up a concrete example with the involvement of multiple traders to test the functioning of this continuous order book.

**Part 1: Creating the Order Book Class**

We then define the methods for adding orders to the order book.  
**ordre_achat** adds a buy order. **ordre_vente** adds a sell order.

First, the **ordre_check** method ensures that tick and lot constraints are respected.  
If not, the user is notified, and the order is not executed.

We use the **ordre_achat** method to register a buy order and the **ordre_vente** method to register a sell order.  
If the order is maker, it is not immediately executed and is added to the corresponding pandas dataframe (**carnetachat** or **carnetvente**).  
If the order is taker, it is immediately executed at the market price via the **taker_exec** method.

The **taker_exec** method allows a taker's order to be executed immediately at the market price.  
The variable type_carnet is assigned to the book corresponding to the orders that will match the taker order (carnetvente if ordre_achat and vice versa).  
We loop through each order in the book, sorted in the appropriate order (ascending for carnetvente, descending for carnetachat).  
If the amount of the book order is less than the amount of the taker order, the former is executed, and we continue the loop with the taker order amount equal to the subtraction of the two.  
The loop continues until the taker order is fully executed, or there are no more "matchable" orders in the book.  
Executed orders are removed from the book using the **ordre_sup** method.  
If at the end of this loop, the taker amount could not be fully executed, it is passed as a maker order in the market.

We define the **ordre_sup** method to remove an order from the book. This method takes three arguments: the participant, the position, and the amount.  
We determine the book concerned by the removal using the position argument.  
We then remove the elements from the book whose participants and amounts match.

**Part 2: Example**

We generate sell and buy orders using the random method to generate random numbers. We also test the **ordre_sup** method to delete orders.  
By displaying the order book, we observe that all taker orders are executed. This demonstrates the proper functioning of the **taker_exec** method.  
However, maker orders are not executed even though there are counterparts. An extension of our program would be to create a fixing algorithm to execute them.
