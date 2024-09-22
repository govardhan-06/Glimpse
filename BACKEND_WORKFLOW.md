### **Final Workflow for the Backend**

1. **User Authentication**:
   - **Tech Stack**: FastAPI/Flask, JWT (JSON Web Tokens), Redis (optional for session management)
   - **Workflow**: Users register and log in. Authentication tokens are generated and optionally stored in Redis for quick session validation.

2. **Swiping Logic**:
   - **Tech Stack**: FastAPI/Flask, PostgreSQL/MySQL
   - **Workflow**:
     - **Right Swipe**: Adds the item to the user's favorites.
     - **Left Swipe**: Logs the item as disliked.
     - Interactions are logged in the database to build user profiles for recommendations.

3. **Recommendation System**:
   - **Tech Stack**: PyTorch, FastAPI/Flask, Redis
   - **Workflow**:
     - **Generate Recommendations**: Based on user interactions and preferences using PyTorch models.
     - **Cache Recommendations**: Store the generated recommendations in Redis with TTL to speed up subsequent requests.

4. **Price Comparison and Cart System**:
   - **Tech Stack**: FastAPI/Flask, PostgreSQL/MySQL, Redis, Vendor APIs/Web Scraping
   - **Workflow**:
     - **Add to Cart**: When an item is added to the cart, fetch price comparisons from various vendors.
     - **Price Comparison**:
       - Check if price data is cached in Redis.
       - If not, fetch from vendor APIs or scrape websites, update Redis with the latest data, and serve it to the user.
     - **Cart Management**: Display items in the cart along with price comparisons. Allow users to select their preferred vendor.

5. **Price Data Aggregation and Updates**:
   - **Tech Stack**: FastAPI/Flask, Redis, Celery (for periodic tasks), Vendor APIs/Web Scraping
   - **Workflow**:
     - **Fetch Prices**: Regularly update price data using APIs or web scraping.
     - **Cache Prices**: Store the latest prices in Redis with a TTL.
     - **Schedule Updates**: Use Celery to periodically update prices in the background.

6. **Rate Limiting (API Requests to Vendors)**:
   - **Tech Stack**: Redis
   - **Workflow**:
     - Track the number of API requests made to each vendor.
     - Ensure API rate limits are not exceeded by checking and updating counts in Redis.

7. **Image Storage and Serving**:
   - **Tech Stack**: AWS S3/Cloudinary
   - **Workflow**:
     - Store and serve images for fashion items (dresses) from cloud storage services.

8. **Frontend Integration**:
   - **Tech Stack**: React Native/Flutter (for mobile), or a web-based frontend
   - **Workflow**:
     - Communicate with the backend API for user authentication, swiping actions, fetching recommendations, and displaying price comparisons.

### **Tech Stack Summary**

1. **Backend Framework**:
   - **FastAPI** or **Flask** for building the API.

2. **Recommendation Model**:
   - **PyTorch** for training and deploying recommendation models.

3. **Database**:
   - **PostgreSQL** or **MySQL** for storing user interactions, favorites, cart data, and other relational information.

4. **Caching**:
   - **Redis** for caching recommendations, price comparisons, and session management.

5. **Price Data Aggregation**:
   - **Vendor APIs** for fetching price data (e.g., Amazon, Walmart).
   - **Web Scraping** tools (e.g., BeautifulSoup, Scrapy) if APIs are not available.

6. **Background Task Scheduling**:
   - **Celery** for scheduling periodic tasks such as price updates.

7. **Image Storage**:
   - **AWS S3** or **Cloudinary** for storing and serving images of fashion items.

8. **Frontend**:
   - **React Native** or **Flutter** for building mobile apps.
   - Web frontend if applicable.

9. **Optional**:
   - **Redis** for session management if needed for fast access to session data.
   - **Rate Limiting** mechanism in Redis to handle API request limits.

### **Workflow Diagram**
Here’s a simplified workflow diagram for clarity:

```
User Interaction → Backend API (FastAPI/Flask)
    ↓                        ↓
  Swipes                 Recommendations
    ↓                        ↓
  Favorites                 Redis Cache (Recommendations)
    ↓                        ↓
   Cart                    Price Comparison (Vendor APIs/Scraping)
    ↓                        ↓
   Redis Cache (Prices)    Store Prices in Redis
    ↓                        ↓
   Price Comparison       Periodic Price Updates (Celery)
    ↓
  Display in Cart
```

This workflow and tech stack ensure that your app can handle user interactions efficiently, provide personalized recommendations, and offer real-time price comparisons while maintaining high performance and scalability.

### **Backend API and DBMS**

A detailed breakdown of the Backend API routes, database structure, and Redis caching structure for your recommendation-based eCommerce app with a price comparison feature.

---

Backend API Routes

1. Authentication

POST /register
Registers a new user.

Request Body:

{
  "username": "string",
  "email": "string",
  "password": "string"
}

Response:
Returns a success message and user ID.


POST /login
Authenticates user and returns a JWT token.

Request Body:

{
  "email": "string",
  "password": "string"
}

Response:
Returns a JWT token for authenticated requests.


POST /logout
Logs out the user and invalidates the session (optional Redis session handling).


2. Item Interaction (Swiping)

POST /item/swipe

Records user’s swipe (right or left).

Request Body:

{
  "user_id": "int",
  "item_id": "int",
  "swipe_direction": "right" or "left"
}

Response:
Acknowledgment of the action.

Use Case: Left for dislike (ignored), right for adding to favorites.



3. Recommendation System

GET /recommendations
Fetches a list of recommended items for the user.

Query Params:

user_id: The ID of the logged-in user.


Response:
Returns a list of recommended fashion items.

{
  "items": [
    {
      "item_id": "int",
      "name": "string",
      "image_url": "string",
      "price": "float",
      "brand": "string"
    },
    ...
  ]
}



4. Cart Management

POST /cart/add
Adds an item to the user’s cart.

Request Body:

{
  "user_id": "int",
  "item_id": "int"
}

Response:
Confirmation that the item has been added to the cart.


GET /cart
Fetches the user’s cart with price comparisons.

Query Params:

user_id: The ID of the user.


Response:

{
  "items": [
    {
      "item_id": "int",
      "name": "string",
      "image_url": "string",
      "price_comparison": [
        {"vendor": "string", "price": "float", "link": "string"}
      ]
    }
  ]
}



5. Price Comparison

GET /price-comparison/{item_id}
Fetches price comparison for a specific item.

Path Params:

item_id: The ID of the item for price comparison.


Response:
Returns a list of price data from various vendors:

{
  "price_comparison": [
    {"vendor": "Amazon", "price": 29.99, "link": "url"},
    {"vendor": "Walmart", "price": 27.99, "link": "url"},
    ...
  ]
}



6. Favorites

GET /favorites
Fetches the list of items the user has favorited.

Query Params:

user_id: The ID of the user.


Response:

{
  "favorites": [
    {"item_id": "int", "name": "string", "image_url": "string", "price": "float"},
    ...
  ]
}




---

Database Structure

The database structure will be based on relational tables, likely implemented in PostgreSQL or MySQL.

1. Users Table

Stores information about registered users.

Table: users | Column Name | Data Type | Constraints             | |-------------|-----------|-------------------------| | id          | INT       | PRIMARY KEY, AUTO_INCREMENT | | username    | VARCHAR   | UNIQUE, NOT NULL         | | email       | VARCHAR   | UNIQUE, NOT NULL         | | password    | VARCHAR   | NOT NULL                 | | created_at  | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP|


2. Items Table

Stores details of fashion items.

Table: items | Column Name   | Data Type  | Constraints             | |---------------|------------|-------------------------| | id            | INT        | PRIMARY KEY, AUTO_INCREMENT | | name          | VARCHAR    | NOT NULL                | | brand         | VARCHAR    | NOT NULL                | | price         | FLOAT      |                         | | image_url     | VARCHAR    |                         | | description   | TEXT       |                         |


3. User Interactions Table

Stores user interactions (swipes).

Table: user_interactions | Column Name    | Data Type  | Constraints                        | |----------------|------------|------------------------------------| | id             | INT        | PRIMARY KEY, AUTO_INCREMENT        | | user_id        | INT        | FOREIGN KEY (users.id)             | | item_id        | INT        | FOREIGN KEY (items.id)             | | interaction    | VARCHAR    | CHECK (interaction IN ('right', 'left')) | | created_at     | TIMESTAMP  | DEFAULT CURRENT_TIMESTAMP          |


4. Favorites Table

Stores items that users have favorited.

Table: favorites | Column Name    | Data Type  | Constraints                        | |----------------|------------|------------------------------------| | id             | INT        | PRIMARY KEY, AUTO_INCREMENT        | | user_id        | INT        | FOREIGN KEY (users.id)             | | item_id        | INT        | FOREIGN KEY (items.id)             | | added_at       | TIMESTAMP  | DEFAULT CURRENT_TIMESTAMP          |


5. Cart Table

Stores the items a user has added to the cart.

Table: cart | Column Name    | Data Type  | Constraints                        | |----------------|------------|------------------------------------| | id             | INT        | PRIMARY KEY, AUTO_INCREMENT        | | user_id        | INT        | FOREIGN KEY (users.id)             | | item_id        | INT        | FOREIGN KEY (items.id)             | | added_at       | TIMESTAMP  | DEFAULT CURRENT_TIMESTAMP          |


6. Price Comparisons Table

Stores price comparisons for items from multiple vendors.

Table: price_comparisons | Column Name    | Data Type  | Constraints                        | |----------------|------------|------------------------------------| | id             | INT        | PRIMARY KEY, AUTO_INCREMENT        | | item_id        | INT        | FOREIGN KEY (items.id)             | | vendor_name    | VARCHAR    | NOT NULL                          | | price          | FLOAT      | NOT NULL                          | | link           | VARCHAR    | URL to the vendor's page           | | updated_at     | TIMESTAMP  | DEFAULT CURRENT_TIMESTAMP          |



---

Redis Structure

Redis will be used to cache:

User Recommendations: Cached to quickly serve user recommendations.

Price Comparison Data: Cached to avoid frequent API calls or scraping.

Session Data: Optionally store user session tokens for fast authentication.


Redis Keys

1. User Recommendations

Key: user:{user_id}:recommendations

Value: List of recommended item IDs.

TTL: Set a TTL (e.g., 24 hours) to keep recommendations fresh.

Example:

{
  "recommendations": [101, 204, 305]
}



2. Price Comparison Data

Key: item:{item_id}:price_comparisons

Value: A list of price comparisons from various vendors.

TTL: Set a TTL (e.g., 1 hour) to frequently update prices.

Example:

{
  "price_comparison": [
    {"vendor": "Amazon", "price": 29.99, "link": "url"},
    {"vendor": "Walmart", "price": 27.99, "link": "url"}
  ]
}



3. Session Management (Optional)

Key: session:{session_id}

Value: User session information (JWT tokens, expiry times, etc.).

TTL: Set a TTL based on session expiration policies (e.g., 1 hour).





---

This API route structure, database design, and Redis caching plan will help ensure that the app performs well and scales efficiently, handling both user interactions and price comparisons dynamically.

