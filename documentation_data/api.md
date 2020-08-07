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
        }
      ], 
      "url": "/api/v1.0/producttype/1"
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
        "details": "",
        "delivery_address": "garmur jorhat ",
        "customer_details": {
            "customer_name":"akhil rajbongshi",
            "contact_phone":"9999999999",
            "contact_address":"navratra pg, lmtc",
            "address_pin":"785007"
        }
    },
  
    "order_items": [
      {
        "quantity": 1,
        "product_id": 1,
        "price": 12
      },
      {
        "quantity": 10,
        "product_id": 1,
        "price": 123
      }
    ]
}  

  ```
  __response:__
```json
{
  "delivery_address": "garmur jorhat ",
  "details": "",
  "order_id": 2,
  "ordered_items": [
    {
      "placed_order_id": 2,
      "product_id": 1,
      "quantity": 1
    },
    {
      "placed_order_id": 2,
      "product_id": 1,
      "quantity": 10
    }
  ],
  "time_placed": "Fri, 07 Aug 2020 18:12:40 GMT"
}

```



