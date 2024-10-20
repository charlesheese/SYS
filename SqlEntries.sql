CREATE TABLE Users (
    userId INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Products (
    productId INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    sellerId INT,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sellerId) REFERENCES Users(userId)
);

CREATE TABLE Orders (
    orderId INT PRIMARY KEY AUTO_INCREMENT,
    buyerId INT,
    productId INT,
    quantity INT NOT NULL,
    totalPrice DECIMAL(10, 2) NOT NULL,
    orderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyerId) REFERENCES Users(userId),
    FOREIGN KEY (productId) REFERENCES Products(productId)
);

CREATE TABLE Payments (
    paymentId INT PRIMARY KEY AUTO_INCREMENT,
    orderId INT,
    amount DECIMAL(10, 2) NOT NULL,
    paymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Completed', 'Pending', 'Failed'),
    FOREIGN KEY (orderId) REFERENCES Orders(orderId)
);

CREATE TABLE Messages (
    messageId INT PRIMARY KEY AUTO_INCREMENT,
    sellerId INT,
    buyerId INT,
    content TEXT,
    dateSent DATETIME,
    FOREIGN KEY (sellerId) REFERENCES Users(userId),
    FOREIGN KEY (buyerId) REFERENCES Users(userId)
);

