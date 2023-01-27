# Internet Shop Rest API
***

## Project setup

### Environment variables

First you need to create a file ".env"
In this file, you need to create 7 variables, namely:
+ **`DJANGO_SECRET_KEY`**

Contains django secret key
+ **`DB_NAME`**

Contains the name of the database
+ **`DB_USER`**

Contains the username for the database
+ **`DB_PASSWORD`**

Contains the database password
+ **`DB_HOST`**

Contains the hostname where the database is located (If you want to use docker compose the hostname should be "db")
+ **`REDIS_HOST`**

Contains the hostname where the redis is located (If you want to use docker compose the hostname should be "redis")

+ **`EMAIL_HOST_USER`**

Contains the name of the gmail account from which emails are sent

+ **`EMAIL_HOST_PASSWORD`**

Contains gmail password
### Setting up a virtual environment
At the root of the project, create a virtual environment using the command:
```shell
python3 -m venv venv
```
Activate it:
```shell
source venv/bin/activate
```

Then we install all the dependencies from the `requirements.txt` file into the virtual environment:

```shell
pip3 install -r requirements.txt
```

### Migrations
**Postgres must be enabled for migration**

If all the previous steps are completed successfully, all that remains for you is to apply the migrations, for this we use this command:

```shell
python3 manage.py migrate
```

### Launch of the project
After successful configuration, you need to write the following command to run the django app:

```shell
python3 manage.py runserver localhost:8000
```
Then, in another terminal window, you need to run celery worker to send emails with order reports:

```shell
celery -A internet_shop_rest worker -l info
```



### Docker
You can also run the project using docker. To do this, it is necessary that the environment variables containing the names of the postgres and redis hosts have the [`corresponding names`](#environment-variables).

To run a project with docker you need to build it using the command:
```shell
docker-compose build
```
And after a successful build, raise your container:
```shell
docker-compose up
```
All this is to run postgres first, then redis, celery worker to send emails, migrations will be made and the django application will start
***
## Endpoints

### Categories

`api/v1/shop/categories/`

Allowed methods: GET, HEAD, OPTIONS

1. GET
    + Description:
    
        Getting all existing categories
        
    + Authorization: Not required
    + Permissions: Allow any

`api/v1/shop/category/`

Allowed methods: POST, OPTIONS

1. POST
    + Description:
    
        Creating a new product category
        
    + Authorization: Required
    + Permissions: Admin Only
        
    + Data:
        + required:
        
            name: string

`api/v1/shop/category/{id}/`

Allowed methods: GET, PUT, PATCH, HEAD, OPTIONS

1. GET
    + Description:
    
        Getting information about a category by ID
        
    + Authorization: Not required
    + Permissions: Allow any  
    
2. PUT, PATCH:
    + Description:
    
        Full or partial change of information about the category
        
    + Authorization: Required
    + Permissions: Admin only 
    
    + Data:
    
        name: string

### Products

`api/v1/shop/products/`

Allowed methods: GET, HEAD, OPTIONS

1. GET
    + Description:
    
        Getting all existing products
        
    + Authorization: Not required
    + Permissions: Allow any
    
    + Params:
    
    category_id: integer | filters products from the same category

`api/v1/shop/product/`

Allowed methods: POST, OPTIONS

1. POST
    + Description:
    
        Creating a new product
        
    + Authorization: Required
    + Permissions: Admin only
        
    + Data:
        + required:
        
            name: string,
            
            vendor_code: string,
            
            price: float,
            
            stock: integer
        + not required:
        
            image: file,
            
            description: string,
            
            available: boolean,
            
            category: foreign key

`api/v1/shop/product/{id}/`

Allowed methods: GET, PUT, PATCH, DELETE, HEAD, OPTIONS

1. GET
    + Description:
    
        Getting information about a product by ID
        
    + Authorization: Not required
    + Permissions: Allow any

2. PUT, PATCH:
    + Description:
    
        Full or partial change of information about the product
        
    + Authorization: Required
    + Permissions: Admin only
    
3. DELETE:
    + Description:
    
        Removing a product by ID
        
    + Authorization: Required
    + Permissions: Admin only

### Cart

`api/v1/shop/checkout/cart/`

Allowed methods: GET, POST, DELETE, HEAD, OPTIONS

1. GET
    + Description:
    
        Returns all items added to the cart, the number of these items and their total cost
    
    + Authorization: Required
    + Permissions: Owner
2. POST
    + Description:
    
        Add a product to the cart and the quantity of this product
        
    + Authorization: Required
    + Permissions: Owner
    
    + Data:
        + required:
        
            quantity: integer,
            
            product: foreign key

3. DELETE
    + Description:
    
        Emptying the cart
        
    + Authorization: Required
    + Permissions: Owner

`api/v1/shop/checkout/cart/item-cart/{id}/`

Allowed methods: GET, PUT, PATCH, DELETE, HEAD, OPTIONS

1. GET
    + Desciption:
    
        Returns information about the product in the cart, its quantity and total cost by ID of the product in the cart
    
    + Authorization: Required
    + Permissions: Owner
    
2. PUT, PATCH:
    + Description:
    
        Changing the quantity of a product in the cart
        
    + Authorization: Required
    + Permissions: Owner
    
3. DELETE:
    + Description:
    
        Removing a specific product from the cart
    
    + Authorization: Required
    + Permissions: Owner

### Order creation

`api/v1/shop/order/customer-info/`

Allowed methods: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS

1. GET
    + Description:
    
        Returns customer information
    
    + Authorization: Required
    + Permissions: Owner
    
2. POST
    + Description:
    
        Adds customer information
        
    + Authorization: Required
    + Permissions: Owner
    
    + Data: 
        + required:
        
            name: string,
            
            email: string,
            
            phone: string,
            
            address: string,
            
            postal_code: string,
            
            city: string

3. PUT, PATCH:
    + Description:
    
        Full or partial change of information about the customer
        
    + Authorization: Required
    + Permissions: Owner

4. DELETE:
    + Description:
    
        Removing customer information
        
    + Authorization: Required
    + Permissions: Owner

`api/v1/shop/order/make-order/`

Allowed methods: POST, OPTIONS

1. POST
    + Description:
    
    Creation of an order based on the products in the cart and customer information, after the order is created, the cart will be cleared
    
    + Authorization: Required
    + Permissions: Owner
    
    + Data:
    
        No data required


## Other endpoints

Of course, in addition to the endpoints I created, there are endpoints of libraries that I use, such as [djoser](https://djoser.readthedocs.io/en/stable/) and [swagger](https://drf-yasg.readthedocs.io/en/stable/). You can get acquainted with them on their official websites with documentation.
