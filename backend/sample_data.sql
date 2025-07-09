-- Insert sample customers
INSERT INTO customerinfo (person_first_name, person_last_name, person_email, person_date_of_birth, person_gender, person_phone_number, person_income, person_occupation, person_marital_status, person_preferred_language, person_loyalty_points, person_is_premium, address_street, address_city, address_state, address_country, address_zipcode, account_has_active_subscription, account_preferred_payment_method, preferences_total_orders, preferences_avg_spent_per_order, preferences_newsletter_subscription, securitytwo_factor_enabled) VALUES
('John', 'Doe', 'john.doe@email.com', '1985-03-15', 'Male', '+1-555-0101', 75000.00, 'Software Engineer', 'Married', 'English', 1250, TRUE, '123 Main St', 'New York', 'NY', 'United States', '10001', TRUE, 'Credit Card', 15, 125.50, TRUE, TRUE),
('Jane', 'Smith', 'jane.smith@email.com', '1990-07-22', 'Female', '+1-555-0102', 65000.00, 'Marketing Manager', 'Single', 'English', 890, FALSE, '456 Oak Ave', 'Los Angeles', 'CA', 'United States', '90210', TRUE, 'PayPal', 8, 89.75, TRUE, FALSE),
('Mike', 'Johnson', 'mike.johnson@email.com', '1988-11-08', 'Male', '+1-555-0103', 85000.00, 'Data Analyst', 'Married', 'English', 2100, TRUE, '789 Pine St', 'Chicago', 'IL', 'United States', '60601', FALSE, 'Credit Card', 22, 156.80, FALSE, TRUE),
('Sarah', 'Williams', 'sarah.williams@email.com', '1992-05-14', 'Female', '+1-555-0104', 55000.00, 'Teacher', 'Single', 'English', 650, FALSE, '321 Elm St', 'Houston', 'TX', 'United States', '77001', TRUE, 'Debit Card', 5, 67.20, TRUE, FALSE),
('David', 'Brown', 'david.brown@email.com', '1987-09-30', 'Male', '+1-555-0105', 95000.00, 'Product Manager', 'Married', 'English', 1800, TRUE, '654 Maple Dr', 'Phoenix', 'AZ', 'United States', '85001', TRUE, 'Credit Card', 18, 198.45, TRUE, TRUE);

-- Insert sample suppliers
INSERT INTO suppliers (official_supplier_business_name, supplier_country_of_operation, registered_business_address, primary_contact_person_name, primary_contact_phone_number, primary_contact_email_address, total_number_of_products_supplied, average_supplier_rating) VALUES
('TechCorp Electronics', 'United States', '100 Tech Blvd, Silicon Valley, CA', 'Robert Tech', '+1-555-1001', 'contact@techcorp.com', 150, 4.5),
('Global Fashion Ltd', 'United Kingdom', '25 Fashion St, London, UK', 'Emma Style', '+44-20-1234', 'info@globalfashion.co.uk', 200, 4.2),
('HomeGoods Inc', 'United States', '500 Home Ave, Atlanta, GA', 'Lisa Home', '+1-555-1002', 'sales@homegoods.com', 300, 4.7),
('Sports Gear Pro', 'Germany', '10 Sport Str, Munich, Germany', 'Hans Sport', '+49-89-1234', 'orders@sportsgear.de', 120, 4.3),
('Beauty Essentials', 'France', '15 Beauté Rue, Paris, France', 'Marie Belle', '+33-1-1234', 'contact@beautyessentials.fr', 80, 4.6);

-- Insert sample campaigns
INSERT INTO campaigns (campaign_name, campaign_type, campaign_status, start_date, end_date, budget, actual_spent, revenue_generated, target_audience, total_reach, impressions, clicks, email_open_rate, cost_per_acquisition, roi, discount_code) VALUES
('Summer Electronics Sale', 'Email', 'completed', '2023-06-01', '2023-06-30', 10000.00, 8500.00, 25000.00, 'Tech Enthusiasts', 50000, 150000, 7500, 0.25, 15.50, 194.12, 'SUMMER2023'),
('Back to School Fashion', 'Social Media', 'active', '2023-08-01', '2023-08-31', 15000.00, 12000.00, 35000.00, 'Students', 75000, 200000, 12000, 0.18, 12.75, 191.67, 'SCHOOL2023'),
('Holiday Home Decor', 'Display', 'completed', '2023-11-01', '2023-12-31', 20000.00, 18500.00, 45000.00, 'Homeowners', 100000, 300000, 18000, 0.22, 18.20, 143.24, 'HOLIDAY2023'),
('New Year Fitness', 'Email', 'active', '2024-01-01', '2024-01-31', 8000.00, 6500.00, 22000.00, 'Fitness Enthusiasts', 40000, 120000, 6000, 0.28, 14.25, 238.46, 'FITNESS2024'),
('Spring Beauty Collection', 'Social Media', 'planned', '2024-03-01', '2024-03-31', 12000.00, 0.00, 0.00, 'Beauty Lovers', 60000, 0, 0, 0.00, 0.00, 0.00, 'BEAUTY2024');

-- Insert sample products
INSERT INTO products (product_display_name, product_category_primary, product_category_secondary, universal_product_code, standard_retail_price_including_tax, promotional_discounted_price, percentage_discount_applied, net_weight_in_kilograms, country_of_product_origin, official_product_release_date, available_stock_quantity_in_units, perishable_product_flag, featured_product_flag, active_product_status, aggregate_customer_review_rating, total_number_of_verified_reviews, standard_warranty_duration, associated_supplier_reference_id) VALUES
('iPhone 14 Pro', 'Electronics', 'Smartphones', '194252014141', 1099.00, 999.00, 0.0909, 0.206, 'United States', '2022-09-16', 50, FALSE, TRUE, TRUE, 4.5, 1250, 12, 1),
('Samsung Galaxy S23', 'Electronics', 'Smartphones', '887276567890', 899.00, 799.00, 0.1112, 0.168, 'South Korea', '2023-02-01', 75, FALSE, TRUE, TRUE, 4.3, 980, 12, 1),
('Nike Air Max 270', 'Fashion', 'Footwear', '194501234567', 150.00, 120.00, 0.2000, 0.450, 'Vietnam', '2023-01-15', 200, FALSE, FALSE, TRUE, 4.4, 650, 6, 4),
('Adidas Ultraboost 22', 'Fashion', 'Footwear', '194505678901', 180.00, 144.00, 0.2000, 0.380, 'Germany', '2022-12-01', 150, FALSE, TRUE, TRUE, 4.6, 820, 6, 4),
('KitchenAid Stand Mixer', 'Home & Garden', 'Kitchen Appliances', '883049567890', 379.00, 299.00, 0.2111, 10.900, 'United States', '2022-08-01', 30, FALSE, TRUE, TRUE, 4.7, 1100, 24, 3);

-- Insert sample inventory
INSERT INTO inventory (referenced_product_id, supplier_id, quantity, purchase_price, stock_status, warehouse_location, safety_stock, stock_threshold, last_restock_date, expected_restock_date, inventory_turnover_rate) VALUES
(1, 1, 50, 750.00, 'in_stock', 'Warehouse A', 10, 15, '2023-12-01', '2024-02-01', 0.85),
(2, 1, 75, 600.00, 'in_stock', 'Warehouse A', 15, 20, '2023-12-15', '2024-02-15', 0.75),
(3, 4, 200, 80.00, 'in_stock', 'Warehouse B', 50, 75, '2023-12-10', '2024-01-30', 1.20),
(4, 4, 150, 95.00, 'in_stock', 'Warehouse B', 30, 50, '2023-12-05', '2024-01-25', 1.10),
(5, 3, 30, 220.00, 'low_stock', 'Warehouse C', 5, 10, '2023-11-20', '2024-01-15', 0.65);

-- Insert sample customer loyalty program data
INSERT INTO customers_loyalty_program (associated_customer_reference_id, accumulated_loyalty_points_balance, loyalty_program_tier_level, eligible_for_special_promotions, exclusive_member_early_access, participation_in_exclusive_beta_testing, initial_enrollment_date, lifetime_loyalty_points_earned, lifetime_loyalty_points_redeemed, customer_birthday_special_discount, annual_loyalty_spending_threshold, free_shipping_eligibility, anniversary_reward_voucher_status) VALUES
(1, 1250, 'Gold', TRUE, TRUE, TRUE, '2022-01-15', 2500, 1250, TRUE, 1000.00, TRUE, TRUE),
(2, 890, 'Silver', TRUE, FALSE, FALSE, '2022-03-22', 1200, 310, FALSE, 500.00, TRUE, FALSE),
(3, 2100, 'Platinum', TRUE, TRUE, TRUE, '2021-11-08', 4200, 2100, TRUE, 2000.00, TRUE, TRUE),
(4, 650, 'Bronze', FALSE, FALSE, FALSE, '2023-05-14', 650, 0, FALSE, 250.00, FALSE, FALSE),
(5, 1800, 'Gold', TRUE, TRUE, FALSE, '2022-09-30', 3000, 1200, TRUE, 1500.00, TRUE, TRUE);

-- Insert sample orders
INSERT INTO orders (person_customer_id, campaign_id, order_date, total_amount, discount_applied, tax_amount, shipping_fee, order_status, payment_status, payment_method, shipping_address_street, shipping_address_city, shipping_address_state, shipping_address_country, shipping_address_postalcode) VALUES
(1, 1, '2023-12-15', 1099.00, 100.00, 87.92, 9.99, 'delivered', 'paid', 'Credit Card', '123 Main St', 'New York', 'NY', 'United States', '10001'),
(2, 2, '2023-12-10', 150.00, 30.00, 12.00, 5.99, 'shipped', 'paid', 'PayPal', '456 Oak Ave', 'Los Angeles', 'CA', 'United States', '90210'),
(3, 1, '2023-12-08', 899.00, 100.00, 71.92, 0.00, 'delivered', 'paid', 'Credit Card', '789 Pine St', 'Chicago', 'IL', 'United States', '60601'),
(4, 3, '2023-12-05', 379.00, 80.00, 30.32, 15.99, 'processing', 'paid', 'Debit Card', '321 Elm St', 'Houston', 'TX', 'United States', '77001'),
(5, 2, '2023-12-01', 180.00, 36.00, 14.40, 7.99, 'delivered', 'paid', 'Credit Card', '654 Maple Dr', 'Phoenix', 'AZ', 'United States', '85001');

-- Insert sample order items
INSERT INTO order_items (order_id, product_id, product_name, quantity, price_per_unit, total_price, warranty_period, item_status, item_weight, return_period, is_returnable, is_replacement_available) VALUES
(1, 1, 'iPhone 14 Pro', 1, 999.00, 999.00, 12, 'delivered', 0.206, 30, TRUE, TRUE),
(2, 3, 'Nike Air Max 270', 1, 120.00, 120.00, 6, 'shipped', 0.450, 30, TRUE, TRUE),
(3, 2, 'Samsung Galaxy S23', 1, 799.00, 799.00, 12, 'delivered', 0.168, 30, TRUE, TRUE),
(4, 5, 'KitchenAid Stand Mixer', 1, 299.00, 299.00, 24, 'processing', 10.900, 30, TRUE, TRUE),
(5, 4, 'Adidas Ultraboost 22', 1, 144.00, 144.00, 6, 'delivered', 0.380, 30, TRUE, TRUE);

-- Insert sample transactions
INSERT INTO transactions_and_payments (corresponding_customer_reference_identifier, linked_order_reference_identifier, total_transaction_amount, final_billed_amount, transaction_status, payment_method_used, transaction_currency_code, promotional_offer_applied, applied_discount_value, refund_status, transaction_review_score, associated_loyalty_points_earned) VALUES
(1, 1, 1099.00, 1096.91, 'completed', 'Credit Card', 'USD', TRUE, 100.00, FALSE, 4.8, 110),
(2, 2, 150.00, 137.99, 'completed', 'PayPal', 'USD', TRUE, 30.00, FALSE, 4.5, 14),
(3, 3, 899.00, 870.92, 'completed', 'Credit Card', 'USD', TRUE, 100.00, FALSE, 4.7, 87),
(4, 4, 379.00, 345.31, 'pending', 'Debit Card', 'USD', TRUE, 80.00, FALSE, 0.0, 35),
(5, 5, 180.00, 158.39, 'completed', 'Credit Card', 'USD', TRUE, 36.00, FALSE, 4.6, 16);

-- Insert sample shipping data
INSERT INTO shipping (fk_order_id, tracking_number, carrier, shipping_method, shipping_cost, shipping_status, shipped_date, estimated_delivery, shipping_address, shipping_city, shipping_state, shipping_country, shipping_zipcode) VALUES
(1, 'TRK123456789', 'UPS', 'Ground', 9.99, 'delivered', '2023-12-16', '2023-12-20', '123 Main St', 'New York', 'NY', 'United States', '10001'),
(2, 'TRK987654321', 'FedEx', 'Express', 5.99, 'shipped', '2023-12-11', '2023-12-15', '456 Oak Ave', 'Los Angeles', 'CA', 'United States', '90210'),
(3, 'TRK456789123', 'UPS', 'Next Day', 0.00, 'delivered', '2023-12-09', '2023-12-12', '789 Pine St', 'Chicago', 'IL', 'United States', '60601'),
(4, 'TRK789123456', 'USPS', 'Priority', 15.99, 'processing', NULL, '2023-12-12', '321 Elm St', 'Houston', 'TX', 'United States', '77001'),
(5, 'TRK321654987', 'DHL', 'Standard', 7.99, 'delivered', '2023-12-02', '2023-12-06', '654 Maple Dr', 'Phoenix', 'AZ', 'United States', '85001');

-- Insert sample product reviews
INSERT INTO product_reviews_and_ratings (referenced_product_identifier, reviewing_customer_identifier, submitted_review_star_rating, textual_review_feedback, review_approval_moderation_status, number_of_helpful_votes_received, verification_status_of_reviewer, previous_product_purchases_count, length_of_review_in_characters, sentiment_analysis_score) VALUES
(1, 1, 5, 'Excellent phone with amazing camera quality and performance!', 'approved', 25, TRUE, 3, 58, 0.92),
(2, 3, 4, 'Great Android phone, battery life could be better.', 'approved', 18, TRUE, 5, 45, 0.75),
(3, 2, 4, 'Comfortable shoes, good for running and daily wear.', 'approved', 12, TRUE, 2, 48, 0.80),
(4, 5, 5, 'Best running shoes I have ever owned! Highly recommended.', 'approved', 30, TRUE, 8, 56, 0.95),
(5, 4, 5, 'Amazing mixer, makes baking so much easier and fun!', 'approved', 22, TRUE, 1, 47, 0.88);

-- Insert sample events
INSERT INTO events (person_customer_id, order_id, order_item_id, event_type, device_platform, device_type, device_os, location_country, location_city, time_spent_seconds, click_count, cart_value, review_rating, email_opened, push_notification_clicked, survey_completed, payment_method, discount_applied) VALUES
(1, 1, 1, 'purchase', 'iOS', 'mobile', 'iOS 16', 'United States', 'New York', 180, 5, 999.00, 5, TRUE, TRUE, FALSE, 'Credit Card', 100.00),
(2, 2, 2, 'purchase', 'Android', 'mobile', 'Android 13', 'United States', 'Los Angeles', 120, 3, 120.00, 4, TRUE, FALSE, TRUE, 'PayPal', 30.00),
(3, 3, 3, 'purchase', 'Windows', 'desktop', 'Windows 11', 'United States', 'Chicago', 240, 8, 799.00, 4, FALSE, TRUE, FALSE, 'Credit Card', 100.00),
(4, 4, 4, 'cart_add', 'macOS', 'desktop', 'macOS 13', 'United States', 'Houston', 90, 2, 299.00, 0, TRUE, FALSE, FALSE, 'Debit Card', 80.00),
(5, 5, 5, 'purchase', 'iOS', 'mobile', 'iOS 17', 'United States', 'Phoenix', 150, 4, 144.00, 5, TRUE, TRUE, TRUE, 'Credit Card', 36.00);

-- Insert sample wishlist items
INSERT INTO wishlist (fk_user_id, fk_product_id, product_name, brand_name, category, price_at_addition, discount_at_addition, quantity, priority_level, reminder_set, expected_purchase_date, wishlist_status, stock_status_at_addition) VALUES
(1, 2, 'Samsung Galaxy S23', 'Samsung', 'Electronics', 899.00, 0.1112, 1, 'high', TRUE, '2024-01-15', 'active', TRUE),
(2, 5, 'KitchenAid Stand Mixer', 'KitchenAid', 'Home & Garden', 379.00, 0.2111, 1, 'medium', FALSE, '2024-02-01', 'active', TRUE),
(3, 1, 'iPhone 14 Pro', 'Apple', 'Electronics', 1099.00, 0.0909, 1, 'high', TRUE, '2024-01-30', 'active', TRUE),
(4, 3, 'Nike Air Max 270', 'Nike', 'Fashion', 150.00, 0.2000, 1, 'low', FALSE, '2024-03-01', 'active', TRUE),
(5, 4, 'Adidas Ultraboost 22', 'Adidas', 'Fashion', 180.00, 0.2000, 1, 'medium', TRUE, '2024-01-20', 'active', TRUE);

-- Insert sample cart items
INSERT INTO cart (fk_user_id, fk_product_id, quantity, price_per_unit, total_price, discounted_total_price, discount_applied, cart_status, estimated_delivery_date, shipping_fee, tax_amount, is_gift, wishlist_flag) VALUES
(1, 3, 1, 150.00, 150.00, 120.00, 0.2000, 'active', '2024-01-20', 5.99, 12.00, FALSE, TRUE),
(2, 1, 1, 1099.00, 1099.00, 999.00, 0.0909, 'active', '2024-01-18', 9.99, 87.92, FALSE, FALSE),
(3, 5, 1, 379.00, 379.00, 299.00, 0.2111, 'saved', '2024-01-25', 15.99, 30.32, TRUE, FALSE),
(4, 2, 1, 899.00, 899.00, 799.00, 0.1112, 'active', '2024-01-22', 0.00, 71.92, FALSE, TRUE),
(5, 4, 2, 180.00, 360.00, 288.00, 0.2000, 'active', '2024-01-19', 7.99, 28.80, FALSE, FALSE);
