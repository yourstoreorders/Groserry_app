### Api End Points

1.Get All Product

  __url:__ https://anvayagrocery.herokuapp.com/api/v1.0/product/

  __response:__
```json
{
  "products": [
    {
      "in_stock": 50, 
      "price_per_unit": "200.550", 
      "product_description": "apple kash", 
      "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/ba821f7fbe06c8c3.png", 
      "product_name": "Applee", 
      "product_type": 1, 
      "unit": 1, 
      "url": "/api/v1.0/product/1"
    }, 
    {
      "in_stock": 10, 
      "price_per_unit": "50.000", 
      "product_description": "Desi Milk", 
      "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/7ba610e6c6fee099.jpeg", 
      "product_name": "Milk", 
      "product_type": 2, 
      "unit": 2, 
      "url": "/api/v1.0/product/2"
    }, 
    {
      "in_stock": 50, 
      "price_per_unit": "12.000", 
      "product_description": "Assamese oranges", 
      "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/08f9fd943e82d332.png", 
      "product_name": "Oranges", 
      "product_type": 1, 
      "unit": 1, 
      "url": "/api/v1.0/product/3"
    }, 
    {
      "in_stock": 10, 
      "price_per_unit": "400.000", 
      "product_description": "Desi Panner", 
      "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/6ff1d003e5aabd6d.png", 
      "product_name": "Panner", 
      "product_type": 2, 
      "unit": 1, 
      "url": "/api/v1.0/product/4"
    }, 
    {
      "in_stock": 10, 
      "price_per_unit": "150.000", 
      "product_description": "Value Life White Peas (Whole)", 
      "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/649d807d9df14ec3.jpg", 
      "product_name": "White Peas(Mattar)", 
      "product_type": 3, 
      "unit": 3, 
      "url": "/api/v1.0/product/5"
    }
  ]
}

```

2.Get All Categories and products in them

  __url:__ https://anvayagrocery.herokuapp.com/api/v1.0/producttype/

  __response:__
```json
{
  "categories": [
    {
      "category_name": "Fruits", 
      "products_count": [
        {
          "in_stock": 50, 
          "price_per_unit": "200.550", 
          "product_description": "apple kash", 
          "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/ba821f7fbe06c8c3.png", 
          "product_name": "Applee", 
          "product_type": 1, 
          "unit": 1, 
          "url": "/api/v1.0/product/1"
        }, 
        {
          "in_stock": 50, 
          "price_per_unit": "12.000", 
          "product_description": "Assamese oranges", 
          "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/08f9fd943e82d332.png", 
          "product_name": "Oranges", 
          "product_type": 1, 
          "unit": 1, 
          "url": "/api/v1.0/product/3"
        }
      ], 
      "url": "/api/v1.0/producttype/1"
    }, 
    {
      "category_name": "Dairy", 
      "products_count": [
        {
          "in_stock": 10, 
          "price_per_unit": "50.000", 
          "product_description": "Desi Milk", 
          "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/7ba610e6c6fee099.jpeg", 
          "product_name": "Milk", 
          "product_type": 2, 
          "unit": 2, 
          "url": "/api/v1.0/product/2"
        }, 
        {
          "in_stock": 10, 
          "price_per_unit": "400.000", 
          "product_description": "Desi Panner", 
          "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/6ff1d003e5aabd6d.png", 
          "product_name": "Panner", 
          "product_type": 2, 
          "unit": 1, 
          "url": "/api/v1.0/product/4"
        }
      ], 
      "url": "/api/v1.0/producttype/2"
    }, 
    {
      "category_name": "Dal and Pulses", 
      "products_count": [
        {
          "in_stock": 10, 
          "price_per_unit": "150.000", 
          "product_description": "Value Life White Peas (Whole)", 
          "product_image": "https://anvayagrocery.herokuapp.com/static/product_images/649d807d9df14ec3.jpg", 
          "product_name": "White Peas(Mattar)", 
          "product_type": 3, 
          "unit": 3, 
          "url": "/api/v1.0/product/5"
        }
      ], 
      "url": "/api/v1.0/producttype/3"
    }
  ]
}

```

3.Place order 

  __url:__ https://anvayagrocery.herokuapp.com/api/v1.0/order/

  __request:__:
  ```json
{
    "order_details":{
        "details": "Delivery after 1pm",
        "delivery_address": "House no 123 B,Garmur,Jorhat ",
        "customer_details": {
            "customer_name":"Riya Das",
            "contact_phone":"9999999999",
            "contact_address":"House No 123 B,Garmur,Jorhat",
            "address_pin":"785007"
        }
    },
  
  "order_items": [
    {
      "quantity": 2,
      "product_id": 1,
      "price": 200.550
    },
    {
      "quantity": 2,
      "product_id": 2,
      "price": 100.00
    }
  ]
}

  ```
  __response:__
```json
{
  "delivery_address": "House no 123 B,Garmur,Jorhat ",
  "details": "Delivery after 1pm",
  "order_id": 1,
  "ordered_items": [
    {
      "placed_order_id": 1,
      "product_id": 1,
      "quantity": 2
    },
    {
      "placed_order_id": 1,
      "product_id": 2,
      "quantity": 2
    }
  ],
  "time_placed": "Fri, 07 Aug 2020 19:10:23 GMT"
}

```



