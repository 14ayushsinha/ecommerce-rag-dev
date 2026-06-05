# Dataset Analysis

## Dataset

**PromptCloudHQ_flipkart-products**

## Total Records

**20,000+ products**

## Columns

- `uniq_id`
- `crawl_timestamp`
- `product_url`
- `product_name`
- `product_category_tree`
- `pid`
- `retail_price`
- `discounted_price`
- `image`
- `is_FK_Advantage_product`
- `description`
- `product_rating`
- `overall_rating`
- `brand`
- `product_specifications`

## Observations

### Useful Fields

- `product_name`
- `brand`
- `retail_price`
- `discounted_price`
- `description`
- `product_specifications`
- `product_category_tree`
- `product_rating`
- `overall_rating`

### Fields Likely Not Needed

- `crawl_timestamp`
- `product_url`
- `image`

### Data Quality Issues

- Missing brand values
- Missing ratings
- Product Specification requires normalization
- Product Category Tree also requires normalization
- Prodouct Rating and Overall rating is same
- Most of the ratings are marked as **No Rating Available**

## Proposed Schema

```json
{
  "id": str,
  "name": str,
  "brand": str,
  "main_category": str,
  "subcategory": str,
  "full_category_path": str,
  "retail_price": float,
  "discounted_price": float,
  "rating": float | None,
  "description": str,
  "specifications": dict
}