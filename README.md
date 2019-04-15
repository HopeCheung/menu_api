# menu_api
A menu api

1. create_database.py is used to initial the menu database. Each row of the database has three columns(id, name, item)

2. menu.py is the main program to implement the API

3. visit.py is the test program, and the result is shown in test_result.txt

4. To run the program:
   First, run create_database.py if menu.db doesn't exist
   Second, run the menu.py
   Third, you can try GET, PUT, POST and DELETE through postman.

5. GET /api/menusection     --------return all the items
   GET /api/menusection/id  --------return corresponding row with specific id
   
   POST /api/menusection    --------insert an item
   body:
   {
      id: id,
      name: name,
      item: item
   }
   POST /api/menusection/id  -------insert an item to specific row
    body:
   {
      name: name,
      item: item
   }
   
   DELETE /api/menusection/id ------- delete corresponding row with specific id
   
   PUT /api/menusection/id/temp ----- update the row satisfying the temp with new items
   eg: /api/menusection/3/name=New specials,item=milk
   body:
   {
	    "name": "New specials",
	    "item": "milk"
   }

6. Result: Test result is shown in the test_output.txt
  
   
   

