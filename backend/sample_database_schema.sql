-- Drop existing tables if they exist
DROP TABLE IF EXISTS product_reviews_and_ratings CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS shipping CASCADE;
DROP TABLE IF EXISTS refunds_returns CASCADE;
DROP TABLE IF EXISTS transactions_and_payments CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS cart CASCADE;
DROP TABLE IF EXISTS wishlist CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS customers_loyalty_program CASCADE;
DROP TABLE IF EXISTS campaigns CASCADE;
DROP TABLE IF EXISTS customerinfo CASCADE;

-- Create enum types
CREATE TYPE wishlist_status_enum AS ENUM ('active', 'inactive', 'archived');
CREATE TYPE priority_level_enum AS ENUM ('low', 'medium', 'high');
CREATE TYPE added_from_source_enum AS ENUM ('web', 'mobile', 'api');

-- Customer Information Table
CREATE TABLE customerinfo (
    person_customer_id SERIAL PRIMARY KEY,
    person_first_name VARCHAR(100) NOT NULL,
    person_last_name VARCHAR(100) NOT NULL,
    person_email VARCHAR(255) UNIQUE NOT NULL,
    person_date_of_birth DATE,
    person_gender VARCHAR(20),
    person_phone_number VARCHAR(20),
    person_income DECIMAL(12,2),
    person_occupation VARCHAR(100),
    person_marital_status VARCHAR(50),
    person_preferred_language VARCHAR(50),
    person_loyalty_points INTEGER DEFAULT 0,
    person_is_premium BOOLEAN DEFAULT FALSE,
    person_registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    address_street VARCHAR(255),
    address_city VARCHAR(100),
    address_state VARCHAR(100),
    address_country VARCHAR(100),
    address_zipcode VARCHAR(20),
    account_has_active_subscription BOOLEAN DEFAULT FALSE,
    account_preferred_payment_method VARCHAR(50),
    account_card_expiry DATE,
    account_account_balance DECIMAL(10,2) DEFAULT 0.00,
    preferences_total_orders INTEGER DEFAULT 0,
    preferences_avg_spent_per_order DECIMAL(10,2) DEFAULT 0.00,
    preferences_last_order_date DATE,
    preferences_newsletter_subscription BOOLEAN DEFAULT FALSE,
    securitytwo_factor_enabled BOOLEAN DEFAULT FALSE,
    securityemail_notifications BOOLEAN DEFAULT TRUE,
    securitysms_notifications BOOLEAN DEFAULT FALSE,
    security_question VARCHAR(255),
    security_answer_hash VARCHAR(255)
);

-- Campaigns Table
CREATE TABLE campaigns (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(255) NOT NULL,
    campaign_type VARCHAR(100),
    campaign_status VARCHAR(50),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12,2),
    actual_spent DECIMAL(12,2),
    revenue_generated DECIMAL(12,2),
    target_audience VARCHAR(255),
    total_reach INTEGER,
    impressions INTEGER,
    clicks INTEGER,
    email_open_rate DECIMAL(5,4),
    cost_per_acquisition DECIMAL(10,2),
    roi DECIMAL(10,2),
    discount_code VARCHAR(50)
);

-- Customer Loyalty Program Table
CREATE TABLE customers_loyalty_program (
    loyalty_membership_unique_identifier SERIAL PRIMARY KEY,
    associated_customer_reference_id INTEGER REFERENCES customerinfo(person_customer_id),
    accumulated_loyalty_points_balance INTEGER DEFAULT 0,
    loyalty_program_tier_level VARCHAR(50),
    eligible_for_special_promotions BOOLEAN DEFAULT FALSE,
    exclusive_member_early_access BOOLEAN DEFAULT FALSE,
    participation_in_exclusive_beta_testing BOOLEAN DEFAULT FALSE,
    initial_enrollment_date DATE,
    last_loyalty_point_update_date DATE,
    last_loyalty_tier_upgrade_date DATE,
    next_loyalty_tier_evaluation_date DATE,
    expiration_date_of_loyalty_points DATE,
    total_discount_amount_redeemed DECIMAL(10,2) DEFAULT 0.00,
    lifetime_loyalty_points_earned INTEGER DEFAULT 0,
    lifetime_loyalty_points_redeemed INTEGER DEFAULT 0,
    customer_birthday_special_discount BOOLEAN DEFAULT FALSE,
    annual_loyalty_spending_threshold DECIMAL(10,2),
    free_shipping_eligibility BOOLEAN DEFAULT FALSE,
    anniversary_reward_voucher_status BOOLEAN DEFAULT FALSE,
    customer_feedback_engagement_score DECIMAL(5,2),
    bonus_loyalty_points_last_month INTEGER DEFAULT 0,
    referral_bonus_points_earned INTEGER DEFAULT 0,
    referred_friends_count INTEGER DEFAULT 0,
    extra_reward_credits_from_surveys INTEGER DEFAULT 0,
    special_event_invitation_status BOOLEAN DEFAULT FALSE,
    last_redemption_date DATE,
    exclusive_coupon_codes_assigned TEXT,
    preferred_communication_channel VARCHAR(50),
    personalized_product_recommendations TEXT
);

-- Suppliers Table
CREATE TABLE suppliers (
    supplier_unique_identifier SERIAL PRIMARY KEY,
    official_supplier_business_name VARCHAR(255) NOT NULL,
    supplier_country_of_operation VARCHAR(100),
    registered_business_address TEXT,
    primary_contact_person_name VARCHAR(255),
    primary_contact_phone_number VARCHAR(20),
    primary_contact_email_address VARCHAR(255),
    preferred_payment_terms_description TEXT,
    supplier_tax_identification_number VARCHAR(100),
    total_number_of_products_supplied INTEGER DEFAULT 0,
    average_supplier_rating DECIMAL(3,2)
);

-- Products Table
CREATE TABLE products (
    unique_product_identifier SERIAL PRIMARY KEY,
    product_display_name VARCHAR(255) NOT NULL,
    product_category_primary VARCHAR(100),
    product_category_secondary VARCHAR(100),
    universal_product_code VARCHAR(50),
    standard_retail_price_including_tax DECIMAL(10,2),
    promotional_discounted_price DECIMAL(10,2),
    percentage_discount_applied DECIMAL(5,4),
    net_weight_in_kilograms DECIMAL(8,3),
    product_dimensions_length_cm DECIMAL(8,2),
    product_dimensions_width_cm DECIMAL(8,2),
    product_dimensions_height_cm DECIMAL(8,2),
    country_of_product_origin VARCHAR(100),
    official_product_release_date DATE,
    estimated_replenishment_date DATE,
    minimum_threshold_for_restocking INTEGER,
    available_stock_quantity_in_units INTEGER,
    perishable_product_flag BOOLEAN DEFAULT FALSE,
    featured_product_flag BOOLEAN DEFAULT FALSE,
    active_product_status BOOLEAN DEFAULT TRUE,
    aggregate_customer_review_rating DECIMAL(3,2),
    total_number_of_verified_reviews INTEGER DEFAULT 0,
    standard_warranty_duration INTEGER,
    associated_supplier_reference_id INTEGER REFERENCES suppliers(supplier_unique_identifier)
);

-- Inventory Table
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    referenced_product_id INTEGER REFERENCES products(unique_product_identifier),
    supplier_id INTEGER REFERENCES suppliers(supplier_unique_identifier),
    quantity INTEGER NOT NULL,
    purchase_price DECIMAL(10,2),
    stock_status VARCHAR(50),
    warehouse_location VARCHAR(255),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    safety_stock INTEGER,
    stock_threshold INTEGER,
    last_restock_date DATE,
    expected_restock_date DATE,
    expiry_date DATE,
    shelf_life INTEGER,
    last_inventory_audit_date DATE,
    inventory_turnover_rate DECIMAL(5,4)
);

-- Events Table
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    person_customer_id INTEGER REFERENCES customerinfo(person_customer_id),
    order_id INTEGER,
    order_item_id INTEGER,
    event_type VARCHAR(100),
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_platform VARCHAR(50),
    device_type VARCHAR(50),
    device_os VARCHAR(50),
    device_browser VARCHAR(50),
    location_country VARCHAR(100),
    location_city VARCHAR(100),
    time_spent_seconds INTEGER,
    click_count INTEGER,
    scroll_depth_percentage DECIMAL(5,2),
    cart_value DECIMAL(10,2),
    review_rating INTEGER,
    email_opened BOOLEAN DEFAULT FALSE,
    push_notification_clicked BOOLEAN DEFAULT FALSE,
    survey_completed BOOLEAN DEFAULT FALSE,
    payment_method VARCHAR(50),
    discount_applied DECIMAL(10,2),
    session_id VARCHAR(255)
);

-- Wishlist Table
CREATE TABLE wishlist (
    id SERIAL PRIMARY KEY,
    fk_user_id INTEGER REFERENCES customerinfo(person_customer_id),
    fk_product_id INTEGER REFERENCES products(unique_product_identifier),
    product_name VARCHAR(255),
    brand_name VARCHAR(255),
    category VARCHAR(100),
    price_at_addition DECIMAL(10,2),
    discount_at_addition DECIMAL(5,4),
    quantity INTEGER DEFAULT 1,
    priority_level priority_level_enum DEFAULT 'medium',
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_viewed_at TIMESTAMP,
    reminder_set BOOLEAN DEFAULT FALSE,
    reminder_date DATE,
    expected_purchase_date DATE,
    wishlist_status wishlist_status_enum DEFAULT 'active',
    stock_status_at_addition BOOLEAN DEFAULT TRUE,
    session_id VARCHAR(255)
);

-- Cart Table
CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    fk_user_id INTEGER REFERENCES customerinfo(person_customer_id),
    fk_product_id INTEGER REFERENCES products(unique_product_identifier),
    quantity INTEGER NOT NULL,
    price_per_unit DECIMAL(10,2),
    total_price DECIMAL(10,2),
    discounted_total_price DECIMAL(10,2),
    discount_applied DECIMAL(5,4),
    cart_status VARCHAR(50),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_delivery_date DATE,
    shipping_fee DECIMAL(8,2),
    tax_amount DECIMAL(8,2),
    is_gift BOOLEAN DEFAULT FALSE,
    wishlist_flag BOOLEAN DEFAULT FALSE,
    session_id VARCHAR(255),
    recommended_products TEXT
);

-- Orders Table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    person_customer_id INTEGER REFERENCES customerinfo(person_customer_id),
    campaign_id INTEGER REFERENCES campaigns(campaign_id),
    order_date DATE DEFAULT CURRENT_DATE,
    shipping_date DATE,
    delivery_date DATE,
    total_amount DECIMAL(10,2),
    discount_applied DECIMAL(10,2),
    tax_amount DECIMAL(8,2),
    shipping_fee DECIMAL(8,2),
    order_status VARCHAR(50),
    payment_status VARCHAR(50),
    payment_method VARCHAR(50),
    tracking_number VARCHAR(100),
    shipping_address_street VARCHAR(255),
    shipping_address_city VARCHAR(100),
    shipping_address_state VARCHAR(100),
    shipping_address_country VARCHAR(100),
    shipping_address_postalcode VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions and Payments Table
CREATE TABLE transactions_and_payments (
    transaction_unique_identifier SERIAL PRIMARY KEY,
    corresponding_customer_reference_identifier INTEGER REFERENCES customerinfo(person_customer_id),
    linked_order_reference_identifier INTEGER REFERENCES orders(order_id),
    transaction_date_and_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_transaction_amount DECIMAL(12,2),
    final_billed_amount DECIMAL(12,2),
    transaction_status VARCHAR(50),
    payment_method_used VARCHAR(100),
    transaction_currency_code VARCHAR(10),
    billing_address_street VARCHAR(255),
    billing_address_city VARCHAR(100),
    billing_address_state VARCHAR(100),
    billing_address_country VARCHAR(100),
    billing_address_zip_code VARCHAR(20),
    shipping_address_street VARCHAR(255),
    shipping_address_city VARCHAR(100),
    shipping_address_state VARCHAR(100),
    shipping_address_country VARCHAR(100),
    shipping_address_zip_code VARCHAR(20),
    promotional_offer_applied BOOLEAN DEFAULT FALSE,
    applied_discount_value DECIMAL(10,2),
    applied_gift_card_code VARCHAR(50),
    refund_status BOOLEAN DEFAULT FALSE,
    refund_amount DECIMAL(10,2),
    chargeback_request_status BOOLEAN DEFAULT FALSE,
    chargeback_dispute_reason TEXT,
    fraud_detection_flagged BOOLEAN DEFAULT FALSE,
    is_transaction_fraudulent BOOLEAN DEFAULT FALSE,
    transaction_review_score DECIMAL(3,2),
    associated_loyalty_points_earned INTEGER DEFAULT 0
);

-- Refunds and Returns Table
CREATE TABLE refunds_returns (
    id SERIAL PRIMARY KEY,
    fk_user_id INTEGER REFERENCES customerinfo(person_customer_id),
    fk_order_id INTEGER REFERENCES orders(order_id),
    fk_product_id INTEGER REFERENCES products(unique_product_identifier),
    request_date DATE DEFAULT CURRENT_DATE,
    processed_date DATE,
    refund_amount DECIMAL(10,2),
    restocking_fee DECIMAL(8,2),
    return_type VARCHAR(50),
    reason TEXT,
    refund_status VARCHAR(50),
    refund_method VARCHAR(50),
    refund_initiated_by VARCHAR(50),
    customer_notes TEXT,
    status VARCHAR(50),
    is_refundable BOOLEAN DEFAULT TRUE
);

-- Shipping Table
CREATE TABLE shipping (
    id SERIAL PRIMARY KEY,
    fk_order_id INTEGER REFERENCES orders(order_id),
    tracking_number VARCHAR(100),
    carrier VARCHAR(100),
    shipping_method VARCHAR(100),
    shipping_cost DECIMAL(8,2),
    shipping_status VARCHAR(50),
    shipped_date DATE,
    estimated_delivery DATE,
    actual_delivery_date DATE,
    shipping_address VARCHAR(255),
    shipping_city VARCHAR(100),
    shipping_state VARCHAR(100),
    shipping_country VARCHAR(100),
    shipping_zipcode VARCHAR(20)
);

-- Order Items Table
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(unique_product_identifier),
    product_name VARCHAR(255),
    quantity INTEGER NOT NULL,
    price_per_unit DECIMAL(10,2),
    total_price DECIMAL(10,2),
    warranty_period INTEGER,
    item_status VARCHAR(50),
    item_weight DECIMAL(8,3),
    return_period INTEGER,
    is_returnable BOOLEAN DEFAULT TRUE,
    is_replacement_available BOOLEAN DEFAULT TRUE
);

-- Product Reviews and Ratings Table
CREATE TABLE product_reviews_and_ratings (
    review_unique_identifier SERIAL PRIMARY KEY,
    referenced_product_identifier INTEGER REFERENCES products(unique_product_identifier),
    reviewing_customer_identifier INTEGER REFERENCES customerinfo(person_customer_id),
    submitted_review_star_rating INTEGER CHECK (submitted_review_star_rating >= 1 AND submitted_review_star_rating <= 5),
    textual_review_feedback TEXT,
    customer_review_submission_date DATE DEFAULT CURRENT_DATE,
    review_approval_moderation_status VARCHAR(50),
    review_moderator_notes TEXT,
    number_of_helpful_votes_received INTEGER DEFAULT 0,
    verification_status_of_reviewer BOOLEAN DEFAULT FALSE,
    previous_product_purchases_count INTEGER DEFAULT 0,
    length_of_review_in_characters INTEGER,
    sentiment_analysis_score DECIMAL(5,4),
    keywords_extracted_from_review TEXT,
    associated_review_image_urls TEXT,
    total_number_of_edits_made INTEGER DEFAULT 0,
    return_request_status BOOLEAN DEFAULT FALSE
);
