# Clopos Open API (v2)

???+ info
    This page is a Markdown version of the v2 API reference from the official Clopos developer docs ([developer.clopos.com](https://developer.clopos.com/docs)), which is the API this package uses. If anything differs, the original is authoritative.

!!! warning
    Clopos marks this API (`integrations.clopos.com/open-api`) as deprecated: it still works and existing integrations keep running, but it no longer gets new endpoints and will eventually be retired. New integrations should use the [Clopos Open API](https://developer.clopos.com/docs/api-reference/open-api/overview) on `open-api.clopos.com`. See [Migrating](https://developer.clopos.com/docs/migrating).

## Authentication

### Authenticate (v2)

Source: <https://developer.clopos.com/docs/api-reference/v2/authentication/auth>

`POST /v2/auth`

Exchange client credentials for a JWT access token

#### Purpose

Request a short-lived JWT that authorizes all other v2 API calls.

#### HTTP Request

```http
POST https://integrations.clopos.com/open-api/v2/auth
```

#### Where the credentials come from

The four values in the request body come from two different sources:

* **`integrator_id`** — issued by Clopos. Every v2 integration must send one. Request it by filling out this form: [https://forms.gle/Y9P1Wnv4QFAruxny8](https://forms.gle/Y9P1Wnv4QFAruxny8)
* **`client_id`, `client_secret`, `brand`** — come from the Clopos customer you are integrating with. They generate the Client ID and Client Secret themselves in their back office under **Add-ons → Open API**, then share both values and their brand identifier with you.

!!! note
    See [Authentication](https://developer.clopos.com/docs/authentication#where-the-client-id-and-client-secret-come-from) for the step-by-step back office instructions to pass on to your customer.

#### Request Example

```bash
curl --location 'https://integrations.clopos.com/open-api/v2/auth' \
  --header 'Content-Type: application/json' \
  --data '{
    "client_id": "your_client_id_here",
    "client_secret": "your_client_secret_here",
    "brand": "your_brand",
    "integrator_id": "your_integrator_id_here"
  }'
```

##### Request body

| Field           | Type   | Required | Description                                                       |
| --------------- | ------ | -------- | ----------------------------------------------------------------- |
| `client_id`     | string | Yes      | Generated in the customer's back office (**Add-ons → Open API**). |
| `client_secret` | string | Yes      | Secret paired with the Client ID, generated at the same time.     |
| `brand`         | string | Yes      | The customer's brand identifier.                                  |
| `integrator_id` | string | Yes      | New in v2. Identifies the integrator making the request.          |

`venue_id` is no longer part of the authentication payload.

#### Response

##### 200 OK — Token issued

```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6Im9hdXRoX1lOellQZE1QV21KeU0zOFVyblQzR3hoS25TelBNTHl2clB2UGgxQnRaeVFScTVzRWJsRkl5b3MwYVIyejMwWmYiLCJicmFuZCI6Im9tZWdhIiwic3RhZ2UiOiJiZXRhIiwidmVudWVfaWQiOjEsImludGVncmF0b3JfaWQiOiJ0ZXN0X2pLc1U5NnJxMzMzYjZQb3RUWmZrZ3ciLCJpYXQiOjE3Njc4NDg3MzIsImV4cCI6MTc2Nzg1MjMzMn0.7atyo3LEPXTyIjs2BjZIcUbWeFYtr375GeDwoVnWSRs",
  "token_type": "Bearer",
  "expires_in": 3600,
  "expires_at": 1767852332,
  "message": "Authentication successful"
}
```

##### How to use the token

* Include only the `x-token` header on all other v2 endpoints:
```bash
x-token: <your JWT here>
```
* Tokens expire after `expires_in` seconds; `expires_at` indicates the epoch timestamp when the token becomes invalid.

#### Integrator ID

Some integrations need to access Clopos Open API without an end-user logging in. For these cases, an **Integrator ID** is required.

!!! note
    Request an Integrator ID by filling out this form: [Request Integrator ID](https://forms.gle/Y9P1Wnv4QFAruxny8)

## Categories

### List Categories

Source: <https://developer.clopos.com/docs/api-reference/v2/categories/get-categories>

`GET /v2/categories`

Retrieve product categories along with their hierarchical structure

#### Purpose

Allows you to retrieve your category tree, including subcategories, in a single call.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/categories
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Query Parameters

- `` (integer): Page number for pagination (1-based).

- `` (integer): Number of categories to return (1-999).

- `` (integer): Filters records under a specific parent category.

- `` (string): Category type; `PRODUCT`, `INGREDIENT`, `ACCOUNTING`.

- `` (boolean): Include child categories in the response.

- `` (boolean): Return inactive categories.

#### Request Example

```bash
curl -X GET "https://integrations.clopos.com/open-api/v2/categories?page=1&limit=20&filters%5B0%5D%5B0%5D=type&filters%5B0%5D%5B1%5D=PRODUCT" \
  -H "x-token: oauth_example_token" \
```

```javascript
const params = new URLSearchParams({
    page: "1",
    limit: "20",
    "filters[0][0]": "type",
    "filters[0][1]": "PRODUCT",
    include_children: "true",
});

const response = await fetch(
    `https://integrations.clopos.com/open-api/v2/categories?${params}`,
    {
        headers: {
            "x-token": "oauth_example_token",
        },
    },
);

const categories = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/categories"
headers = {
    "x-token": "oauth_example_token",
}
params = {
    "page": 1,
    "limit": 20,
    "filters[0][0]": "type",
    "filters[0][1]": "PRODUCT",
    "include_children": True,
}

response = requests.get(url, headers=headers, params=params)
result = response.json()
```

#### Response

##### 200 OK — List of categories

```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Pizza",
            "status": 1,
            "hidden": false,
            "type": "PRODUCT",
            "position": null,
            "parent_id": null,
            "depth": 0,
            "color": "00bcd4",
            "children": [],
            "media": [],
            "created_at": "2026-01-28T18:23:53.000000Z",
            "updated_at": "2026-01-28T18:23:53.000000Z"
        },
        {
            "id": 2,
            "name": "Drinks",
            "status": 1,
            "hidden": false,
            "type": "PRODUCT",
            "position": null,
            "parent_id": null,
            "depth": 0,
            "color": "00bcd4",
            "children": [],
            "media": [
                {
                    "uuid": "1d76f22b-c209-4fac-be3a-cfde7b8f0d74",
                    "mime_type": "image/jpeg",
                    "size": 87281,
                    "urls": {
                        "original": "https://cdn.clopos.com/omega/1d76f22b-.../original.jpg",
                        "extra_large": "https://cdn.clopos.com/omega/1d76f22b-.../extra_large.jpg",
                        "thumb": "https://cdn.clopos.com/omega/1d76f22b-.../thumb.jpg"
                    },
                    "blur_hash": "LEIpFsE%t1}TxpENEgaK0iowRktQ",
                    "dimensions": {
                        "width": 612,
                        "height": 459
                    }
                }
            ],
            "created_at": "2026-02-13T16:31:36.000000Z",
            "updated_at": "2026-02-13T16:31:36.000000Z"
        }
    ],
    "total": 2
}
```

##### 400 Bad Request — Parameter error

```json
{
    "success": false,
    "error": "invalid_parameter",
    "message": "type must be one of PRODUCT, INGREDIENT, ACCOUNTING"
}
```

#### Field Reference

##### Category Object

| Field        | Type               | Description                                                                                                    |
| ------------ | ------------------ | -------------------------------------------------------------------------------------------------------------- |
| `id`         | integer            | Unique identifier.                                                                                             |
| `name`       | string             | Category name.                                                                                                 |
| `status`     | integer            | `1` = active, `0` = inactive.                                                                                  |
| `type`       | string             | `PRODUCT`, `INGREDIENT`, or `ACCOUNTING`.                                                                      |
| `position`   | integer (nullable) | Display order position.                                                                                        |
| `parent_id`  | integer (nullable) | Parent category ID, `null` for root categories.                                                                |
| `_lft`       | integer            | Left boundary in the nested-set tree. Useful for ordering and subtree queries.                                 |
| `_rgt`       | integer            | Right boundary in the nested-set tree. A category's descendants have `_lft` and `_rgt` values between its own. |
| `depth`      | integer            | Hierarchy level (`0` = root).                                                                                  |
| `color`      | string             | HEX color code (without `#` prefix).                                                                           |
| `hidden`     | boolean            | Whether the category is hidden from menus.                                                                     |
| `children`   | array              | Subcategories (same structure, nested recursively).                                                            |
| `media`      | array              | Image attachments. See [Media object](https://developer.clopos.com/docs/common-objects#media).                                             |
| `created_at` | string             | Creation timestamp (ISO 8601).                                                                                 |
| `updated_at` | string             | Last update timestamp (ISO 8601).                                                                              |

#### Notes

* With the `type` parameter, you can call different category collections (menu, ingredient, accounting) from a single endpoint.
* By sending `include_children=false`, you can retrieve only top-level categories; sub-branches are retrieved with separate calls.
* The `depth` field indicates the hierarchy level: `0` for root categories, `1` for first-level children, and so on.
* To see inactive categories, send `include_inactive=true`; otherwise, they are hidden by default.
* In a production environment, adjust pagination values (`page`, `limit`) according to the brand's inventory size.

### Get Category by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/categories/get-category-by-id>

`GET /v2/categories/{id}`

Retrieve a specific menu category with its hierarchical details

#### Purpose

Returns a single category, regardless of whether it is a root or subcategory, and optionally its child nodes.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/categories/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Request Example

```bash
curl -X GET "https://integrations.clopos.com/open-api/v2/categories/1?include_children=true" \
  -H "x-token: oauth_example_token" \
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/categories/1?include_children=true', {
  headers: {
    'x-token': 'oauth_example_token',
  }
});

const category = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/categories/1"
headers = {
    "x-token": "oauth_example_token",
}
params = {
    "include_children": True
}

response = requests.get(url, headers=headers, params=params)
category = response.json()
```

#### Response

##### 200 OK — Category found

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Pizza",
    "status": 1,
    "hidden": false,
    "type": "PRODUCT",
    "position": null,
    "parent_id": null,
    "depth": 0,
    "color": "00bcd4",
    "children": [],
    "media": [
      {
        "uuid": "1d76f22b-c209-4fac-be3a-cfde7b8f0d74",
        "mime_type": "image/jpeg",
        "size": 87281,
        "urls": {
          "original": "https://cdn.clopos.com/omega/1d76f22b-.../original.jpg",
          "extra_large": "https://cdn.clopos.com/omega/1d76f22b-.../extra_large.jpg",
          "thumb": "https://cdn.clopos.com/omega/1d76f22b-.../thumb.jpg"
        },
        "blur_hash": "LEIpFsE%t1}TxpENEgaK0iowRktQ",
        "dimensions": {
          "width": 612,
          "height": 459
        }
      }
    ],
    "created_at": "2026-01-28T18:23:53.000000Z",
    "updated_at": "2026-01-28T18:23:53.000000Z"
  }
}
```

##### 404 Not Found — Category does not exist

```json
{
  "success": false,
  "error": "resource_not_found",
  "message": "Category not found"
}
```

#### Field Reference

##### Category Object

| Field        | Type               | Description                                                                                                    |
| ------------ | ------------------ | -------------------------------------------------------------------------------------------------------------- |
| `id`         | integer            | Unique identifier.                                                                                             |
| `name`       | string             | Category name.                                                                                                 |
| `status`     | integer            | `1` = active, `0` = inactive.                                                                                  |
| `type`       | string             | `PRODUCT`, `INGREDIENT`, or `ACCOUNTING`.                                                                      |
| `position`   | integer (nullable) | Display order position.                                                                                        |
| `parent_id`  | integer (nullable) | Parent category ID, `null` for root categories.                                                                |
| `_lft`       | integer            | Left boundary in the nested-set tree. Useful for ordering and subtree queries.                                 |
| `_rgt`       | integer            | Right boundary in the nested-set tree. A category's descendants have `_lft` and `_rgt` values between its own. |
| `depth`      | integer            | Hierarchy level (`0` = root).                                                                                  |
| `color`      | string             | HEX color code (without `#` prefix).                                                                           |
| `hidden`     | boolean            | Whether the category is hidden from menus.                                                                     |
| `children`   | array              | Subcategories (same structure, nested recursively).                                                            |
| `media`      | array              | Image attachments. See [Media object](https://developer.clopos.com/docs/common-objects#media).                                             |
| `created_at` | string             | Creation timestamp (ISO 8601).                                                                                 |
| `updated_at` | string             | Last update timestamp (ISO 8601).                                                                              |

#### Notes

* The `include_children=false` parameter returns only a single category record; recommended for performance in large trees.
* The returned `children` array recursively uses the same schema; be careful when processing the tree structure repeatedly on the client side.
* Based on the `type` field in the response, you can read menu, ingredient, or accounting categories from the same endpoint.
* If the category is not found, it returns `404`; add fallback or remapping logic on the client side.

## Customers

### Create Customer

Source: <https://developer.clopos.com/docs/api-reference/v2/customers/create-customer>

`POST /v2/customers`

Create a new customer with contact information and group assignment

#### Purpose

Create a new customer in the Clopos system. This endpoint allows you to register customers with their contact information, assign them to customer groups, and set up their profile details.

#### HTTP Request

```http
POST https://integrations.clopos.com/open-api/v2/customers
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

!!! note
    The fields `code`, `phone`, and `cid` are unique. If you attempt to create a customer with duplicate values for any of these fields, the API will return an error.

#### Request Body

- `` (string): Customer's full name. This field is required.

- `` (string): Customer's email address.

- `` (string): Customer's primary phone number. Must be unique across all customers.

- `` (string): Customer code/identifier. Must be unique across all customers.

- `` (string): Customer UUID identifier. Must be unique across all customers. If not provided, the system will generate one automatically.

- `` (string): Additional notes or description about the customer.

- `` (integer): ID of the customer group to assign this customer to.

- `` (integer): Customer's gender. Use `1` for male, `2` for female, or `null` for unspecified.

- `` (string): Customer's date of birth in `YYYY-MM-DD` format.

#### Request Examples

```bash
curl --location 'https://integrations.clopos.com/open-api/v2/customers' \
  --header 'accept: application/json, text/plain, */*' \
  --header 'x-token: oauth_example_token' \
  --header 'content-type: application/json' \
  --data-raw '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "code": "CUST001",
    "cid": "0f9654bc-9520-43d7-8109-317d9820f54c",
    "phone": "+15551234567",
    "description": "Test Customer",
    "group_id": 1,
    "gender": 1,
    "date_of_birth": "1990-05-15"
}'
```

```javascript
const customerData = {
  name: "John Doe",
  email: "john.doe@example.com",
  code: "CUST001",
  cid: "0f9654bc-9520-43d7-8109-317d9820f54c",
  phone: "+15551234567",
  description: "Test Customer",
  group_id: 1,
  gender: 1,
  date_of_birth: "1990-05-15"
};

const response = await fetch('https://integrations.clopos.com/open-api/v2/customers', {
  method: 'POST',
  headers: {
    'x-token': 'oauth_example_token',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(customerData)
});

const customer = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/customers"
headers = {
    "x-token": "oauth_example_token",
    "Content-Type": "application/json"
}

customer_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "code": "CUST001",
    "cid": "0f9654bc-9520-43d7-8109-317d9820f54c",
    "phone": "+15551234567",
    "description": "Test Customer",
    "group_id": 1,
    "gender": 1,
    "date_of_birth": "1990-05-15"
}

response = requests.post(url, headers=headers, json=customer_data)
customer = response.json()
```

#### Response

##### 200 OK — Customer created successfully

```json
{
  "success": true,
  "data": {
    "id": 14,
    "venue_id": 1,
    "cid": "0f9654bc-9520-43d7-8109-317d9820f54c",
    "group_id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+15551234567",
    "phones": [],
    "address": null,
    "address_data": [],
    "description": "Test Customer",
    "discount": 0,
    "spent": 0,
    "total_discount": 0,
    "total_bonus": 0,
    "receipt_count": 0,
    "gender": 1,
    "date_of_birth": "1990-05-15",
    "code": "CUST001",
    "source": null,
    "reference_id": null,
    "status": true,
    "can_use_loyalty_system": false,
    "is_verified": false,
    "created_at": "2025-11-14T08:31:17.000000Z",
    "updated_at": "2025-11-14T08:31:17.000000Z"
  }
}
```

##### 400 Bad Request — Validation error

```json
{
    "success": false,
    "message": "Validation failed",
    "error": "The name field is required."
}
```

##### 409 Conflict — Duplicate unique field

```json
{
    "success": false,
    "message": "Customer with this phone number already exists",
    "error": "duplicate_phone"
}
```

#### Field Reference

##### Required Fields

| Field  | Type   | Description           |
| ------ | ------ | --------------------- |
| `name` | string | Customer's full name. |

##### Optional Fields

| Field           | Type    | Description                                                    |
| --------------- | ------- | -------------------------------------------------------------- |
| `email`         | string  | Customer's email address.                                      |
| `phone`         | string  | Primary phone number. Must be unique.                          |
| `code`          | string  | Customer code/identifier. Must be unique.                      |
| `cid`           | string  | Customer UUID. Must be unique. Auto-generated if not provided. |
| `description`   | string  | Additional notes about the customer.                           |
| `group_id`      | integer | ID of the customer group.                                      |
| `gender`        | integer | Gender: `1` = male, `2` = female, `null` = unspecified.        |
| `date_of_birth` | string  | Date of birth in `YYYY-MM-DD` format.                          |

##### Response Fields

| Field                    | Type    | Description                                      |
| ------------------------ | ------- | ------------------------------------------------ |
| `id`                     | integer | Unique customer identifier (auto-assigned).      |
| `venue_id`               | integer | Venue the customer was created in.               |
| `cid`                    | string  | UUID identifier for the customer.                |
| `status`                 | boolean | Account status (defaults to `true`).             |
| `can_use_loyalty_system` | boolean | Loyalty enrollment status (defaults to `false`). |
| `is_verified`            | boolean | Verification status (defaults to `false`).       |
| `created_at`             | string  | Creation timestamp (ISO 8601).                   |
| `updated_at`             | string  | Last update timestamp (ISO 8601).                |

#### Notes

* The `name` field is required and cannot be empty.
* The fields `code`, `phone`, and `cid` must be unique. Attempting to create a customer with duplicate values will result in a `409 Conflict` error.
* If `cid` is not provided, the system will automatically generate a UUID for the customer.
* The response includes the customer's group information if `group_id` was provided.
* The `can_use_loyalty_system` and `is_verified` fields are set to `false` by default for new customers.

### List All Customers

Source: <https://developer.clopos.com/docs/api-reference/v2/customers/get-all-customers>

`GET /v2/customers`

Retrieve all customers with pagination, filtering, and relationship inclusion.

This endpoint retrieves a list of all customers with support for pagination, filtering, and including related data.

!!! note
    There is no `search` parameter on this endpoint. To find customers by name
    or phone, use the `filters` parameter described below.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/customers
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Query Parameters

- `` (integer): Page number for pagination (1-based).

- `` (integer): Number of customers to return per page (1-999).

- `` (string): Include related data in the response. Supported values: `group`. You can include multiple `with` parameters.

- `` (array): 

    Filter customers by specific fields. Filters use array notation:
    `filters[0][0]=field_name&filters[0][1]=value`. Multiple filters can be
    combined using different indices (e.g., `filters[0]`, `filters[1]`).
    **Supported filter fields:** - `name`: Filter by customer name (partial
    match) - `phones`: Filter by phone number (searches in all phone numbers) -
    `group_id`: Filter by customer group ID **Filter Examples:** - Filter by
    name: `filters[0][0]=name&filters[0][1]=John` - Filter by phone:
    `filters[0][0]=phones&filters[0][1]=15551234567` - Multiple filters:
    `filters[0][0]=name&filters[0][1]=John&filters[1][0]=phones&filters[1][1]=15551234567`

#### Request Examples

```bash
curl --location "https://integrations.clopos.com/open-api/v2/customers?page=1&limit=50" \
  -H "x-token: oauth_example_token" \
```

```bash
curl --location --globoff 'https://integrations.clopos.com/open-api/v2/customers?page=1&limit=50&with[0]=group&filters[0][0]=name&filters[0][1]=John&filters[1][0]=phones&filters[1][1]=15551234567' \
  -H "x-token: oauth_example_token" \
```

```javascript
// Basic request
const params = new URLSearchParams({
    page: "1",
    limit: "50",
});

// With filters and relations
const paramsWithFilters = new URLSearchParams({
    page: "1",
    limit: "50",
    "with[0]": "group",
    "filters[0][0]": "name",
    "filters[0][1]": "John",
    "filters[1][0]": "phones",
    "filters[1][1]": "15551234567",
});

const response = await fetch(
    `https://integrations.clopos.com/open-api/v2/customers?${paramsWithFilters}`,
    {
        headers: {
            "x-token": "oauth_example_token",
        },
    },
);

const customers = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/customers"
headers = {
    "x-token": "oauth_example_token",
}

# Basic request
params = {
    "page": 1,
    "limit": 50
}

# With filters and relations
params_with_filters = {
    "page": 1,
    "limit": 50,
    "with[0]": "group",
    "filters[0][0]": "name",
    "filters[0][1]": "John",
    "filters[1][0]": "phones",
    "filters[1][1]": "15551234567"
}

response = requests.get(url, headers=headers, params=params_with_filters)
customers = response.json()
```

#### Response Example

```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "venue_id": 1,
            "cid": "1266eb42-9bdb-4e93-9fe0-3603c110f128",
            "group_id": 5,
            "name": "Rahid Akhundzada",
            "discount": 0,
            "email": null,
            "phones": [],
            "phone": "+994505355757",
            "address": null,
            "description": null,
            "address_data": [],
            "spent": 1162.8,
            "total_discount": 1.7,
            "total_bonus": 0,
            "receipt_count": 9,
            "gender": 1,
            "date_of_birth": null,
            "code": null,
            "source": null,
            "reference_id": null,
            "status": true,
            "can_use_loyalty_system": false,
            "is_verified": false,
            "created_at": "2026-01-31T16:23:27.000000Z",
            "updated_at": "2026-03-12T16:37:15.000000Z"
        },
        {
            "id": 2,
            "venue_id": 1,
            "cid": "24d7865f-f1bc-4948-be6a-e497d20bad0c",
            "group_id": 1,
            "name": "Reyal",
            "discount": 0,
            "email": null,
            "phones": [],
            "phone": null,
            "address": null,
            "description": null,
            "address_data": [],
            "spent": 714,
            "total_discount": 0,
            "total_bonus": 0,
            "receipt_count": 10,
            "gender": null,
            "date_of_birth": null,
            "code": null,
            "source": null,
            "reference_id": null,
            "status": true,
            "can_use_loyalty_system": false,
            "is_verified": false,
            "created_at": "2026-02-02T19:45:10.000000Z",
            "updated_at": "2026-02-02T23:37:33.000000Z"
        }
    ],
    "total": 7
}
```

#### Field Reference

##### Customer Object

| Field                    | Type               | Description                                                          |
| ------------------------ | ------------------ | -------------------------------------------------------------------- |
| `id`                     | integer            | Unique customer identifier.                                          |
| `cid`                    | string             | UUID identifier for the customer.                                    |
| `venue_id`               | integer            | The venue this customer belongs to.                                  |
| `group_id`               | integer            | The ID of the customer group they belong to.                         |
| `name`                   | string             | Customer's full name.                                                |
| `email`                  | string (nullable)  | Customer's email address.                                            |
| `phone`                  | string (nullable)  | Primary phone number.                                                |
| `phones`                 | array              | Additional phone numbers.                                            |
| `address`                | string (nullable)  | Customer's address.                                                  |
| `address_data`           | array              | Structured address entries with type, source, and formatted address. |
| `description`            | string (nullable)  | Additional notes about the customer.                                 |
| `discount`               | number             | Customer-level discount value.                                       |
| `spent`                  | number             | Total amount spent by the customer.                                  |
| `total_discount`         | number             | Total discount amount received across all receipts.                  |
| `total_bonus`            | number             | Total bonus amount used.                                             |
| `receipt_count`          | integer            | Total number of receipts for the customer.                           |
| `gender`                 | integer (nullable) | Gender: `1` = male, `2` = female, `null` = unspecified.              |
| `date_of_birth`          | string (nullable)  | Date of birth in `YYYY-MM-DD` format.                                |
| `code`                   | string (nullable)  | Customer code/identifier.                                            |
| `source`                 | string (nullable)  | Where the customer was created from (e.g., `LOYALTY`).               |
| `reference_id`           | string (nullable)  | External reference ID for third-party integrations.                  |
| `status`                 | boolean            | Whether the customer account is active.                              |
| `can_use_loyalty_system` | boolean            | Whether the customer is enrolled in the loyalty system.              |
| `is_verified`            | boolean            | Whether the customer's identity has been verified.                   |
| `created_at`             | string             | Timestamp when the customer was created (ISO 8601).                  |
| `updated_at`             | string             | Timestamp when the customer was last updated (ISO 8601).             |

#### Notes

* **Filterable fields:** `name` (partial match), `phones` (searches across all phone numbers), `group_id` (exact match). Note: use `phones` (plural) — the singular `phone` field is not filterable.
* **Sortable fields:** `id`, `cid`, `group_id`, `name`, `email`, `address`, `created_at`, `updated_at`.
* The `search` query parameter is listed in some older references but is **not implemented** — use `filters` instead.

### Get Customer by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/customers/get-customer>

`GET /v2/customers/{id}`

Retrieve a specific customer by their unique identifier.

This endpoint retrieves a specific customer by their unique ID.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/customers/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

- `` (integer): The unique identifier of the customer to retrieve.

#### Request Example

```bash
curl --location 'https://integrations.clopos.com/open-api/v2/customers/1' \
  -H "x-token: oauth_example_token" \
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/customers/1', {
  headers: {
    'x-token': 'oauth_example_token',
  }
});

const customer = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/customers/1"
headers = {
    "x-token": "oauth_example_token",
}

response = requests.get(url, headers=headers)
customer = response.json()
```

#### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "venue_id": 1,
    "cid": "1266eb42-9bdb-4e93-9fe0-3603c110f128",
    "group_id": 5,
    "name": "Rahid Akhundzada",
    "discount": 0,
    "email": null,
    "phones": [],
    "phone": "+994505355757",
    "address": null,
    "description": null,
    "address_data": [],
    "spent": 1162.8,
    "total_discount": 1.7,
    "total_bonus": 0,
    "receipt_count": 9,
    "gender": 1,
    "date_of_birth": null,
    "code": null,
    "source": null,
    "reference_id": null,
    "status": true,
    "can_use_loyalty_system": false,
    "is_verified": false,
    "created_at": "2026-01-31T16:23:27.000000Z",
    "updated_at": "2026-03-12T16:37:15.000000Z"
  }
}
```

#### Field Reference

##### Customer Object

| Field                    | Type               | Description                                                          |
| ------------------------ | ------------------ | -------------------------------------------------------------------- |
| `id`                     | integer            | Unique customer identifier.                                          |
| `cid`                    | string             | UUID identifier for the customer.                                    |
| `venue_id`               | integer            | The venue this customer belongs to.                                  |
| `group_id`               | integer            | The ID of the customer group they belong to.                         |
| `name`                   | string             | Customer's full name.                                                |
| `email`                  | string (nullable)  | Customer's email address.                                            |
| `phone`                  | string (nullable)  | Primary phone number.                                                |
| `phones`                 | array              | Additional phone numbers.                                            |
| `address`                | string (nullable)  | Customer's address.                                                  |
| `address_data`           | array              | Structured address entries with type, source, and formatted address. |
| `description`            | string (nullable)  | Additional notes about the customer.                                 |
| `discount`               | number             | Customer-level discount value.                                       |
| `spent`                  | number             | Total amount spent by the customer.                                  |
| `total_discount`         | number             | Total discount amount received across all receipts.                  |
| `total_bonus`            | number             | Total bonus amount used.                                             |
| `receipt_count`          | integer            | Total number of receipts for the customer.                           |
| `gender`                 | integer (nullable) | Gender: `1` = male, `2` = female, `null` = unspecified.              |
| `date_of_birth`          | string (nullable)  | Date of birth in `YYYY-MM-DD` format.                                |
| `code`                   | string (nullable)  | Customer code/identifier.                                            |
| `source`                 | string (nullable)  | Where the customer was created from (e.g., `LOYALTY`).               |
| `reference_id`           | string (nullable)  | External reference ID for third-party integrations.                  |
| `status`                 | boolean            | Whether the customer account is active.                              |
| `can_use_loyalty_system` | boolean            | Whether the customer is enrolled in the loyalty system.              |
| `is_verified`            | boolean            | Whether the customer's identity has been verified.                   |
| `created_at`             | string             | Timestamp when the customer was created (ISO 8601).                  |
| `updated_at`             | string             | Timestamp when the customer was last updated (ISO 8601).             |

### List Customer Groups

Source: <https://developer.clopos.com/docs/api-reference/v2/customers/get-customer-groups>

`GET /v2/customer-groups`

Retrieve a list of all customer groups with pagination support.

This endpoint retrieves a list of all customer groups.

```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "My Customers",
            "discount_type": null,
            "discount_value": 0,
            "system_type": "my_customers",
            "created_at": "2025-08-16T15:21:15.000000Z",
            "updated_at": "2025-08-16T15:21:15.000000Z",
            "deleted_at": null
        }
    ],
    "total": 1,
    "time": 71,
    "timestamp": "2025-10-24 05:38:15",
    "sorts": [
        "id",
        "name",
        "discount_type",
        "discount_value",
        "total_amount",
        "created_at",
        "updated_at",
        "deleted_at"
    ],
    "unix": 1761284295
}
```

##### Customer Group Object

| Field            | Type           | Description                                           |
| ---------------- | -------------- | ----------------------------------------------------- |
| `id`             | integer        | The unique identifier for the customer group.         |
| `name`           | string         | The name of the customer group.                       |
| `discount_type`  | string \| null | The type of discount associated with the group.       |
| `discount_value` | number         | The value of the discount.                            |
| `system_type`    | string \| null | The system type of the group (e.g., 'my\_customers'). |
| `created_at`     | string         | The timestamp when the group was created.             |

## Finance

### Get Balance by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-balance-by-id>

`GET /v2/finance/balances/{id}`

Retrieve a single account.

Fetch one account by its identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/balances/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `finance-balances:read` |
| User ability     | `FINANCE_BALANCE_VIEW`  |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/balances/1" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/balances/1', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/balances/1",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Balance Date States

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-balance-date-states>

`GET /v2/finance/balances/date-states`

Per-date balance states.

Balance state per date across the requested range.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/balances/date-states
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `finance-balances:read` |
| User ability     | `FINANCE_BALANCE_VIEW`  |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/balances/date-states" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/balances/date-states', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/balances/date-states",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Balance Transactions

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-balance-transactions>

`GET /v2/finance/balances/transactions`

Transactions grouped by account.

Transactions viewed per account.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/balances/transactions
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `finance-balances:read` |
| User ability     | `FINANCE_BALANCE_VIEW`  |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/balances/transactions" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/balances/transactions', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/balances/transactions",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Proxies to client-api `finance/balance/transaction`.

### List Balances

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-balances>

`GET /v2/finance/balances`

Cash and bank accounts.

Accounts money is held in, each with its current `amount`.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/balances
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `finance-balances:read` |
| User ability     | `FINANCE_BALANCE_VIEW`  |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/balances" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/balances', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/balances",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Balance List

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-balances-list>

`GET /v2/finance/balances/list`

Condensed account list.

A lighter account list intended for selectors.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/balances/list
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `finance-balances:read` |
| User ability     | `FINANCE_BALANCE_VIEW`  |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/balances/list" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/balances/list', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/balances/list",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Get Cash Shift by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-cash-shift-by-id>

`GET /v2/finance/cash-shifts/{id}`

Retrieve a single shift.

Fetch one cash shift. **The identifier is a UUID, not an integer.**

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/cash-shifts/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                      |
| ---------------- | -------------------------- |
| Integrator scope | `finance-cash-shifts:read` |
| User ability     | `CASH_SHIFT_VIEW`          |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/cash-shifts/9c1e7a30-4b2f-4d18-9f6a-71c0d8e4b5a2" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/cash-shifts/9c1e7a30-4b2f-4d18-9f6a-71c0d8e4b5a2', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/cash-shifts/9c1e7a30-4b2f-4d18-9f6a-71c0d8e4b5a2",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Cash shifts are the one resource in v2 keyed by a UUID; passing an integer returns `400`.

### Cash Shift Report

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-cash-shift-report>

`GET /v2/finance/cash-shifts/{id}/report`

Totals for one shift.

Sales, refunds and cash in/out totals for a single shift. The identifier is a UUID.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/cash-shifts/{id}/report
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                      |
| ---------------- | -------------------------- |
| Integrator scope | `finance-cash-shifts:read` |
| User ability     | `CASH_SHIFT_VIEW`          |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/cash-shifts/9c1e7a30-4b2f-4d18-9f6a-71c0d8e4b5a2/report" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/cash-shifts/9c1e7a30-4b2f-4d18-9f6a-71c0d8e4b5a2/report', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/cash-shifts/9c1e7a30-4b2f-4d18-9f6a-71c0d8e4b5a2/report",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### List Cash Shifts

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-cash-shifts>

`GET /v2/finance/cash-shifts`

Till sessions.

Till sessions opened and closed on terminals.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/cash-shifts
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                      |
| ---------------- | -------------------------- |
| Integrator scope | `finance-cash-shifts:read` |
| User ability     | `CASH_SHIFT_VIEW`          |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/cash-shifts" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/cash-shifts', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/cash-shifts",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Requires the Cash Shift module; without it the endpoint answers `403`.

### Customer Balances

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-customer-balances>

`GET /v2/finance/balances/customer`

Balances held against customers.

Outstanding balances per customer.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/balances/customer
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `finance-balances:read` |
| User ability     | `FINANCE_BALANCE_VIEW`  |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/balances/customer" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/balances/customer', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/balances/customer",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### List Finance Categories

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-finance-categories>

`GET /v2/finance/categories`

Categories money movements are classified under.

The categories transactions are filed under.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/categories
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                     |
| ---------------- | ------------------------- |
| Integrator scope | `finance-categories:read` |
| User ability     | `FINANCE_CATEGORY_VIEW`   |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/categories" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/categories', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/categories",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Get Finance Category by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-finance-category-by-id>

`GET /v2/finance/categories/{id}`

Retrieve a single category.

Fetch one finance category by its identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/categories/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                     |
| ---------------- | ------------------------- |
| Integrator scope | `finance-categories:read` |
| User ability     | `FINANCE_CATEGORY_VIEW`   |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/categories/1" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/categories/1', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/categories/1",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Get Tax by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-tax-by-id>

`GET /v2/finance/taxes/{id}`

Retrieve a single tax rate.

Fetch one tax rate by its identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/taxes/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                |
| ---------------- | -------------------- |
| Integrator scope | `finance-taxes:read` |
| User ability     | `TAX_VIEW`           |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/taxes/1" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/taxes/1', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/taxes/1",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Tax Report

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-tax-report>

`GET /v2/finance/taxes/report`

Tax report over a period.

Tax report across the requested period.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/taxes/report
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                |
| ---------------- | -------------------- |
| Integrator scope | `finance-taxes:read` |
| User ability     | `TAX_REPORT_SHOW`    |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/taxes/report" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/taxes/report', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/taxes/report",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Proxies to client-api `finance/tax/report`. Requires `TAX_REPORT_SHOW`, not `TAX_VIEW`.

### Tax Totals

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-tax-total>

`GET /v2/finance/taxes/total`

Aggregate tax amounts.

Aggregate tax amounts for the current filters.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/taxes/total
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                |
| ---------------- | -------------------- |
| Integrator scope | `finance-taxes:read` |
| User ability     | `TAX_REPORT_SHOW`    |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/taxes/total" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/taxes/total', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/taxes/total",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Proxies to client-api `finance/tax/total`. Requires `TAX_REPORT_SHOW`.

### Tax Types

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-tax-types>

`GET /v2/finance/taxes/types`

The tax type vocabulary.

Returns the tax type list, so you do not have to hard-code it.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/taxes/types
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                |
| ---------------- | -------------------- |
| Integrator scope | `finance-taxes:read` |
| User ability     | `TAX_VIEW`           |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/taxes/types" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/taxes/types', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/taxes/types",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Proxies to client-api `finance/tax/types`.

### List Taxes

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-taxes>

`GET /v2/finance/taxes`

Configured tax rates.

Tax rates configured for the brand.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/taxes
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                |
| ---------------- | -------------------- |
| Integrator scope | `finance-taxes:read` |
| User ability     | `TAX_VIEW`           |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/taxes" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/taxes', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/taxes",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Get Transaction by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-transaction-by-id>

`GET /v2/finance/transactions/{id}`

Retrieve a single transaction.

Fetch one transaction by its identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/transactions/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                       |
| ---------------- | --------------------------- |
| Integrator scope | `finance-transactions:read` |
| User ability     | `FINANCE_TRANSACTION_VIEW`  |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/transactions/1" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/transactions/1', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/transactions/1",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### List Transactions

Source: <https://developer.clopos.com/docs/api-reference/v2/finance/get-transactions>

`GET /v2/finance/transactions`

Money movements.

Money in and out. `before_amount`/`after_amount` bracket each movement against `balance_id`.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/finance/transactions
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                       |
| ---------------- | --------------------------- |
| Integrator scope | `finance-transactions:read` |
| User ability     | `FINANCE_TRANSACTION_VIEW`  |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/finance/transactions" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/finance/transactions', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/finance/transactions",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Transactions link back to whatever caused them: `receipt_id`, `operation_id`, `customer_id` or `supplier_id`.

## Inventory

### Get Operation by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-operation-by-id>

`GET /v2/operations/{id}`

Retrieve a single document.

Fetch one inventory document by its identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/operations/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value             |
| ---------------- | ----------------- |
| Integrator scope | `operations:read` |
| User ability     | `STOCK_VIEW`      |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/operations/1" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/operations/1', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/operations/1",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Get Operation Items

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-operation-items>

`GET /v2/operations/{id}/items`

Line items of one document.

The line items belonging to a single operation.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/operations/{id}/items
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value             |
| ---------------- | ----------------- |
| Integrator scope | `operations:read` |
| User ability     | `STOCK_VIEW`      |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/operations/1/items" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/operations/1/items', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/operations/1/items",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Operation Statuses

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-operation-statuses>

`GET /v2/operations/statuses`

The status vocabulary.

Returns the status list with localised display names, so you do not have to hard-code them.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/operations/statuses
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value             |
| ---------------- | ----------------- |
| Integrator scope | `operations:read` |
| User ability     | `STOCK_VIEW`      |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/operations/statuses" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/operations/statuses', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/operations/statuses",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### List Operations

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-operations>

`GET /v2/operations`

Inventory documents.

The documents that move stock: supply, waste, transfer, production and inventory checks. `type` says which; see the table below.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/operations
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value             |
| ---------------- | ----------------- |
| Integrator scope | `operations:read` |
| User ability     | `STOCK_VIEW`      |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/operations" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/operations', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/operations",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Operation Types

| `type` | Meaning           |
| ------ | ----------------- |
| `1`    | IN — supply       |
| `3`    | TRANSFER          |
| `4`    | WASTE             |
| `5`    | RETURN            |
| `7`    | MAKE — production |
| `9`    | INVENTORY\_CHECK  |
| `10`   | SUPPLY\_RETURN    |
| `11`   | INITIAL\_STOCK    |

`2` (OUT), `6` (FIXATION) and `8` (MERGE) are deprecated and only appear on historical records.

`status` is `1` (Published) or `2` (Draft).

### Operation Totals

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-operations-total>

`GET /v2/operations/total`

Aggregate subtotal.

Aggregate over the same filters as the list endpoint.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/operations/total
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value             |
| ---------------- | ----------------- |
| Integrator scope | `operations:read` |
| User ability     | `STOCK_VIEW`      |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/operations/total" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/operations/total', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/operations/total",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### List Stock

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock>

`GET /v2/stock`

Current stock levels per product and storage.

Read what is currently on hand. Each row is a product in one storage, with `quantity` on hand and `reserved` held by open receipts.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value        |
| ---------------- | ------------ |
| Integrator scope | `stock:read` |
| User ability     | `STOCK_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Use `/v2/stock/total` for the aggregate, and `/v2/storages` to resolve `storage_id`.

### Get Stock by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock-by-id>

`GET /v2/stock/{id}`

Retrieve a single stock row.

Fetch one stock row by its identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value        |
| ---------------- | ------------ |
| Integrator scope | `stock:read` |
| User ability     | `STOCK_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock/1" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock/1', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock/1",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Stock by Product

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock-by-product>

`GET /v2/stock/product`

Stock resolved per product.

Same data as `/v2/stock`, collapsed to one row per product instead of one per storage row.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock/product
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value        |
| ---------------- | ------------ |
| Integrator scope | `stock:read` |
| User ability     | `STOCK_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock/product" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock/product', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock/product",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Stock by Product Group

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock-by-product-group>

`GET /v2/stock/product-group`

Stock aggregated by product group.

Stock rolled up to product groups.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock/product-group
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value        |
| ---------------- | ------------ |
| Integrator scope | `stock:read` |
| User ability     | `STOCK_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock/product-group" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock/product-group', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock/product-group",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Proxies to client-api `stock/productGroup`; the gateway exposes the hyphenated form.

### Stock Info

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock-info>

`GET /v2/stock/info`

Summary information about stock across storages.

Summary counters used by the stock dashboard.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock/info
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value        |
| ---------------- | ------------ |
| Integrator scope | `stock:read` |
| User ability     | `STOCK_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock/info" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock/info', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock/info",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Get Stock Operation by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock-operation-by-id>

`GET /v2/stock-operations/{id}`

Retrieve a single movement.

Fetch one stock movement by its identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock-operations/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `stock-operations:read` |
| User ability     | `STOCK_VIEW`            |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock-operations/1" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock-operations/1', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock-operations/1",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### List Stock Operations

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock-operations>

`GET /v2/stock-operations`

Every stock movement.

The movement ledger: supplies, waste, transfers, production and the deductions receipts cause. `before_quantity`/`after_quantity` bracket each movement.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock-operations
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `stock-operations:read` |
| User ability     | `STOCK_VIEW`            |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock-operations" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock-operations', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock-operations",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Rows caused by a receipt carry `receipt_id` and `receipt_product_id`; rows caused by an inventory document carry `operation_id`.

### Stock Operations by Product

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock-operations-by-product>

`GET /v2/stock-operations/products`

Per-product movement view.

Movement grouped per product rather than per row.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock-operations/products
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `stock-operations:read` |
| User ability     | `STOCK_VIEW`            |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock-operations/products" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock-operations/products', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock-operations/products",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* Proxies to client-api `stock-operations/follow/products`.

### Stock Operation Totals

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock-operations-total>

`GET /v2/stock-operations/total`

Aggregate quantity and cost.

Aggregate over the same filters as the list endpoint.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock-operations/total
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                   |
| ---------------- | ----------------------- |
| Integrator scope | `stock-operations:read` |
| User ability     | `STOCK_VIEW`            |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock-operations/total" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock-operations/total', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock-operations/total",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Stock Totals

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-stock-total>

`GET /v2/stock/total`

Aggregate stock value and quantity.

Aggregate of the same rows `/v2/stock` returns, honouring the same filters.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stock/total
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value        |
| ---------------- | ------------ |
| Integrator scope | `stock:read` |
| User ability     | `STOCK_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/stock/total" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stock/total', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/stock/total",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Get Storage by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-storage-by-id>

`GET /v2/storages/{id}`

Retrieve a single storage.

Fetch one storage by its identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/storages/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                |
| ---------------- | -------------------- |
| Integrator scope | `storages:read`      |
| User ability     | `STOCK_STORAGE_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/storages/1" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/storages/1', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/storages/1",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### List Storages

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-storages>

`GET /v2/storages`

Storage locations.

The storages stock is tracked against. Needed to make sense of `storage_id` on stock rows and operations.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/storages
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                |
| ---------------- | -------------------- |
| Integrator scope | `storages:read`      |
| User ability     | `STOCK_STORAGE_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/storages" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/storages', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/storages",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Get Supplier by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-supplier-by-id>

`GET /v2/suppliers/{id}`

Retrieve a single supplier.

Fetch one supplier by its identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/suppliers/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                 |
| ---------------- | --------------------- |
| Integrator scope | `suppliers:read`      |
| User ability     | `STOCK_SUPPLIER_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/suppliers/1" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/suppliers/1', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/suppliers/1",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### List Suppliers

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-suppliers>

`GET /v2/suppliers`

Suppliers goods are purchased from.

Suppliers referenced by supply operations, with `spent` and the linked finance account in `balance_id`.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/suppliers
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                 |
| ---------------- | --------------------- |
| Integrator scope | `suppliers:read`      |
| User ability     | `STOCK_SUPPLIER_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/suppliers" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/suppliers', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/suppliers",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Supplier Totals

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/get-suppliers-total>

`GET /v2/suppliers/total`

Aggregate spend and balance.

Aggregate across suppliers matching the current filters.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/suppliers/total
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                 |
| ---------------- | --------------------- |
| Integrator scope | `suppliers:read`      |
| User ability     | `STOCK_SUPPLIER_VIEW` |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/suppliers/total" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/suppliers/total', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/suppliers/total",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### List Operation Items

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/list-operation-items>

`GET /v2/operation-items`

Line items across documents.

Operation line items across every document, for reconciliation exports.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/operation-items
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                  |
| ---------------- | ---------------------- |
| Integrator scope | `operation-items:read` |
| User ability     | `STOCK_VIEW`           |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/operation-items" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/operation-items', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/operation-items",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

### Operation Item Totals

Source: <https://developer.clopos.com/docs/api-reference/v2/inventory/list-operation-items-total>

`GET /v2/operation-items/total`

Aggregate quantity and cost.

Aggregate over the same filters as the list endpoint.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/operation-items/total
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value                  |
| ---------------- | ---------------------- |
| Integrator scope | `operation-items:read` |
| User ability     | `STOCK_VIEW`           |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/operation-items/total" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/operation-items/total', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/operation-items/total",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

## Orders

### Create Order (v2)

Source: <https://developer.clopos.com/docs/api-reference/v2/orders/create-order>

`POST /v2/orders`

Submit a POS order using the streamlined v2 schema

#### Purpose

Create a new order in Clopos using the simplified v2 payload. Optional fields with defaults can be omitted.

#### HTTP Request

```http
POST https://integrations.clopos.com/open-api/v2/orders
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Request Example

```bash
curl --location 'https://integrations.clopos.com/open-api/v2/orders' \
  --header 'x-token: <your JWT token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "auto_accept_terminal": 1,
    "auto_order_accept": true,
    "auto_order_sent_to_station": true,
    "order_number": "A-1024",
    "sale_type_id": 2,
    "venue_id": 1,
    "delivery_fee": 2.5,
    "customer": {
      "id": 9,
      "phone": "+994705401040",
      "address": "123 Main St",
      "customer_discount_type": 1,
      "name": "Rahid Akhundzada"
    },
    "comment": "Leave at the door",
    "discount": {
      "discount_type": 1,
      "discount_value": 10
    },
    "service_charge": {
      "enabled": true,
      "value": 5
    },
    "products": [
      {
        "product_id": 101,
        "product_name": "Pizza",
        "count": 2,
        "price": 8.5,
        "status": "new",
        "product_hash": "abc123",
        "portion_size": 1,
        "note": "No onions",
        "modifiers": [
          {
            "modifier_id": 501,
            "modifier_name": "Extra Cheese",
            "count": 1,
            "price": 0.5,
            "portion_size": 1
          }
        ]
      }
    ]
  }'
```

#### Payload fields

##### Top-level

* `auto_accept_terminal` (number, optional): Terminal that auto-accepts.
* `auto_order_accept` (boolean, default `false`): Auto-accept the order.
* `auto_order_sent_to_station` (boolean, default `false`): Auto-send to stations after acceptance.
* `order_number` (string, optional, max 20 chars): Custom order number to assign to the order.
* `sale_type_id` (number, required): Sale type to use.
* `venue_id` (number, required): Venue where the order belongs.
* `delivery_fee` (number, optional): Delivery charge to apply.
* `comment` (string, optional): Free text note for the order.

##### Discounts

* `discount` (object, optional; defaults applied if present but fields omitted)
  * `discount_type` (number, default `0`)
  * `discount_value` (number, default `0`)

##### Service charge

* `service_charge` (object, optional; defaults applied if present but fields omitted)
  * `enabled` (boolean, default `false`)
  * `value` (number, default `0`)

##### Customer (required)

* `id` (number)
* `phone` (string)
* `address` (string)
* `customer_discount_type` (number)
* `name` (string)

##### Products (array, required)

Each product item requires:

* `product_id` (number)
* `product_name` (string, required) — Display name of the product
* `count` (number)
* `price` (number)
* `status` (string)
* `product_hash` (string)
* `portion_size` (number, default `1`, optional)
* `note` (string, optional) — Free text note for the product (e.g., "No onions")
* `modifiers` (array, optional; defaults to `[]`)
  * `modifier_id` (number)
  * `modifier_name` (string, required) — Display name of the modifier
  * `count` (number)
  * `price` (number, default `0`, optional)
  * `portion_size` (number, default `1`, optional)

!!! info
    Optional fields and any values with defaults can be omitted; defaults are
    applied server-side .

##### Response (example)

```json
{
  "success": true,
  "message": "Order created",
  "data": {
    "id": 295,
    "venue_id": 1,
    "type": "CALL_CENTER_ORDER",
    "integration": "call_center_new",
    "integration_uuid": null,
    "integration_id": null,
    "customer_ref_id": null,
    "integration_status": "CREATED",
    "status": "PENDING",
    "created_at": "2026-01-08T06:28:23.000000Z",
    "updated_at": "2026-01-08T06:28:23.000000Z",
    "integration_response": null
  }
}
```

#### Response Field Reference

| Field                  | Type              | Description                                    |
| ---------------------- | ----------------- | ---------------------------------------------- |
| `id`                   | integer           | Newly created order identifier.                |
| `venue_id`             | integer           | Venue where the order was placed.              |
| `type`                 | string            | Order type (e.g., `CALL_CENTER_ORDER`).        |
| `integration`          | string            | Integration channel (e.g., `call_center_new`). |
| `integration_uuid`     | string (nullable) | UUID from the integration source, if provided. |
| `integration_id`       | string (nullable) | External ID from the integration source.       |
| `customer_ref_id`      | string (nullable) | External customer reference ID.                |
| `integration_status`   | string            | Initial integration state (`CREATED`).         |
| `status`               | string            | Initial order lifecycle state (`PENDING`).     |
| `integration_response` | object (nullable) | Response from the integration, if any.         |
| `created_at`           | string            | Creation timestamp (ISO 8601).                 |
| `updated_at`           | string            | Last update timestamp (ISO 8601).              |

### Get Order by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/orders/get-order-by-id>

`GET /v2/orders/{id}`

Retrieve a single order with status, customer, and line item details.

#### Purpose

Return a specific order so you can inspect its metadata, customer, payment, and fulfillment status without fetching the entire list.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/orders/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Path Parameters

- `` (string): Unique identifier of the order (numeric ID).

#### Query Parameters

- `` (string): 

    Include related resources in the response. Currently supported: `receipt:id,service_notification_id,status`.
    When included, the `data.receipt` field will be present in the response (or `null` if no receipt exists for the order).

#### Request Example

```bash
# Basic request
curl --location "https://integrations.clopos.com/open-api/v2/orders/1" \
  -H "x-token: oauth_example_token" \

# Request including receipt (note: --globoff to avoid shell globbing)
curl --location --globoff 'https://integrations.clopos.com/open-api/v2/orders/1?with[0]=receipt%3Aid%2Cservice_notification_id%2Cstatus' \
  -H "x-token: oauth_example_token" \
```

```javascript
// Basic request
const orderId = 1;
let url = `https://integrations.clopos.com/open-api/v2/orders/${orderId}`;

// Include receipt
const params = new URLSearchParams({
  'with[0]': 'receipt:id,service_notification_id,status'
});
const urlWithReceipt = `${url}?${params}`;

const response = await fetch(urlWithReceipt, {
  headers: {
    'x-token': 'oauth_example_token',
  }
});

const order = await response.json();
```

```python
import requests

order_id = 1
base = f"https://integrations.clopos.com/open-api/v2/orders/{order_id}"
params = {
    'with[0]': 'receipt:id,service_notification_id,status'
}
headers = {
    "x-token": "oauth_example_token",
}

response = requests.get(base, headers=headers, params=params)
order = response.json()
```

#### Response

##### 200 OK — Order found

```json
{
  "success": true,
  "data": {
    "id": 1,
    "venue_id": 1,
    "type": "CALL_CENTER_ORDER",
    "integration": "call_center_new",
    "integration_uuid": null,
    "integration_id": null,
    "customer_ref_id": null,
    "integration_status": "CREATED",
    "status": "RECEIVED",
    "payload": {
      "auto_order_accept": false,
      "auto_order_sent_to_station": false,
      "delivery_fee": 2.5,
      "service": {
        "sale_type_id": 2,
        "venue_id": 1
      },
      "customer": {
        "id": 1,
        "phone": "+994705401040",
        "address": "123 Main St",
        "customer_discount_type": 1,
        "name": "Rahid Akhundzada"
      },
      "products": [
        {
          "product_id": 51,
          "count": 2,
          "product_modificators": [],
          "portion_size": 1,
          "meta": {
            "price": 8.5,
            "order_product": {
              "count": 2,
              "status": "new",
              "product_modificators": [],
              "product_hash": "abc123",
              "product": {
                "id": 51,
                "name": "Pizza",
                "price": 8.5
              }
            }
          }
        }
      ],
      "meta": {
        "comment": "Leave at the door",
        "discount": {
          "discount_type": 1,
          "discount_value": 10
        },
        "apply_service_charge": true,
        "customer_discount_type": 1,
        "service_charge_value": 5
      },
      "customer_id": 1,
      "sale_type_id": 2
    },
    "created_at": "2026-02-02T13:45:53.000000Z",
    "updated_at": "2026-02-02T17:46:02.000000Z",
    "integration_response": null
  }
}
```

##### 404 Not Found — Order does not exist

```json
{
  "success": false,
  "error": "resource_not_found",
  "message": "Order not found"
}
```

#### Field Reference

##### Order Object

| Field                  | Type              | Description                                                            |
| ---------------------- | ----------------- | ---------------------------------------------------------------------- |
| `id`                   | integer           | Order identifier.                                                      |
| `venue_id`             | integer           | Venue that owns the order.                                             |
| `type`                 | string            | Source of the order (e.g., `CALL_CENTER_ORDER`).                       |
| `integration`          | string            | Integration channel that created the order (e.g., `call_center_new`).  |
| `integration_uuid`     | string (nullable) | UUID assigned by the integration source.                               |
| `integration_id`       | string (nullable) | External ID from the integration source.                               |
| `integration_status`   | string            | State reported by the upstream integration (e.g., `CREATED`).          |
| `customer_ref_id`      | string (nullable) | External customer reference ID from the integration.                   |
| `status`               | string            | Current lifecycle state: `PENDING`, `RECEIVED`, `IGNORE`, `DELIVERED`. |
| `payload`              | object            | Full order content including service, customer, products, and meta.    |
| `payload.service`      | object            | Sale type and venue for the order.                                     |
| `payload.customer`     | object            | Customer details (id, phone, address, name).                           |
| `payload.products`     | array             | Line items with product\_id, count, modifiers, and pricing meta.       |
| `payload.meta`         | object            | Order-level metadata: comment, discount, service charge settings.      |
| `integration_response` | object (nullable) | Response data from the integration, if any.                            |
| `created_at`           | string            | Creation timestamp (ISO 8601).                                         |
| `updated_at`           | string            | Last update timestamp (ISO 8601).                                      |

#### Notes

* Returns the same structure as the list endpoint, providing parity between detail and collection responses.
* Use this endpoint after receiving webhook notifications to hydrate UI with complete order data.
* You can embed the linked receipt using the `with[0]` parameter. If the order has no receipt, `receipt` will be `null`.
* Combine with the receipts endpoint when you need final settlement information once the order is delivered.

### Get Orders

Source: <https://developer.clopos.com/docs/api-reference/v2/orders/get-orders>

`GET /v2/orders`

Retrieve orders with replicable filters and status-based searches

#### Purpose

Fetches the statuses, customer details, and line items of your multi-channel orders in a single request.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/orders
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Query Parameters

- `` (integer): Page number for pagination (1-based).

- `` (integer): Number of orders per page.

- `` (string): Lifecycle state to filter by. Allowed values: `PENDING`, `RECEIVED`, `IGNORE`, `DELIVERED`.

- `` (array[string]): Related resources to include in each order. Repeat with indexed brackets (e.g. `with[0]=customer&with[1]=receipt`).

- `` (string): Start date of a `created_at` range, inclusive. Format: `YYYY-MM-DD`. Pair with `date[1]`.

- `` (string): End date of a `created_at` range, inclusive. Format: `YYYY-MM-DD`.

- `` (string): Field to sort by (e.g. `created_at`, `updated_at`, `id`).

- `` (integer): Sort direction: `1` = ascending, `-1` = descending.

- `` (array): Additional filter tuples using PHP bracket notation: `filters[N][0]=field_name&filters[N][1]=value`. Stack filters by incrementing `N` (0-based).

#### Request Example

```bash
curl -X GET "https://integrations.clopos.com/open-api/v2/orders?limit=20&status=DELIVERED" \
  -H "x-token: oauth_example_token" \
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/orders?limit=20&status=DELIVERED', {
  headers: {
    'x-token': 'oauth_example_token',
  }
});

const { data } = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/orders"
headers = {
    "x-token": "oauth_example_token",
}
params = {
    "limit": 20,
    "status": "DELIVERED"
}

response = requests.get(url, headers=headers, params=params)
orders = response.json()
```

#### Response

##### 200 OK — Orders list

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "venue_id": 1,
      "type": "CALL_CENTER_ORDER",
      "integration": "call_center_new",
      "integration_uuid": null,
      "integration_id": null,
      "customer_ref_id": null,
      "integration_status": "CREATED",
      "status": "RECEIVED",
      "payload": {
        "auto_order_accept": false,
        "auto_order_sent_to_station": false,
        "delivery_fee": 2.5,
        "service": {
          "sale_type_id": 2,
          "venue_id": 1
        },
        "customer": {
          "id": 1,
          "phone": "+994705401040",
          "address": "123 Main St",
          "customer_discount_type": 1,
          "name": "Rahid Akhundzada"
        },
        "products": [
          {
            "product_id": 51,
            "count": 2,
            "product_modificators": [],
            "portion_size": 1,
            "meta": {
              "price": 8.5,
              "order_product": {
                "count": 2,
                "status": "new",
                "product_modificators": [],
                "product_hash": "abc123",
                "product": {
                  "id": 51,
                  "name": "Pizza",
                  "price": 8.5
                }
              }
            }
          }
        ],
        "meta": {
          "comment": "Leave at the door",
          "discount": {
            "discount_type": 1,
            "discount_value": 10
          },
          "apply_service_charge": true,
          "customer_discount_type": 1,
          "service_charge_value": 5
        },
        "customer_id": 1,
        "sale_type_id": 2
      },
      "created_at": "2026-02-02T13:45:53.000000Z",
      "updated_at": "2026-02-02T17:46:02.000000Z",
      "integration_response": null
    }
  ],
  "total": 4
}
```

##### 401 Unauthorized — Authentication is missing or invalid

```json
{
  "success": false,
  "error": "unauthorized",
  "message": "Missing or invalid authentication headers"
}
```

#### Field Reference

##### Order Object

| Field                  | Type              | Description                                                            |
| ---------------------- | ----------------- | ---------------------------------------------------------------------- |
| `id`                   | integer           | Order identifier.                                                      |
| `venue_id`             | integer           | Venue that owns the order.                                             |
| `type`                 | string            | Source of the order (e.g., `CALL_CENTER_ORDER`).                       |
| `integration`          | string            | Integration channel that created the order (e.g., `call_center_new`).  |
| `integration_uuid`     | string (nullable) | UUID assigned by the integration source.                               |
| `integration_id`       | string (nullable) | External ID from the integration source.                               |
| `integration_status`   | string            | State reported by the upstream integration (e.g., `CREATED`).          |
| `customer_ref_id`      | string (nullable) | External customer reference ID from the integration.                   |
| `status`               | string            | Current lifecycle state: `PENDING`, `RECEIVED`, `IGNORE`, `DELIVERED`. |
| `payload`              | object            | Full order content including service, customer, products, and meta.    |
| `payload.service`      | object            | Sale type and venue for the order.                                     |
| `payload.customer`     | object            | Customer details (id, phone, address, name).                           |
| `payload.products`     | array             | Line items with product\_id, count, modifiers, and pricing meta.       |
| `payload.meta`         | object            | Order-level metadata: comment, discount, service charge settings.      |
| `integration_response` | object (nullable) | Response data from the integration, if any.                            |
| `created_at`           | string            | Creation timestamp (ISO 8601).                                         |
| `updated_at`           | string            | Last update timestamp (ISO 8601).                                      |

#### Notes

* When an order is created through this endpoint, the POS receives a push notification and notifies the clerk of the new order. `RECEIVED` orders automatically transition into open receipts.
* Use `status=PENDING` to monitor orders awaiting POS confirmation.
* Poll or subscribe to webhooks to track further status changes if your integration requires real-time updates.

### Update Order

Source: <https://developer.clopos.com/docs/api-reference/v2/orders/update-order>

`PUT /v2/orders/{id}`

Update the status of an existing order

#### Purpose

Send a simple status update to mark an order as ignored.

#### HTTP Request

```http
PUT https://integrations.clopos.com/open-api/v2/orders/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Path Parameters

- `` (string): Unique identifier of the order.

#### Request Body

| Field    | Type   | Required | Description                          |
| -------- | ------ | -------- | ------------------------------------ |
| `status` | string | Yes      | Set to `IGNORE` to cancel the order. |

#### Request Example

```bash
curl --location --request PUT 'https://integrations.clopos.com/open-api/v2/orders/108' \
  --header 'Content-Type: application/json' \
  --header 'x-token: oauth_example_token' \
  --data '{
        "status": "IGNORE"
  }'
```

```javascript
const orderId = 108;

const response = await fetch(`https://integrations.clopos.com/open-api/v2/orders/${orderId}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'x-token': 'oauth_example_token',
  },
  body: JSON.stringify({ status: 'IGNORE' })
});

const data = await response.json();
```

```python
import requests

order_id = 108
url = f"https://integrations.clopos.com/open-api/v2/orders/{order_id}"
headers = {
    "Content-Type": "application/json",
    "x-token": "oauth_example_token",
}

payload = {"status": "IGNORE"}

response = requests.put(url, headers=headers, json=payload)
order = response.json()
```

#### Response

##### 200 OK — Order updated

```json
{
  "success": true,
  "data": {
    "id": 108,
    "venue_id": 1,
    "type": "CALL_CENTER_ORDER",
    "integration": "call_center_new",
    "integration_uuid": null,
    "integration_id": null,
    "customer_ref_id": null,
    "integration_status": "CREATED",
    "status": "IGNORE",
    "created_at": "2026-02-02T13:45:53.000000Z",
    "updated_at": "2026-02-02T17:46:02.000000Z",
    "integration_response": null
  }
}
```

##### 400 Bad Request — Invalid status

```json
{
  "success": false,
  "error": "validation_failed",
  "message": "Status is not allowed"
}
```

#### Field Reference

| Field                  | Type              | Description                                 |
| ---------------------- | ----------------- | ------------------------------------------- |
| `id`                   | integer           | Order identifier.                           |
| `venue_id`             | integer           | Venue that owns the order.                  |
| `type`                 | string            | Source of the order.                        |
| `integration`          | string            | Integration channel.                        |
| `integration_uuid`     | string (nullable) | UUID from the integration source.           |
| `integration_id`       | string (nullable) | External ID from the integration source.    |
| `customer_ref_id`      | string (nullable) | External customer reference ID.             |
| `integration_status`   | string            | State reported by the upstream integration. |
| `status`               | string            | Updated lifecycle state (e.g., `IGNORE`).   |
| `integration_response` | object (nullable) | Response data from the integration, if any. |
| `created_at`           | string            | Creation timestamp (ISO 8601).              |
| `updated_at`           | string            | Last update timestamp (ISO 8601).           |

#### Notes

* Request body must include only the status field as shown.
* Currently, only the `IGNORE` status transition is supported through this endpoint.

## Overview

### API Overview (v2)

Source: <https://developer.clopos.com/docs/api-reference/v2/overview>

Base URL and authentication changes for Clopos Open API v2

!!! note
    Version 2 of the Clopos Open API introduces JWT-based authentication and
    simplifies request headers. After authentication you only need to send
    `x-token` with each call.

#### Base URL

```bash
https://integrations.clopos.com/open-api/v2
```

#### What changed in v2

* Endpoints live under `/open-api/v2`.
* `/auth` now requires an `integrator_id` along with your existing client credentials.
* `venue_id` is **not** part of the auth payload.
* Subsequent requests require only the `x-token` header; brand and venue headers are no longer needed.
* Auth responses now return both `expires_in` and `expires_at` (epoch seconds).

#### Authentication flow

  
**1. Collect credentials**

Use your `client_id`, `client_secret`, `brand`, and `integrator_id`. Clopos issues the `integrator_id`; the other three come from the customer's back office (**Add-ons → Open API**). See [Authentication](https://developer.clopos.com/docs/authentication#where-the-client-id-and-client-secret-come-from).

  
**2. Call /v2/auth**

Exchange credentials for a JWT access token and note the `expires_at` value.

  
**3. Call other endpoints**

Include only `x-token` with the JWT you received.

##### Required header for all v2 endpoints (except `/auth`)

```bash
x-token: your_jwt_token_here
```

##### Sample authenticated request

```bash
curl -X GET https://integrations.clopos.com/open-api/v2/orders \
  -H "x-token: your_jwt_token_here"
```

## Price Lists

### List Price Lists

Source: <https://developer.clopos.com/docs/api-reference/v2/price-lists/get-price-lists>

`GET /v2/price-lists`

Retrieve all price lists configured for the brand.

This endpoint retrieves all price lists. A **price list** is a named set of product prices that can be applied to specific venues or sales channels — for example, a dedicated price list for delivery orders that differs from in-store prices.

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Query Parameters

- `` (integer): Maximum number of price lists to return per page (1-999).

- `` (array): Include related data in the response. Supported value: `prices` — embeds the individual product prices that belong to each list.

- `` (array): Sort the results. Supported fields: `id`, `name`, `created_at`. Use array notation, e.g. `sort[0][0]=name&sort[0][1]=asc`.

- `` (string): Comma-separated list of fields to include in the response (e.g. `id,name,status`).

#### Request Example

```bash
curl "https://integrations.clopos.com/open-api/v2/price-lists?with[]=prices" \
  -H "x-token: YOUR_ACCESS_TOKEN"
```

```javascript
const response = await fetch(
  "https://integrations.clopos.com/open-api/v2/price-lists?with[]=prices",
  { headers: { "x-token": "YOUR_ACCESS_TOKEN" } }
);
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/price-lists",
    params={"with[]": "prices"},
    headers={"x-token": "YOUR_ACCESS_TOKEN"},
)
data = response.json()
```

#### Response Example

```json
{
  "data": [
    {
      "id": 1,
      "name": "Delivery Prices",
      "description": "Prices applied to delivery orders",
      "status": true,
      "prices": [
        {
          "id": 10,
          "list_id": 1,
          "product_id": 105,
          "price": 12.5
        }
      ],
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T10:22:12.000000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 1,
    "total_pages": 1
  }
}
```

#### Field Reference

##### Price List Object

| Field         | Type              | Description                                                                                                                                                  |
| ------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`          | integer           | Unique identifier for the price list.                                                                                                                        |
| `name`        | string            | Display name of the price list (e.g., "Delivery Prices").                                                                                                    |
| `description` | string (nullable) | Optional description of the price list, or `null`.                                                                                                           |
| `status`      | boolean           | Whether the price list is active.                                                                                                                            |
| `prices`      | array             | Individual product prices in this list. Included only when requested via `with[]=prices`. See [Price object](https://developer.clopos.com/docs/api-reference/v2/price-lists/get-prices). |
| `created_at`  | string            | Creation timestamp (ISO 8601).                                                                                                                               |
| `updated_at`  | string            | Last update timestamp (ISO 8601).                                                                                                                            |

### List Prices

Source: <https://developer.clopos.com/docs/api-reference/v2/price-lists/get-prices>

`GET /v2/price-lists/prices`

Retrieve the individual product prices that belong to price lists.

This endpoint retrieves the individual **prices** stored across all price lists. Each entry maps a product to its price within a specific price list, letting you read product pricing per channel without loading every list separately.

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Query Parameters

- `` (integer): Maximum number of prices to return per page (1-999).

- `` (array): Filter prices by specific fields. Use array notation: `filters[0][0]=field_name&filters[0][1]=value`. Supported fields: `id`, `product_id`, `list_id`.

- `` (array): Include related data in the response. Supported values: `product` (embeds the related product) and `list` (embeds the related price list).

#### Request Example

```bash
curl "https://integrations.clopos.com/open-api/v2/price-lists/prices?filters[0][0]=list_id&filters[0][1]=1" \
  -H "x-token: YOUR_ACCESS_TOKEN"
```

```javascript
const response = await fetch(
  "https://integrations.clopos.com/open-api/v2/price-lists/prices?filters[0][0]=list_id&filters[0][1]=1",
  { headers: { "x-token": "YOUR_ACCESS_TOKEN" } }
);
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/price-lists/prices",
    params={"filters[0][0]": "list_id", "filters[0][1]": "1"},
    headers={"x-token": "YOUR_ACCESS_TOKEN"},
)
data = response.json()
```

#### Response Example

```json
{
  "data": [
    {
      "id": 10,
      "list_id": 1,
      "product_id": 105,
      "price": 12.5
    },
    {
      "id": 11,
      "list_id": 1,
      "product_id": 106,
      "price": 8.0
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total": 2,
    "total_pages": 1
  }
}
```

#### Field Reference

##### Price Object

| Field        | Type              | Description                                                                                                                                          |
| ------------ | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`         | integer           | Unique identifier for the price entry.                                                                                                               |
| `list_id`    | integer           | ID of the [price list](https://developer.clopos.com/docs/api-reference/v2/price-lists/get-price-lists) this price belongs to.                                                    |
| `product_id` | integer           | ID of the product this price applies to.                                                                                                             |
| `price`      | number            | The product's price within this price list.                                                                                                          |
| `product`    | object (nullable) | The related product. Included only when requested via `with[]=product`. See [Product object](https://developer.clopos.com/docs/api-reference/v2/products/get-all-products).      |
| `list`       | object (nullable) | The related price list. Included only when requested via `with[]=list`. See [Price List object](https://developer.clopos.com/docs/api-reference/v2/price-lists/get-price-lists). |

## Products

### List Products

Source: <https://developer.clopos.com/docs/api-reference/v2/products/get-all-products>

`GET /v2/products`

Get the product catalog with advanced filtering and pagination.

#### Overview

This endpoint allows you to retrieve your branch-based product catalog. It offers a multitude of filtering options such as `type`, `category_id`, and `tags`, and supports five main product types: `GOODS`, `DISH`, `TIMER`, `PREPARATION`, and `INGREDIENT`.

The returned data includes product variants (`modifications`), modifiers (`modificator_groups`), recipes (`recipe`), and all other related data.

##### Product Types and Behaviors

While all product types are fundamentally "products," each has its own specific models and behaviors:

* **GOODS:** These can have variants (`modifications`).
  * **With Variants:** If a product has variants, only those variants can be sold. The main product acts as a parent and cannot be sold itself. Each modification behaves like a standard `GOODS` product without variants.
  * **Without Variants:** Standard products that can be sold directly.

* **DISH:** This type can have `modificator_groups` (modifiers).
  * **Modifiers:** Modifiers (`Modificator`) are used exclusively for `DISH` type products. They represent add-on options like "Spice Level" or "Extra Lavash."

* **TIMER:** Represents time-based services (e.g., PS5 rental). Pricing is determined by rules defined in the `setting` field.

* **PREPARATION:** Semi-finished items that have their own recipe and are used in the production of other `DISH` items.

* **INGREDIENT:** Raw materials used in production.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/products
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Query Parameters

All parameters are standard URL query parameters. Array and filter values use PHP/Laravel bracket notation — **not** a JSON blob. Arrays are indexed (`with[0]=category&with[1]=station`), and each filter is a tuple under `filters[N]`: field name at `filters[N][0]`, value at `filters[N][1]` (or `filters[N][1][M]` when the value is itself an array).

- `` (integer): Page number for pagination.

- `` (integer): Products per page. Maximum: 100.

- `` (array[string]): 

    Related resources to include in each product. Repeat with indexed brackets. Common values: `category`, `station`, `modifications`, `modifications.codes`, `taxes`, `codes`, `modificator_groups`, `recipe`, `packages`, `tags`.
    **Example:** `with[0]=category&with[1]=station&with[2]=modifications`

- `` (string): 

    Comma-separated list of fields to include in the response. `id`, `name`, and `type` are always returned.
    **Example:** `selects=id,name,type,price,image`

- `` (array): Zero or more filter tuples, where `N` is a 0-based index. Each tuple is `[field_name, value]`. `value` may be a scalar (`filters[N][1]=...`) or an array (`filters[N][1][0]=...&filters[N][1][1]=...`). See the **Filtering** section for the full list of supported fields.

#### Filtering

Each filter occupies its own index under `filters[]`. Stack multiple filters by incrementing the outer index — for example `filters[0]` for `type`, `filters[1]` for `inventory_behavior`, and so on. The outer index order does not matter; only uniqueness does.

- `type` (array[string]): 

    Product type. Possible values: `GOODS`, `DISH`, `TIMER`, `PREPARATION`, `INGREDIENT`.
    **Example:** `filters[0][0]=type&filters[0][1][0]=GOODS&filters[0][1][1]=DISH`

- `category_id` (array[integer]): 

    Products belonging to the specified category IDs.
    **Example:** `filters[0][0]=category_id&filters[0][1][0]=1&filters[0][1][1]=3`

- `station_id` (array[integer]): 

    Products assigned to the specified station IDs.
    **Example:** `filters[0][0]=station_id&filters[0][1][0]=1&filters[0][1][1]=2`

- `tags` (array[integer]): 

    Products with the specified tag IDs.
    **Example:** `filters[0][0]=tags&filters[0][1][0]=1&filters[0][1][1]=2`

- `giftable` (string): 

    `"1"` = giftable, `"0"` = not giftable.
    **Example:** `filters[0][0]=giftable&filters[0][1]=1`

- `discountable` (string): 

    `"1"` = discountable, `"0"` = not discountable.
    **Example:** `filters[0][0]=discountable&filters[0][1]=1`

- `inventory_behavior` (string): 

    Inventory tracking mode. Allowed values: `"0"` (`MINUS_INGREDIENTS` — deduct recipe ingredients on sale, typical for `DISH`), `"1"` (`MINUS_SELF` — deduct the product itself from stock, countable `GOODS`/`INGREDIENT`), `"3"` (`PASSIVE` — no inventory tracking, uncountable).
    **Example:** `filters[0][0]=inventory_behavior&filters[0][1]=0`

- `haveIngredients` (string): 

    `"1"` = has a recipe/ingredients.
    **Example:** `filters[0][0]=haveIngredients&filters[0][1]=1`

- `sold_by_portion` (string): 

    `"1"` = sold by portion.
    **Example:** `filters[0][0]=sold_by_portion&filters[0][1]=1`

- `has_variants` (string): 

    `"1"` = has variants (`modifications`).
    **Example:** `filters[0][0]=has_variants&filters[0][1]=1`

- `has_modifiers` (string): 

    `"1"` = has a modifier group (`modificator_groups`).
    **Example:** `filters[0][0]=has_modifiers&filters[0][1]=1`

- `has_barcode` (string): 

    `"1"` = has at least one barcode. The filter still works, but the top-level `barcode` string on the product is **deprecated** — request `with[]=codes` and read barcodes from the `codes` array instead.
    **Example:** `filters[0][0]=has_barcode&filters[0][1]=1`

- `has_service_charge` (string): 

    `"1"` = service charge applies.
    **Example:** `filters[0][0]=has_service_charge&filters[0][1]=1`

##### Combining filters

Stack filters by incrementing the outer index. Scalar and array values can be mixed freely:

```
?page=1&limit=50
 &filters[0][0]=type&filters[0][1][0]=GOODS&filters[0][1][1]=DISH&filters[0][1][2]=TIMER
 &filters[1][0]=inventory_behavior&filters[1][1]=0
```

(Line breaks shown only for readability — the real URL must be a single string with no whitespace. Brackets should be URL-encoded by your HTTP client; `curl` users can pass `--globoff` to avoid shell interpretation.)

#### Request Examples

```bash
# Basic request with pagination and selects
curl --globoff 'https://integrations.clopos.com/open-api/v2/products?page=1&limit=100&selects=id,name,type' \
  -H "x-token: oauth_example_token"
```

```bash
# Relations + two filters (type IN (GOODS,DISH,TIMER) AND inventory_behavior = 0)
curl --globoff 'https://integrations.clopos.com/open-api/v2/products?with[0]=category&with[1]=station&with[2]=modifications&with[3]=modifications.codes&with[4]=taxes&with[5]=codes&page=1&limit=50&filters[0][0]=type&filters[0][1][0]=GOODS&filters[0][1][1]=DISH&filters[0][1][2]=TIMER&filters[1][0]=inventory_behavior&filters[1][1]=0' \
  -H "x-token: oauth_example_token"
```

```javascript
// URLSearchParams handles the bracket encoding for you
const params = new URLSearchParams({
  page: '1',
  limit: '50',
  'with[0]': 'category',
  'with[1]': 'station',
  'with[2]': 'modifications',
  'with[3]': 'modifications.codes',
  'with[4]': 'taxes',
  'with[5]': 'codes',
  'filters[0][0]': 'type',
  'filters[0][1][0]': 'GOODS',
  'filters[0][1][1]': 'DISH',
  'filters[0][1][2]': 'TIMER',
  'filters[1][0]': 'inventory_behavior',
  'filters[1][1]': '0',
});

const response = await fetch(`https://integrations.clopos.com/open-api/v2/products?${params}`, {
  headers: { 'x-token': 'oauth_example_token' },
});

const result = await response.json();
console.log(result);
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/products"
headers = {"x-token": "oauth_example_token"}
params = {
    "page": 1,
    "limit": 50,
    "with[0]": "category",
    "with[1]": "station",
    "with[2]": "modifications",
    "with[3]": "modifications.codes",
    "with[4]": "taxes",
    "with[5]": "codes",
    "filters[0][0]": "type",
    "filters[0][1][0]": "GOODS",
    "filters[0][1][1]": "DISH",
    "filters[0][1][2]": "TIMER",
    "filters[1][0]": "inventory_behavior",
    "filters[1][1]": 0,
}

response = requests.get(url, headers=headers, params=params)
result = response.json()
```

#### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "parent_id": null,
      "station_id": null,
      "category_id": null,
      "unit_id": 1,
      "type": "INGREDIENT",
      "name": "Test_Tomato",
      "parent_name": "",
      "full_name": "Test_Tomato",
      "position": null,
      "barcode": null,
      "gov_code": null,
      "status": 1,
      "hidden": 0,
      "sold_by_weight": false,
      "discountable": true,
      "giftable": false,
      "has_modifications": false,
      "description": null,
      "price": 0,
      "cost_price": 0,
      "cooking_time": 0,
      "inventory_behavior": 0,
      "low_stock": 0,
      "unit_weight": 0,
      "venues": [],
      "media": [],
      "created_at": "2026-01-13 20:04:05",
      "updated_at": "2026-01-13 20:04:05"
    },
    {
      "id": 2,
      "parent_id": null,
      "station_id": null,
      "category_id": null,
      "unit_id": 1,
      "type": "INGREDIENT",
      "name": "Test_Onion",
      "parent_name": "",
      "full_name": "Test_Onion",
      "position": null,
      "barcode": null,
      "gov_code": null,
      "status": 1,
      "hidden": 0,
      "sold_by_weight": false,
      "discountable": true,
      "giftable": false,
      "has_modifications": false,
      "description": null,
      "price": 0,
      "cost_price": 1,
      "cooking_time": 0,
      "inventory_behavior": 0,
      "low_stock": 0,
      "unit_weight": 0,
      "venues": [],
      "media": [],
      "created_at": "2026-01-13 20:04:06",
      "updated_at": "2026-04-01 17:05:36"
    }
  ],
  "total": 284
}
```

#### Field Reference

##### Product Object

| Field                | Type               | Description                                                                                                                                                                                                                                                                                                                             |
| -------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                 | integer            | Unique product identifier.                                                                                                                                                                                                                                                                                                              |
| `parent_id`          | integer (nullable) | ID of the parent product for a variant. A row with `type: "MODIFICATION"` is a **variant** of the `GOODS` product referenced here — "modification" and "variant" mean the same thing in this API, and a variant carries the full product schema (same fields as the parent, with its own `price`, `cost_price`, stock, barcodes, etc.). |
| `station_id`         | integer (nullable) | ID of the preparation station assigned to this product.                                                                                                                                                                                                                                                                                 |
| `category_id`        | integer (nullable) | ID of the category this product belongs to.                                                                                                                                                                                                                                                                                             |
| `unit_id`            | integer            | ID of the unit of measurement.                                                                                                                                                                                                                                                                                                          |
| `type`               | string             | Product type: `GOODS`, `DISH`, `TIMER`, `PREPARATION`, `INGREDIENT`, `MODIFICATION`, `MODIFIER`.                                                                                                                                                                                                                                        |
| `name`               | string             | Product name.                                                                                                                                                                                                                                                                                                                           |
| `parent_name`        | string             | Name of the parent product (empty string if none).                                                                                                                                                                                                                                                                                      |
| `full_name`          | string             | Full product name including variant info (e.g., "Fanta 0.5 L").                                                                                                                                                                                                                                                                         |
| `position`           | integer (nullable) | Display order position within the category.                                                                                                                                                                                                                                                                                             |
| `barcode`            | string (nullable)  | **Deprecated.** Legacy single-barcode field, kept for backwards compatibility and not guaranteed to be populated. For current barcodes, request `with[]=codes` and read from the `codes` array.                                                                                                                                         |
| `gov_code`           | string (nullable)  | Government/tax code for the product.                                                                                                                                                                                                                                                                                                    |
| `status`             | integer            | `1` = active, `0` = inactive.                                                                                                                                                                                                                                                                                                           |
| `hidden`             | integer            | `1` = hidden from menus, `0` = visible.                                                                                                                                                                                                                                                                                                 |
| `sold_by_weight`     | boolean            | Whether the product is sold by weight rather than quantity.                                                                                                                                                                                                                                                                             |
| `discountable`       | boolean            | Whether discounts can be applied to this product.                                                                                                                                                                                                                                                                                       |
| `giftable`           | boolean            | Whether this product can be given as a gift/complimentary item.                                                                                                                                                                                                                                                                         |
| `has_modifications`  | boolean            | If `true`, the product has variants in the `modifications` array.                                                                                                                                                                                                                                                                       |
| `description`        | string (nullable)  | Product description text.                                                                                                                                                                                                                                                                                                               |
| `price`              | number             | Base selling price. For parent GOODS with variants, this may be `0` since variants carry their own prices.                                                                                                                                                                                                                              |
| `cost_price`         | number             | Cost price used for margin calculations.                                                                                                                                                                                                                                                                                                |
| `cooking_time`       | integer            | Estimated preparation time in minutes.                                                                                                                                                                                                                                                                                                  |
| `inventory_behavior` | integer            | Inventory tracking mode. `0` = `MINUS_INGREDIENTS` — on sale, deduct the recipe's ingredients from stock (typical for `DISH`). `1` = `MINUS_SELF` — deduct the product itself from stock (countable `GOODS` / `INGREDIENT`). `3` = `PASSIVE` — no inventory tracking (uncountable).                                                     |
| `low_stock`          | integer            | Low stock threshold for alerts.                                                                                                                                                                                                                                                                                                         |
| `unit_weight`        | number             | Physical weight of a single unit, in **kilograms**. For example, if `unit_id` resolves to `pcs`, this is how much one piece weighs (a single packet that weighs 3 kg is stored as `3`). Independent of `sold_by_weight`; used for logistics, shipping, and stock-by-weight calculations, not for pricing mode.                          |
| `venues`             | array              | Venue-specific availability and pricing overrides.                                                                                                                                                                                                                                                                                      |
| `media`              | array              | Image attachments. See [Media object](https://developer.clopos.com/docs/common-objects#media).                                                                                                                                                                                                                                                                      |
| `created_at`         | string             | Creation timestamp.                                                                                                                                                                                                                                                                                                                     |
| `updated_at`         | string             | Last update timestamp.                                                                                                                                                                                                                                                                                                                  |

##### Variant Object (`modifications`)

Represents different versions (e.g., size, color) of a `GOODS` type product.

A variant has the **same shape as a product** — every field listed in the [Product Object](#field-reference) above (`id`, `parent_id`, `category_id`, `unit_id`, `price`, `cost_price`, `unit_weight`, `inventory_behavior`, `media`, `venues`, `created_at`, `updated_at`, …) is present on each variant. The only differences worth calling out:

* `type` is always `MODIFICATION`.
* `parent_id` points at the parent `GOODS` product instead of being `null`.
* `full_name` combines the parent name with the variant name (e.g. `"Fanta 0.5 L"`).
* The variant carries its own `price`, `cost_price`, `barcode`/`codes`, `status`, stock, etc. — the parent's values are not inherited at sale time.

##### Modifier Group (`modificator_groups`)

Defines groups of options that can be added to a `DISH` type product (e.g., "Pizza Toppings").

| Field          | Type    | Description                                             |
| -------------- | ------- | ------------------------------------------------------- |
| `id`           | integer | The group's identifier.                                 |
| `name`         | string  | The name of the group (e.g., "Spice Level").            |
| `type`         | integer | Selection rule (`1`: Single-choice, `0`: Multi-choice). |
| `min_select`   | integer | Minimum number of selections.                           |
| `max_select`   | integer | Maximum number of selections.                           |
| `modificators` | array   | List of selectable items. See **Modifier Object**.      |

##### Modifier Object (`modificators`)

| Field        | Type              | Description                                                                  |
| ------------ | ----------------- | ---------------------------------------------------------------------------- |
| `id`         | integer           | The modifier's identifier.                                                   |
| `name`       | string            | The name of the modifier (e.g., "Medium Hot").                               |
| `price`      | number            | The additional price for the option.                                         |
| `ingredient` | object (nullable) | If the modifier is linked to an ingredient, contains ingredient information. |

##### Timer Settings (`setting`)

Contains the time-based pricing rules for `TIMER` type products.

| Field      | Type    | Description                                                        |
| ---------- | ------- | ------------------------------------------------------------------ |
| `interval` | integer | The pricing interval in minutes.                                   |
| `prices`   | array   | Prices for different time periods. `[{ "price": 3, "from": 120 }]` |

##### Recipe Item (`recipe`)

| Field           | Type    | Description                             |
| --------------- | ------- | --------------------------------------- |
| `ingredient_id` | integer | The product ID of the recipe component. |
| `name`          | string  | The name of the component.              |
| `gross`         | string  | Gross amount.                           |
| `net`           | string  | Net amount.                             |

##### Package Object (`packages`)

Specifies the purchasing packages defined for `INGREDIENT` type products.

| Field   | Type    | Description                                        |
| ------- | ------- | -------------------------------------------------- |
| `id`    | integer | The package's identifier.                          |
| `name`  | string  | The name of the package (e.g., "Bundle 10 pcs").   |
| `equal` | integer | The number of base units contained in the package. |

### Get Product by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/products/get-product-by-id>

`GET /v2/products/{id}`

Retrieve a single product with type-specific details.

#### Purpose

Returns a single product from the Clopos catalog, along with related data specific to its type (variants, modifiers, recipe, timer settings, etc.). Use the `with` parameters to fetch only the sub-resources you need.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/products/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Path Parameters

- `` (string): The product ID (integer or UUID).

#### Query Parameters

- `` (string): Related data selector. Example: `taxes`, `unit`, `modifications`, `modificator_groups`, `recipe`, `packages`, `media`, `tags`, `setting`. You can include multiple `with` parameters.

> Supported `with` values may vary based on your backend version.

#### Request Example

```bash
curl -X GET "https://integrations.clopos.com/open-api/v2/products/419?with[]=modifications&with[]=taxes" \
  -H "x-token: oauth_example_token" \
```

```bash
curl -X GET "https://integrations.clopos.com/open-api/v2/products/1?with[]=modificator_groups&with[]=recipe" \
  -H "x-token: oauth_example_token" \
```

```javascript
const params = new URLSearchParams([
  ['with[]', 'taxes'],
  ['with[]', 'unit'],
  ['with[]', 'modificator_groups.modificators.ingredient.unit'],
  ['with[]', 'recipe'],
  ['with[]', 'packages']
]);

const response = await fetch(`https://integrations.clopos.com/open-api/v2/products/1?${params}`, {
  headers: {
    'x-token': 'oauth_example_token',
  }
});

const product = await response.json();
```

#### Response

##### 200 OK — Product found

```json
{
  "success": true,
  "data": {
    "id": 1,
    "parent_id": null,
    "station_id": null,
    "category_id": null,
    "unit_id": 1,
    "type": "INGREDIENT",
    "name": "Test_Tomato",
    "parent_name": "",
    "full_name": "Test_Tomato",
    "position": null,
    "barcode": null,
    "gov_code": null,
    "status": 1,
    "hidden": 0,
    "sold_by_weight": false,
    "discountable": true,
    "giftable": false,
    "has_modifications": false,
    "description": null,
    "price": 0,
    "cost_price": 0,
    "cooking_time": 0,
    "inventory_behavior": 0,
    "low_stock": 0,
    "unit_weight": 0,
    "venues": [],
    "media": [],
    "created_at": "2026-01-13 20:04:05",
    "updated_at": "2026-01-13 20:04:05"
  }
}
```

##### 404 Not Found — Product does not exist

```json
{
  "success": false,
  "error": "resource_not_found",
  "message": "Product not found"
}
```

#### Field Reference

[See the full breakdown of the `Product` object and nested structures such as `modifications` and `modificator_groups` on the List Products page.](https://developer.clopos.com/docs/api-reference/v2/products/get-all-products#field-reference)

##### Product Object

| Field                | Type               | Description                                                                                                                                                                                                                                                                                                                             |
| -------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                 | integer            | Unique product identifier.                                                                                                                                                                                                                                                                                                              |
| `parent_id`          | integer (nullable) | ID of the parent product for a variant. A row with `type: "MODIFICATION"` is a **variant** of the `GOODS` product referenced here — "modification" and "variant" mean the same thing in this API, and a variant carries the full product schema (same fields as the parent, with its own `price`, `cost_price`, stock, barcodes, etc.). |
| `station_id`         | integer (nullable) | ID of the preparation station assigned to this product.                                                                                                                                                                                                                                                                                 |
| `category_id`        | integer (nullable) | ID of the category this product belongs to.                                                                                                                                                                                                                                                                                             |
| `unit_id`            | integer            | ID of the unit of measurement.                                                                                                                                                                                                                                                                                                          |
| `type`               | string             | Product type: `GOODS`, `DISH`, `TIMER`, `PREPARATION`, `INGREDIENT`, `MODIFICATION`, `MODIFIER`.                                                                                                                                                                                                                                        |
| `name`               | string             | Product name.                                                                                                                                                                                                                                                                                                                           |
| `parent_name`        | string             | Name of the parent product (empty string if none).                                                                                                                                                                                                                                                                                      |
| `full_name`          | string             | Full product name including variant info (e.g., "Fanta 0.5 L").                                                                                                                                                                                                                                                                         |
| `position`           | integer (nullable) | Display order position within the category.                                                                                                                                                                                                                                                                                             |
| `barcode`            | string (nullable)  | **Deprecated.** Legacy single-barcode field, kept for backwards compatibility and not guaranteed to be populated. For current barcodes, request `with[]=codes` and read from the `codes` array.                                                                                                                                         |
| `gov_code`           | string (nullable)  | Government/tax code for the product.                                                                                                                                                                                                                                                                                                    |
| `status`             | integer            | `1` = active, `0` = inactive.                                                                                                                                                                                                                                                                                                           |
| `hidden`             | integer            | `1` = hidden from menus, `0` = visible.                                                                                                                                                                                                                                                                                                 |
| `sold_by_weight`     | boolean            | Whether the product is sold by weight rather than quantity.                                                                                                                                                                                                                                                                             |
| `discountable`       | boolean            | Whether discounts can be applied to this product.                                                                                                                                                                                                                                                                                       |
| `giftable`           | boolean            | Whether this product can be given as a gift/complimentary item.                                                                                                                                                                                                                                                                         |
| `has_modifications`  | boolean            | If `true`, the product has variants in the `modifications` array.                                                                                                                                                                                                                                                                       |
| `description`        | string (nullable)  | Product description text.                                                                                                                                                                                                                                                                                                               |
| `price`              | number             | Base selling price. For parent GOODS with variants, this may be `0` since variants carry their own prices.                                                                                                                                                                                                                              |
| `cost_price`         | number             | Cost price used for margin calculations.                                                                                                                                                                                                                                                                                                |
| `cooking_time`       | integer            | Estimated preparation time in minutes.                                                                                                                                                                                                                                                                                                  |
| `inventory_behavior` | integer            | Inventory tracking mode. `0` = `MINUS_INGREDIENTS` — on sale, deduct the recipe's ingredients from stock (typical for `DISH`). `1` = `MINUS_SELF` — deduct the product itself from stock (countable `GOODS` / `INGREDIENT`). `3` = `PASSIVE` — no inventory tracking (uncountable).                                                     |
| `low_stock`          | integer            | Low stock threshold for alerts.                                                                                                                                                                                                                                                                                                         |
| `unit_weight`        | number             | Physical weight of a single unit, in **kilograms**. For example, if `unit_id` resolves to `pcs`, this is how much one piece weighs (a single packet that weighs 3 kg is stored as `3`). Independent of `sold_by_weight`; used for logistics, shipping, and stock-by-weight calculations, not for pricing mode.                          |
| `venues`             | array              | Venue-specific availability and pricing overrides.                                                                                                                                                                                                                                                                                      |
| `media`              | array              | Image attachments. See [Media object](https://developer.clopos.com/docs/common-objects#media).                                                                                                                                                                                                                                                                      |
| `created_at`         | string             | Creation timestamp.                                                                                                                                                                                                                                                                                                                     |
| `updated_at`         | string             | Last update timestamp.                                                                                                                                                                                                                                                                                                                  |

#### Notes

* If the `id` parameter is in the wrong format, the backend returns a `400` error; validate it on the client side.
* Since `with` parameters are evaluated sequentially, avoid using the same key more than once.
* Type-specific heavy relationships (for example, large `recipe` or `modificator_groups`) can produce large responses; request only what you need.
* Some fields may be empty or null depending on the product type; use the `type` field to drive conditional rendering on the client.
* For TIMER products, the `setting.prices` array represents additional fees applied after a certain duration.
* For INGREDIENT products, the `packages` field shows the package sizes used in stock entries; if not applicable, it is an empty array.

### Get Stop List

Source: <https://developer.clopos.com/docs/api-reference/v2/products/get-stop-list>

`GET /v2/products/stop-list`

Get stop list data for specific products

#### Purpose

Retrieve stop list data for specific products. The stop list indicates product limitations such as stock limits. If a product is not returned in the response, it means that product does not have any stop list limitations.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/products/stop-list
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Query Parameters

##### Filters

You can filter by product IDs to get stop list data for specific products.

| Parameter       | Type   | Required | Description                                            |
| --------------- | ------ | -------- | ------------------------------------------------------ |
| `filters[0][0]` | string | No       | Filter field name. Use `"id"` to filter by product ID. |
| `filters[0][1]` | array  | No       | Array of product IDs to filter.                        |

##### Filter Syntax

To filter by product IDs, use the following format:

```
filters[0][0]=id&filters[0][1][0]=1&filters[0][1][1]=332
```

This will filter for products with IDs `1` and `332`.

#### Request Example

```bash
curl --location --globoff 'https://integrations.clopos.com/open-api/v2/products/stop-list?filters[0][0]=id&filters[0][1][0]=1&filters[0][1][1]=332' \
  --header 'x-token: oauth_example_token' \
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/products/stop-list?filters[0][0]=id&filters[0][1][0]=1&filters[0][1][1]=332', {
  headers: {
    'x-token': 'oauth_example_token',
  }
});

const data = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/products/stop-list"
headers = {
    "x-token": "oauth_example_token",
}
params = {
    "filters[0][0]": "id",
    "filters[0][1][0]": 1,
    "filters[0][1][1]": 332
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
```

#### Response

##### 200 OK — Success

Returns an array of stop list entries for the requested products. If a product does not have stop list limitations, it will not appear in the response.

```json
{
  "success": true,
  "data": [
    {
      "id": 54,
      "limit": 0,
      "timestamp": 1761202010781
    },
    {
      "id": 57,
      "limit": 3,
      "timestamp": 1761202001368
    },
    {
      "id": 275,
      "limit": 5,
      "timestamp": 1762929390368
    }
  ]
}
```

!!! note
    When no products are on the stop list, the response returns an empty `data` array: `{"success": true, "data": []}`. This is normal and indicates no products currently have stock limitations.

##### 400 Bad Request — Invalid Parameters

```json
{
  "success": false,
  "error": "invalid_parameter",
  "message": "Invalid filter parameters"
}
```

##### 401 Unauthorized — Missing Header

```json
{
  "success": false,
  "error": "unauthorized",
  "message": "Missing authentication headers"
}
```

#### Field Reference

##### Stop List Entry Object

| Field       | Type    | Description                                                                                      |
| ----------- | ------- | ------------------------------------------------------------------------------------------------ |
| `id`        | integer | Product ID. This corresponds to the product identifier.                                          |
| `limit`     | integer | Stock limit for the product. `0` means the product is out of stock or has no available quantity. |
| `timestamp` | integer | Unix timestamp (in milliseconds) when the stop list entry was last updated.                      |

#### Notes

* The `id` field in the response represents the `product_id`.
* If a product is not included in the response data, it means that product does not have any stop list limitations.
* Use the `filters` parameter to query specific products by their IDs.
* The `limit` field indicates the available stock limit. A value of `0` typically means the product is unavailable.
* The `timestamp` field shows when the stop list entry was last updated, useful for tracking changes.

## Receipts

### Close Receipt

Source: <https://developer.clopos.com/docs/api-reference/v2/receipts/close-receipt>

`POST /v2/receipts/{id}/close`

Close an existing receipt with payment methods and closing timestamp

#### Purpose

Close an existing receipt by updating its payment methods and setting the closing timestamp. This endpoint is used to finalize a receipt that was previously created but not yet closed.

#### HTTP Request

```http
POST https://integrations.clopos.com/open-api/v2/receipts/{id}/close
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Path Parameters

| Parameter | Type   | Description                                |
| --------- | ------ | ------------------------------------------ |
| `id`      | number | Unique identifier of the receipt to close. |

#### Request Body

| Field             | Type   | Required | Description                                                                                                  |
| ----------------- | ------ | -------- | ------------------------------------------------------------------------------------------------------------ |
| `payment_methods` | array  | Yes      | List of payment methods with amounts. See [Payment method](https://developer.clopos.com/docs/common-objects#payment-method-in-receipts). |
| `closed_at`       | string | No       | Closing timestamp (YYYY-MM-DD HH:mm:ss). Defaults to current time if omitted.                                |

##### `payment_methods[]`

| Field    | Type   | Required | Description                                 |
| -------- | ------ | -------- | ------------------------------------------- |
| `id`     | number | Yes      | Payment method ID.                          |
| `name`   | string | Yes      | Payment method name (e.g., "Cash", "Card"). |
| `amount` | number | Yes      | Amount paid using this method.              |

#### Request Example

```bash
curl --location --request POST 'https://integrations.clopos.com/open-api/v2/receipts/10950/close' \
  --header 'Content-Type: application/json' \
  --header 'x-token: oauth_example_token' \
  --data '{
    "payment_methods": [
      {
        "id": 2,
        "name": "Cash",
        "amount": 8140
      }
    ],
    "closed_at": "2026-01-20 09:59:54"
  }'
```

```javascript
const receiptId = 10950;

const response = await fetch(`https://integrations.clopos.com/open-api/v2/receipts/${receiptId}/close`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-token': 'oauth_example_token',
  },
  body: JSON.stringify({
    payment_methods: [
      {
        id: 2,
        name: 'Cash',
        amount: 8140
      }
    ],
    closed_at: '2026-01-20 09:59:54'
  })
});

const receipt = await response.json();
```

```python
import requests

receipt_id = 10950
url = f"https://integrations.clopos.com/open-api/v2/receipts/{receipt_id}/close"
headers = {
    "Content-Type": "application/json",
    "x-token": "oauth_example_token",
}
payload = {
    "payment_methods": [
        {
            "id": 2,
            "name": "Cash",
            "amount": 8140
        }
    ],
    "closed_at": "2026-01-20 09:59:54"
}

response = requests.post(url, headers=headers, json=payload)
receipt = response.json()
```

#### Response

##### 200 OK — Receipt Closed

```json
{
  "success": true,
  "message": "Receipt closed",
  "data": {
    "id": 10950,
    "closed_at": "2026-01-20 09:59:54",
    "payment_methods": [
      {
        "id": 2,
        "name": "Cash",
        "amount": 8140
      }
    ]
  }
}
```

##### 400 Bad Request — Validation Error

```json
{
  "success": false,
  "error": "validation_failed",
  "message": "closed_at must be greater than created_at"
}
```

##### 404 Not Found — Receipt Not Found

```json
{
  "success": false,
  "error": "not_found",
  "message": "Receipt not found"
}
```

#### Field Reference

##### Response fields

| Field                  | Type    | Description                                                     |
| ---------------------- | ------- | --------------------------------------------------------------- |
| `success`              | boolean | Indicates the result of the request.                            |
| `message`              | string  | Human-readable status message.                                  |
| `data.id`              | number  | Receipt identifier that was closed.                             |
| `data.closed_at`       | string  | Closing timestamp applied to the receipt (YYYY-MM-DD HH:mm:ss). |
| `data.payment_methods` | array   | Payment methods recorded on the receipt.                        |

##### `payment_methods[]`

| Field    | Type   | Description                                 |
| -------- | ------ | ------------------------------------------- |
| `id`     | number | Payment method ID.                          |
| `name`   | string | Payment method name (e.g., "Cash", "Card"). |
| `amount` | number | Amount paid using this method.              |

#### Notes

* The receipt must be in an open state (`status: 1`) to be closed through this endpoint.
* If `closed_at` is omitted, the server uses the current timestamp.
* The `closed_at` value must be later than the receipt's `created_at` timestamp.
* After closing, the receipt's `status` changes to `2` (closed).

### Get Receipt by CID

Source: <https://developer.clopos.com/docs/api-reference/v2/receipts/get-receipt-by-cid>

`GET /v2/receipts/cid/{cid}`

Retrieve a receipt by its cid UUID.

Terminals key receipts by a `cid` UUID, so integrations often hold that rather than the numeric id. Returns exactly the same payload as fetching by id.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/receipts/cid/{cid}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Access

| Requirement      | Value           |
| ---------------- | --------------- |
| Integrator scope | `receipts:read` |
| User ability     | `RECEIPT_VIEW`  |

The integration user must hold the ability as well as the scope — the scope alone is not enough.

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/receipts/cid/96ab5d26-d6bb-4976-a6f8-9e8806ef6aa5" \
  -H "x-token: oauth_example_token"
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/receipts/cid/96ab5d26-d6bb-4976-a6f8-9e8806ef6aa5', {
  headers: { 'x-token': 'oauth_example_token' }
});
const data = await response.json();
```

```python
import requests

response = requests.get(
    "https://integrations.clopos.com/open-api/v2/receipts/cid/96ab5d26-d6bb-4976-a6f8-9e8806ef6aa5",
    headers={"x-token": "oauth_example_token"},
)
data = response.json()
```

#### Notes

* The `cid` must be a well-formed UUID; anything else returns `400` without reaching the API.

### Get Receipt by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/receipts/get-receipt-by-id>

`GET /v2/receipts/{id}`

Retrieve the full details of a specific receipt

#### Purpose

Fetch the final state of a single receipt, including payment breakdowns and line items.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/receipts/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Path Parameters

| Parameter | Type   | Description                                           |
| --------- | ------ | ----------------------------------------------------- |
| `id`      | number | Unique identifier of the receipt you want to inspect. |

#### Query Parameters

- `` (string): 

    Include related resources in the response. Supported values:

    * `receipt_products` — line items on the receipt
    * `receipt_products.modificators` — modifiers applied to each line item

#### Request Example

```bash
# Basic request
curl --location "https://integrations.clopos.com/open-api/v2/receipts/1" \
  -H "x-token: oauth_example_token"

# With products and modifiers (note: --globoff to avoid shell globbing)
curl --location --globoff "https://integrations.clopos.com/open-api/v2/receipts/1?with[0]=receipt_products.product.unit&with[1]=receipt_products.product.station&with[2]=receipt_products.modificators.modificator_group" \
  -H "x-token: oauth_example_token"
```

```javascript
const receiptId = 1;
const headers = { 'x-token': 'oauth_example_token' };

// Basic request
const response = await fetch(
  `https://integrations.clopos.com/open-api/v2/receipts/${receiptId}`,
  { headers }
);
const receipt = await response.json();

// With products and modifiers
const params = new URLSearchParams({
  'with[0]': 'receipt_products.product.unit',
  'with[1]': 'receipt_products.product.station',
  'with[2]': 'receipt_products.modificators.modificator_group'
});

const responseWithProducts = await fetch(
  `https://integrations.clopos.com/open-api/v2/receipts/${receiptId}?${params}`,
  { headers }
);
const receiptWithProducts = await responseWithProducts.json();
```

```python
import requests

receipt_id = 1
url = f"https://integrations.clopos.com/open-api/v2/receipts/{receipt_id}"
headers = {
    "x-token": "oauth_example_token",
}

# Basic request
response = requests.get(url, headers=headers)
receipt = response.json()

# With products and modifiers
params = {
    "with[0]": "receipt_products.product.unit",
    "with[1]": "receipt_products.product.station",
    "with[2]": "receipt_products.modificators.modificator_group"
}

response = requests.get(url, headers=headers, params=params)
receipt_with_products = response.json()
```

#### Response

##### 200 OK — Receipt

```json
{
  "success": true,
  "data": {
    "id": 1,
    "venue_id": 1,
    "cid": "96ab5d26-d6bb-4976-a6f8-9e8806ef6aa5",
    "customer_id": null,
    "sale_type_id": 2,
    "source": "web",
    "guests": 1,
    "status": 2,
    "order_status": "IN_PROGRESS",
    "order_number": "006",
    "lock": false,
    "total": 30000,
    "subtotal": 30000,
    "discount_type": 0,
    "discount_value": 0,
    "discount_rate": 0,
    "total_discount": 0,
    "service_charge": 0,
    "service_charge_value": 0,
    "delivery_fee": 0,
    "remaining": 0,
    "i_tax": 0,
    "e_tax": 0,
    "total_tax": 0,
    "payment_methods": [
      {
        "id": 1,
        "name": "Cash",
        "amount": 30000
      }
    ],
    "fiscal_id": null,
    "loyalty_type": null,
    "loyalty_value": null,
    "address": null,
    "description": null,
    "created_at": "2026-01-19 14:51:33",
    "updated_at": "2026-01-19 15:07:49",
    "closed_at": "2026-01-19 15:07:49",
    "shift_date": "2026-01-19",
    "receipt_products": [
      {
        "id": 1,
        "cid": "0fd784b1-ee5a-4745-a130-a849b4e5db2f",
        "product_id": 51,
        "count": 1,
        "portion_size": 1,
        "total": 10,
        "price": 10,
        "subtotal": 10,
        "is_gift": false,
        "discount_type": 0,
        "discount_value": 0,
        "discount_rate": 0,
        "total_discount": 0,
        "receipt_discount": 0,
        "loyalty_type": null,
        "loyalty_value": null,
        "meta": {
          "product": {
            "name": "Test_Margherita Pizza",
            "type": "DISH",
            "price": 10,
            "barcode": null
          }
        },
        "modificators": [],
        "created_at": "2026-01-19 14:51:34",
        "updated_at": "2026-01-19 15:07:53"
      }
    ]
  }
}
```

##### 404 Not Found — Invalid ID

```json
{
  "success": false,
  "error": "not_found",
  "message": "Receipt not found"
}
```

#### Field Reference

##### Receipt object

| Field                  | Type         | Description                                                                                                       |
| ---------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------- |
| `id`                   | number       | Unique receipt identifier.                                                                                        |
| `cid`                  | string       | Client-generated UUID for the receipt.                                                                            |
| `venue_id`             | number       | Venue (location) the receipt belongs to.                                                                          |
| `customer_id`          | number\|null | Customer associated with the receipt.                                                                             |
| `sale_type_id`         | number       | Sale type identifier (e.g., dine-in, delivery).                                                                   |
| `source`               | string       | Origin of the receipt (e.g., `"web"`, `"pos"`).                                                                   |
| `guests`               | number       | Number of guests on the receipt.                                                                                  |
| `status`               | number       | Receipt status: `1` = open, `2` = closed.                                                                         |
| `order_status`         | string       | Order workflow status. One of: `NEW`, `SCHEDULED`, `IN_PROGRESS`, `READY`, `PICKED_UP`, `COMPLETED`, `CANCELLED`. |
| `order_number`         | string\|null | External or display order number.                                                                                 |
| `lock`                 | boolean      | Whether the receipt is locked from further changes.                                                               |
| `total`                | number       | Total amount collected.                                                                                           |
| `subtotal`             | number       | Subtotal before discounts, taxes, and fees.                                                                       |
| `discount_type`        | number       | Discount type applied (0 = none).                                                                                 |
| `discount_value`       | number       | Discount amount or percentage value.                                                                              |
| `discount_rate`        | number       | Effective discount rate.                                                                                          |
| `total_discount`       | number       | Total discount applied to the receipt.                                                                            |
| `service_charge`       | number       | Service charge percentage.                                                                                        |
| `service_charge_value` | number       | Calculated service charge amount.                                                                                 |
| `delivery_fee`         | number       | Delivery fee amount.                                                                                              |
| `remaining`            | number       | Outstanding balance (0 when fully paid).                                                                          |
| `i_tax`                | number       | Inclusive tax amount.                                                                                             |
| `e_tax`                | number       | Exclusive tax amount.                                                                                             |
| `total_tax`            | number       | Total tax amount (inclusive + exclusive).                                                                         |
| `payment_methods`      | array        | Payment breakdown. See [Payment method](https://developer.clopos.com/docs/common-objects#payment-method-in-receipts).                         |
| `fiscal_id`            | string\|null | Fiscal receipt identifier for tax reporting.                                                                      |
| `loyalty_type`         | string\|null | Loyalty program type applied.                                                                                     |
| `loyalty_value`        | number\|null | Loyalty discount or points value.                                                                                 |
| `address`              | string\|null | Delivery address.                                                                                                 |
| `description`          | string\|null | Delivery or order notes.                                                                                          |
| `created_at`           | string       | Receipt creation time (YYYY-MM-DD HH:mm:ss).                                                                      |
| `updated_at`           | string       | Last update time (YYYY-MM-DD HH:mm:ss).                                                                           |
| `closed_at`            | string\|null | Receipt close time (YYYY-MM-DD HH:mm:ss).                                                                         |
| `shift_date`           | string       | Business day the receipt belongs to (YYYY-MM-DD).                                                                 |

See [Payment method](https://developer.clopos.com/docs/common-objects#payment-method-in-receipts) for the `payment_methods[]` structure.

##### `receipt_products[]`

Included when `with[]=receipt_products` is passed. Each item represents one line on the receipt.

| Field                  | Type              | Description                                                                                                          |
| ---------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------- |
| `id`                   | integer           | Line item identifier.                                                                                                |
| `cid`                  | string            | Client-generated UUID for the line item.                                                                             |
| `product_id`           | integer           | Product ID from your catalog.                                                                                        |
| `count`                | integer           | Quantity ordered.                                                                                                    |
| `portion_size`         | integer           | Portion size multiplier (usually `1`).                                                                               |
| `total`                | number            | Line total after adjustments.                                                                                        |
| `price`                | number            | Unit price at the time of sale.                                                                                      |
| `subtotal`             | number            | Subtotal before receipt-level discounts.                                                                             |
| `is_gift`              | boolean           | Whether this item was given as a complimentary gift.                                                                 |
| `discount_type`        | integer           | Discount type on this line item (`0` = none).                                                                        |
| `discount_value`       | number            | Discount amount or percentage.                                                                                       |
| `discount_rate`        | number            | Effective discount rate.                                                                                             |
| `total_discount`       | number            | Total discount on this line item.                                                                                    |
| `receipt_discount`     | number            | Portion of the receipt-level discount allocated to this item.                                                        |
| `loyalty_type`         | string (nullable) | Loyalty program type applied to this item.                                                                           |
| `loyalty_value`        | number (nullable) | Loyalty points or discount value.                                                                                    |
| `meta.product.name`    | string            | Product name at the time of sale.                                                                                    |
| `meta.product.type`    | string            | Product type (`DISH`, `GOODS`, etc.).                                                                                |
| `meta.product.price`   | number            | Product's catalog price at the time of sale.                                                                         |
| `meta.product.barcode` | string (nullable) | Product barcode.                                                                                                     |
| `modificators`         | array             | Modifiers applied to this item. Included when `with[]=receipt_products.modificators` is passed. Empty array if none. |
| `created_at`           | string            | When the line item was added (`YYYY-MM-DD HH:mm:ss`).                                                                |
| `updated_at`           | string            | Last update time (`YYYY-MM-DD HH:mm:ss`).                                                                            |

#### Notes

* Closed receipts store the final totals; quantities and amounts cannot be edited through this endpoint.
* Use `receipt_products` for reconciliation with inventory or accounting systems.
* The response also includes `time`, `timestamp`, and `unix` fields for diagnostics; these are omitted from the example for brevity.
* Combine with the list endpoint when you need to cross-check totals before exporting reports.

### Get Receipt Stock Operations

Source: <https://developer.clopos.com/docs/api-reference/v2/receipts/get-receipt-stock-operations>

`GET /v2/receipts/{id}/stock-operations`

Retrieve the stock deductions ("Çıxarılan ehtiyat") generated by a receipt

#### Purpose

Fetch the stock write-offs caused by a single receipt — the inventory deducted from your storages when the receipt's products were sold. Use it to reconcile a sale against the warehouse movements it produced ("Çıxarılan ehtiyat" / stock deduction by receipt id).

Only the deductions of the receipt itself are returned: each item has `operation_id = null` and a non-null `receipt_product_id`. Manual stock corrections or operations from other documents are excluded.

This endpoint requires the `receipts:read` scope.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/receipts/{id}/stock-operations
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Path Parameters

| Parameter | Type   | Description                                                                  |
| --------- | ------ | ---------------------------------------------------------------------------- |
| `id`      | number | Unique identifier of the receipt whose stock deductions you want to inspect. |

#### Request Example

```bash
curl --location "https://integrations.clopos.com/open-api/v2/receipts/1/stock-operations" \
  -H "x-token: oauth_example_token"
```

```javascript
const receiptId = 1;
const headers = { 'x-token': 'oauth_example_token' };

const response = await fetch(
  `https://integrations.clopos.com/open-api/v2/receipts/${receiptId}/stock-operations`,
  { headers }
);
const stockOperations = await response.json();
```

```python
import requests

receipt_id = 1
url = f"https://integrations.clopos.com/open-api/v2/receipts/{receipt_id}/stock-operations"
headers = {
    "x-token": "oauth_example_token",
}

response = requests.get(url, headers=headers)
stock_operations = response.json()
```

#### Response

##### 200 OK — Stock operations

```json
{
  "data": [
    {
      "id": 1001,
      "receipt_id": 1,
      "receipt_product_id": 14,
      "product_id": 31042,
      "stock_id": 5001,
      "storage_id": 3,
      "quantity": 1,
      "before_quantity": 120,
      "after_quantity": 119,
      "cost": 8000,
      "before_cost": 8000,
      "total_cost": 8000,
      "operated_at": "2026-01-19 15:07:49",
      "product": {
        "id": 31042,
        "name": "Апельсинли реване"
      },
      "stock": {
        "id": 5001,
        "storage": {
          "id": 3,
          "name": "Main Storage"
        }
      }
    },
    {
      "id": 1002,
      "receipt_id": 1,
      "receipt_product_id": 15,
      "product_id": 31046,
      "stock_id": 5002,
      "storage_id": 3,
      "quantity": 2,
      "before_quantity": 50,
      "after_quantity": 48,
      "cost": 1500,
      "before_cost": 1500,
      "total_cost": 3000,
      "operated_at": "2026-01-19 15:07:49",
      "product": {
        "id": 31046,
        "name": "Ачма узум жевиз"
      },
      "stock": {
        "id": 5002,
        "storage": {
          "id": 3,
          "name": "Main Storage"
        }
      }
    }
  ]
}
```

##### 404 Not Found — Invalid ID

```json
{
  "success": false,
  "error": "not_found",
  "message": "Receipt not found"
}
```

#### Field Reference

##### Stock operation object

| Field                | Type   | Description                                                                           |
| -------------------- | ------ | ------------------------------------------------------------------------------------- |
| `id`                 | number | Stock operation identifier.                                                           |
| `receipt_id`         | number | Receipt the operation belongs to.                                                     |
| `receipt_product_id` | number | Receipt product line that produced the write-off (always set for receipt deductions). |
| `product_id`         | number | Product whose stock was deducted.                                                     |
| `stock_id`           | number | Stock record affected by the operation.                                               |
| `storage_id`         | number | Storage the stock belongs to.                                                         |
| `quantity`           | number | Quantity deducted from stock.                                                         |
| `before_quantity`    | number | Stock quantity before the operation.                                                  |
| `after_quantity`     | number | Stock quantity after the operation.                                                   |
| `cost`               | number | Unit cost applied to the deduction.                                                   |
| `before_cost`        | number | Stock cost before the operation.                                                      |
| `total_cost`         | number | Total cost of the deducted quantity.                                                  |
| `operated_at`        | string | When the operation was applied (YYYY-MM-DD HH:mm:ss).                                 |
| `product`            | object | Related product. Present even when the product was soft-deleted.                      |
| `stock`              | object | Affected stock together with its storage.                                             |

##### `stock`

| Field     | Type   | Description                                  |
| --------- | ------ | -------------------------------------------- |
| `id`      | number | Stock identifier.                            |
| `storage` | object | Storage the stock belongs to (`id`, `name`). |

#### Notes

* The endpoint returns only the receipt's own deductions (`operation_id = null`, `receipt_product_id != null`); inventory adjustments from other documents are not included.
* A `product` may be soft-deleted but is still returned so historical receipts remain fully reconcilable.
* Combine with [Get Receipt by ID](https://developer.clopos.com/docs/api-reference/v2/receipts/get-receipt-by-id) to map each `receipt_product_id` back to its sold line item.

### List Receipts

Source: <https://developer.clopos.com/docs/api-reference/v2/receipts/get-receipts>

`GET /v2/receipts`

Retrieve all receipts with support for filters and sorting

#### Purpose

Speeds up your reconciliation flows by listing sales receipts by date, amount, or status.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/receipts
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Query Parameters

- `` (integer): Page number for pagination (1-based).

- `` (integer): Number of receipts per page.

- `` (string): Start date of a `created_at` range, inclusive. Format: `YYYY-MM-DD`. Pair with `date[1]`.

- `` (string): End date of a `created_at` range, inclusive. Format: `YYYY-MM-DD`.

- `` (string): Field to sort by (e.g. `created_at`, `updated_at`, `closed_at`, `total`). Inspect the `sorts` array in the response to discover all sortable fields the API currently supports.

- `` (integer): Sort direction: `1` = ascending, `-1` = descending.

- `` (array[string]): 

    Related resources to include in each receipt. Repeat with indexed brackets (e.g. `with[0]=receipt_products&with[1]=receipt_products.modificators`). Common values:

    * `receipt_products` — line items on each receipt
    * `receipt_products.modificators` — modifiers applied to each line item
    * `receipt_products.product.unit`, `receipt_products.product.station` — product relations

- `` (array): Field-level filter tuples using PHP bracket notation: `filters[N][0]=field_name&filters[N][1]=value`. Stack filters by incrementing `N` (0-based). Commonly used with `status`, `sale_type_id`, `terminal_id`.

#### Request Example

```bash
# Basic request with filters
curl --location --globoff "https://integrations.clopos.com/open-api/v2/receipts?page=1&sort[0]=created_at&sort[1]=-1&limit=50&date[0]=2026-01-19&date[1]=2026-01-19" \
  -H "x-token: oauth_example_token"

# With products and modifiers
curl --location --globoff "https://integrations.clopos.com/open-api/v2/receipts?page=1&sort[0]=created_at&sort[1]=-1&limit=50&date[0]=2026-01-19&date[1]=2026-01-19&with[0]=receipt_products.product.unit&with[1]=receipt_products.product.station&with[2]=receipt_products.modificators.modificator_group" \
  -H "x-token: oauth_example_token"
```

```javascript
const headers = { 'x-token': 'oauth_example_token' };

// Basic request with filters
const params = new URLSearchParams({
  'page': '1',
  'sort[0]': 'created_at',
  'sort[1]': '-1',
  'limit': '50',
  'date[0]': '2026-01-19',
  'date[1]': '2026-01-19'
});

const response = await fetch(
  `https://integrations.clopos.com/open-api/v2/receipts?${params}`,
  { headers }
);
const receipts = await response.json();

// With products and modifiers
const paramsWithProducts = new URLSearchParams({
  'page': '1',
  'sort[0]': 'created_at',
  'sort[1]': '-1',
  'limit': '50',
  'date[0]': '2025-08-12',
  'date[1]': '2025-08-18',
  'with[0]': 'receipt_products.product.unit',
  'with[1]': 'receipt_products.product.station',
  'with[2]': 'receipt_products.modificators.modificator_group'
});

const responseWithProducts = await fetch(
  `https://integrations.clopos.com/open-api/v2/receipts?${paramsWithProducts}`,
  { headers }
);
const receiptsWithProducts = await responseWithProducts.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/receipts"
headers = {
    "x-token": "oauth_example_token",
}

# Basic request with filters
params = {
    "page": 1,
    "sort[0]": "created_at",
    "sort[1]": -1,
    "limit": 50,
    "date[0]": "2026-01-19",
    "date[1]": "2026-01-19"
}

response = requests.get(url, headers=headers, params=params)
receipts = response.json()

# With products and modifiers
params_with_products = {
    "page": 1,
    "sort[0]": "created_at",
    "sort[1]": -1,
    "limit": 50,
    "date[0]": "2025-08-12",
    "date[1]": "2025-08-18",
    "with[0]": "receipt_products.product.unit",
    "with[1]": "receipt_products.product.station",
    "with[2]": "receipt_products.modificators.modificator_group"
}

response = requests.get(url, headers=headers, params=params_with_products)
receipts_with_products = response.json()
```

#### Response

##### 200 OK — List of receipts

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "venue_id": 1,
      "cid": "96ab5d26-d6bb-4976-a6f8-9e8806ef6aa5",
      "customer_id": null,
      "sale_type_id": 2,
      "source": "web",
      "guests": 1,
      "status": 2,
      "order_status": "IN_PROGRESS",
      "order_number": "006",
      "lock": false,
      "total": 33000,
      "subtotal": 33000,
      "discount_type": 0,
      "discount_value": 0,
      "discount_rate": 0,
      "total_discount": 0,
      "service_charge": 0,
      "service_charge_value": 0,
      "delivery_fee": 0,
      "remaining": 0,
      "i_tax": 0,
      "e_tax": 0,
      "total_tax": 0,
      "payment_methods": [
        {
          "id": 1,
          "name": "Cash",
          "amount": 33000
        }
      ],
      "fiscal_id": null,
      "loyalty_type": null,
      "loyalty_value": null,
      "address": null,
      "description": null,
      "created_at": "2026-01-19 14:51:33",
      "updated_at": "2026-01-19 15:07:49",
      "closed_at": "2026-01-19 15:07:49",
      "shift_date": "2026-01-19"
    }
  ],
  "total": 1
}
```

##### 400 Bad Request — Parameter error

```json
{
  "success": false,
  "error": "invalid_parameter",
  "message": "sort[1] must be 1 or -1"
}
```

##### 401 Unauthorized — Missing header

```json
{
  "success": false,
  "error": "unauthorized",
  "message": "Missing authentication headers"
}
```

#### Field Reference

##### Receipt object

| Field                  | Type         | Description                                                                                                       |
| ---------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------- |
| `id`                   | number       | Unique receipt identifier.                                                                                        |
| `cid`                  | string       | Client-generated UUID for the receipt.                                                                            |
| `venue_id`             | number       | Venue (location) the receipt belongs to.                                                                          |
| `customer_id`          | number\|null | Customer associated with the receipt.                                                                             |
| `sale_type_id`         | number       | Sale type identifier (e.g., dine-in, delivery).                                                                   |
| `source`               | string       | Origin of the receipt (e.g., `"web"`, `"pos"`).                                                                   |
| `guests`               | number       | Number of guests on the receipt.                                                                                  |
| `status`               | number       | Receipt status: `1` = open, `2` = closed.                                                                         |
| `order_status`         | string       | Order workflow status. One of: `NEW`, `SCHEDULED`, `IN_PROGRESS`, `READY`, `PICKED_UP`, `COMPLETED`, `CANCELLED`. |
| `order_number`         | string\|null | External or display order number.                                                                                 |
| `lock`                 | boolean      | Whether the receipt is locked from further changes.                                                               |
| `total`                | number       | Total amount collected.                                                                                           |
| `subtotal`             | number       | Subtotal before discounts, taxes, and fees.                                                                       |
| `discount_type`        | number       | Discount type applied (0 = none).                                                                                 |
| `discount_value`       | number       | Discount amount or percentage value.                                                                              |
| `discount_rate`        | number       | Effective discount rate.                                                                                          |
| `total_discount`       | number       | Total discount applied to the receipt.                                                                            |
| `service_charge`       | number       | Service charge percentage.                                                                                        |
| `service_charge_value` | number       | Calculated service charge amount.                                                                                 |
| `delivery_fee`         | number       | Delivery fee amount.                                                                                              |
| `remaining`            | number       | Outstanding balance (0 when fully paid).                                                                          |
| `i_tax`                | number       | Inclusive tax amount.                                                                                             |
| `e_tax`                | number       | Exclusive tax amount.                                                                                             |
| `total_tax`            | number       | Total tax amount (inclusive + exclusive).                                                                         |
| `payment_methods`      | array        | Payment breakdown. See [Payment method](https://developer.clopos.com/docs/common-objects#payment-method-in-receipts).                         |
| `fiscal_id`            | string\|null | Fiscal receipt identifier for tax reporting.                                                                      |
| `loyalty_type`         | string\|null | Loyalty program type applied.                                                                                     |
| `loyalty_value`        | number\|null | Loyalty discount or points value.                                                                                 |
| `address`              | string\|null | Delivery address.                                                                                                 |
| `description`          | string\|null | Delivery or order notes.                                                                                          |
| `created_at`           | string       | Receipt creation time (YYYY-MM-DD HH:mm:ss).                                                                      |
| `updated_at`           | string       | Last update time (YYYY-MM-DD HH:mm:ss).                                                                           |
| `closed_at`            | string\|null | Receipt close time (YYYY-MM-DD HH:mm:ss).                                                                         |
| `shift_date`           | string       | Business day the receipt belongs to (YYYY-MM-DD).                                                                 |

See [Payment method](https://developer.clopos.com/docs/common-objects#payment-method-in-receipts) for the `payment_methods[]` structure.

#### Notes

* Use the `date[0]` and `date[1]` filters to restrict receipts to a date range (inclusive, YYYY-MM-DD).
* Sorting accepts multiple fields (`sort[0]`, `sort[1]`, etc.); directions must be `1` (ascending) or `-1` (descending).
* Pagination uses classic `page` and `limit` semantics; the default `limit` is 50.
* Combine `status`, `sale_type_id`, and date filters via the OpenAPI explorer when you need more granular reporting.
* The response also includes `time`, `timestamp`, `unix`, and `sorts` fields for diagnostics and discovering sortable fields; these are omitted from examples for brevity.

### Update Receipt (after close)

Source: <https://developer.clopos.com/docs/api-reference/v2/receipts/patch-update-receipt>

`PATCH /v2/receipts/{id}`

Update specific fields of an existing receipt

#### Purpose

Update specific fields of a receipt using the PATCH method. Only the provided fields will be updated; all other fields remain unchanged.

**Important Notes:**

* The PATCH method can update receipts even after they are closed (when `closed_at` is not null).
* Only limited fields can be updated via PATCH (see the field list below).

#### HTTP Request

```http
PATCH https://integrations.clopos.com/open-api/v2/receipts/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Path Parameters

| Parameter | Type   | Description                                 |
| --------- | ------ | ------------------------------------------- |
| `id`      | number | Unique identifier of the receipt to update. |

#### Request Body

Only the fields you want to update need to be included in the request body. Available updateable fields:

| Field          | Type    | Description                                                                                                                  |
| -------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `order_status` | string  | Order status. Valid values: `"NEW"`, `"SCHEDULED"`, `"IN_PROGRESS"`, `"READY"`, `"PICKED_UP"`, `"COMPLETED"`, `"CANCELLED"`. |
| `order_number` | string  | Order number identifier (e.g., `"RPO-00001"`).                                                                               |
| `fiscal_id`    | string  | Fiscal receipt identifier.                                                                                                   |
| `lock`         | boolean | Lock status of the receipt (`true` or `false`).                                                                              |

#### Request Example

```bash
curl --location --request PATCH 'https://integrations.clopos.com/open-api/v2/receipts/1' \
  --header 'Content-Type: application/json' \
  --header 'x-token: oauth_example_token' \
  --data '{
    "order_status": "NEW",
    "order_number": "RPO-00001",
    "fiscal_id": "Twrewr89fnscvj22",
    "lock": false
}'
```

```javascript
const receiptId = 1;

const response = await fetch(`https://integrations.clopos.com/open-api/v2/receipts/${receiptId}`, {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
    'x-token': 'oauth_example_token',
  },
  body: JSON.stringify({
    order_status: 'NEW',
    order_number: 'RPO-00001',
    fiscal_id: 'Twrewr89fnscvj22',
    lock: false
  })
});

const receipt = await response.json();
```

```python
import requests

receipt_id = 1
url = f"https://integrations.clopos.com/open-api/v2/receipts/{receipt_id}"
headers = {
    "Content-Type": "application/json",
    "x-token": "oauth_example_token",
}
payload = {
    "order_status": "NEW",
    "order_number": "RPO-00001",
    "fiscal_id": "Twrewr89fnscvj22",
    "lock": False
}

response = requests.patch(url, headers=headers, json=payload)
receipt = response.json()
```

#### Response

##### 200 OK — Receipt Updated

The response returns the full receipt data with updated fields:

```json
{
  "success": true,
  "data": {
    "id": 1,
    "venue_id": 1,
    "cid": "96ab5d26-d6bb-4976-a6f8-9e8806ef6aa5",
    "customer_id": null,
    "sale_type_id": 2,
    "source": "web",
    "guests": 1,
    "status": 2,
    "order_status": "NEW",
    "order_number": "RPO-00001",
    "lock": false,
    "total": 30000,
    "subtotal": 30000,
    "discount_type": 0,
    "discount_value": 0,
    "discount_rate": 0,
    "total_discount": 0,
    "service_charge": 0,
    "service_charge_value": 0,
    "delivery_fee": 0,
    "remaining": 0,
    "i_tax": 0,
    "e_tax": 0,
    "total_tax": 0,
    "payment_methods": [
      {
        "id": 1,
        "name": "Cash",
        "amount": 30000
      }
    ],
    "fiscal_id": "Twrewr89fnscvj22",
    "loyalty_type": null,
    "loyalty_value": null,
    "address": null,
    "description": null,
    "created_at": "2026-01-19 14:51:33",
    "updated_at": "2026-01-20 12:43:07",
    "closed_at": "2026-01-19 15:07:49",
    "shift_date": "2026-01-19"
  },
  "message": "Operation completed successfully"
}
```

##### 404 Not Found — Receipt Not Found

```json
{
  "success": false,
  "error": "not_found",
  "message": "Receipt not found"
}
```

##### 400 Bad Request — Validation Error

```json
{
  "success": false,
  "error": "validation_failed",
  "message": "Invalid field values provided"
}
```

#### Field Reference

##### Updateable Fields

| Field          | Type    | Description                                                                                                                          |
| -------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `order_status` | string  | Current order status. Valid values: `"NEW"`, `"SCHEDULED"`, `"IN_PROGRESS"`, `"READY"`, `"PICKED_UP"`, `"COMPLETED"`, `"CANCELLED"`. |
| `order_number` | string  | External order number or identifier.                                                                                                 |
| `fiscal_id`    | string  | Fiscal receipt identifier used for tax reporting.                                                                                    |
| `lock`         | boolean | If `true`, locks the receipt to prevent further modifications.                                                                       |

#### Notes

* Only the fields provided in the request body will be updated; all other fields remain unchanged.
* The response includes the complete receipt object with all integrator-relevant fields, not just the updated ones.
* Only the specified fields (`order_status`, `order_number`, `fiscal_id`, `lock`) can be updated through this endpoint.
* Other receipt fields are read-only and cannot be modified via this API.
* This method can update receipts even after they are closed (when `closed_at` is not null).
* The response also includes `time`, `timestamp`, and `unix` fields for diagnostics; these are omitted from the example for brevity.

## Sales

### List Payment Methods

Source: <https://developer.clopos.com/docs/api-reference/v2/sales/get-payment-methods>

`GET /v2/payment-methods`

Retrieve a list of all configured payment methods.

This endpoint retrieves a list of all configured payment methods.

Payment methods represent tender types (e.g., cash, card, wallet). They are used when closing receipts and reconciling totals.

!!! note
    The `status` object is a venue map. Its keys are `venue_id` strings and the
    values indicate enablement at that venue: `1` = enabled, `0` = disabled.
    For example, `status["1"] = 1` means this payment method is enabled for
    venue `1`.

**Used by**

* [Close Receipt](https://developer.clopos.com/docs/api-reference/v2/receipts/close-receipt): map each tender to `payment_methods[]`

#### Response Example

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Cash",
      "status": {
        "1": 1,
        "2": 1,
        "3": 1
      },
      "split": 1,
      "position": 0,
      "customer_required": 0,
      "is_system": 0,
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T10:22:12.000000Z",
      "balance": {
        "id": 1,
        "system_type": "CASH",
        "name": "Kassa",
        "type": "CASH"
      },
      "service": null
    },
    {
      "id": 2,
      "name": "Card",
      "status": {
        "1": 1,
        "2": 1,
        "3": 1
      },
      "split": 1,
      "position": 0,
      "customer_required": 0,
      "is_system": 0,
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T10:22:12.000000Z",
      "balance": {
        "id": 2,
        "system_type": "CARD",
        "name": "Kart",
        "type": "CARD"
      },
      "service": null
    },
    {
      "id": 3,
      "name": "Customer Balance",
      "status": {
        "1": 0,
        "2": 1,
        "3": 1
      },
      "split": 1,
      "position": 0,
      "customer_required": 1,
      "is_system": 0,
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T10:22:12.000000Z",
      "balance": null,
      "service": null
    },
    {
      "id": 4,
      "name": "Cashback",
      "status": {
        "1": 0,
        "2": 0,
        "3": 0
      },
      "split": 1,
      "position": 0,
      "customer_required": 1,
      "is_system": 0,
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T10:22:12.000000Z",
      "balance": null,
      "service": {
        "name": "loyalty",
        "check": [],
        "payload": []
      }
    }
  ],
  "total": 4
}
```

#### Field Reference

##### Payment Method Object

| Field               | Type              | Description                                                                                    |
| ------------------- | ----------------- | ---------------------------------------------------------------------------------------------- |
| `id`                | integer           | Unique identifier for the payment method.                                                      |
| `name`              | string            | Display name of the payment method (e.g., "Cash", "Card").                                     |
| `status`            | object            | Map of `venue_id` (string) to `0`/`1` indicating whether this method is enabled at each venue. |
| `split`             | integer           | `1` if this payment method can be used for split payments, `0` otherwise.                      |
| `position`          | integer           | Display order position.                                                                        |
| `customer_required` | integer           | `1` if a customer must be attached to the transaction, `0` otherwise.                          |
| `is_system`         | integer           | `1` if this is a system-default payment method, `0` otherwise.                                 |
| `created_at`        | string            | Creation timestamp (ISO 8601).                                                                 |
| `updated_at`        | string            | Last update timestamp (ISO 8601).                                                              |
| `balance`           | object (nullable) | Associated balance account, or `null` if none. See Balance object.                             |
| `service`           | object (nullable) | External service integrated with this payment method (e.g., loyalty), or `null`.               |

##### Balance Object (nested in `balance`)

| Field         | Type    | Description                                        |
| ------------- | ------- | -------------------------------------------------- |
| `id`          | integer | Balance account identifier.                        |
| `system_type` | string  | System type of the balance (e.g., `CASH`, `CARD`). |
| `name`        | string  | Display name of the balance account.               |
| `type`        | string  | Balance type (e.g., `CASH`, `CARD`).               |

### List Sale Types

Source: <https://developer.clopos.com/docs/api-reference/v2/sales/get-sale-types>

`GET /v2/sale-types`

Retrieve a list of all available sale types.

This endpoint retrieves a list of all available sale types, such as In-store, Delivery, and Takeaway.

Sale types represent the fulfillment channel for an order (e.g., dine-in, delivery, takeaway) and may determine service charge behavior.

!!! note
    The `status` object is a venue map. Its keys are `venue_id` strings and the
    values indicate enablement at that venue: `1` = enabled, `0` = disabled.
    For example, `status["1"] = 1` means this sale type is enabled for
    venue `1`.

**Used by**

* [Create Order](https://developer.clopos.com/docs/api-reference/v2/orders/create-order): provide `payload.service.sale_type_id` and `payload.service.venue_id`

#### Response Example

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Yerinde",
      "system_type": "IN",
      "channel": "IN",
      "status": {
        "1": 1,
        "2": 1,
        "3": 1
      },
      "service_charge_rate": null,
      "position": 0,
      "media": [],
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T10:22:12.000000Z"
    },
    {
      "id": 2,
      "name": "Catdirilma",
      "system_type": "DELIVERY",
      "channel": "DELIVERY",
      "status": {
        "1": 1,
        "2": 1,
        "3": 1
      },
      "service_charge_rate": null,
      "position": 0,
      "media": [
        {
          "urls": {
            "original": "https://cdn.clopos.com/_clopos/delivery.png",
            "large": "https://cdn.clopos.com/_clopos/delivery.png"
          }
        }
      ],
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T10:22:12.000000Z"
    },
    {
      "id": 3,
      "name": "Takeaway",
      "system_type": "TAKEAWAY",
      "channel": "TAKEAWAY",
      "status": {
        "1": 1,
        "2": 1,
        "3": 1
      },
      "service_charge_rate": null,
      "position": 0,
      "media": [
        {
          "urls": {
            "original": "https://cdn.clopos.com/_clopos/takeaway.png",
            "large": "https://cdn.clopos.com/_clopos/takeaway.png"
          }
        }
      ],
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T10:22:12.000000Z"
    }
  ],
  "total": 3
}
```

#### Field Reference

##### Sale Type Object

| Field                 | Type              | Description                                                                                       |
| --------------------- | ----------------- | ------------------------------------------------------------------------------------------------- |
| `id`                  | integer           | Unique identifier for the sale type.                                                              |
| `name`                | string            | Display name of the sale type (e.g., "In-store", "Delivery").                                     |
| `system_type`         | string            | System-defined type identifier: `IN`, `DELIVERY`, `TAKEAWAY`.                                     |
| `channel`             | string            | Sales channel this type belongs to.                                                               |
| `status`              | object            | Map of `venue_id` (string) to `0`/`1` indicating whether this sale type is enabled at each venue. |
| `service_charge_rate` | number (nullable) | Service charge rate associated with this sale type, or `null` if none.                            |
| `position`            | integer           | Display order position.                                                                           |
| `media`               | array             | Image attachments. See [Media object](https://developer.clopos.com/docs/common-objects#media).                                |
| `created_at`          | string            | Creation timestamp (ISO 8601).                                                                    |
| `updated_at`          | string            | Last update timestamp (ISO 8601).                                                                 |

## Stations

### Get Station by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/stations/get-station-by-id>

`GET /v2/stations/{id}`

Retrieve a specific preparation or service station

#### Purpose

Verifies the status and printing capabilities of a single station, such as a kitchen, bar, or custom station.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stations/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Request Example

```bash
curl -X GET "https://integrations.clopos.com/open-api/v2/stations/1" \
  -H "x-token: oauth_example_token" \
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stations/1', {
  headers: {
    'x-token': 'oauth_example_token',
  }
});

const station = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/stations/1"
headers = {
    "x-token": "oauth_example_token",
}

response = requests.get(url, headers=headers)
station = response.json()
```

#### Response

##### 200 OK — Station found

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Kitchen",
    "status": 1,
    "type": 1,
    "printable": 1,
    "created_at": "2026-01-13T14:08:49.000000Z",
    "updated_at": "2026-01-13T14:08:49.000000Z"
  }
}
```

##### 404 Not Found — Station does not exist

```json
{
  "success": false,
  "error": "resource_not_found",
  "message": "Station not found"
}
```

#### Field Reference

##### Station object

| Field        | Type    | Description                                          |
| ------------ | ------- | ---------------------------------------------------- |
| `id`         | integer | Station identifier.                                  |
| `name`       | string  | Station name.                                        |
| `status`     | integer | `1` = active, `0` = inactive.                        |
| `type`       | integer | Station type. `1` = kitchen, `0` = other.            |
| `printable`  | integer | `1` if the station can print tickets, `0` otherwise. |
| `created_at` | string  | Creation timestamp (ISO 8601).                       |
| `updated_at` | string  | Last update timestamp (ISO 8601).                    |

#### Notes

* The station ID is used for product and printer mapping on the POS side; verify the current restaurant flow before making changes.
* Stations with `printable=0` are designed only for screen notifications or digital preparation processes.
* If a station is not found, it returns `404`; selecting a fallback station on the client side or showing a remapping screen to the user provides a good experience.

### List Stations

Source: <https://developer.clopos.com/docs/api-reference/v2/stations/get-stations>

`GET /v2/stations`

Retrieve all preparation and service stations

#### Purpose

Allows you to check printer, reminder, and status information by retrieving all stations in your POS and kitchen flows in a single call.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/stations
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Query Parameters

- `` (integer): Filter by station status (`1` = active, `0` = inactive).

- `` (boolean): Filter stations that can redirect to a printer.

- `` (integer): Page number for pagination.

- `` (integer): Number of stations to return (1-200).

#### Request Example

```bash
curl -X GET "https://integrations.clopos.com/open-api/v2/stations?status=1" \
  -H "x-token: oauth_example_token" \
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/stations?status=1', {
  headers: {
    'x-token': 'oauth_example_token',
  }
});

const stations = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/stations"
headers = {
    "x-token": "oauth_example_token",
}
params = {
    "status": 1,
    "limit": 50
}

response = requests.get(url, headers=headers, params=params)
stations = response.json()
```

#### Response

##### 200 OK — List of stations

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Kitchen",
      "status": 1,
      "type": 1,
      "printable": 1,
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T14:08:49.000000Z"
    },
    {
      "id": 2,
      "name": "Bar",
      "status": 1,
      "type": 0,
      "printable": 1,
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-01-13T14:08:49.000000Z"
    },
    {
      "id": 3,
      "name": "Tandir",
      "status": 1,
      "type": 0,
      "printable": 0,
      "created_at": "2026-01-13T14:36:51.000000Z",
      "updated_at": "2026-01-13T14:36:51.000000Z"
    }
  ],
  "total": 3
}
```

##### 401 Unauthorized — Authorization missing

```json
{
  "success": false,
  "error": "unauthorized",
  "message": "Missing authentication headers"
}
```

#### Field Reference

##### Station object

| Field        | Type    | Description                                          |
| ------------ | ------- | ---------------------------------------------------- |
| `id`         | integer | Station identifier.                                  |
| `name`       | string  | Station name.                                        |
| `status`     | integer | `1` = active, `0` = inactive.                        |
| `type`       | integer | Station type. `1` = kitchen, `0` = other.            |
| `printable`  | integer | `1` if the station can print tickets, `0` otherwise. |
| `created_at` | string  | Creation timestamp (ISO 8601).                       |
| `updated_at` | string  | Last update timestamp (ISO 8601).                    |

#### Notes

* Stations with `printable=0` are designed only for screen notifications or digital preparation processes.
* The active/inactive status of stations affects product routing on the POS side; inactive stations are not assigned to new orders.
* Adjust pagination parameters (`page`, `limit`) for performance in large restaurant chains; it is generally not necessary for a single branch.

## Users

### Get User by ID

Source: <https://developer.clopos.com/docs/api-reference/v2/users/get-user-by-id>

`GET /v2/users/{id}`

Retrieve a specific user by their unique identifier.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/users/{id}
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Path Parameters

- `` (integer): The unique identifier of the user.

#### Request Example

```bash
curl --location 'https://integrations.clopos.com/open-api/v2/users/1' \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json'
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/users/1', {
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
});
```

```python
import requests

url = 'https://integrations.clopos.com/open-api/v2/users/1'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

response = requests.get(url, headers=headers)
print(response.json())
```

#### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "vitrin@clopos.com",
    "username": "Clopos Test",
    "first_name": "Clopos",
    "last_name": "Test",
    "mobile_number": null,
    "owner": 1,
    "status": true,
    "created_at": "2026-01-13T14:08:48.000000Z",
    "updated_at": "2026-02-20T15:07:02.000000Z"
  }
}
```

***

#### Field Reference

##### User Object

| Field           | Type              | Description                                          |
| --------------- | ----------------- | ---------------------------------------------------- |
| `id`            | integer           | Unique user identifier.                              |
| `email`         | string (nullable) | Email address associated with the user.              |
| `username`      | string            | Display name shown in the POS.                       |
| `first_name`    | string (nullable) | First name of the user.                              |
| `last_name`     | string (nullable) | Last name of the user.                               |
| `mobile_number` | string (nullable) | Mobile phone number.                                 |
| `owner`         | integer           | `1` if the user owns the brand, otherwise `0`.       |
| `status`        | boolean           | Indicates whether the user account is active.        |
| `created_at`    | string            | Timestamp when the user was created (ISO 8601).      |
| `updated_at`    | string            | Timestamp when the user was last updated (ISO 8601). |

### List Users

Source: <https://developer.clopos.com/docs/api-reference/v2/users/get-users>

`GET /v2/users`

Retrieve a list of active Clopos users

Use this endpoint to inspect staff accounts, roles, and access levels across your venues.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/users
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Request Example

```bash
curl --location 'https://integrations.clopos.com/open-api/v2/users' \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json'
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/users', {
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
});
```

```python
import requests

url = 'https://integrations.clopos.com/open-api/v2/users'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

response = requests.get(url, headers=headers)
print(response.json())
```

#### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "email": "vitrin@clopos.com",
      "username": "Clopos Test",
      "first_name": "Clopos",
      "last_name": "Test",
      "mobile_number": null,
      "owner": 1,
      "status": true,
      "created_at": "2026-01-13T14:08:48.000000Z",
      "updated_at": "2026-02-20T15:07:02.000000Z"
    },
    {
      "id": 3,
      "email": null,
      "username": "Cashier",
      "first_name": null,
      "last_name": null,
      "mobile_number": null,
      "owner": 0,
      "status": true,
      "created_at": "2026-01-13T14:08:49.000000Z",
      "updated_at": "2026-03-12T16:32:36.000000Z"
    }
  ],
  "total": 3
}
```

***

#### Field Reference

##### User Object

| Field           | Type              | Description                                          |
| --------------- | ----------------- | ---------------------------------------------------- |
| `id`            | integer           | Unique user identifier.                              |
| `email`         | string (nullable) | Email address associated with the user.              |
| `username`      | string            | Display name shown in the POS.                       |
| `first_name`    | string (nullable) | First name of the user.                              |
| `last_name`     | string (nullable) | Last name of the user.                               |
| `mobile_number` | string (nullable) | Mobile phone number.                                 |
| `owner`         | integer           | `1` if the user owns the brand, otherwise `0`.       |
| `status`        | boolean           | Indicates whether the user account is active.        |
| `created_at`    | string            | Timestamp when the user was created (ISO 8601).      |
| `updated_at`    | string            | Timestamp when the user was last updated (ISO 8601). |

## Venues

### List Venues

Source: <https://developer.clopos.com/docs/api-reference/v2/venues/get-venues>

`GET /v2/venues`

Retrieve a list of all venues (locations).

#### Purpose

Allows you to quickly retrieve active branches connected to your brand to initiate location-based operations.

#### HTTP Request

```http
GET https://integrations.clopos.com/open-api/v2/venues
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Request Example

```bash
curl -X GET "https://integrations.clopos.com/open-api/v2/venues" \
  -H "x-token: oauth_example_token" \
```

```javascript
const response = await fetch('https://integrations.clopos.com/open-api/v2/venues', {
  headers: {
    'x-token': 'oauth_example_token',
  }
});

const venues = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/venues"
headers = {
    "x-token": "oauth_example_token",
}

response = requests.get(url, headers=headers)
venues = response.json()
```

#### Response

##### 200 OK — List of branches

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Main",
      "is_main": 1,
      "media": []
    },
    {
      "id": 2,
      "name": "Baku",
      "is_main": 0,
      "media": []
    },
    {
      "id": 3,
      "name": "Masally",
      "is_main": 0,
      "media": []
    }
  ]
}
```

##### 401 Unauthorized — Missing header

```json
{
  "success": false,
  "error": "unauthorized",
  "message": "Missing authentication headers"
}
```

#### Field Reference

##### Branch object

| Field     | Type    | Description                                                        |
| --------- | ------- | ------------------------------------------------------------------ |
| `id`      | integer | Branch ID.                                                         |
| `name`    | string  | Branch name.                                                       |
| `is_main` | integer | `1` if this is the primary branch, `0` otherwise.                  |
| `media`   | array   | Image attachments. See [Media object](https://developer.clopos.com/docs/common-objects#media). |

#### Notes

* This endpoint returns all branches you have access to; use client-side logic to filter the result set.
* Use `is_main` to identify the primary branch in multi-location setups.
* Although the response size is small, client-side caching is recommended for large brands.

## Waiter Call

### Waiter Call

Source: <https://developer.clopos.com/docs/api-reference/v2/waiter-call/waiter-call>

`POST /v2/waiter-call`

Trigger a waiter call or a payment request for a table

#### Purpose

Allows integrators to notify restaurant staff at a specific table — either to request a waiter or to initiate a payment with a chosen payment method.

#### HTTP Request

```http
POST https://integrations.clopos.com/open-api/v2/waiter-call
```

!!! warning
    This endpoint requires authentication. Include your JWT in the `x-token` header. See [Authentication](https://developer.clopos.com/docs/authentication) for how to obtain a token and [Errors](https://developer.clopos.com/docs/errors) for error responses.

#### Module Requirement

!!! warning
    This endpoint requires the `restaurant_emenu` module to be enabled for your brand. Requests made without this module active will return the standard "module not available" error.

#### Request Body

- `` (integer): The ID of the table for which the call is being triggered. Must correspond to an existing table in the venue.

- `` (string): 

    The type of call to trigger. Accepted values:

    * `WAITER` — notify staff that a waiter is needed at the table
    * `PAY` — request payment for the table

- `` (integer): 

    The payment method ID to use when `type` is `PAY`. Must be the default **CASH** or **CARD** payment method configured for the venue.

    
!!! note
    `payment_method` is required when `type` is `PAY` and must not be sent for `type` `WAITER`.

#### Request Example

```bash
curl --location 'https://integrations.clopos.com/open-api/v2/waiter-call' \
  -H 'x-token: oauth_example_token' \
  -H 'Content-Type: application/json' \
  -d '{
        "table_id": 5,
        "type": "WAITER"
      }'
```

```bash
curl --location 'https://integrations.clopos.com/open-api/v2/waiter-call' \
  -H 'x-token: oauth_example_token' \
  -H 'Content-Type: application/json' \
  -d '{
        "table_id": 5,
        "type": "PAY",
        "payment_method": 1
      }'
```

```javascript
// WAITER call
const response = await fetch('https://integrations.clopos.com/open-api/v2/waiter-call', {
  method: 'POST',
  headers: {
    'x-token': 'oauth_example_token',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    table_id: 5,
    type: 'WAITER'
  })
});

// PAY call
const payResponse = await fetch('https://integrations.clopos.com/open-api/v2/waiter-call', {
  method: 'POST',
  headers: {
    'x-token': 'oauth_example_token',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    table_id: 5,
    type: 'PAY',
    payment_method: 1
  })
});

const data = await response.json();
```

```python
import requests

url = "https://integrations.clopos.com/open-api/v2/waiter-call"
headers = {
    "x-token": "oauth_example_token",
    "Content-Type": "application/json"
}

# WAITER call
payload = {
    "table_id": 5,
    "type": "WAITER"
}

# PAY call
# payload = {
#     "table_id": 5,
#     "type": "PAY",
#     "payment_method": 1
# }

response = requests.post(url, headers=headers, json=payload)
result = response.json()
```

#### Response

##### 200 OK — Call triggered successfully

```json
{
  "success": true
}
```

##### 400 Bad Request — Validation or creation failure

Returned when the request body is invalid (e.g. unknown `table_id`, unsupported `type`, missing `payment_method` for a `PAY` call, or invalid payment method ID).

```json
{
  "success": false
}
```
