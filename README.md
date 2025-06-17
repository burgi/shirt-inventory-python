# Shirt Inventory Task

A shirt retail company uses this application to manage its inventory.  
The application is web-based and allows users to create shirt items, retrieve all items in the inventory, and query a specific item by name.  
When retrieving all shirts, the application should return the items sorted by color and size.  
Currently, there are several bugs in the application, and some functionalities are missing.

## General
The application uses AWS Lambda functions to handle user requests. There are two handlers:
1. A get handler to retrieve all items or search for a specific item by name.
2. A create handler to add a new item to the inventory.

The application uses a file-based database to store items. The database is a JSON file that contains a mapping of IDs to shirt objects.

## Steps to Complete the Task
1. Start by reviewing the handlers to understand their functionality and implementation.
2. Learn how the database works and how to interact with it.
3. Identify errors or areas for improvement in the code. Consider code quality, handling of different user inputs, concurrent requests, and best practices.
4. Make the necessary changes to ensure the test `test_create_and_get` in `/tests/integration/test_apis.py` passes successfully.
5. Implement the sorting functionality in the get handler so that the test `test_create_and_get_with_sort` in `/tests/integration/test_apis.py` passes successfully.  
   The sort order is:
   - First by color, following the rainbow order: red, orange, yellow, green, blue, indigo, violet.
   - Then by size, in this order: S, M, L, XL, XXL for adults, and 2, 4, 6, 8, 10 for kids.
   - For the same color, adult shirts should come before kids' shirts.
6. You may search the internet for help, but do not use AI tools to write the code for you.
