# Southwest Airlines Automated Flight Booker

This is a project I've made to partially automate the booking of flights through
Southwest Airline's website.

Booking flights can be a tedious ordeal that involves the entry of large
amounts of data. My automation tool aims to provide a simple, easy to use
command line interface in order to expedite this process.

By entering basic flight information through the command line, this tool will automatically pull up
the cheapest flight meeting your constraints, and you only have to enter personal and payment data in order to book it.

If no flight meeting the maximum desired price is found, the page is left open for the user to select a different option.

In the future, this could be automated to a much further extent. I plan on taking text files containing address information as well as payment info through paypal (handling raw card data seems problematic).

Usage -- positional arguments:

  DEPART_IATA     Enter the three letter airport code for departure location
  
  ARRIVAL_IATA    Enter the three letter airport code for arrival location
  
  DEPART_DATE     Enter the departure date in the format MM/DD
  
  NUM_PASSENGERS  Enter the number of adult passengers for this flight
  
  TIME_OF_DAY     Enter a number from 1-4 corresponding to the desired time of
                  day. [1]-Anytime, [2]-Before Noon, [3]-Noon - 6PM, [4]-After
                  6PM
                  
  FLIGHT_TYPE     Enter a single character corresponding to the ticket type:
                  [1]-Business Select, [2]-Anytime, [3]-Wanna Get Away
                  
  MAX_PRICE       Enter the maximum ticket price
