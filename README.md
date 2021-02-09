![workflow_branch](https://github.com/Agamiru/online_store/workflows/Run%20Django%20Tests/badge.svg?branch=development)

# online_store

An electronics online store backend

**Features include**

1. **Smart Categories**: Categories have uniform behavior and properties, hence implementing a compare feature, frequently bought together or accessories features is easy and intuitive.

   *For example, all products in Studio Speaker category, though having different product specs are still comparable with one another and have similar accessories.*

   

2. **Smart Product Search**: Search uses Trigram Similarity to get the best match even for misspelled queries. You can also search for products using its alias or "street name" 

   *For example, "canon to canon" will bring up results for "XLR to XLR" cables the same way a shopper on a shoe vendor site might type "all stars" and expect to see "Converse" products.*

 

3. **Custom HTML table to JSON converter**: A built in HTML table to JSON parser makes converting product specs (usually in HTML tables) to database friendly format - JSON a breeze. It's specially optimized for electronic specs tables.

   *Simply copy html table into 'specs' product field on the add product admin page and save. Conversion is done on save.*



4. **Telegram Client (In progress)** : Currently working on a Telegram client that will wield the full power of this backend without getting in its way.



**Development to come**

- Implement a cart, order and payment system.
- Implement cloud hosting for product images.
