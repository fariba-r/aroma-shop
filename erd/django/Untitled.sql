CREATE TABLE `orders` (
  `id` integer PRIMARY KEY,
  `user_id` integer,
  `item_order_id` integer,
  `discount_code_id` integer,
  `final_payment` float,
  `created_at` timestamp,
  `status` choices,
  `is_deleted` bool
);

CREATE TABLE `addresses` (
  `id` integer PRIMARY KEY,
  `city` choices,
  `user_id` integer,
  `description` varchar[200],
  `is_deleted` bool
);

CREATE TABLE `users` (
  `id` integer PRIMARY KEY,
  `first_name` varchar[50],
  `last_name` varchar[50],
  `phone` varchar[11],
  `email` varchar[100],
  `is_active` bool,
  `created_at` timestamp,
  `is_deleted` bool,
  `username` varchar[50],
  `password` varchar[50]
);

CREATE TABLE `items` (
  `id` integer PRIMARY KEY,
  `title` varchar[50],
  `description` varchar[500],
  `detail_id` integer,
  `count` integer,
  `price` float,
  `is_deleted` bool,
  `created_at` timestamp,
  `creator` integer(foreign to users)
);

CREATE TABLE `admin_proxy_user` (
  `title` varchar[50],
  `description` varchar[500],
  `category_id` integer,
  `detail_id` integer,
  `count` integer,
  `price` float,
  `is_deleted` bool,
  `created_at` timestamp,
  `creator` integer(foreign to users)
);

CREATE TABLE `staffs` (
  `id` integer PRIMARY KEY,
  `user_id` integer,
  `created_at` timestamp,
  `salary` float,
  `position` choices,
  `is_deleted` bool,
  `creator` integer
);

CREATE TABLE `details` (
  `id` integer PRIMARY KEY,
  `title` varchar[50],
  `parent` integer,
  `is_deleted` bool
);

CREATE TABLE `discount_code` (
  `id` integer PRIMARY KEY,
  `creator` integer,
  `created_at` timestamp,
  `value` float,
  `condition` float,
  `user_id` integer
);

CREATE TABLE `discount_percent` (
  `id` integer PRIMARY KEY,
  `creator` integer,
  `created_at` timestamp,
  `is_deleted` timestamp,
  `expiration` timestamp,
  `value` float,
  `item_id` integer
);

CREATE TABLE `discount_code_used` (
  `id` integer PRIMARY KEY,
  `creator` integer,
  `created_at` timestamp,
  `date_used` timestamp,
  `value` float
);

CREATE TABLE `likes` (
  `id` integer PRIMARY KEY,
  `creator` integer,
  `content_type_model` integer,
  `object_id` integer,
  `created_at` timestamp
);

CREATE TABLE `comments` (
  `id` integer PRIMARY KEY,
  `creator` integer,
  `is_ok` bool,
  `parent` integer,
  `item_id` integer,
  `is_deleted` bool
);

CREATE TABLE `images` (
  `id` integer PRIMARY KEY,
  `image` varchar[500],
  `content_type_model` integer,
  `object_id` integer,
  `is_deleted` bool,
  `creator` integer,
  `created_at` timestamp
);

CREATE TABLE `edits` (
  `id` integer PRIMARY KEY,
  `content_type_model` integer,
  `object_id` integer,
  `creator` integer,
  `created_at` timestamp,
  `change_filed` choices,
  `old_value` varchar[200],
  `is_deleted` bool
);

CREATE TABLE `otp_code` (
  `id` integer PRIMARY KEY,
  `user_id` integer,
  `code` varchar[10]
);

CREATE TABLE `item_order` (
  `id` integer PRIMARY KEY,
  `item_id` integer,
  `order_id` integer,
  `count` integer
);

CREATE TABLE `orders_discount_code_used` (
  `id` integer PRIMARY KEY,
  `orders_discount_code_id` integer,
  `discount_code_used_id` integer,
  PRIMARY KEY (`orders_discount_code_id`, `discount_code_used_id`)
);

CREATE TABLE `items_details` (
  `id` integer PRIMARY KEY,
  `items_detail_id` integer,
  `details_id` integer,
  PRIMARY KEY (`items_detail_id`, `details_id`)
);

CREATE TABLE `discount_code_users` (
  `id` integer PRIMARY KEY,
  `discount_code_user_id` integer,
  `users_id` integer,
  PRIMARY KEY (`discount_code_user_id`, `users_id`)
);

CREATE TABLE `discount_percent_categorys` (
  `id` integer PRIMARY KEY,
  `discount_percent_category_id` integer,
  `categorys_id` integer,
  PRIMARY KEY (`discount_percent_category_id`, `categorys_id`)
);

CREATE TABLE `Province` (
  `id` integer PRIMARY KEY,
  `title` varchar[200]
);

CREATE TABLE `City` (
  `id` integer PRIMARY KEY,
  `title` varchar[200],
  `parent` integer
);

ALTER TABLE `addresses` ADD FOREIGN KEY (`city`) REFERENCES `City` (`id`);

ALTER TABLE `addresses` ADD FOREIGN KEY (`city`) REFERENCES `users` (`id`);

ALTER TABLE `staffs` ADD FOREIGN KEY (`creator`) REFERENCES `users` (`id`);

ALTER TABLE `City` ADD FOREIGN KEY (`parent`) REFERENCES `Province` (`id`);

ALTER TABLE `orders` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `item_order` ADD FOREIGN KEY (`id`) REFERENCES `orders` (`item_order_id`);

ALTER TABLE `orders_discount_code_used` ADD FOREIGN KEY (`orders_discount_code_id`) REFERENCES `orders` (`discount_code_id`);

ALTER TABLE `orders_discount_code_used` ADD FOREIGN KEY (`discount_code_used_id`) REFERENCES `discount_code_used` (`id`);

ALTER TABLE `items_details` ADD FOREIGN KEY (`items_detail_id`) REFERENCES `items` (`detail_id`);

ALTER TABLE `items_details` ADD FOREIGN KEY (`details_id`) REFERENCES `details` (`id`);

ALTER TABLE `items` ADD FOREIGN KEY (`creator`) REFERENCES `users` (`id`);

ALTER TABLE `users` ADD FOREIGN KEY (`id`) REFERENCES `staffs` (`user_id`);

ALTER TABLE `discount_code_users` ADD FOREIGN KEY (`discount_code_user_id`) REFERENCES `discount_code` (`user_id`);

ALTER TABLE `discount_code_users` ADD FOREIGN KEY (`users_id`) REFERENCES `users` (`id`);

ALTER TABLE `discount_percent` ADD FOREIGN KEY (`creator`) REFERENCES `users` (`id`);

CREATE TABLE `discount_percent_items` (
  `discount_percent_item_id` integer,
  `items_id` integer,
  PRIMARY KEY (`discount_percent_item_id`, `items_id`)
);

ALTER TABLE `discount_percent_items` ADD FOREIGN KEY (`discount_percent_item_id`) REFERENCES `discount_percent` (`item_id`);

ALTER TABLE `discount_percent_items` ADD FOREIGN KEY (`items_id`) REFERENCES `items` (`id`);


ALTER TABLE `discount_percent_categorys` ADD FOREIGN KEY (`categorys_id`) REFERENCES `items` (`id`);

ALTER TABLE `likes` ADD FOREIGN KEY (`creator`) REFERENCES `users` (`id`);

ALTER TABLE `comments` ADD FOREIGN KEY (`creator`) REFERENCES `users` (`id`);

ALTER TABLE `comments` ADD FOREIGN KEY (`item_id`) REFERENCES `items` (`id`);

ALTER TABLE `images` ADD FOREIGN KEY (`creator`) REFERENCES `users` (`id`);

ALTER TABLE `edits` ADD FOREIGN KEY (`creator`) REFERENCES `users` (`id`);

ALTER TABLE `users` ADD FOREIGN KEY (`id`) REFERENCES `otp_code` (`user_id`);

ALTER TABLE `items` ADD FOREIGN KEY (`id`) REFERENCES `item_order` (`item_id`);

ALTER TABLE `users` ADD FOREIGN KEY (`id`) REFERENCES `item_order` (`item_id`);

ALTER TABLE `users` ADD FOREIGN KEY (`first_name`) REFERENCES `users` (`id`);

ALTER TABLE `details` ADD FOREIGN KEY (`parent`) REFERENCES `details` (`id`);
